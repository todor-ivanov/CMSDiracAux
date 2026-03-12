# Session Checkpoint

Date:
Session ID:

## Project Context

Project: WMCore to DIRAC interoperability proof of concept inside CMSDiracAux

Goal:
Translate serialized WMCore workflows into DIRAC compatible
transformations and job objects as a proof of concept interoperability layer.

---

## Current Pipeline

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

---

## Repository Components

Main scripts

bin/wmcGet.py  
bin/wmc2transf.py  
bin/runLocalTransformation.py  

Interop library

src/python/CMSDirac/Interop

- io.py
- model.py
- normalize.py
- materialize.py
- emit.py
- task_materialize.py

DIRAC plugin

CMSDirac/TransformationSystem/Agent/TransformationPlugin.py

---

## Current State

Working:

- WMCore serialization pipeline
- canonical translation model
- local DIRAC transformation emission
- CMSWMCoreSplittingPlugin execution
- task grouping
- per task job emission

Limitations:

- no server side DIRAC extension
- no CMS DBS or DAS integration
- placeholder LFNs
- WMJob.json integration postponed

---

## Architectural Observations

### WMBS vs DIRAC Granularity

CMS workflows operate at lumisection level bookkeeping.  
DIRAC and HTCondor operate primarily at file and job granularity.

WMBS bridges this mismatch.

### CMS Runtime Bootstrap

Runtime configuration depends on

- WMCore runtime sandbox
- CMSSW runtime environment via CVMFS
- workload and job pickle objects
- worker node architecture

---

## Output Bundle Structure

Output directory contains

Reports
translation_document.json
translation_report.json
local_task_materialization_report.json

PluginInput
GenSimFull.inputdata.json

Jobs
GenSimFull.jobDescription.xml
GenSimFull.job.jdl

Transformations
GenSimFull.transformation.json

Tasks
GenSimFull.tasks.json

TaskJobs
GenSimFull_task_0001.jobDescription.xml
GenSimFull_task_0001.job.jdl

---

## Next Work Item

Restore repository consistency across

io.py
model.py
normalize.py
materialize.py
emit.py
task_materialize.py
runLocalTransformation.py
wmc2transf.py

---

## Deferred Topics

- WMJob.json aware job materialization
- intra file splitting
- run and lumi masks
- CMS DBS and DAS integration
- Rucio integration
- DIRACX workflow portability

---

## Notes for Final Report

Topics to expand later

- WMBS architecture rationale
- CMS runtime bootstrap model
- static splitting implications
- comparison of CMS and DIRAC scheduling models
