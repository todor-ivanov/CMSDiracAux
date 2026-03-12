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


def _extract_placeholder_input_lfns(task):
    input_dataset = (
        task.get("inputDataset")
        or task.get("inputDataSet")
        or task.get("InputDataset")
        or "mock-dataset"
    )
    input_dataset = str(input_dataset).strip("/").replace("/", "_")

    return [
        f"/store/mock/{input_dataset}/file_{idx:04d}.root"
        for idx in range(1, 6)
    ]


def normalize_bundle(bundle):
    request = bundle["request"]
    task = bundle["task"]
    step = bundle["step"]
    splitting = bundle["splitting"]

    task_path = task["pathName"]
    split_cfg = splitting[task_path]
    perf = split_cfg.get("performance", {}) or {}

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
        TaskName=task.get("taskName", "GenSimFull"),
        TaskPath=task_path,
        ParentTaskNames=[],
        TransformationType="Production",
        TransformationGroup="CMS",
        TransformationFamily="WMCoreInterOp",
        Priority=request.get("RequestPriority"),
        InputDataset={
            "DatasetHint": task.get("inputDataset"),
            "PlaceholderLFNs": _extract_placeholder_input_lfns(task),
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
        "Static placeholder LFNs are used for stage-1 plugin/materialization tests.",
        "WMJob.json handling is intentionally deferred to a later refinement stage.",
        "Next deferred technical step: query DBS and DAS to resolve LFNs from serialized WM objects per task.",
        "Report follow-up: update the complete architecture diagram to reflect WMCore.fetched.d, DIRAC.transf.d, and DIRAC.cwl.d, and include the parameter-mapping tables in the report.",
    ]

    return TranslationDocument(
        SchemaVersion="wmcore-to-dirac/v0.3-request-layout",
        SourceSystem="WMCore",
        TargetSystem="DIRAC",
        Production=prod,
        Tasks=[task_obj],
        Warnings=[],
        Notes=notes,
    )
