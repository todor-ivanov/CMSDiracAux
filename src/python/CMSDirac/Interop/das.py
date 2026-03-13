import json
import subprocess


def _normalize_dataset_hints(task):
    candidates = []

    flat_candidates = [
        task.get("inputDataset"),
        task.get("inputDataSet"),
        task.get("InputDataset"),
        task.get("primaryDataset"),
        task.get("PrimaryDataset"),
    ]

    for item in flat_candidates:
        if item:
            candidates.append(item)

    task_input = task.get("input") or {}
    dataset_info = task_input.get("dataset") or {}

    if dataset_info.get("name"):
        candidates.append(dataset_info["name"])

    if dataset_info.get("primary"):
        candidates.append(dataset_info["primary"])
    if dataset_info.get("processed"):
        candidates.append(dataset_info["processed"])

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

    normalized = []
    seen = set()

    for dataset in datasets:
        dataset = dataset.strip()
        if not dataset:
            continue
        if not dataset.startswith("/"):
            continue
        if dataset not in seen:
            seen.add(dataset)
            normalized.append(dataset)

    return normalized


def _extract_file_records_from_dasgoclient_json(payload):
    file_records = []

    if isinstance(payload, list):
        for entry in payload:
            if not isinstance(entry, dict):
                continue

            for record in entry.get("file", []):
                if isinstance(record, dict) and record.get("name"):
                    file_records.append(record)

            for value in entry.values():
                if isinstance(value, list):
                    for record in value:
                        if (
                            isinstance(record, dict)
                            and record.get("name")
                            and str(record.get("name")).startswith("/")
                        ):
                            file_records.append(record)

    elif isinstance(payload, dict):
        for record in payload.get("file", []):
            if isinstance(record, dict) and record.get("name"):
                file_records.append(record)

    # preserve order, drop duplicates by file name
    seen = set()
    out = []
    for record in file_records:
        name = record.get("name")
        if name and name not in seen:
            seen.add(name)
            out.append(record)

    return out


def query_das_files_for_dataset(dataset, host="https://cmsweb-testbed.cern.ch"):
    shell_cmd = (
        f'type dasgoclient >&2; '
        f'dasgoclient -host "{host}" -query "file dataset={dataset}" -json'
    )

    proc = subprocess.run(
        ["bash", "-ic", shell_cmd],
        capture_output=True,
        text=True,
    )

    if proc.returncode != 0:
        raise RuntimeError(
            "dasgoclient failed\n"
            f"dataset: {dataset}\n"
            f"host: {host}\n"
            f"returncode: {proc.returncode}\n"
            f"stdout:\n{proc.stdout}\n"
            f"stderr:\n{proc.stderr}"
        )

    if not proc.stdout.strip():
        raise RuntimeError(
            "dasgoclient returned empty stdout\n"
            f"dataset: {dataset}\n"
            f"host: {host}\n"
            f"stderr:\n{proc.stderr}"
        )

    try:
        payload = json.loads(proc.stdout)
    except Exception as exc:
        raise RuntimeError(
            "Failed to decode dasgoclient JSON output\n"
            f"dataset: {dataset}\n"
            f"host: {host}\n"
            f"stdout:\n{proc.stdout}\n"
            f"stderr:\n{proc.stderr}\n"
            f"json error: {exc}"
        ) from exc

    return _extract_file_records_from_dasgoclient_json(payload)


def resolve_task_lfns(task, host="https://cmsweb-testbed.cern.ch"):
    datasets = _normalize_dataset_hints(task)

    result = {
        "datasets": datasets,
        "lfns": [],
        "file_records": [],
        "resolution_mode": "none",
        "errors": [],
    }

    if not datasets:
        return result

    all_file_records = []

    for dataset in datasets:
        try:
            records = query_das_files_for_dataset(dataset, host=host)
            all_file_records.extend(records)
        except Exception as exc:
            result["errors"].append(f"{dataset}: {exc}")

    # preserve order, drop duplicates by LFN
    seen = set()
    unique_records = []
    unique_lfns = []

    for record in all_file_records:
        name = record.get("name")
        if name and name not in seen:
            seen.add(name)
            unique_records.append(record)
            unique_lfns.append(name)

    result["file_records"] = unique_records
    result["lfns"] = unique_lfns

    if unique_lfns:
        result["resolution_mode"] = "das"
    elif datasets:
        result["resolution_mode"] = "dataset-hints-only"

    return result
