#!/usr/bin/env python3
"""
Minimal WMCore → DIRAC translator.

This script converts previously serialized WMCore workflow artifacts
(WMRequest.json, WMTask.json, WMStep.json, WMSplitting.json)
into a minimal DIRAC transformation description.

Inputs can either be provided directly via --input-dir
or fetched first using bin/wmcGet.py.
"""

from pathlib import Path
import argparse

from CMSDirac.Interop.io import load_serialized_bundle
from CMSDirac.Interop.normalize import normalize_bundle
from CMSDirac.Interop.emit import emit_translation_document
from CMSDirac.Interop.fetch import run_wmcget


parser = argparse.ArgumentParser(
    description="Translate serialized WMCore workflow to DIRAC artifacts"
)

parser.add_argument(
    "--fetch-inputs",
    action="store_true",
    help="Fetch workflow inputs using bin/wmcGet.py",
)

parser.add_argument(
    "--input-dir",
    dest="inputDir",
    default="",
    help="Directory containing serialized WM*.json files",
)

parser.add_argument(
    "--outdir",
    required=True,
    help="Directory where DIRAC artifacts will be written",
)

parser.add_argument("-r", "--wmReqName", default="")
parser.add_argument("-i", "--wmJobIndex", default="")
parser.add_argument("-m", "--wmReqMgr", default="cmsweb-testbed.cern.ch")

parser.add_argument(
    "--fetch-outdir",
    dest="fetchOutDir",
    default="/tmp",
)


if __name__ == "__main__":

    opts = parser.parse_args()

    if opts.fetch_inputs:
        serialized_dir = run_wmcget(opts)
    else:
        if not opts.inputDir:
            raise SystemExit("Provide --input-dir or use --fetch-inputs")
        serialized_dir = Path(opts.inputDir)

    serialized_dir = serialized_dir.resolve()
    outdir = Path(opts.outdir).resolve()

    print("Input directory:", serialized_dir)
    print("Output directory:", outdir)

    bundle = load_serialized_bundle(serialized_dir)

    translation_document = normalize_bundle(bundle)

    emit_translation_document(translation_document, outdir)

    # expose objects for interactive inspection
    request = bundle["request"]
    workload = bundle["workload"]
    task = bundle["task"]
    step = bundle["step"]
    splitting = bundle["splitting"]
    doc = translation_document

    print("Translation complete.")
