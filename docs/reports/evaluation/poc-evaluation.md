# Proof-of-Concept Evaluation

## Overview

The CMSDiracAux prototype demonstrates that workflows defined within the CMS workflow management system can be translated into execution structures compatible with the DIRAC distributed computing framework.

The prototype focuses on validating the architectural feasibility of such a translation rather than implementing a full production-grade system.

---

# Translation Feasibility

The project successfully demonstrates that workflow descriptions originating from WMCore can be converted into a canonical intermediate representation.

This representation captures:

* workflow metadata
* task structure
* dataset references
* splitting policies

The resulting IR provides a stable abstraction for further processing.

---

# Execution Model Compatibility

The translation pipeline successfully bridges the conceptual differences between CMS and DIRAC execution models.

CMS workflows follow an explicit workflow evolution model:

```
workflow → tasks → jobs
```

DIRAC workflows follow a dynamic execution model:

```
transformation → tasks → jobs
```

The Translation IR allows CMS workflows to be expressed in a form compatible with the DIRAC transformation system.

---

# Preservation of Splitting Semantics

A key challenge in the translation process is preserving CMS splitting semantics.

CMS workflows often define splitting policies at the level of data content rather than storage containers.

The CMSDiracAux architecture demonstrates that this functionality can be reproduced inside DIRAC through a CMS-specific splitting plugin.

---

# Runtime Reconstruction

The prototype demonstrates the feasibility of reconstructing CMS runtime environments on worker nodes using bootstrap scripts.

These scripts inject the runtime parameters required by CMS jobs and ensure that the correct dataset partitions are processed.

---

# Architectural Insight

The most important architectural insight emerging from this work is that CMS workflow bookkeeping cannot be removed simply by changing the execution backend.

Even when workflows are executed through DIRAC, the system must maintain the mapping between:

```
workflow tasks
data partitions
jobs
```

This mapping was originally implemented by WMBS and must be reproduced within the DIRAC transformation system.

---

# Summary

The CMSDiracAux proof-of-concept confirms that interoperability between the CMS workflow management system and the DIRAC distributed computing framework is achievable through a carefully designed translation architecture centered around a canonical intermediate representation.


# Proof of Concept Evaluation

This document summarizes the results, limitations, and lessons learned
from the WMCore → DIRAC interoperability proof of concept implemented
in CMSDiracAux.

The goal of the PoC was not to provide a production-ready integration,
but to demonstrate that CMS workflows defined in WMCore can be
translated into a form compatible with DIRAC-style execution models
and portable workflow representations.


------------------------------------------------------------
1. PoC goals
------------------------------------------------------------

The proof of concept aimed to demonstrate the following capabilities.

1. Extract workflow information from WMCore.

2. Translate WMCore workflow structures into an intermediate
   representation independent from both WMCore and DIRAC.

3. Materialize a local representation of DIRAC transformations.

4. Simulate DIRAC transformation splitting behavior locally.

5. Resolve CMS datasets into file lists using DAS.

6. Export the resulting workflow structure into a CWL-compatible
   workflow bundle.


------------------------------------------------------------
2. Successfully demonstrated capabilities
------------------------------------------------------------

The PoC successfully demonstrated the following architectural concepts.

Workflow extraction

WMCore workflows can be serialized into portable JSON artifacts.

Translation layer

A canonical Translation IR can represent workflow semantics in a
system-neutral way.

Dataset discovery

CMS datasets can be resolved to file lists using DAS queries.

Transformation simulation

DIRAC-style transformations and job definitions can be materialized
locally without running DIRAC services.

Workflow export

The translated workflow can be exported into CWL, aligning with
future workflow-language-based execution models.


------------------------------------------------------------
3. Key architectural achievements
------------------------------------------------------------

Translation IR abstraction

The introduction of a canonical intermediate representation provides a
clean separation between:

workflow definition semantics

and

execution infrastructure semantics.


Request-scoped artifact layout

All artifacts produced during translation are grouped under a single
request directory.

REQUEST_ROOT
|
|-- WMCore.fetched.d
|
|-- DIRAC.transf.d
|
`-- DIRAC.cwl.d


This structure makes the pipeline easy to inspect and debug.


Local transformation simulation

DIRAC transformations can be simulated locally using:

runLocalTransformation.py

This allows transformation logic to be tested without a full DIRAC
server deployment.


CWL workflow export

The ability to export the workflow into CWL demonstrates that the
workflow representation can be decoupled from the legacy DIRAC Python
object model.


------------------------------------------------------------
4. Current limitations
------------------------------------------------------------

Several limitations remain in the current implementation.


Dataset materialization limit

The PoC currently limits dataset materialization to:

20 files per dataset.


Reason

Large CMS datasets often contain thousands of files.

Example dataset used during testing:

approximately 7100 files.


Without this limit the PoC would generate extremely large job
structures.


Run and luminosity section handling

CMS workflows operate at run and luminosity section granularity.

The PoC currently operates only at file granularity.


DIRAC server integration

The PoC simulates DIRAC transformations locally.

Server-side DIRAC components such as the Transformation Agent are not
currently integrated.


CMS runtime integration

CMS jobs require a complex runtime environment involving:

CMSSW software

WMCore runtime modules

runtime configuration artifacts.


The PoC currently focuses on workflow structure rather than full
runtime execution.


------------------------------------------------------------
5. Lessons learned
------------------------------------------------------------

Different workflow abstractions

WMCore and DIRAC operate at fundamentally different conceptual levels.

WMCore describes physics workflows.

DIRAC schedules distributed workloads.


Importance of an intermediate representation

Attempting to directly map WMCore objects to DIRAC objects would
introduce tight coupling between systems.

The Translation IR enables clean abstraction boundaries.


Dataset discovery is essential

WMCore workflows reference datasets rather than explicit files.

Therefore dataset discovery must occur before job definitions can be
generated.


CMS data hierarchy matters

CMS data is organized as:

dataset → block → file

Understanding this hierarchy is essential when designing splitting and
data discovery logic.


------------------------------------------------------------
6. Future work
------------------------------------------------------------

Several directions remain for future development.


Improved dataset handling

Block-level dataset partitioning

Richer DBS metadata usage

More scalable dataset materialization


DIRAC integration

Server-side deployment of CMS transformation plugins

Integration with the DIRAC Transformation Agent


Workflow representation

Native CWL workflows aligned with DIRACX

Workflow portability across execution infrastructures


CMS runtime support

Integration of CMSSW runtime environments

Support for CMS job sandbox semantics


------------------------------------------------------------
7. PoC conclusion
------------------------------------------------------------

The proof of concept demonstrates that CMS workflows defined in WMCore
can be translated into an intermediate representation that can be
materialized as DIRAC-style transformations and exported as portable
workflow definitions.

The Translation IR serves as the central abstraction layer enabling
this interoperability.

Although significant engineering work remains for production-scale
integration, the PoC validates the architectural feasibility of this
approach.
