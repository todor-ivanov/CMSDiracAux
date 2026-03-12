import json
import shutil
import subprocess


def _normalize_dataset_hints(task):
    candidates = [
        task.get("inputDataset"),
        task.get("inputDataSet"),
        task.get("InputDataset"),
        task.get("primaryDataset"),
        task.get("PrimaryDataset"),
    ]

    datasets = []

    for item in candidates:
        if not item:
            continue
        if isinstance(item, str):
            datasets.append(item)
        elif isinstance(item, (list, tuple, set)):
            for value in item:
                if isinstance(value, str) and value:
                    datasets.append(value)

    # preserve order, drop duplicates
    seen = set()
    out = []
    for dataset in datasets:
        dataset = dataset.strip()
        if dataset and dataset not in seen:
            seen.add(dataset)
            out.append(dataset)

    return out


def _extract_lfns_from_dasgoclient_json(payload):
    lfns = []

    # expected shape from dasgoclient README:
    # {"file":[{"name":"/store/...root", ...}, ...]}
    for record in payload.get("file", []):
        if isinstance(record, dict):
            name = record.get("name")
            if name:
                lfns.append(name)

    # preserve order, drop duplicates
    seen = set()
    out = []
    for lfn in lfns:
        if lfn not in seen:
            seen.add(lfn)
            out.append(lfn)

    return out


def query_das_files_for_dataset(dataset, host="https://cmsweb-testbed.cern.ch"):
    if not shutil.which("dasgoclient"):
        raise RuntimeError("dasgoclient is not available in PATH")

    cmd = [
        "dasgoclient",
        "-host",
        host,
        "-query",
        f"file dataset={dataset}",
        "-json",
    ]

    proc = subprocess.run(
        cmd,
        check=True,
        capture_output=True,
        text=True,
    )

    payload = json.loads(proc.stdout)
    return _extract_lfns_from_dasgoclient_json(payload)


def resolve_task_lfns(task, host="https://cmsweb-testbed.cern.ch"):
    datasets = _normalize_dataset_hints(task)

    result = {
        "datasets": datasets,
        "lfns": [],
        "resolution_mode": "none",
        "errors": [],
    }

    if not datasets:
        return result

    all_lfns = []

    for dataset in datasets:
        try:
            lfns = query_das_files_for_dataset(dataset, host=host)
            all_lfns.extend(lfns)
        except Exception as exc:
            result["errors"].append(f"{dataset}: {exc}")

    # preserve order, drop duplicates
    seen = set()
    unique_lfns = []
    for lfn in all_lfns:
        if lfn not in seen:
            seen.add(lfn)
            unique_lfns.append(lfn)

    result["lfns"] = unique_lfns
    if unique_lfns:
        result["resolution_mode"] = "das"
    elif datasets:
        result["resolution_mode"] = "dataset-hints-only"

    return result
