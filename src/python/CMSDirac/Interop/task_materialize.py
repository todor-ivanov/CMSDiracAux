import json
from pathlib import Path
from xml.sax.saxutils import escape

from CMSDirac.Interop.io import write_json, write_text


def _stringify(value):
    if value is None:
        return ""
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, sort_keys=True)
    return str(value)


def _build_task_workflow_xml(transformation, task_record):
    transformation_name = transformation["Name"]
    task_name = task_record["TaskName"]
    lfns = task_record.get("LFNs", [])
    source_task_path = transformation.get("Parameters", {}).get("SourceTaskPath", "")

    workflow_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        "<Workflow>",
        f'  <Parameter name="JobName" value="{escape(task_name)}"/>',
        f'  <Parameter name="TransformationName" value="{escape(transformation_name)}"/>',
        f'  <Parameter name="SourceTaskPath" value="{escape(source_task_path)}"/>',
        f'  <Parameter name="StorageElement" value="{escape(_stringify(task_record.get("StorageElement")))}"/>',
        f'  <Parameter name="InputLFNs" value="{escape(_stringify(lfns))}"/>',
        '  <Step name="FetchCMSDiracAux">',
        '    <Command>/bin/git clone --depth 1 -b runtime https://github.com/todor-ivanov/CMSDiracAux.git</Command>',
        '  </Step>',
        '  <Step name="SourceCMSDiracAux">',
        '    <Command>source ./CMSDiracAux/env.sh</Command>',
        '  </Step>',
        '  <Step name="RunCMSStartup">',
        '    <Command>./CMSDiracAux/bin/Startup.py</Command>',
        '  </Step>',
        "</Workflow>",
    ]
    return "\n".join(workflow_lines) + "\n"


def _build_task_jdl(transformation, task_record):
    plugin_params = transformation.get("PluginParams", {})
    resource_hints = plugin_params.get("ResourceHints", {}) or {}

    input_sandbox = [
        "step_cfg.py",
        "WMWorkload.pkl",
        "JobPackage.pkl",
    ]
    output_sandbox = [
        "FrameworkJobReport.xml",
        "wmcoreReport.json",
        "*.log",
    ]

    lines = [
        f'JobName = "{task_record["TaskName"]}";',
        'JobType = "User";',
        'Executable = "cmsRun";',
        'Arguments = "step_cfg.py";',
        f"InputSandbox = {json.dumps(input_sandbox)};",
        f"OutputSandbox = {json.dumps(output_sandbox)};",
    ]

    memory_mb = resource_hints.get("MemoryMB")
    if memory_mb:
        lines.append(f"Memory = {int(memory_mb)};")

    if resource_hints.get("RequiresGPU"):
        lines.append('Tag = {"GPU"};')

    return "\n".join(lines) + "\n"


def _build_task_params(transformation, task_record):
    return {
        "TaskID": task_record["TaskID"],
        "TaskName": task_record["TaskName"],
        "TransformationName": transformation["Name"],
        "StorageElement": task_record.get("StorageElement"),
        "LFNs": task_record.get("LFNs", []),
        "LFNCount": task_record.get("InputData", {}).get("LFNCount", 0),
        "Plugin": transformation.get("Plugin"),
        "PluginParams": transformation.get("PluginParams", {}),
        "TransformationParameters": transformation.get("Parameters", {}),
        "ServerSideExecution": False,
        "Note": (
            "Local task-specific job materialization only. "
            "No live DIRAC server-side job or task injection is performed."
        ),
    }


def emit_task_specific_jobs(transformation, tasks, outdir):
    outdir = Path(outdir)
    task_dir = outdir / "TaskJobs" / transformation["Name"]
    task_dir.mkdir(parents=True, exist_ok=True)

    emitted = []

    for task_record in tasks:
        task_name = task_record["TaskName"]

        workflow_xml = _build_task_workflow_xml(transformation, task_record)
        jdl = _build_task_jdl(transformation, task_record)
        params = _build_task_params(transformation, task_record)

        xml_path = task_dir / f"{task_name}.jobDescription.xml"
        jdl_path = task_dir / f"{task_name}.job.jdl"
        params_path = task_dir / f"{task_name}.job.params.json"

        write_text(xml_path, workflow_xml)
        write_text(jdl_path, jdl)
        write_json(params_path, params)

        emitted.append(
            {
                "TaskName": task_name,
                "JobDescriptionXML": str(xml_path),
                "JobJDL": str(jdl_path),
                "JobParams": str(params_path),
            }
        )

    return emitted
