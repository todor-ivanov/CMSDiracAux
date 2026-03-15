# WMCore → DIRAC Parameter Mapping

This document describes the conceptual and practical parameter mapping
between WMCore workflow objects and the corresponding DIRAC constructs
used in the CMSDiracAux interoperability proof of concept.

The mapping is implemented through an intermediate canonical
representation referred to as the Translation IR.


------------------------------------------------------------
1. Translation layers
------------------------------------------------------------

The interoperability layer introduces three conceptual levels.

WMCore objects
  |
  v
Canonical Translation IR
  |
  v
DIRAC workflow objects


WMCore represents CMS workflow semantics.

DIRAC represents workload execution semantics.

The Translation IR bridges the conceptual differences between the two
systems.


------------------------------------------------------------
2. WMCore request → Production mapping
------------------------------------------------------------

WMCore Request objects describe the global workflow context.

Example WMCore fields:

RequestName
Campaign
RequestPriority
ProcessingString
AcquisitionEra
PrepID


Translation IR production fields:

ProductionName
CampaignName
Priority
ProcessingString
AcquisitionEra
PrepId


DIRAC representation:

Transformation group
Production metadata
Transformation priority


Conceptual mapping:

WMCore Request
  |
  v
IR Production
  |
  v
DIRAC Transformation metadata


------------------------------------------------------------
3. WMCore Task → DIRAC Transformation
------------------------------------------------------------

In WMCore the Task represents the main execution unit.

Example WMCore Task parameters:

taskName
pathName
input.dataset.name
splitting configuration


Example WMCore task path:

/pdmvserv_Run2024E_DisplacedJet_MINIv6NANOv15_260309_125412_4202/DataProcessing


Derived IR task parameters:

TaskName
TaskPath
InputDataset
Splitting
Step


DIRAC equivalent:

Transformation definition
Transformation body
Transformation parameters


Conceptual mapping:

WMCore Task
  |
  v
IR Task
  |
  v
DIRAC Transformation


------------------------------------------------------------
4. WMCore Step → DIRAC Job workflow
------------------------------------------------------------

A WMCore Step describes a runtime processing stage.

Typical WMCore Step properties:

stepName
runtime configuration
CMSSW version
Scram architecture


Example WMCore step:

cmsRun


IR representation:

StepName
Executable
Arguments
SoftwareVersion
SoftwareArchitecture


DIRAC equivalent:

jobDescription.xml workflow step


Conceptual mapping:

WMCore Step
  |
  v
IR Step
  |
  v
DIRAC job workflow definition


------------------------------------------------------------
5. WMCore Splitting → DIRAC Transformation Plugin
------------------------------------------------------------

WMCore splitting defines how datasets are divided across jobs.

Example splitting parameters:

algorithm
events_per_job
files_per_job
lumis_per_job


IR representation:

PluginName
SplitMode
FilesPerJob
EventsPerJob
LumisPerJob


DIRAC equivalent:

TransformationPlugin


Example plugin used in the PoC:

CMSWMCoreSplittingPlugin


Conceptual mapping:

WMCore Splitting
  |
  v
IR Splitting
  |
  v
DIRAC Transformation plugin


------------------------------------------------------------
6. Dataset → LFN mapping
------------------------------------------------------------

WMCore tasks usually reference datasets rather than explicit files.

Example dataset:

/DisplacedJet/Run2024E-2024CDEReprocessing-v1/AOD


The PoC resolves file lists through DAS.

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


Example resolved LFN:

/store/data/Run2024E/DisplacedJet/AOD/2024CDEReprocessing-v1/2550000/7e4f9e3e-9757-4484-bc73-232921339a58.root


The resolved file metadata is propagated into the IR.


------------------------------------------------------------
7. IR InputDataset structure
------------------------------------------------------------

The canonical IR stores dataset information as:

DatasetHint
DatasetsResolved
ResolvedFileRecords
ResolvedLFNs
PlaceholderLFNs


Example IR dataset structure:

DatasetHint
ResolvedFileRecords
ResolvedLFNs


The IR preserves both:

dataset semantics
file-level metadata


------------------------------------------------------------
8. Plugin input generation
------------------------------------------------------------

DIRAC transformations require explicit file input definitions.

The PoC generates plugin input datasets as:

PluginInput/TASKNAME.inputdata.json


Structure:

LFN
  events
  size
  dataset
  block


Example entry:

/store/data/...root
  events: 12889
  size: 1427947644
  dataset: /DisplacedJet/Run2024E-2024CDEReprocessing-v1/AOD


------------------------------------------------------------
9. PoC scalability limitation
------------------------------------------------------------

The current implementation intentionally caps file materialization.

Maximum files per dataset:

20


Reason:

Datasets may contain thousands of files.

Example observed dataset:

~7100 files


Generating a job definition per file would produce an extremely large
local transformation structure.


Important:

This limit is temporary and exists only for the proof of concept.


------------------------------------------------------------
10. CMS data hierarchy implications
------------------------------------------------------------

CMS data follows a strict hierarchical structure.

dataset
  |
  v
block
  |
  v
file


Production workflows often operate across:

thousands of files
hundreds of blocks


The current PoC operates only on a small subset of the file layer.


------------------------------------------------------------
11. Future mapping extensions
------------------------------------------------------------

Future work may extend the mapping to include:

run and lumi masks

block-level dataset partitioning

DBS metadata enrichment

Rucio integration for data management

CWL-native workflow definitions compatible with DIRACX


------------------------------------------------------------
12. Summary
------------------------------------------------------------

The Translation IR enables a clean conceptual separation between:

WMCore workflow semantics
DIRAC execution semantics


The mapping can be summarized as:

WMCore Request
  |
  v
IR Production
  |
  v
DIRAC Transformation metadata


WMCore Task
  |
  v
IR Task
  |
  v
DIRAC Transformation


WMCore Step
  |
  v
IR Step
  |
  v
DIRAC job workflow
