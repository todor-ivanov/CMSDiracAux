# Current Stage Limitations and Checkpoints

## Server-side limitation

The current environment does not provide access to a CMS-specific DIRAC server-side
extension deployment.

As a result, the current prototype can:

- translate serialized WMCore workflow artifacts,
- materialize local DIRAC-like Job and Transformation objects,
- execute the CMSWMCoreSplittingPlugin locally,

but cannot yet produce real server-side Transformation task creation.

## Data visibility limitation

The current DIRAC test environment does not see CMS data or CMS storage
definitions in the way needed for real CMS data discovery and runtime execution.

Because of that, the current stage uses placeholder LFNs and static plugin-input
sidecars.

## Postponed topics

The following topics are intentionally postponed:

- intra-file splitting,
- run/lumi masks,
- CMS DBS/DAS-based data discovery,
- integration or replacement of DIRAC data-management calls with Rucio,
- full CMS runtime and sandbox distribution redesign.

## Current milestone

The current milestone is:

- represent the WMCore workflow structure faithfully,
- preserve key CMS/WMBS semantics locally,
- materialize DIRAC-style objects on disk,
- prepare the path toward later workflow-language translation and/or DIRACX-facing evolution.
