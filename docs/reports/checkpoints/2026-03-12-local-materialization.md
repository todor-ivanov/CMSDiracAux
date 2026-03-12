# Checkpoint — Local Transformation Materialization

Date: 2026-03-12

## Achieved

Implemented a complete local WMCore to DIRAC translation pipeline.

Components

1. wmcGet.py  
   Fetches workflows and serializes WMCore objects.

2. wmc2transf.py  
   Converts serialized objects into canonical translation objects
   and emits local DIRAC style artifacts.

3. runLocalTransformation.py  
   Runs CMSWMCoreSplittingPlugin locally and produces grouped tasks
   and per task job descriptions.

Result

A fully local transformation simulation independent of server side DIRAC.

---

## Local Pipeline

WMCore request
    ↓
wmcGet.py
    ↓
WM JSON artifacts
    ↓
wmc2transf.py
    ↓
Transformations
PluginInput
Jobs
    ↓
runLocalTransformation.py
    ↓
Tasks
TaskJobs

---

## Important Decision

Server side DIRAC integration is postponed.

The available environment

- does not provide CMS DIRAC extensions
- cannot access CMS DBS or DAS
- cannot register transformation plugins

Therefore the PoC focuses on correct translation and local object materialization.

---

## Known Gaps

Repository main branch currently contains partial merges in the
emit and materialization layer.

Modules requiring synchronization

emit.py  
io.py  
task_materialize.py  
runLocalTransformation.py  

---

## Next Step

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

## Future Branch

WMJob.json aware task job generation.

This will allow emitted jobs to inherit WMBS job parameters when available.
