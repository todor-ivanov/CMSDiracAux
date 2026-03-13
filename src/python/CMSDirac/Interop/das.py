import json
import shutil
import subprocess
from pprint import pformat,pprint


def _normalize_dataset_hints(task):
    candidates = []

    # Older flat guesses
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

    # WMTask serialized structure used in this repository:
    # task["input"]["dataset"]["name"]
    task_input = task.get("input") or {}
    dataset_info = task_input.get("dataset") or {}

    if dataset_info.get("name"):
        candidates.append(dataset_info["name"])

    # Optional extra dataset-level hints
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

    # keep only dataset-like paths for DAS file queries
    # example: /DisplacedJet/Run2024E-2024CDEReprocessing-v1/AOD
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


def _extract_lfns_from_dasgoclient_json(payload):
    lfns = []

    if isinstance(payload, list):
        # dasgoclient -json commonly returns a list of records
        for entry in payload:
            if not isinstance(entry, dict):
                continue

            # format often contains a "file" list
            for record in entry.get("file", []):
                if isinstance(record, dict):
                    name = record.get("name")
                    if name:
                        lfns.append(name)

            # defensive fallback for nested dict values
            for value in entry.values():
                if isinstance(value, list):
                    for record in value:
                        if isinstance(record, dict):
                            name = record.get("name")
                            if name and str(name).startswith("/"):
                                lfns.append(name)

    elif isinstance(payload, dict):
        for record in payload.get("file", []):
            if isinstance(record, dict):
                name = record.get("name")
                if name:
                    lfns.append(name)

    seen = set()
    out = []
    for lfn in lfns:
        if lfn not in seen:
            seen.add(lfn)
            out.append(lfn)

    return out


def query_das_files_for_dataset(dataset, host="https://cmsweb-testbed.cern.ch"):
    # subprocess.run already waits for completion.
    # Use one single shell line so alias expansion works reliably.

    shell_cmd = (
        'shopt -s expand_aliases; '
        'type dasgoclient >&2; '
        # f'/cvmfs/cms.cern.ch/common/dasgoclient -host "{host}" -query "file dataset={dataset}" -json'
        f'dasgoclient -host "{host}" -query "file dataset={dataset}" -json'
    )

    proc = subprocess.run(
        ["bash", "-ic", shell_cmd],
        capture_output=True,
        text=True,
    )

    print(proc.stderr)
    # print(proc.stdout)

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
        # print(f"DAS result: {pformat(payload)}")
    except Exception as exc:
        raise RuntimeError(
            "Failed to decode dasgoclient JSON output\n"
            f"dataset: {dataset}\n"
            f"host: {host}\n"
            f"stdout:\n{proc.stdout}\n"
            f"stderr:\n{proc.stderr}\n"
            f"json error: {exc}"
        ) from exc

    return _extract_lfns_from_dasgoclient_json(payload)


def resolve_task_lfns(task, host="https://cmsweb-testbed.cern.ch"):
    datasets = _normalize_dataset_hints(task)
    print(f"DAS datasets: {pformat(datasets)}")
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
