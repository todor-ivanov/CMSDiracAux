# Next Milestone: CWL Export

## Current decision

The next milestone is not deeper WMBS alignment.

Instead, the next milestone is to express the currently materialized local
DIRAC-style CMS workflow in a CWL-digestible form aligned with the dirac-cwl
direction.

## Why this is the shortest path

The current environment does not support:

- CMS-specific DIRAC server-side extensions
- plugin deployment on the server side
- real CMS data visibility in the DIRAC test setup

Because of that, the most useful next step is to export the local
materialization bundle into CWL and validate it locally.

## Current request-scoped output layout

REQUEST_ROOT
    ├── WMCore.fetched.d
    ├── DIRAC.transf.d
    └── DIRAC.cwl.d

## Report follow-up note

The report should include:

- the updated complete architecture diagram using the three-stage layout
- the WMCore to canonical IR to DIRAC mapping tables
- the rationale for choosing CWL as the next milestone
- the deferred note that the next technical branch is DBS and DAS based LFN resolution
