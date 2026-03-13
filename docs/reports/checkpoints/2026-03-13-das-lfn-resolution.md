# Checkpoint — DAS LFN Resolution and PoC File Cap

Date
2026-03-13


## Current milestone state

The WMCore → DIRAC PoC pipeline is now able to:

1. Fetch and serialize a CMS workflow from WMCore
2. Translate the workflow into a canonical translation IR
3. Materialize a local DIRAC-style transformation bundle
4. Resolve real CMS dataset LFNs using DAS (dasgoclient)
5. Propagate real file metadata into plugin input structures
6. Export the materialized transformation into a CWL-compatible bundle


End-to-end pipeline:

WMCore request
  |
  v
wmcGet.py
  |
  v
serialized WM JSON artifacts
  |
  v
wmc2transf.py
  |
  v
canonical translation objects
  |
  v
local DIRAC-style artifacts
  |
  v
runLocalTransformation.py
  |
  v
CMSWMCoreSplittingPlugin
  |
  v
Tasks and TaskJobs
  |
  v
transf2cwl.py
  |
  v
CWL bundle


## Output directory structure

Each request is materialized under a request-scoped root directory.

REQUEST_ROOT
|
|-- WMCore.fetched.d
|
|-- DIRAC.transf.d
|
`-- DIRAC.cwl.d


Meaning:

WMCore.fetched.d
Serialized WMCore objects such as:

- WMTask.json
- WMStep.json
- WMSplitting.json


DIRAC.transf.d
Local DIRAC-style materialization artifacts:

- transformation definitions
- job descriptions
- plugin input data
- task objects


DIRAC.cwl.d
CWL-export bundle representing the same workflow.


## DAS-based LFN resolution

Dataset LFNs are now resolved using:

dasgoclient

The call is executed through an interactive shell so that environments where
dasgoclient is provided through a shell alias (for example via CVMFS) work
correctly.

Example dataset:

/DisplacedJet/Run2024E-2024CDEReprocessing-v1/AOD

Example resolved LFN:

/store/data/Run2024E/DisplacedJet/AOD/2024CDEReprocessing-v1/2550000/7e4f9e3e-9757-4484-bc73-232921339a58.root

The translator now propagates:

- full DAS file records
- per-file event counts
- per-file metadata

into the canonical IR and plugin input data.


## PoC scalability limitation

The current PoC intentionally materializes only the first 20 files per dataset.

This cap is implemented during the canonical IR normalization stage.

Reason:

Generating a job definition per file becomes extremely heavy when datasets
contain thousands of files.

Example dataset size in current testing:

~7100 files

Without the cap, the PoC would generate thousands of jobs and large plugin
input artifacts.

This limit is strictly temporary and must be clearly documented in the report.


## CMS data hierarchy relevance

This limitation is particularly important because CMS data follows a strict
hierarchy.

dataset
  |
  v
block
  |
  v
file

Large CMS productions operate at:

- dataset scale
- block scale
- file scale
- sometimes run/lumi scale

The current PoC only operates at a small subset of the file layer.

Therefore performance and scalability conclusions cannot yet be drawn.


## DIRAC runtime observations

During testing we confirmed:

- runtime parameters must ultimately live in jobDescription.xml
- .jdl files should not attempt to propagate large sandboxes
- DIRAC sandbox handling differs from CMS WMCore runtime assumptions

This topic is marked for a dedicated report section:

DIRAC InputSandbox vs jobDescription.xml runtime contract.


## Next technical directions


Data discovery improvements:

- more robust DAS queries
- optional DBS-based metadata enrichment
- better block-level dataset handling


CWL export refinement:

Continue aligning the exported bundle with:

DIRACGrid/dirac-cwl

Goals:

- validate workflow with cwltool
- preserve DIRAC task metadata
- maintain compatibility with future DIRACX workflows


CMS runtime bootstrap analysis:

Further work needed on:

- CMSSW runtime distribution
- WMCore runtime sandbox structure
- interaction with CVMFS
- possible future Rucio integration


## Report workstream reminder

The final report must include:

- architecture diagram of the full system
- parameter mapping tables
- comparison between WMCore and DIRAC execution models
- discussion of WMBS splitting vs DIRAC task generation
- the current PoC file cap limitation
- CMS dataset/block/file hierarchy explanation
