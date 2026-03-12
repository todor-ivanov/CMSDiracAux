markdown
# CMSWMCoreSplittingPlugin Design Notes

## Role of the plugin

`CMSWMCoreSplittingPlugin` is the DIRAC-side component responsible for turning
normalized splitting parameters into task groups.

This plugin is not intended to parse raw WMCore workflow objects directly.
The translator performs the normalization step first.

## Current stage responsibilities

At the current stage, the plugin:

- consumes normalized plugin parameters,
- consumes staged input data records,
- groups records according to the requested splitting mode,
- returns DIRAC-style task groups.

Expected output shape:

```python
[
    ("StorageElement", ["lfn1", "lfn2"]),
    ...
]
```

## Supported modes

Current or planned modes:

- EventBased
- FileBased
- LumiBased
- EventAwareLumiBased

The stage-1 implementation focuses first on EventBased, because that matches
the current example workflow most directly.

## Current boundary

The plugin currently groups whole-file work units.

This means that each output task references one or more full LFNs.

## Important postponed topic

DIRAC does not natively support multiple jobs per input file in the same way
WMCore supports sub-file splitting.

This means two topics require future dedicated design:

- intra-file splitting,
- run/lumi masks.

These are intentionally postponed in the current prototype.

## Stage-1 testing strategy

Before live DIRAC integration, the plugin is tested with a mock input-data
sidecar produced by the translator. This allows the splitting logic to be
validated independently of catalog and data-management integration.


## Server-side limitation in the current stage

The current prototype does not yet have access to a CMS-specific DIRAC server-side
extension deployment.

This means that even though the repository can now:

- translate serialized WMCore workflow artifacts,
- materialize local DIRAC-like Job and Transformation objects,
- run the CMSWMCoreSplittingPlugin locally,

it should **not** be expected to create server-side Transformation tasks in a live
DIRAC instance yet.

That future step depends on:

- deployment of the CMS DIRAC extension on the server side,
- registration/allow-listing of `CMSWMCoreSplittingPlugin`,
- implementation of the corresponding Transformation Agent integration,
- later runtime and data-management integration work.
