# Architecture and Design Notes

This document consolidates architectural observations collected during the
WMCore → DIRAC interoperability proof of concept.

The notes originate from iterative design discussions during development and
are intended to serve as the foundation of the final project report.


------------------------------------------------------------
1. High-level architecture
------------------------------------------------------------

The PoC currently implements the following translation pipeline.

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
canonical translation IR
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
task-specific jobs
  |
  v
transf2cwl.py
  |
  v
CWL workflow bundle


------------------------------------------------------------
2. Request-scoped output layout
------------------------------------------------------------

Each workflow request is materialized under a single directory root.

REQUEST_ROOT
|
|-- WMCore.fetched.d
|
|-- DIRAC.transf.d
|
`-- DIRAC.cwl.d


Purpose of each layer:

WMCore.fetched.d

Serialized WMCore objects.

Examples:

- WMTask.json
- WMStep.json
- WMSplitting.json


DIRAC.transf.d

Local representation of DIRAC constructs.

Includes:

- transformations
- tasks
- job descriptions
- plugin input datasets


DIRAC.cwl.d

CWL representation of the workflow.


------------------------------------------------------------
3. Parameter translation layers
------------------------------------------------------------

The PoC introduces an intermediate canonical representation.

WMCore
  |
  v
Canonical Translation IR
  |
  v
DIRAC transformation objects


Example mapping conceptually:

WMCore parameter

RequestName

↓

IR field

ProductionName

↓

DIRAC object

TransformationName


WMCore step parameters

↓

IR Step object

↓

DIRAC job workflow definition


A full parameter mapping table will be included in the final report.


------------------------------------------------------------
4. DIRAC runtime contract observations
------------------------------------------------------------

Testing revealed an important constraint in the DIRAC execution model.

Runtime parameters must ultimately reside in:

jobDescription.xml


While JDL files describe job submission properties, they are not designed
to carry complex runtime sandbox contents.

This is relevant because the CMS WMCore runtime model relies heavily on
runtime artifacts such as:

- WMWorkload.pkl
- JobPackage.pkl
- step_cfg.py


These artifacts must ultimately be transferred in a way compatible with
DIRAC sandbox semantics.

This topic will form a dedicated report section:

DIRAC InputSandbox versus jobDescription.xml runtime contract.


------------------------------------------------------------
5. CMS data hierarchy implications
------------------------------------------------------------

CMS data is strictly hierarchical.

dataset
  |
  v
block
  |
  v
file


Large productions operate across:

- thousands of files
- hundreds of blocks
- multi-terabyte datasets


This structure affects:

- splitting strategy
- task generation
- data discovery
- runtime job scheduling


------------------------------------------------------------
6. PoC scalability limitation
------------------------------------------------------------

The current PoC intentionally limits materialization to:

20 files per dataset.


Reason:

Generating one job definition per file quickly becomes extremely heavy for
datasets containing thousands of files.

Example observed dataset size:

~7100 files


Without the cap the PoC would generate thousands of jobs and very large
plugin input artifacts.


Important:

This limitation must be clearly stated in the report and must not be confused
with the intended production-scale behavior.


------------------------------------------------------------
7. Future data discovery improvements
------------------------------------------------------------

Current implementation:

dataset → DAS query → file list


Future improvements may include:

- richer DBS metadata usage
- block-level dataset handling
- dataset size estimation
- integration with CMS data management systems


------------------------------------------------------------
8. CWL export motivation
------------------------------------------------------------

DIRACX is moving toward a workflow-language driven architecture.

Exporting the PoC workflow into CWL allows:

- workflow validation with cwltool
- decoupling from the legacy DIRAC Python object model
- easier interoperability with modern workflow engines


------------------------------------------------------------
9. Documentation rendering convention
------------------------------------------------------------

To ensure correct rendering in GitHub and Firefox ESR environments,
documentation follows strict ASCII-only diagram conventions.

Flow diagrams:

|
v


Directory trees:

|--
`--


Avoid:

- Unicode arrows
- Unicode tree characters
- HTML tags inside code blocks
