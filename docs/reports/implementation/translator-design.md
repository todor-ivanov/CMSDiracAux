# Translator Design

## Overview

The CMSDiracAux translator is responsible for converting workflow definitions originating from the CMS workflow management system (WMCore) into a canonical intermediate representation that can later be materialized into execution structures compatible with the DIRAC distributed computing framework.

The translator operates as a multi-stage pipeline:

```
WMCore workflow
      │
      ▼
Workflow extraction
      │
      ▼
Normalization
      │
      ▼
Translation IR
      │
      ▼
Execution materialization
```

The translator isolates the semantic components of the workflow from execution details.

---

# Translator Pipeline

The current proof-of-concept pipeline consists of the following stages:

```
┌──────────────────────────┐
│ WMCore Workflow          │
│ (ReqMgr / WMCore APIs)   │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│ Workflow extraction      │
│ wmcGet.py                │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│ Workflow normalization   │
│ metadata cleanup         │
│ DAS dataset resolution   │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│ Translation IR creation  │
│ canonical workflow model │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│ DIRAC materialization    │
│ transformation objects   │
└──────────────────────────┘
```

Each stage performs a well-defined transformation.

---

# Workflow Extraction

The workflow extraction stage retrieves workflow definitions from WMCore and serializes them into portable artifacts.

This stage is implemented by:

```
wmcGet.py
```

Its responsibilities include:

* retrieving workflow request information
* extracting task graphs
* collecting dataset references
* capturing splitting policies
* serializing workflow metadata

The output of this stage is a **serialized representation of the WMCore workflow structure**.

---

# Workflow Normalization

After extraction the workflow description is normalized.

Normalization includes:

* resolving dataset references
* querying DAS for file lists
* converting metadata formats
* preparing splitting information

Dataset resolution pipeline:

```
dataset name
     │
     ▼
DAS query
     │
     ▼
file records
     │
     ▼
LFN list
```

Normalization ensures the workflow description becomes deterministic and portable.

---

# Translation IR Construction

The canonical workflow representation is built during this stage.

The Translation IR captures the following elements:

```
CanonicalWorkflow
      │
      ▼
CanonicalTasks
      │
      ▼
CanonicalSplitting
      │
      ▼
CanonicalDatasetReferences
```

The IR intentionally removes WMCore-specific implementation details while preserving workflow semantics.

---

# Translation Strategy

The translation logic follows a structured mapping approach.

| WMCore Object     | Translation IR Object |
| ----------------- | --------------------- |
| Workflow          | CanonicalWorkflow     |
| Task              | CanonicalTask         |
| Splitting policy  | CanonicalSplitting    |
| Dataset reference | CanonicalDataset      |

This mapping preserves the conceptual workflow structure while enabling independent execution backends.

---

# Translation Design Principles

The translator is designed according to several principles.

### Deterministic translation

Given the same WMCore workflow definition, the translator must produce identical Translation IR objects.

### Execution independence

The IR must not depend on a specific execution system.

### Minimal loss of semantics

Important workflow parameters such as splitting policies and runtime configuration must remain intact.

### Extensibility

The translator should allow future execution targets to be supported without rewriting the extraction logic.

---

# Relationship to Execution Systems

The translator intentionally stops before execution system specifics are introduced.

Execution systems are handled in the subsequent stage:

```
Translation IR
      │
      ▼
DIRAC materialization
```

This separation ensures that workflow semantics remain stable even if the execution infrastructure evolves.

---

# Summary

The CMSDiracAux translator forms the front end of the interoperability pipeline.

It extracts CMS workflows from WMCore, normalizes their metadata, and constructs a canonical representation that can later be used to generate execution structures for the DIRAC distributed computing framework.
