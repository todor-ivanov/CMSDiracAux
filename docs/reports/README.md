# CMSDiracAux Technical Report

This directory contains the evolving technical report for the
WMCore → DIRAC interoperability proof of concept implemented in
CMSDiracAux.

The report is organized as follows.

## Core architecture

- `system-architecture.md`
- `architecture-diagram.md`
- `architecture-diagram-readable.md`
- `architecture-and-design-notes.md`

## Conceptual design

- `translation-ir-design.md`
- `wmcore-vs-dirac-execution-model.md`
- `wmcore-dirac-parameter-mapping.md`

## Evaluation

- `poc-evaluation.md`

## Development record

- `checkpoints/`

## Current major PoC limitations

- only the first 20 files per dataset are materialized
- no full run/lumi support
- no server-side DIRAC transformation agent integration yet

## Current request-scoped output layout
```
REQUEST_ROOT
|
|-- WMCore.fetched.d
|
|-- DIRAC.transf.d
|
`-- DIRAC.cwl.d
```
## Active follow-up items

- update the architecture diagram whenever the pipeline structure changes
- preserve the parameter mapping tables
- preserve the DIRAC InputSandbox vs jobDescription.xml analysis
- preserve the DAS/DBS data discovery branch notes
