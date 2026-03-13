from dataclasses import asdict
from pathlib import Path

from CMSDirac.Interop.io import write_json, write_text
from CMSDirac.Interop.materialize import build_local_dirac_job, build_local_transformation


def _build_plugin_input_data(task):
    file_records = task.InputDataset.get("ResolvedFileRecords", []) or []
    lfns = (
        task.InputDataset.get("LFNs")
        or task.InputDataset.get("ResolvedLFNs")
        or task.InputDataset.get("PlaceholderLFNs", [])
    )

    # Best case: build from full DAS file records
    if file_records:
        plugin_input = {}

        for record in file_records:
            lfn = record.get("name")
            if not lfn:
                continue

            plugin_input[lfn] = {
                "events": int(record.get("nevents", 0) or 0),
                "se": "UNKNOWN_SE",
                "size": int(record.get("size", 0) or 0),
                "dataset": record.get("dataset"),
                "block": record.get("block.name") or record.get("block_name"),
            }

        if plugin_input:
            return plugin_input

    # Fallback: resolved LFNs but without per-file metadata
    default_events = task.Splitting.EventsPerJob or 0

    return {
        lfn: {
            "events": int(default_events),
            "se": "UNKNOWN_SE",
        }
        for lfn in lfns
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
    write_json(outdir / "Reports" / "translation_report.json", report)
