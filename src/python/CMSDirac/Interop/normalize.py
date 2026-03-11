from CMSDirac.Interop.model import *


def normalize_bundle(bundle):

    request = bundle["request"]
    task = bundle["task"]
    step = bundle["step"]
    splitting = bundle["splitting"]

    task_path = task["pathName"]

    step_obj = CanonicalStep(
        StepName="cmsRun",
        Executable="cmsRun",
        Arguments=["step_cfg.py"],
        SoftwareVersion=request.get("CMSSWVersion"),
        SoftwareArchitecture=request.get("ScramArch"),
    )

    split_cfg = splitting[task_path]

    split_obj = CanonicalSplitting(
        PluginName="CMSWMCoreSplittingPlugin",
        SplitMode=split_cfg.get("algorithm"),
        EventsPerJob=split_cfg.get("events_per_job"),
    )

    task_obj = CanonicalTask(
        TaskName=task.get("taskName", "GenSimFull"),
        TaskPath=task_path,
        ParentTaskNames=[],
        TransformationType="Simulation",
        TransformationGroup="CMS",
        TransformationFamily="WMCoreInterOp",
        Priority=request.get("RequestPriority"),
        InputDataset={},
        OutputDataset={},
        SitePolicy={},
        Step=step_obj,
        Splitting=split_obj,
    )

    prod = CanonicalProduction(
        ProductionName=request["RequestName"],
        ProductionType="Production",
        Priority=request.get("RequestPriority"),
    )

    return TranslationDocument(
        SchemaVersion="wmcore-to-dirac/v0.1",
        SourceSystem="WMCore",
        TargetSystem="DIRAC",
        Production=prod,
        Tasks=[task_obj],
    )
