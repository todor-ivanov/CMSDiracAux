import json
from pathlib import Path


def read_json(path):
    path = Path(path)
    with path.open() as f:
        return json.load(f)


def write_json(path, payload):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        json.dump(payload, f, indent=2, sort_keys=True)


def unwrap_request(raw):
    if isinstance(raw, dict):
        return raw

    if not isinstance(raw, list) or len(raw) != 1:
        raise ValueError("WMRequest.json is expected to be a dict or a one-element list")

    wrapper = raw[0]
    if not isinstance(wrapper, dict) or len(wrapper) != 1:
        raise ValueError("WMRequest.json wrapper must contain exactly one request")

    return list(wrapper.values())[0]


def load_serialized_bundle(input_dir):
    input_dir = Path(input_dir)

    request = unwrap_request(read_json(input_dir / "WMRequest.json"))
    workload = read_json(input_dir / "WMWorkload.json")
    task = read_json(input_dir / "WMTask.json")
    step = read_json(input_dir / "WMStep.json")
    splitting = read_json(input_dir / "WMSplitting.json")

    return {
        "request": request,
        "workload": workload,
        "task": task,
        "step": step,
        "splitting": splitting,
    }
