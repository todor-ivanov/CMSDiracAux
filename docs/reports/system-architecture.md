# System Architecture

This document describes the overall architecture of the WMCore → DIRAC
interoperability proof of concept implemented in CMSDiracAux.

The architecture bridges two different workflow systems:

WMCore (CMS workflow management)

and

DIRAC (distributed workload management).

The translation layer introduced in this repository enables workflows
originating from WMCore to be expressed in terms compatible with DIRAC
execution models and eventually exportable into CWL workflows.


------------------------------------------------------------
1. Architectural overview
------------------------------------------------------------

The system is structured as a translation and materialization pipeline.

WMCore workflow
  |
  v
WMCore serialization
  |
  v
Translation layer (canonical IR)
  |
  v
Local DIRAC-style materialization
  |
  v
DIRAC transformation simulation
  |
  v
CWL workflow export


Each stage produces artifacts that can be inspected and validated
independently.


------------------------------------------------------------
2. High level system diagram
------------------------------------------------------------

CMS Workflow Management System

WMCore
  |
  v
WMCore request objects
  |
  v
wmcGet.py
  |
  v
serialized WMCore JSON objects


Translation Layer

canonical translation IR
  |
  v
wmc2transf.py
  |
  v
canonical task and production objects


DIRAC-style Materialization

emit_translation_document
  |
  v
DIRAC.transf.d artifacts
  |
  v
runLocalTransformation.py
  |
  v
CMSWMCoreSplittingPlugin
  |
  v
task-specific job definitions


Workflow Language Export

transf2cwl.py
  |
  v
DIRAC.cwl.d bundle


------------------------------------------------------------
3. Request-scoped artifact layout
------------------------------------------------------------

All artifacts produced for a workflow request are grouped under a
single request root directory.

REQUEST_ROOT
|
|-- WMCore.fetched.d
|
|-- DIRAC.transf.d
|
`-- DIRAC.cwl.d


WMCore.fetched.d

Contains serialized WMCore objects.

Examples:

WMTask.json
WMStep.json
WMSplitting.json


DIRAC.transf.d

Contains the local representation of DIRAC constructs.

Examples:

Transformations
PluginInput
Jobs
Reports


DIRAC.cwl.d

Contains the CWL workflow bundle exported from the transformation.


------------------------------------------------------------
4. Translation architecture
------------------------------------------------------------

The key architectural concept is the canonical Translation IR.

WMCore and DIRAC have very different conceptual models.

WMCore focuses on physics workflows and dataset processing.

DIRAC focuses on job execution and workload scheduling.

To bridge these models, the PoC introduces a canonical intermediate
representation.

WMCore objects
  |
  v
Canonical Translation IR
  |
  v
DIRAC transformation objects


This IR allows:

clean separation of concerns

independent evolution of source and target systems

future export to workflow languages such as CWL


------------------------------------------------------------
5. Data discovery layer
------------------------------------------------------------

WMCore tasks normally reference datasets rather than explicit files.

Example dataset:

/DisplacedJet/Run2024E-2024CDEReprocessing-v1/AOD


The PoC resolves dataset files using DAS.

dataset
  |
  v
dasgoclient query
  |
  v
file records
  |
  v
LFN list


The resolved metadata is propagated through the IR and used to build
plugin input structures for the DIRAC transformation simulation.


------------------------------------------------------------
6. DIRAC execution model simulation
------------------------------------------------------------

DIRAC transformations normally run inside DIRAC services.

Because server-side DIRAC deployment is not available in the current
environment, the PoC simulates transformation execution locally.

runLocalTransformation.py

This component:

loads transformation definitions

invokes CMSWMCoreSplittingPlugin

generates task-level job descriptions


The result is a local approximation of a DIRAC transformation execution.


------------------------------------------------------------
7. CMS runtime considerations
------------------------------------------------------------

CMS jobs rely on a complex runtime environment.

Key components include:

CMSSW software distribution

WMCore runtime modules

runtime configuration artifacts such as:

step_cfg.py
WMWorkload.pkl
JobPackage.pkl


These artifacts are normally distributed through CMS workflow
management infrastructure and worker node environments.

Integrating these runtime requirements with the DIRAC execution model
is a key challenge for future work.


------------------------------------------------------------
8. CWL workflow export
------------------------------------------------------------

The PoC exports the materialized transformation into CWL.

Purpose:

align the workflow representation with future DIRACX workflow models

allow validation using standard workflow tools such as:

cwltool


Export process:

DIRAC.transf.d
  |
  v
transf2cwl.py
  |
  v
CWL workflow bundle


This export step prepares the workflow representation for potential
integration with modern workflow engines.


------------------------------------------------------------
9. PoC scalability limitation
------------------------------------------------------------

The current implementation intentionally limits dataset materialization.

Maximum files per dataset:

20


Reason:

CMS datasets often contain thousands of files.

Example dataset size observed in testing:

~7100 files


Generating one job definition per file without limits would produce a
very large transformation structure and slow down development.


Important:

This limitation is temporary and must be clearly stated in the final
report.


------------------------------------------------------------
10. CMS data hierarchy
------------------------------------------------------------

CMS data is organized hierarchically.

dataset
  |
  v
block
  |
  v
file


Large productions operate across many blocks and thousands of files.

The PoC currently operates only on a small subset of the file layer.


------------------------------------------------------------
11. Future architecture directions
------------------------------------------------------------

Several architectural directions remain for future work.

Improved data discovery

integration with DBS metadata

block-level dataset partitioning

Rucio-based data management integration


DIRAC integration

server-side deployment of CMS transformation plugins

full DIRAC Transformation Agent integration


Workflow representation

native CWL workflows

compatibility with DIRACX workflow architecture


------------------------------------------------------------
12. Architecture summary
------------------------------------------------------------

The architecture introduced in this repository provides a bridge
between two workflow ecosystems.

WMCore
  |
  v
Translation IR
  |
  v
DIRAC workflow representation
  |
  v
CWL workflow export


The canonical Translation IR acts as the central abstraction layer
that allows these systems to interoperate while remaining loosely
coupled.
