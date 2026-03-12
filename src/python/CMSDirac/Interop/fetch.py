import subprocess
import sys
from pathlib import Path

from CMSDirac.Interop.layout import build_request_layout


def run_wmcget(opts):
    script = Path("bin/wmcGet.py")

    if not opts.wmReqName:
        raise RuntimeError(
            "--fetch-inputs currently requires --wmReqName so the request-scoped "
            "output layout can be constructed deterministically."
        )

    layout = build_request_layout(opts.outputBase, opts.wmReqName)

    cmd = [sys.executable, str(script)]

    if getattr(opts, "wmReqMgr", ""):
        cmd += ["-m", opts.wmReqMgr]
    if getattr(opts, "wmReqName", ""):
        cmd += ["-r", opts.wmReqName]
    if getattr(opts, "wmJobPkgFile", ""):
        cmd += ["-j", opts.wmJobPkgFile]
    if getattr(opts, "wmWorkloadFile", ""):
        cmd += ["-w", opts.wmWorkloadFile]
    if getattr(opts, "wmJobIndex", ""):
        cmd += ["-i", opts.wmJobIndex]

    cmd += ["-o", str(layout["wmcore_dir"])]

    subprocess.run(cmd, check=True)

    # Backward-compatible fallback:
    # if wmcGet.py still created an extra wf_REQUEST_NAME layer,
    # resolve it transparently.
    legacy_nested_dir = layout["wmcore_dir"] / f"wf_{layout['request_name']}"

    if legacy_nested_dir.exists():
        return legacy_nested_dir

    return layout["wmcore_dir"]
