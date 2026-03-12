from pathlib import Path


def sanitize_request_name(request_name):
    if not request_name:
        return "UNKNOWN_REQUEST"
    return str(request_name).strip().replace("/", "_")


def build_request_layout(output_base, request_name):
    output_base = Path(output_base).resolve()
    request_name = sanitize_request_name(request_name)

    request_root = output_base / request_name

    return {
        "request_name": request_name,
        "request_root": request_root,
        "wmcore_dir": request_root / "WMCore.fetched.d",
        "dirac_dir": request_root / "DIRAC.transf.d",
        "cwl_dir": request_root / "DIRAC.cwl.d",
    }
