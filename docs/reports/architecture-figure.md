# System Architecture Figure

This diagram illustrates the full architecture of the WMCore → DIRAC
interoperability proof of concept implemented in CMSDiracAux.

The architecture bridges three conceptual layers:

CMS workflow management
translation layer
workload execution representation


------------------------------------------------------------
1. Full system architecture
------------------------------------------------------------

                 CMS Workflow Management
                 -----------------------

                     WMCore / WMAgent
                            |
                            v
                    WMCore Request Objects
                            |
                            v
                        wmcGet.py
                            |
                            v
                 Serialized WMCore Artifacts
                 (WMTask.json, WMStep.json,
                  WMSplitting.json)
                            |
                            v


                 Translation Layer
                 -----------------

                 Canonical Translation IR
                            |
                            |
             +--------------+--------------+
             |                             |
             v                             v

     DIRAC-style Materialization        Workflow Export
             |                             |
             v                             v

        emit_translation_document         transf2cwl.py
             |                             |
             v                             v

         DIRAC.transf.d                 DIRAC.cwl.d
     (local transformation)          (CWL workflow bundle)


------------------------------------------------------------
2. Detailed execution pipeline
------------------------------------------------------------

WMCore request
  |
  v
wmcGet.py
  |
  v
WMCore.fetched.d
  |
  v
wmc2transf.py
  |
  v
Canonical Translation IR
  |
  v
emit_translation_document
  |
  v
DIRAC.transf.d
  |
  v
runLocalTransformation.py
  |
  v
CMSWMCoreSplittingPlugin
  |
  v
Task-specific job descriptions
  |
  v
transf2cwl.py
  |
  v
DIRAC.cwl.d


------------------------------------------------------------
3. Request-scoped artifact layout
------------------------------------------------------------

REQUEST_ROOT
|
|-- WMCore.fetched.d
|     |
|     |-- WMTask.json
|     |-- WMStep.json
|     `-- WMSplitting.json
|
|-- DIRAC.transf.d
|     |
|     |-- Transformations
|     |-- PluginInput
|     |-- Jobs
|     `-- Reports
|
`-- DIRAC.cwl.d
      |
      |-- tool.cwl
      |-- workflow.cwl
      |-- inputs
      `-- metadata


------------------------------------------------------------
4. Data discovery path
------------------------------------------------------------

WMCore Task
  |
  v
dataset reference
  |
  v
DAS query (dasgoclient)
  |
  v
dataset file records
  |
  v
LFN list
  |
  v
PluginInput dataset


Example dataset:

/DisplacedJet/Run2024E-2024CDEReprocessing-v1/AOD


Example LFN:

/store/data/Run2024E/DisplacedJet/AOD/2024CDEReprocessing-v1/2550000/file.root


------------------------------------------------------------
5. CMS data hierarchy
------------------------------------------------------------

CMS data is structured hierarchically.

dataset
  |
  v
block
  |
  v
file


Large CMS workflows typically operate on:

thousands of files
hundreds of blocks
multiple datasets


------------------------------------------------------------
6. PoC scalability limitation
------------------------------------------------------------

The current proof of concept intentionally limits file materialization.

Maximum files per dataset:

20


Reason:

Large CMS datasets can contain thousands of files.

Example dataset used during testing:

approximately 7100 files.


Without this limit the PoC would generate extremely large
transformation structures.


------------------------------------------------------------
7. Conceptual architecture summary
------------------------------------------------------------

The architecture can be summarized as:

WMCore
  |
  v
Translation IR
  |
  v
DIRAC execution representation
  |
  v
CWL workflow


The Translation IR acts as the central abstraction layer between
workflow semantics and execution semantics.
