import subprocess
import sys
from pathlib import Path


def run_wmcget(opts):

    script = Path("bin/wmcGet.py")

    cmd = [sys.executable, str(script)]

    if opts.wmReqName:
        cmd += ["-r", opts.wmReqName]

    if opts.wmJobIndex:
        cmd += ["-i", opts.wmJobIndex]

    cmd += ["-o", opts.fetchOutDir]

    subprocess.run(cmd, check=True)

    if opts.wmReqName:
        base = Path(opts.fetchOutDir) / f"wf_{opts.wmReqName}"
    else:
        base = Path(opts.fetchOutDir)

    if opts.wmJobIndex:
        return base / f"job_{opts.wmJobIndex}"

    return base
