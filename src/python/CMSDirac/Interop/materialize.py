import json
from xml.sax.saxutils import escape

from CMSDirac.Interop.model import LocalDIRACJob, LocalDIRACTransformation


def _stringify(value):
    if value is None:
        return ""
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, sort_keys=True)
    return str(value)


def build_local_dirac_job(task, wmjob=None):
    job_name = f"{task.TaskName}.job"

    workflow_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        "<Workflow>",
        f'  <Parameter name="JobName" value="{escape(job_name)}"/>',
        f'  <Parameter name="Executable" value="{escape(task.Step.Executable)}"/>',
        f'  <Parameter name="SoftwareVersion" value="{escape(_stringify(task.Step.SoftwareVersion))}"/>',
        f'  <Parameter name="SoftwareArchitecture" value="{escape(_stringify(task.Step.SoftwareArchitecture))}"/>',
        f'  <Parameter name="TaskPath" value="{escape(task.TaskPath)}"/>',
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
    workflow_xml = "\n".join(workflow_lines) + "\n"

    input_sandbox = task.Step.InputArtifacts + ["WMWorkload.pkl", "JobPackage.pkl"]
    output_sandbox = task.Step.OutputArtifacts + ["*.log"]

    jdl_lines = [
        f'JobName = "{job_name}";',
        'JobType = "User";',
        f'Executable = "{task.Step.Executable}";',
        f'Arguments = "{" ".join(task.Step.Arguments)}";',
        f"InputSandbox = {json.dumps(input_sandbox)};",
        f"OutputSandbox = {json.dumps(output_sandbox)};",
    ]
    if task.Step.MemoryMB:
        jdl_lines.append(f"Memory = {int(task.Step.MemoryMB)};")
    if task.Step.CpuCores:
        jdl_lines.append(f"CPUNumber = {int(task.Step.CpuCores)};")
    if task.Step.GpuRequired:
        jdl_lines.append('Tag = {"GPU"};')

    jdl = "\n".join(jdl_lines) + "\n"

    return LocalDIRACJob(
        Name=job_name,
        WorkflowXML=workflow_xml,
        JDL=jdl,
        Parameters={},
    )


def build_local_transformation(task, local_job):
    plugin_params = {
        "Mode": task.Splitting.SplitMode,
        "FilesPerJob": task.Splitting.FilesPerJob,
        "EventsPerJob": task.Splitting.EventsPerJob,
        "LumisPerJob": task.Splitting.LumisPerJob,
        "EventsPerLumi": task.Splitting.EventsPerLumi,
        "ResourceHints": task.Splitting.ResourceHints,
        "StaticDatasetMode": task.Splitting.StaticDatasetMode,
    }

    transf_params = {
        "SourceTaskPath": task.TaskPath,
        "SourceRefs": task.SourceRef,
        "PlaceholderLFNs": task.InputDataset.get("PlaceholderLFNs", []),
        "ServerSideNote": (
            "Server-side task creation is not expected yet; the CMS DIRAC extension "
            "and Transformation Agent/plugin deployment are not available."
        ),
    }

    return LocalDIRACTransformation(
        Name=task.TaskName,
        Type=task.TransformationType,
        Group=task.TransformationGroup,
        Family=task.TransformationFamily,
        Plugin=task.Splitting.PluginName,
        PluginParams=plugin_params,
        BodyXML=local_job.WorkflowXML,
        InputData={"LFNs": task.InputDataset.get("PlaceholderLFNs", [])},
        Parameters=transf_params,
    )
