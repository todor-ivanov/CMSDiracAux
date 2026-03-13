# WMCore vs DIRAC Execution Model

This document explains the conceptual differences between the CMS
workflow management system (WMCore / WMAgent / WMBS) and the DIRAC
workload management framework.

Understanding these differences is essential for explaining why the
translation layer implemented in CMSDiracAux is necessary.


------------------------------------------------------------
1. System roles
------------------------------------------------------------

Both systems operate in the domain of distributed computing, but they
focus on different layers of the workload lifecycle.


WMCore

workflow management system


DIRAC

workload execution and scheduling framework


WMCore defines physics workflows and dataset processing logic.

DIRAC focuses on scheduling jobs on distributed resources.


------------------------------------------------------------
2. Execution unit definition
------------------------------------------------------------

One of the most important differences is the definition of the atomic
processing unit.


WMCore atomic unit

luminosity section


DIRAC atomic unit

file


This difference originates from the needs of CMS data processing.


CMS workflows must guarantee that each luminosity section is processed
exactly once.


The CMS workflow management system therefore operates on a finer level
than most workload schedulers.


------------------------------------------------------------
3. WMCore workflow structure
------------------------------------------------------------

A simplified WMCore workflow structure is:

Request
  |
  v
Task
  |
  v
Step
  |
  v
WMBS job


Where:

Request

global workflow description


Task

dataset processing unit


Step

runtime configuration stage


WMBS job

execution unit assigned to the batch system


The WMBS component performs bookkeeping and static splitting.


------------------------------------------------------------
4. WMBS splitting model
------------------------------------------------------------

WMBS exists because the CMS workflow system operates on data units
that are finer than the scheduling capabilities of typical batch
systems.

Typical scheduling systems operate at:

file granularity


WMCore requires processing guarantees at:

luminosity section granularity


To reconcile these layers, WMBS performs static job splitting and
tracks the relationship between:

dataset
file
run
luminosity section


This allows CMS workflows to enforce strict data processing guarantees.


------------------------------------------------------------
5. DIRAC execution structure
------------------------------------------------------------

DIRAC organizes workload execution differently.

A simplified DIRAC structure is:

Transformation
  |
  v
Task
  |
  v
Job


Transformation

logical workload definition


Task

unit of work derived from transformation input data


Job

execution unit submitted to worker nodes


DIRAC transformations dynamically generate jobs based on input data.


------------------------------------------------------------
6. Static vs dynamic splitting
------------------------------------------------------------

Another important difference is splitting strategy.


WMCore

static splitting


DIRAC

dynamic splitting


WMCore splitting is usually performed before jobs are submitted.

DIRAC splitting typically occurs inside the Transformation Agent
during workload execution.


------------------------------------------------------------
7. Data discovery
------------------------------------------------------------

CMS workflows rely heavily on dataset discovery.

Typical data discovery path:

dataset
  |
  v
DBS / DAS query
  |
  v
block list
  |
  v
file list


DIRAC usually receives explicit input file lists.


Therefore the translation layer must perform dataset resolution.


------------------------------------------------------------
8. Runtime environment
------------------------------------------------------------

CMS jobs require a complex runtime environment.

Important components include:

CMSSW software framework

WMCore runtime modules

runtime configuration artifacts


Examples of runtime artifacts:

step_cfg.py
WMWorkload.pkl
JobPackage.pkl


These artifacts describe the physics workflow logic executed by the
job.


DIRAC jobs normally execute simpler command-line payloads.


Integrating CMS runtime expectations with the DIRAC execution model
requires additional translation logic.


------------------------------------------------------------
9. Why a translation layer is required
------------------------------------------------------------

Because WMCore and DIRAC operate at different abstraction levels.

WMCore focuses on:

physics workflow semantics

dataset processing logic

luminosity-level bookkeeping


DIRAC focuses on:

job scheduling

resource matchmaking

distributed execution


The translation layer converts workflow semantics into execution
semantics.


------------------------------------------------------------
10. Role of the Translation IR
------------------------------------------------------------

The canonical Translation IR provides an intermediate abstraction
layer.

WMCore
  |
  v
Translation IR
  |
  v
DIRAC transformation


The IR:

decouples source and target systems

preserves workflow semantics

enables export to workflow languages such as CWL


------------------------------------------------------------
11. Limitations of the current PoC
------------------------------------------------------------

The current proof of concept does not yet reproduce the full CMS
workflow execution model.

Key limitations include:

file-level processing only

no run/lumi mask support

limited dataset materialization


Current file materialization cap:

20 files per dataset


This limitation exists to keep the PoC manageable during development.


------------------------------------------------------------
12. Future integration challenges
------------------------------------------------------------

Several challenges remain for a full integration.

Handling run/lumi masks

intra-file splitting

integration with CMS data management systems

integration with DIRAC server-side transformation agents

mapping CMS runtime sandbox semantics


------------------------------------------------------------
13. Conceptual summary
------------------------------------------------------------

WMCore and DIRAC operate at different conceptual layers.

WMCore

workflow management


DIRAC

workload execution


The translation layer implemented in CMSDiracAux bridges these layers
through a canonical intermediate representation.


This architecture allows CMS workflows to be expressed in terms that
can eventually be executed through DIRAC-based infrastructures or
modern workflow languages.
