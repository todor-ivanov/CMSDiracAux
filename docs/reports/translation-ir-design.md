# Translation IR Design

This document describes the design and purpose of the canonical
Translation IR introduced in the CMSDiracAux interoperability proof
of concept.

The Translation IR acts as an intermediate representation between
WMCore workflow objects and DIRAC execution constructs.


------------------------------------------------------------
1. Motivation
------------------------------------------------------------

WMCore and DIRAC represent workflows in fundamentally different ways.

WMCore focuses on physics workflow semantics and dataset processing.

DIRAC focuses on workload execution and distributed job scheduling.

Directly mapping WMCore objects into DIRAC objects would create a
fragile coupling between two systems with different abstractions.

The Translation IR introduces a clean separation between:

workflow semantics

and

execution semantics.


------------------------------------------------------------
2. Translation architecture
------------------------------------------------------------

The architecture implemented in the PoC follows a three-layer model.

WMCore
  |
  v
Translation IR
  |
  v
DIRAC workflow representation


This architecture allows:

stable translation logic

independent evolution of WMCore and DIRAC

future export to workflow languages such as CWL


------------------------------------------------------------
3. Why direct mapping is problematic
------------------------------------------------------------

Direct WMCore → DIRAC mapping would introduce several problems.

Different abstraction layers

WMCore models workflow logic.

DIRAC models job execution.


Different splitting models

WMCore uses static splitting through WMBS.

DIRAC uses dynamic splitting inside transformation agents.


Different data models

WMCore references datasets.

DIRAC expects explicit file lists.


Different runtime expectations

WMCore jobs rely on CMS-specific runtime artifacts.

DIRAC jobs usually execute simpler command-line payloads.


Because of these differences, a direct mapping would require
embedding many WMCore concepts inside DIRAC structures.


------------------------------------------------------------
4. Canonical IR structure
------------------------------------------------------------

The Translation IR defines a simplified workflow representation.

The main objects are:

Production

Task

Step

Splitting


Conceptually the IR looks like this.

Production
  |
  v
Task
  |
  v
Step
  |
  v
Splitting


Production

global workflow metadata


Task

dataset processing unit


Step

runtime execution definition


Splitting

job generation strategy


------------------------------------------------------------
5. IR responsibilities
------------------------------------------------------------

The Translation IR performs several important functions.

Normalize workflow metadata

Extract relevant parameters from WMCore objects.


Resolve dataset inputs

Convert dataset references into explicit file lists using DAS.


Represent execution semantics

Express runtime parameters in a form compatible with DIRAC.


Preserve workflow structure

Keep task and step relationships intact.


Prepare workflow export

Provide a representation that can be exported into CWL.


------------------------------------------------------------
6. IR object example
------------------------------------------------------------

Example conceptual IR structure.

Production

ProductionName
CampaignName
Priority


Task

TaskName
TaskPath
InputDataset
OutputDataset
Step
Splitting


Step

Executable
Arguments
SoftwareVersion
SoftwareArchitecture


Splitting

PluginName
SplitMode
FilesPerJob
EventsPerJob


This structure is intentionally minimal and focuses only on the
parameters required for workflow execution.


------------------------------------------------------------
7. Dataset resolution inside the IR
------------------------------------------------------------

WMCore tasks usually reference datasets rather than files.

Example dataset:

/DisplacedJet/Run2024E-2024CDEReprocessing-v1/AOD


The IR resolves datasets into file lists using DAS.

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


Resolved file metadata is stored in the IR.


------------------------------------------------------------
8. PoC dataset materialization limit
------------------------------------------------------------

The current PoC intentionally limits dataset materialization.

Maximum files per dataset:

20


Reason:

CMS datasets often contain thousands of files.

Example dataset size observed during testing:

approximately 7100 files.


Without this limit the PoC would generate extremely large local
transformations.


This limitation is temporary and exists only for development.


------------------------------------------------------------
9. IR role in DIRAC materialization
------------------------------------------------------------

The IR is used to generate a local representation of DIRAC constructs.

IR Task
  |
  v
DIRAC Transformation


IR Step
  |
  v
DIRAC job workflow


IR Splitting
  |
  v
DIRAC transformation plugin


This mapping allows the PoC to simulate transformation execution
without a running DIRAC server.


------------------------------------------------------------
10. IR role in CWL export
------------------------------------------------------------

The IR also enables workflow export into CWL.

IR Task
  |
  v
CWL CommandLineTool


IR workflow structure
  |
  v
CWL Workflow


This makes the workflow representation portable across execution
systems.


------------------------------------------------------------
11. Relationship to DIRACX
------------------------------------------------------------

DIRACX is moving toward workflow language based execution models.

Using the Translation IR makes it possible to export workflows into
languages such as:

CWL


This provides a potential path toward future DIRACX integration.


------------------------------------------------------------
12. Design summary
------------------------------------------------------------

The Translation IR provides the core abstraction layer of the
interoperability architecture.

WMCore
  |
  v
Translation IR
  |
  v
DIRAC execution model
  |
  v
CWL workflow export


The IR allows workflow semantics to remain independent from the
underlying execution infrastructure.
