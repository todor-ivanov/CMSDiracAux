# CWL Export Path for the CMSDiracAux WMCore to DIRAC PoC

## Purpose

The next milestone of this proof of concept is to express the already
materialized local DIRAC-like CMS workflow in a CWL-digestible form.

The short-term goal is not to reproduce the full DIRAC Python object model in
CWL, but to export the current local transformation and task structure into a
bundle that is structurally compatible with the direction taken by dirac-cwl.

## Current local materialization baseline

At the current stage, the repository can already produce:

- local DIRAC-like job artifacts
- local DIRAC-like transformation artifacts
- plugin input sidecars
- grouped tasks
- task-specific local jobs

This means the PoC already has enough structure to perform a deterministic
export into CWL.

Current local pipeline:

WMCore request
    ↓
wmcGet.py
    ↓
serialized WM JSON artifacts
    ↓
wmc2transf.py
    ↓
canonical translation objects
    ↓
local DIRAC style artifacts
    ↓
runLocalTransformation.py
    ↓
CMSWMCoreSplittingPlugin
    ↓
Tasks and TaskJobs

## New request-scoped output layout

The output layout is now organized under one request-scoped root:

REQUEST_ROOT
    ├── WMCore.fetched.d
    ├── DIRAC.transf.d
    └── DIRAC.cwl.d

This separates:

- fetched and serialized WMCore artifacts
- local DIRAC-style materialization artifacts
- CWL export artifacts

## Reference target: dirac-cwl

The dirac-cwl prototype supports:

- local workflow validation with cwltool
- submission as DIRAC jobs
- submission as DIRAC transformations
- submission as DIRAC productions

The current PoC targets a bundle shape that is easy to validate locally and is
structurally aligned with those usage modes.

## Shortest export path

The shortest path to the milestone is:

1. keep the current local materialized transformation as the source
2. export one task tool as CWL CommandLineTool
3. export one workflow wrapper as CWL Workflow
4. export one YAML input file per generated task
5. export one job metadata YAML
6. export one transformation metadata YAML
7. validate locally with cwltool
8. only then align more tightly with dirac-cwl submission commands

## Source and target mapping

Source objects:

- DIRAC.transf.d/Transformations/NAME.transformation.json
- DIRAC.transf.d/Tasks/NAME.tasks.json
- optionally DIRAC.transf.d/Jobs
- optionally DIRAC.transf.d/TaskJobs

Target bundle:

DIRAC.cwl.d
    tool.cwl
    workflow.cwl
    inputs
    metadata
    README.md

## Conceptual mapping

### Local transformation to CWL workflow

A local transformation becomes:

- one CWL Workflow
- referencing one CommandLineTool
- with task-specific input YAML files

### Task-specific local job to CWL parameter set

Each generated task-specific local job becomes:

- one YAML file
- containing:
  - task name
  - transformation name
  - storage element
  - LFN list
  - optional resource hints

### CMS runtime bootstrap to CommandLineTool

The current CMS runtime bootstrap is represented in CWL as a single
CommandLineTool step.

That tool encapsulates the stage-1 execution model:

- fetch CMSDiracAux
- source the environment
- run Startup.py
- pass task-specific LFNs and metadata as inputs

## Stage-1 scope

Included:

- one generic CommandLineTool
- one Workflow wrapper
- one input YAML per generated task
- one job metadata YAML
- one transformation metadata YAML

Not included yet:

- full WMBS job semantics
- intra-file splitting
- run/lumi masks
- real DBS or DAS based data resolution
- Rucio based data management integration
- multi-step production decomposition

## Definition of done for the milestone

This milestone is achieved when:

- the local transformation bundle can be exported into a CWL bundle
- the generated CWL validates with cwltool
- the generated metadata shape is suitable for future dirac-cwl integration
- the exported task inputs preserve:
  - transformation name
  - task name
  - storage element
  - placeholder LFNs

## Expected usage

python bin/transf2cwl.py \
  --bundle-dir OUTPUT_BASE/REQUEST_NAME/DIRAC.transf.d \
  --output-base OUTPUT_BASE \
  --transformation-name GenSimFull

Expected output:

OUTPUT_BASE/REQUEST_NAME/DIRAC.cwl.d
    tool.cwl
    workflow.cwl
    inputs
    metadata
    README.md

## Report follow-up note

The report workstream must keep expanding in parallel.

The following should be added to the report:

- the updated complete architecture diagram reflecting:
  - WMCore.fetched.d
  - DIRAC.transf.d
  - DIRAC.cwl.d
- the parameter-mapping tables between WMCore, canonical IR, and DIRAC
- the rationale for moving from local DIRAC-style materialization toward CWL

## Deferred technical note

After this layout unification and CWL export stage, the next technical branch is:

- query DBS and DAS to resolve LFNs from serialized WM objects per task

## Important note

At this stage, the CWL export is not intended to be a perfect representation of
the full CMS runtime model.

Its purpose is to prove that the current local DIRAC-like materialization can be
re-expressed in a workflow language that matches the future DIRACX direction
more closely than the old Python object model.
