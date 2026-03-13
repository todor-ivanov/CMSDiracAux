# CMSDiracAux Technical Report

This directory contains the evolving technical report describing the
WMCore → DIRAC interoperability proof of concept implemented in the
CMSDiracAux repository.

The report documents the architecture, translation layer design,
execution model differences between WMCore and DIRAC, and the lessons
learned during the development of the proof of concept.

The report is organized into the following sections.


---

## 1. System architecture

Describes the overall architecture of the translation pipeline and
the relationship between WMCore, the Translation IR, DIRAC-style
materialization, and CWL export.

File

docs/reports/system-architecture.md


---

## 2. Architecture diagram

Provides a visual overview of the full system architecture and the
execution pipeline implemented in the repository.

File

docs/reports/architecture-diagram-readable.md


---

## 3. Architecture design notes

Contains additional architectural observations and design decisions
collected during the development of the PoC.

File

docs/reports/architecture-and-design-notes.md


---

## 4. Translation IR design

Explains the design and purpose of the canonical Translation IR,
which acts as the central abstraction layer between WMCore workflow
objects and DIRAC execution constructs.

File

docs/reports/translation-ir-design.md


---

## 5. WMCore vs DIRAC execution model

Compares the conceptual execution models of WMCore and DIRAC and
explains why a translation layer is necessary.

File

docs/reports/wmcore-vs-dirac-execution-model.md


---

## 6. Parameter mapping

Documents how WMCore parameters are translated into IR fields and
how those fields map to DIRAC transformation and job definitions.

File

docs/reports/wmcore-dirac-parameter-mapping.md


---

## 7. Proof of concept evaluation

Summarizes the results of the PoC implementation, including the
features successfully demonstrated and the current limitations.

File

docs/reports/poc-evaluation.md


---

## 8. Development checkpoints

Contains incremental development checkpoints documenting important
milestones during the implementation.

Directory

docs/reports/checkpoints/


---

## 9. Important PoC limitations

The current implementation includes several deliberate simplifications
for development purposes.

The most important limitation is the dataset materialization cap.

Maximum files per dataset:

20

This avoids generating extremely large job structures when working
with CMS datasets that may contain thousands of files.


---

## 10. Future work

Several directions remain for future development.

• integration with DIRAC server-side transformation agents  
• improved dataset discovery using DBS and DAS  
• support for CMS run/lumi masks  
• integration with CMS runtime environments  
• workflow portability through CWL and DIRACX


---

## Repository structure overview

The proof of concept produces artifacts grouped under a request
directory.

```
REQUEST_ROOT
|
|-- WMCore.fetched.d
|
|-- DIRAC.transf.d
|
`-- DIRAC.cwl.d
```

This layout separates:

• workflow extraction artifacts  
• DIRAC-style transformation materialization  
• workflow-language exports
