# Future Data Management Architecture Notes

## Current status

The current proof of concept intentionally does not implement the full data
discovery and data management chain needed for production usage.

Instead, it uses staged or synthetic input records to validate the workflow
translation and splitting architecture.

## Future topic 1: sub-file execution semantics

DIRAC transformations currently operate at file granularity.

WMCore, however, supports richer splitting policies that may require more than
one job to be produced from a single input file.

This creates a future design problem around:

- intra-file splitting,
- event-range style execution,
- run/lumi-aware partitioning.

These topics need dedicated design work in later stages.

## Future topic 2: run/lumi masks

CMS workflows can require explicit run/lumi selection.

Future solutions may include:

- passing run/lumi masks through job arguments,
- generating sidecar mask files,
- extending plugin metadata to carry run/lumi partitions.

This will be especially important for real-data workflows.

## Future topic 3: data discovery

In a future CMS-oriented architecture, authoritative data discovery should rely on:

- DBS
- DAS

These services provide dataset, block, file, event, and run/lumi information.

This is expected to replace the current stage-1 synthetic or staged input data.

## Future topic 4: data management and replica handling

The long-term system will likely need to replace or integrate parts of DIRAC's
internal data management flow with CMS-native mechanisms.

A future design should consider:

- using DBS/DAS for discovery,
- using Rucio for replica and transfer management,
- deciding how to integrate or replace DIRAC-side data management requests.

This may affect interactions traditionally associated with DIRAC data/request
management components.

## Likely long-term hybrid model

A plausible future architecture is:

```text
Data discovery   -> DBS / DAS
Replica lookup   -> Rucio
Workflow control -> DIRAC
Execution        -> DIRAC
```

This would preserve CMS-native data semantics while still using DIRAC for
workflow and workload execution.

## Current checkpoint

All topics in this document are intentionally out of scope for the current stage.
The current priority remains:

- translation of serialized WMCore workflow objects,
- plugin-driven task grouping,
- validation of the basic execution path.
