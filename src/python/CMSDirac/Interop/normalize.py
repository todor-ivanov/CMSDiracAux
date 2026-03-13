from CMSDirac.Interop.das import resolve_task_lfns
from CMSDirac.Interop.model import (
    CanonicalProduction,
    CanonicalSplitting,
    CanonicalStep,
    CanonicalTask,
    TranslationDocument,
)


def infer_gpu_required(request, step):
    if request.get("RequiresGPU"):
        return True
    if request.get("GPUParams"):
        return True

    runtime = step.get("runtime", {}) or {}
    return bool(runtime.get("requiresGPU"))


def _derive_task_name(task):
    # First prefer explicit task names if present
    for key in ("taskName", "name", "TaskName", "Name"):
        value = task.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()

    # Otherwise derive from pathName, e.g.
    # /REQUEST/GenSimFull      -> GenSimFull
    # /REQUEST/DataProcessing  -> DataProcessing
    path_name = task.get("pathName", "")
    if isinstance(path_name, str) and path_name.strip():
        parts = [part for part in path_name.split("/") if part]
        if parts:
            return parts[-1]

    return "UnknownTask"


def _extract_dataset_name(task):
    task_input = task.get("input") or {}
    dataset_info = task_input.get("dataset") or {}
    return dataset_info.get("name")


def _extract_placeholder_input_lfns(task):
    input_dataset = _extract_dataset_name(task) or "mock-dataset"
    input_dataset = str(input_dataset).strip("/").replace("/", "_")

    return [
        f"/store/mock/{input_dataset}/file_{idx:04d}.root"
        for idx in range(1, 6)
    ]


def normalize_bundle(bundle, das_host="https://cmsweb-testbed.cern.ch"):
    request = bundle["request"]
    task = bundle["task"]
    step = bundle["step"]
    splitting = bundle["splitting"]

    task_path = task["pathName"]
    task_name = _derive_task_name(task)
    split_cfg = splitting[task_path]
    perf = split_cfg.get("performance", {}) or {}

    das_resolution = resolve_task_lfns(task, host=das_host)
    placeholder_lfns = _extract_placeholder_input_lfns(task)
    resolved_lfns = das_resolution["lfns"] or placeholder_lfns

    step_obj = CanonicalStep(
        StepName=step.get("stepName", "cmsRun1"),
        Executable="cmsRun",
        Arguments=["step_cfg.py"],
        SoftwareVersion=request.get("CMSSWVersion"),
        SoftwareArchitecture=request.get("ScramArch"),
        MemoryMB=perf.get("memoryRequirement") or request.get("Memory"),
        CpuCores=request.get("Multicore", 1),
        GpuRequired=infer_gpu_required(request, step),
        InputArtifacts=["step_cfg.py"],
        OutputArtifacts=["FrameworkJobReport.xml", "wmcoreReport.json"],
        SourceRef={"WMStep": "WMStep.json"},
    )

    split_obj = CanonicalSplitting(
        PluginName="CMSWMCoreSplittingPlugin",
        SplitMode=split_cfg.get("algorithm", "EventBased"),
        FilesPerJob=split_cfg.get("files_per_job"),
        EventsPerJob=split_cfg.get("events_per_job"),
        LumisPerJob=split_cfg.get("lumis_per_job"),
        EventsPerLumi=split_cfg.get("events_per_lumi"),
        ResourceHints={
            "MemoryMB": perf.get("memoryRequirement"),
            "TimePerEvent": perf.get("timePerEvent"),
            "SizePerEvent": perf.get("sizePerEvent"),
            "RequiresGPU": step_obj.GpuRequired,
        },
        StaticDatasetMode=True,
        SourceRef={"WMSplitting": "WMSplitting.json"},
    )

    task_obj = CanonicalTask(
        RequestName=request["RequestName"],
        TaskName=task_name,
        TaskPath=task_path,
        ParentTaskNames=[],
        TransformationType="Production",
        TransformationGroup="CMS",
        TransformationFamily="WMCoreInterOp",
        Priority=request.get("RequestPriority"),
        InputDataset={
            "DatasetHint": _extract_dataset_name(task),
            "DatasetsResolved": das_resolution["datasets"],
            "LFNResolutionMode": das_resolution["resolution_mode"],
            "LFNResolutionErrors": das_resolution["errors"],
            "PlaceholderLFNs": placeholder_lfns,
            "ResolvedLFNs": resolved_lfns,
            "LFNs": resolved_lfns,
        },
        OutputDataset={
            "ProcessingString": request.get("ProcessingString"),
            "AcquisitionEra": request.get("AcquisitionEra"),
        },
        SitePolicy={},
        Step=step_obj,
        Splitting=split_obj,
        SourceRef={
            "WMTask": "WMTask.json",
            "WMStep": "WMStep.json",
            "WMSplitting": "WMSplitting.json",
        },
    )

    prod = CanonicalProduction(
        ProductionName=request["RequestName"],
        ProductionType="Production",
        Priority=request.get("RequestPriority"),
        CampaignName=request.get("Campaign"),
        AcquisitionEra=request.get("AcquisitionEra"),
        ProcessingString=request.get("ProcessingString"),
        PrepId=request.get("PrepID"),
    )

    notes = [
        "Server-side DIRAC Transformation Agent integration is not available in the current environment.",
        "DAS-based LFN resolution is attempted from WMTask dataset hints; placeholder LFNs are used as fallback.",
        "WMJob.json handling is intentionally deferred to a later refinement stage.",
        "Report follow-up: update the complete architecture diagram to reflect WMCore.fetched.d, DIRAC.transf.d, and DIRAC.cwl.d, and include the parameter-mapping tables in the report.",
        "Preserve the DIRAC InputSandbox vs jobDescription.xml analysis as a dedicated report section.",
    ]

    return TranslationDocument(
        SchemaVersion="wmcore-to-dirac/v0.4-das-lfn-resolution",
        SourceSystem="WMCore",
        TargetSystem="DIRAC",
        Production=prod,
        Tasks=[task_obj],
        Warnings=[],
        Notes=notes,
    )
