#!/usr/bin/env python3
"""
Run a locally materialized transformation through CMSWMCoreSplittingPlugin.

This is a stage-1 local runner. It does not contact DIRAC services.
It consumes:

  - Transformations/<Task>.transformation.json
  - PluginInput/<Task>.inputdata.json

and produces:

  - Tasks/<Task>.tasks.json
  - TaskJobs/<Task>/<TaskName>.jobDescription.xml
  - TaskJobs/<Task>/<TaskName>.job.jdl
  - TaskJobs/<Task>/<TaskName>.job.params.json
  - Reports/local_task_materialization_report.json
"""

from pathlib import Path
import argparse

from CMSDirac.Interop.io import read_json, write_json
from CMSDirac.Interop.task_materialize import emit_task_specific_jobs
from CMSDirac.TransformationSystem.Agent.TransformationPlugin import TransformationPlugin


def build_task_records(plugin_result, transformation_name):
    tasks = []

    for idx, item in enumerate(plugin_result, start=1):
        storage_element, lfns = item

        tasks.append(
            {
                "TaskID": idx,
                "TaskName": f"{transformation_name}_task_{idx:04d}",
                "TransformationName": transformation_name,
                "StorageElement": storage_element,
                "LFNs": lfns,
                "InputData": {
                    "LFNCount": len(lfns),
                },
            }
        )

    return tasks


parser = argparse.ArgumentParser(
    description="Run a local transformation through CMSWMCoreSplittingPlugin"
)

parser.add_argument(
    "--transformation-file",
    required=True,
    help="Path to <Task>.transformation.json",
)

parser.add_argument(
    "--plugin-input-file",
    default="",
    help="Optional explicit path to <Task>.inputdata.json",
)

parser.add_argument(
    "--outdir",
    default="",
    help="Optional explicit output directory; defaults to the parent transformation bundle directory",
)


if __name__ == "__main__":
    opts = parser.parse_args()

    transformation_file = Path(opts.transformation_file).resolve()
    transformation = read_json(transformation_file)

    bundle_dir = transformation_file.parent.parent
    outdir = Path(opts.outdir).resolve() if opts.outdir else bundle_dir

    if opts.plugin_input_file:
        plugin_input_file = Path(opts.plugin_input_file).resolve()
    else:
        transformation_name = transformation["Name"]
        plugin_input_file = bundle_dir / "PluginInput" / f"{transformation_name}.inputdata.json"

    plugin_name = transformation["Plugin"]
    plugin_params = transformation.get("PluginParams", {})
    input_data = read_json(plugin_input_file)

    plugin = TransformationPlugin(plugin_name)
    plugin.params = plugin_params
    plugin.setInputData(input_data)

    result = plugin._CMSWMCoreSplittingPlugin()

    if not result.get("OK"):
        raise SystemExit(f"Plugin execution failed: {result.get('Message')}")

    tasks = build_task_records(result["Value"], transformation["Name"])

    (outdir / "Tasks").mkdir(parents=True, exist_ok=True)
    (outdir / "Reports").mkdir(parents=True, exist_ok=True)

    tasks_file = outdir / "Tasks" / f"{transformation['Name']}.tasks.json"
    write_json(tasks_file, tasks)

    emitted_jobs = emit_task_specific_jobs(transformation, tasks, outdir)

    report = {
        "TransformationName": transformation["Name"],
        "Plugin": plugin_name,
        "PluginParams": plugin_params,
        "PluginInputFile": str(plugin_input_file),
        "TaskCount": len(tasks),
        "TasksFile": str(tasks_file),
        "EmittedTaskJobCount": len(emitted_jobs),
        "TaskJobs": emitted_jobs,
        "ServerSideExecution": False,
        "Note": (
            "This is a local stage-1 materialization run. "
            "No live DIRAC Transformation Agent or server-side task creation is involved."
        ),
    }

    write_json(outdir / "Reports" / "local_task_materialization_report.json", report)

    print("Local transformation run complete.")
    print("Transformation:", transformation["Name"])
    print("Plugin:", plugin_name)
    print("Task count:", len(tasks))
    print("Tasks file:", tasks_file)
    print("Task-specific local jobs emitted:", len(emitted_jobs))
