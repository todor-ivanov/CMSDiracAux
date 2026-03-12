from dataclasses import asdict
from pathlib import Path

from CMSDirac.Interop.io import write_json, write_text
from CMSDirac.Interop.materialize import build_local_dirac_job, build_local_transformation


def _build_plugin_input_data(task):
    events_per_job = task.Splitting.EventsPerJob or 100
    lfns = task.InputDataset.get("PlaceholderLFNs", [])

    return {
        lfn: {
            "se": "T2_TEST_SE",
            "events": events_per_job,
        }
        for lfn in lfns
    }

def _build_mock_input_data(task):
    """
    Stage-1 mock input dataset for the splitting plugin.

    Since we do not yet have full WMCore dataset -> DIRAC FileCatalog mapping,
    we emit a small synthetic input-data file that can be consumed directly by
    CMSWMCoreSplittingPlugin.

    The number of entries is intentionally small and deterministic.
    """
    events_per_job = task.Splitting.EventsPerJob or 100

    return {
        f"/store/mock/{task.TaskName}/file_{idx:04d}.root": {
            "se": "T2_TEST_SE",
            "events": events_per_job,
        }
        for idx in range(1, 6)
    }

def emit_translation_document(doc, bundle, outdir):
    outdir = Path(outdir)

    (outdir / "Reports").mkdir(parents=True, exist_ok=True)
    (outdir / "Transformations").mkdir(parents=True, exist_ok=True)
    (outdir / "PluginInput").mkdir(parents=True, exist_ok=True)
    (outdir / "Jobs").mkdir(parents=True, exist_ok=True)

    write_json(outdir / "Reports" / "translation_document.json", asdict(doc))

    task = doc.Tasks[0]
    wmjob = bundle.get("wmjob")

    local_job = build_local_dirac_job(task, wmjob=wmjob)
    local_transf = build_local_transformation(task, local_job)

    write_text(outdir / f"Jobs/{task.TaskName}.jobDescription.xml", local_job.WorkflowXML)
    write_text(outdir / f"Jobs/{task.TaskName}.job.jdl", local_job.JDL)
    write_json(outdir / f"Jobs/{task.TaskName}.job.params.json", local_job.Parameters)

    write_text(outdir / f"Transformations/{task.TaskName}.transformation.body.xml", local_transf.BodyXML)
    write_json(outdir / f"Transformations/{task.TaskName}.transformation.params.json", local_transf.Parameters)
    write_json(outdir / f"Transformations/{task.TaskName}.transformation.json", asdict(local_transf))

    plugin_input = _build_plugin_input_data(task)
    write_json(outdir / f"PluginInput/{task.TaskName}.inputdata.json", plugin_input)

    report = {
        "Workflow": doc.Production.ProductionName,
        "TransformationsCreated": len(doc.Tasks),
        "Notes": doc.Notes,
        "Warnings": doc.Warnings,
        "ServerSideReady": False,
        "ServerSideReadyReason": (
            "CMS server-side DIRAC extension, plugin deployment, and Transformation Agent integration "
            "are not yet available in the current environment."
        ),
    }
    write_json(outdir / "Reports/translation_report.json", report)
