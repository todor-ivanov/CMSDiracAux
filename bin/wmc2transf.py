#!/usr/bin/env python3
"""
Minimal WMCore to DIRAC translator and local object materializer.
"""

from pathlib import Path
import argparse

from CMSDirac.Interop.emit import emit_translation_document
from CMSDirac.Interop.fetch import run_wmcget
from CMSDirac.Interop.io import load_serialized_bundle
from CMSDirac.Interop.layout import build_request_layout
from CMSDirac.Interop.normalize import normalize_bundle


parser = argparse.ArgumentParser(
    description="Translate serialized WMCore workflow to local DIRAC artifacts"
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
    help="Directory containing serialized WM JSON files",
)

parser.add_argument(
    "--output-base",
    dest="outputBase",
    default="test/materialized",
    help="Top-level output directory for all generated artifacts",
)

parser.add_argument(
    "--wmDasHost",
    default="https://cmsweb-testbed.cern.ch",
    help="DAS host used for dataset to LFN resolution",
)

parser.add_argument("-r", "--wmReqName", default="")
parser.add_argument("-i", "--wmJobIndex", default="")
parser.add_argument("-j", "--wmJobPkg", dest="wmJobPkgFile", default="")
parser.add_argument("-w", "--wmWorkload", dest="wmWorkloadFile", default="")
parser.add_argument("-m", "--wmReqMgr", default="cmsweb-testbed.cern.ch")


if __name__ == "__main__":
    opts = parser.parse_args()

    if opts.fetch_inputs:
        serialized_dir = run_wmcget(opts)
        bundle = load_serialized_bundle(serialized_dir)
    else:
        if not opts.inputDir:
            raise SystemExit("Provide --input-dir or use --fetch-inputs")
        serialized_dir = Path(opts.inputDir).resolve()
        bundle = load_serialized_bundle(serialized_dir)

    request_name = bundle["request"]["RequestName"]
    layout = build_request_layout(opts.outputBase, request_name)

    print("Request root:", layout["request_root"])
    print("WMCore fetched dir:", layout["wmcore_dir"])
    print("DIRAC transformation dir:", layout["dirac_dir"])
    print("DAS host:", opts.wmDasHost)

    translation_document = normalize_bundle(bundle, das_host=opts.wmDasHost)
    emit_translation_document(translation_document, bundle, layout["dirac_dir"])

    request = bundle["request"]
    workload = bundle["workload"]
    task = bundle["task"]
    step = bundle["step"]
    splitting = bundle["splitting"]
    wmjob = bundle.get("wmjob")
    doc = translation_document

    print("Translation and local materialization complete.")
    print("Interactive objects available: request, workload, task, step, splitting, wmjob, doc")
