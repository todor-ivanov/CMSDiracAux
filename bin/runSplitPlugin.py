#!/usr/bin/env python3

import argparse
import json
from pathlib import Path

from CMSDirac.TransformationSystem.Agent.TransformationPlugin import TransformationPlugin


def read_json(path):
    with open(path) as f:
        return json.load(f)


parser = argparse.ArgumentParser(
    description="Run CMSWMCoreSplittingPlugin against translator output"
)

parser.add_argument(
    "--transf-file",
    required=True,
    help="Path to the transformation JSON produced by wmc2transf.py",
)

parser.add_argument(
    "--base-dir",
    default="",
    help="Optional base directory for resolving PluginInputData relative paths",
)


if __name__ == "__main__":
    opts = parser.parse_args()

    transf_file = Path(opts.transf_file).resolve()
    transf = read_json(transf_file)

    base_dir = Path(opts.base_dir).resolve() if opts.base_dir else transf_file.parent.parent
    input_data_file = base_dir / transf["PluginInputData"]

    input_data = read_json(input_data_file)

    plugin_name = transf["Plugin"]
    plugin_params = transf.get("PluginParams", {})

    plugin = TransformationPlugin(plugin_name)
    plugin.params = plugin_params
    plugin.setInputData(input_data)

    result = plugin._CMSWMCoreSplittingPlugin()

    print(json.dumps(result, indent=2))
