#!/usr/bin/env python3
"""
Export a locally materialized transformation bundle to a minimal CWL bundle.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from CMSDirac.Interop.io import read_json, write_text
from CMSDirac.Interop.layout import build_request_layout


def dump_yaml_scalar(value):
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)

    text = str(value)
    text = text.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{text}"'


def dump_yaml(value, indent=0):
    space = " " * indent

    if isinstance(value, dict):
        lines = []
        for key, item in value.items():
            if isinstance(item, (dict, list)):
                lines.append(f"{space}{key}:")
                lines.append(dump_yaml(item, indent + 2))
            else:
                lines.append(f"{space}{key}: {dump_yaml_scalar(item)}")
        return "\n".join(lines)

    if isinstance(value, list):
        lines = []
        for item in value:
            if isinstance(item, (dict, list)):
                lines.append(f"{space}-")
                lines.append(dump_yaml(item, indent + 2))
            else:
                lines.append(f"{space}- {dump_yaml_scalar(item)}")
        return "\n".join(lines)

    return f"{space}{dump_yaml_scalar(value)}"


def build_tool_cwl():
    return """cwlVersion: v1.2
class: CommandLineTool
baseCommand:
  - bash
inputs:
  task_name:
    type: string
  transformation_name:
    type: string
  storage_element:
    type: string
  lfns:
    type:
      type: array
      items: string
outputs:
  execution_log:
    type: File
    outputBinding:
      glob: execution.log
arguments:
  - position: 1
    valueFrom: |
      set -e
      echo "Transformation: $(inputs.transformation_name)" > execution.log
      echo "Task: $(inputs.task_name)" >> execution.log
      echo "StorageElement: $(inputs.storage_element)" >> execution.log
      echo "LFNs:" >> execution.log
      for lfn in $(inputs.lfns); do
        echo "$lfn" >> execution.log
      done
      echo "Fetching CMSDiracAux runtime bundle" >> execution.log
      echo "Sourcing environment" >> execution_log
      echo "Running Startup.py" >> execution.log
stdout: execution.log
requirements:
  InlineJavascriptRequirement: {}
"""


def build_workflow_cwl():
    return """cwlVersion: v1.2
class: Workflow
inputs:
  task_name: string
  transformation_name: string
  storage_element: string
  lfns:
    type:
      type: array
      items: string
outputs:
  execution_log:
    type: File
    outputSource: run_task/execution_log
steps:
  run_task:
    run: tool.cwl
    in:
      task_name: task_name
      transformation_name: transformation_name
      storage_element: storage_element
      lfns: lfns
    out:
      - execution_log
"""


def build_job_metadata(transformation):
    return {
        "job_type": "User",
        "source": "CMSDiracAux",
        "workflow_type": "cwl",
        "transformation_name": transformation["Name"],
        "plugin": transformation.get("Plugin"),
        "note": (
            "Stage-1 CWL export of a locally materialized CMS workflow. "
            "Intended for local validation and future dirac-cwl alignment."
        ),
    }


def build_transformation_metadata(transformation, tasks):
    plugin_params = transformation.get("PluginParams", {})
    return {
        "job_type": "Transformation",
        "source": "CMSDiracAux",
        "workflow_type": "cwl",
        "transformation_name": transformation["Name"],
        "group_size": len(tasks),
        "plugin": transformation.get("Plugin"),
        "query_parameters": {
            "static_dataset_mode": plugin_params.get("StaticDatasetMode", True),
            "mode": plugin_params.get("Mode"),
        },
        "note": (
            "Stage-1 transformation metadata exported from a local DIRAC-like "
            "materialization bundle."
        ),
    }


def build_task_input_yaml(transformation, task_record):
    return {
        "task_name": task_record["TaskName"],
        "transformation_name": transformation["Name"],
        "storage_element": task_record.get("StorageElement", "UnknownSE"),
        "lfns": task_record.get("LFNs", []),
    }


def build_readme(transformation_name, task_count):
    return f"""# CWL Export Bundle

This bundle was generated from a local CMSDiracAux transformation materialization.

Transformation name: {transformation_name}
Exported task count: {task_count}

Contents

- tool.cwl
  Generic stage-1 CommandLineTool representing the CMS runtime bootstrap.

- workflow.cwl
  Single-step CWL workflow wrapping tool.cwl.

- inputs
  One YAML input file per generated task.

- metadata/job.metadata.yaml
  Minimal job-style metadata.

- metadata/transformation.metadata.yaml
  Minimal transformation-style metadata.

Typical local validation

cwltool workflow.cwl inputs/task_0001.yaml

This bundle is intended as a stage-1 CWL representation aligned with the
dirac-cwl direction, not as a final CMS runtime model.
"""


parser = argparse.ArgumentParser(
    description="Export a local transformation bundle to a minimal CWL bundle"
)

parser.add_argument(
    "--bundle-dir",
    required=True,
    help="Path to the local DIRAC transformation bundle",
)

parser.add_argument(
    "--transformation-name",
    default="",
    help="Transformation name. If omitted, the first transformation JSON found is used.",
)

parser.add_argument(
    "--output-base",
    dest="outputBase",
    default="",
    help="Optional top-level output base. If set, output goes to REQUEST_NAME/DIRAC.cwl.d",
)

parser.add_argument(
    "--outdir",
    default="",
    help="Optional explicit output directory. If not set, the request layout is used when possible.",
)


if __name__ == "__main__":
    opts = parser.parse_args()

    bundle_dir = Path(opts.bundle_dir).resolve()

    if opts.transformation_name:
        transformation_name = opts.transformation_name
        transformation_file = bundle_dir / "Transformations" / f"{transformation_name}.transformation.json"
    else:
        candidates = sorted((bundle_dir / "Transformations").glob("*.transformation.json"))
        if not candidates:
            raise SystemExit("No transformation JSON files found under Transformations")
        transformation_file = candidates[0]
        transformation_name = transformation_file.name.replace(".transformation.json", "")

    tasks_file = bundle_dir / "Tasks" / f"{transformation_name}.tasks.json"

    if not transformation_file.exists():
        raise SystemExit(f"Missing transformation file: {transformation_file}")
    if not tasks_file.exists():
        raise SystemExit(f"Missing tasks file: {tasks_file}. Run bin/runLocalTransformation.py first.")

    transformation = read_json(transformation_file)
    tasks = read_json(tasks_file)

    request_name = transformation.get("Parameters", {}).get("WMRequestName")

    if opts.outdir:
        outdir = Path(opts.outdir).resolve()
    elif opts.outputBase and request_name:
        layout = build_request_layout(opts.outputBase, request_name)
        outdir = layout["cwl_dir"]
    else:
        outdir = bundle_dir.parent / "DIRAC.cwl.d"

    inputs_dir = outdir / "inputs"
    metadata_dir = outdir / "metadata"

    inputs_dir.mkdir(parents=True, exist_ok=True)
    metadata_dir.mkdir(parents=True, exist_ok=True)

    write_text(outdir / "tool.cwl", build_tool_cwl())
    write_text(outdir / "workflow.cwl", build_workflow_cwl())

    for idx, task_record in enumerate(tasks, start=1):
        input_payload = build_task_input_yaml(transformation, task_record)
        write_text(inputs_dir / f"task_{idx:04d}.yaml", dump_yaml(input_payload) + "\n")

    write_text(metadata_dir / "job.metadata.yaml", dump_yaml(build_job_metadata(transformation)) + "\n")
    write_text(
        metadata_dir / "transformation.metadata.yaml",
        dump_yaml(build_transformation_metadata(transformation, tasks)) + "\n",
    )
    write_text(outdir / "README.md", build_readme(transformation_name, len(tasks)))

    print("CWL export complete.")
    print("Transformation:", transformation_name)
    print("Bundle directory:", outdir)
