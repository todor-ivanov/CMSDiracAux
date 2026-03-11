import json
from dataclasses import asdict
from pathlib import Path

from CMSDirac.Interop.io import write_json


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


def emit_translation_document(doc, outdir):
    outdir = Path(outdir)

    (outdir / "Transformations").mkdir(parents=True, exist_ok=True)
    (outdir / "Reports").mkdir(parents=True, exist_ok=True)
    (outdir / "PluginInput").mkdir(parents=True, exist_ok=True)

    write_json(outdir / "Reports" / "translation_document.json", asdict(doc))

    task = doc.Tasks[0]

    transf = {
        "TransformationName": task.TaskName,
        "Plugin": task.Splitting.PluginName,
        "PluginParams": {
            "Mode": task.Splitting.SplitMode,
            "FilesPerJob": task.Splitting.FilesPerJob,
            "EventsPerJob": task.Splitting.EventsPerJob,
            "LumisPerJob": task.Splitting.LumisPerJob,
            "EventsPerLumi": task.Splitting.EventsPerLumi,
            "ResourceHints": task.Splitting.ResourceHints,
            "StaticDatasetMode": task.Splitting.StaticDatasetMode,
        },
        "PluginInputData": f"PluginInput/{task.TaskName}.inputdata.json",
    }

    write_json(outdir / f"Transformations/{task.TaskName}.json", transf)

    plugin_input_data = _build_mock_input_data(task)
    write_json(
        outdir / f"PluginInput/{task.TaskName}.inputdata.json",
        plugin_input_data,
    )
