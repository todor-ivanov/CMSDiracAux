# USAGE

These are usage instructions for working with the CMS to DIRAC workflows translation software  provided at the current repository:

## Local end-to-end materialization workflow

The current proof of concept supports a fully local workflow from serialized
WMCore inputs to locally materialized DIRAC-like task groups.

```
WM*.json or wmcGet.py
    ↓
bin/wmc2transf.py
    ↓
local DIRAC-like Job / Transformation objects
    ↓
bin/runLocalTransformation.py
    ↓
CMSWMCoreSplittingPlugin
    ↓
local task groups
```

### Starting points

The workflow can start from either:

- an existing directory containing serialized `WM*.json` files, or
- a fresh call to `bin/wmcGet.py`, which fetches and serializes the WMCore
  workflow description.

### Important note about `--wmJobIndex`

`--wmJobIndex` is **not mandatory** in general.

It becomes relevant only when working from a pre-split WMBS job bundle
(for example via `--wmJobPkg`), where a specific job must be selected from the
bundle.

When starting only from a request name or a workload description, `--wmJobIndex`
is not required.

### Step 1: translate serialized WMCore inputs

```bash
python3 bin/wmc2transf.py \
  --input-dir <serialized_input_dir> \
  --outdir <output_bundle_dir>
```

This produces:

- canonical translation artifacts,
- local DIRAC-like Job artifacts,
- local DIRAC-like Transformation artifacts,
- plugin input sidecars.

### Step 2: run the local transformation through the splitting plugin
```
python3 bin/runLocalTransformation.py \
  --transformation-file <output_bundle_dir>/Transformations/GenSimFull.transformation.json
```

This runs CMSWMCoreSplittingPlugin locally and writes the grouped task
descriptions to disk.

## Expected output directory structure
```
<outdir>/
  Reports/
    translation_document.json
    translation_report.json
    local_task_materialization_report.json

  PluginInput/
    GenSimFull.inputdata.json

  Jobs/
    GenSimFull.jobDescription.xml
    GenSimFull.job.jdl
    GenSimFull.job.params.json

  Transformations/
    GenSimFull.transformation.body.xml
    GenSimFull.transformation.params.json
    GenSimFull.transformation.json

  Tasks/
    GenSimFull.tasks.json
```

Where:

- `translation_document.json` is the canonical translation artifact
- `translation_report.json` is the translator/materializer report
- `GenSimFull.jobDescription.xml` is the local DIRAC-like workflow XML
- `GenSimFull.job.jdl` is the local JDL
- `GenSimFull.transformation.json` is the local transformation description
- `GenSimFull.inputdata.json` is the static plugin input sidecar
- `GenSimFull.tasks.json` is the final local grouped-task output
- `local_task_materialization_report.json` summarizes the local runner result

## Important limitation

This is a local stage-1 materialization workflow only.

It does not yet create real server-side DIRAC Transformation tasks, because the
CMS DIRAC server-side extension, plugin deployment, and Transformation Agent
integration are not yet available in the current environment.

### Artifact preservation

When using bin/wmcGet.py, repository-local output directories should be used so
that all intermediate serialized WM*.json artifacts are preserved for later
inspection, debugging, and reporting.


## Example Shell command sequence for manual execution of all scripts

### 1. Starting from existing serialized WM*.json inputs

```
# 1. Choose the serialized WMCore input directory
INPUT_DIR=test/wf_pdmvserv_RVCMSSW_16_0_0_pre2QCD__STD_GPU_Pix_202_PU_KIT_251125_103426_8717/job_219128

# 2. Choose the output bundle directory
OUTDIR=test/wf_pdmvserv_RVCMSSW_16_0_0_pre2QCD__STD_GPU_Pix_202_PU_KIT_251125_103426_8717.transf

# 3. Translate the WMCore artifacts and materialize local DIRAC-like objects
python3 bin/wmc2transf.py \
  --input-dir "${INPUT_DIR}" \
  --outdir "${OUTDIR}"

# 4. Run the local transformation through CMSWMCoreSplittingPlugin
python3 bin/runLocalTransformation.py \
  --transformation-file "${OUTDIR}/Transformations/GenSimFull.transformation.json"

# 5. Inspect the generated local task groups
cat "${OUTDIR}/Tasks/GenSimFull.tasks.json"

# 6. Inspect the local materialization report
cat "${OUTDIR}/Reports/local_task_materialization_report.json"
```

### 2. Starting from bin/wmcGet.py using a CMS request name

```
# 1. Define the request name and request manager
REQNAME=pdmvserv_RVCMSSW_16_0_0_pre2QCD__STD_GPU_Pix_202_PU_KIT_251125_103426_8717
REQMGR=cmsweb-testbed.cern.ch

# 2. Choose a repository-local base directory for fetched/serialized artifacts
FETCH_BASE=test/fetched

# 3. Choose the final translator/materialization output directory
OUTDIR=test/${REQNAME}.transf

# 4. Fetch and serialize the WMCore workflow inputs
python3 bin/wmcGet.py \
  -r "${REQNAME}" \
  -m "${REQMGR}" \
  -o "${FETCH_BASE}"

# 5. Translate the serialized inputs and materialize local DIRAC-like objects
python3 bin/wmc2transf.py \
  --input-dir "${FETCH_BASE}/wf_${REQNAME}" \
  --outdir "${OUTDIR}"

# 6. Run the local transformation through CMSWMCoreSplittingPlugin
python3 bin/runLocalTransformation.py \
  --transformation-file "${OUTDIR}/Transformations/GenSimFull.transformation.json"

# 7. Inspect the final local task grouping output
cat "${OUTDIR}/Tasks/GenSimFull.tasks.json"
```

### 3. Starting from bin/wmcGet.py using a pre-split WMBS job bundle

```
# 1. Define inputs
JOBPKG=test/CMSWorkflows.d/.../JobPackage.pkl
WORKLOAD=test/CMSWorkflows.d/.../WMWorkload.pkl
JOBINDEX=219128

# 2. Choose a repository-local base directory for serialized artifacts
FETCH_BASE=test/fetched

# 3. Choose the final translator/materialization output directory
OUTDIR=test/presplit_job_219128.transf

# 4. Fetch/serialize from the workload + JobPackage pair
python3 bin/wmcGet.py \
  -j "${JOBPKG}" \
  -w "${WORKLOAD}" \
  -i "${JOBINDEX}" \
  -o "${FETCH_BASE}"

# 5. Translate the selected pre-split job directory
python3 bin/wmc2transf.py \
  --input-dir "${FETCH_BASE}/wf_*/job_${JOBINDEX}" \
  --outdir "${OUTDIR}"

# 6. Run the local transformation through CMSWMCoreSplittingPlugin
python3 bin/runLocalTransformation.py \
  --transformation-file "${OUTDIR}/Transformations/GenSimFull.transformation.json"
```

### 4. Single-command variant using --fetch-inputs

 ```
REQNAME=pdmvserv_RVCMSSW_16_0_0_pre2QCD__STD_GPU_Pix_202_PU_KIT_251125_103426_8717
REQMGR=cmsweb-testbed.cern.ch

# Keep fetched/serialized WMCore artifacts in a repository-local directory
FETCH_BASE=test/${REQNAME}.wm

# Final translator/materialization bundle
OUTDIR=test/${REQNAME}.transf

python3 bin/wmc2transf.py \
  --fetch-inputs \
  --wmReqName "${REQNAME}" \
  --wmReqMgr "${REQMGR}" \
  --fetch-outdir "${FETCH_BASE}" \
  --outdir "${OUTDIR}"

python3 bin/runLocalTransformation.py \
  --transformation-file "${OUTDIR}/Transformations/GenSimFull.transformation.json"
 ```

And for the pre-split WMBS case:

```
JOBPKG=test/CMSWorkflows.d/.../JobPackage.pkl
WORKLOAD=test/CMSWorkflows.d/.../WMWorkload.pkl
JOBINDEX=219128
FETCH_BASE=test/presplit_job_${JOBINDEX}.wm
OUTDIR=test/presplit_job_${JOBINDEX}.transf

python3 bin/wmc2transf.py \
  --fetch-inputs \
  --wmJobPkg "${JOBPKG}" \
  --wmWorkload "${WORKLOAD}" \
  --wmJobIndex "${JOBINDEX}" \
  --fetch-outdir "${FETCH_BASE}" \
  --outdir "${OUTDIR}"

python3 bin/runLocalTransformation.py \
  --transformation-file "${OUTDIR}/Transformations/GenSimFull.transformation.json"
```
