import json
from dataclasses import asdict
from pathlib import Path


def emit_translation_document(doc, outdir):

    outdir = Path(outdir)

    (outdir / "Transformations").mkdir(parents=True, exist_ok=True)
    (outdir / "Reports").mkdir(parents=True, exist_ok=True)

    with open(outdir / "Reports/translation_document.json", "w") as f:
        json.dump(asdict(doc), f, indent=2)

    task = doc.Tasks[0]

    transf = {
        "TransformationName": task.TaskName,
        "Plugin": task.Splitting.PluginName,
        "Mode": task.Splitting.SplitMode,
    }

    with open(outdir / f"Transformations/{task.TaskName}.json", "w") as f:
        json.dump(transf, f, indent=2)
