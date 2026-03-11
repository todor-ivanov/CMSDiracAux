import json
from pathlib import Path


def read_json(path):
    with open(path) as f:
        return json.load(f)


def unwrap_request(raw):

    if isinstance(raw, dict):
        return raw

    wrapper = raw[0]
    return list(wrapper.values())[0]


def load_serialized_bundle(job_dir):

    job_dir = Path(job_dir)

    request = unwrap_request(read_json(job_dir / "WMRequest.json"))
    workload = read_json(job_dir / "WMWorkload.json")
    task = read_json(job_dir / "WMTask.json")
    step = read_json(job_dir / "WMStep.json")
    splitting = read_json(job_dir / "WMSplitting.json")

    return {
        "request": request,
        "workload": workload,
        "task": task,
        "step": step,
        "splitting": splitting,
    }
