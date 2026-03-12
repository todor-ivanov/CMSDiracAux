# CWL Export Path for the CMSDiracAux WMCore to DIRAC PoC

## Purpose

The next milestone of this proof of concept is to express the already
materialized local DIRAC-like CMS workflow in a CWL-digestible form.

The short-term goal is not to reproduce the full DIRAC Python object model in
CWL, but to export the current local transformation and task structure into a
bundle that is structurally compatible with the direction taken by `dirac-cwl`.

The `dirac-cwl` prototype already supports:

- local testing with `cwltool`
- submission as DIRAC jobs
- submission as DIRAC transformations
- submission as DIRAC productions

and distinguishes these modes using CWL plus additional metadata files.
This makes it the correct target for the next stage of the PoC.

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

## Why CWL is the next milestone

The CWL milestone is intentionally chosen before deeper server-side DIRAC
integration because:

- the current environment does not provide a CMS-specific DIRAC server-side extension
- server-side plugin deployment is not yet possible
- real CMS data discovery is not available in the current DIRAC test setup
- DIRACX is heading toward workflow descriptions that are more portable than the old Python object layer

In this context, the current local materialized workflow should be treated as an
intermediate representation that can now be exported into CWL.

## Reference target: dirac-cwl

The `dirac-cwl` prototype describes the following usage model:

1. local workflow validation with `cwltool`
2. submission as DIRAC jobs using:
   - CWL task
   - one or more input parameter sets
   - DIRAC metadata
3. submission as DIRAC transformations using:
   - CWL task
   - transformation metadata
4. submission as DIRAC productions using:
   - CWL task
   - step metadata per transformation

This is enough for the current PoC to define a short export path.

## Shortest export path

The shortest path to the next milestone is:

1. keep the current local materialized transformation as the source
2. export one task tool as CWL CommandLineTool
3. export one workflow wrapper as CWL Workflow
4. export one YAML input file per generated task
5. export one job metadata YAML
6. export one transformation metadata YAML
7. validate locally with cwltool
8. only then align more tightly with dirac-cwl submission commands

This avoids unnecessary deviation into unresolved WMBS details.

## Mapping strategy

### Source objects

The CWL exporter uses:

- Transformations/NAME.transformation.json
- Tasks/NAME.tasks.json
- optionally Jobs/NAME.jobDescription.xml
- optionally TaskJobs/NAME/*.job.params.json

### Target bundle

The exporter writes:

cwl_bundle/
    tool.cwl
    workflow.cwl
    inputs/
        task_0001.yaml
        task_0002.yaml
    metadata/
        job.metadata.yaml
        transformation.metadata.yaml
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

This is intentionally a stage-1 abstraction and does not yet attempt full CMS
runtime fidelity.

## Stage-1 scope

The first CWL milestone is intentionally limited.

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
- real DBS/DAS based data resolution
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

## Expected repository additions

New script:

bin/transf2cwl.py

Expected usage:

python bin/transf2cwl.py \
  --bundle-dir OUTPUT_DIR \
  --transformation-name GenSimFull

Expected output:

OUTPUT_DIR/cwl_bundle/
    tool.cwl
    workflow.cwl
    inputs/
        task_0001.yaml
    metadata/
        job.metadata.yaml
        transformation.metadata.yaml
    README.md

## Immediate next step after this milestone

Once this export exists, the next follow-up is:

- validate generated CWL with cwltool
- compare generated metadata against dirac-cwl test bundles
- then decide whether to target:
  - job submission first
  - transformation submission first
  - or direct production decomposition

## Important note

At this stage, the CWL export is not intended to be a perfect representation of
the full CMS runtime model.

Its purpose is to prove that the current local DIRAC-like materialization can be
re-expressed in a workflow language that matches the future DIRACX direction
more closely than the old Python object model.
