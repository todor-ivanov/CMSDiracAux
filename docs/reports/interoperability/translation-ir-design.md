# Translation IR Design

## Overview

The CMSDiracAux project introduces a **Translation Intermediate Representation (Translation IR)** that acts as the semantic bridge between the CMS workflow management system (WMCore) and the DIRAC distributed workload management system.

The purpose of this layer is to decouple the **workflow description semantics** from the **execution infrastructure**.

Without such an abstraction layer, the system would require a direct mapping between WMCore workflow objects and DIRAC execution objects. Because the two systems were designed under very different architectural assumptions, such a direct mapping would be brittle, difficult to maintain, and tightly coupled to the internal structure of both systems.

The Translation IR therefore provides a **canonical workflow description** that captures the essential semantics of a CMS workflow in a form that can later be materialized into different execution environments.

Conceptually the architecture becomes:

```
WMCore Workflow
        │
        ▼
Translation IR
        │
        ▼
DIRAC Execution Model
```

The Translation IR is therefore the **core abstraction layer of the CMSDiracAux architecture**.

---

# Architectural Role of the Translation IR

The role of the Translation IR can be understood by examining the architectural layers involved in workflow execution.

```
        CMS Workflow Infrastructure
 ┌────────────────────────────────────┐
 │ ReqMgr / WMCore                    │
 │                                    │
 │ Workflow definition                │
 │ Task graph                         │
 │ Splitting policies                 │
 └────────────────────────────────────┘
                │
                ▼
        CMSDiracAux Translation Layer
 ┌────────────────────────────────────┐
 │ Translation IR                     │
 │                                    │
 │ Canonical workflow objects         │
 │ Canonical task definitions         │
 │ Canonical splitting description    │
 └────────────────────────────────────┘
                │
                ▼
          DIRAC Execution System
 ┌────────────────────────────────────┐
 │ DIRAC Transformation               │
 │ DIRAC Workload Management System   │
 │ Pilot-based execution              │
 └────────────────────────────────────┘
```

The Translation IR acts as the **contract between the workflow domain and the execution domain**.

---

# Motivation for an Intermediate Representation

The need for a canonical translation layer arises from several fundamental differences between WMCore and DIRAC.

## Workflow definition philosophy

CMS workflows are defined as **explicit workflow graphs** where tasks and splitting rules are determined before execution begins.

DIRAC workflows are defined as **execution templates** where jobs are generated dynamically as data becomes available and resources are scheduled.

This difference can be summarized as:

```
CMS
workflow → jobs → execution

DIRAC
workflow template → runtime job generation
```

A direct translation between these models is difficult because the semantic structures differ significantly.

---

## Data-driven splitting differences

CMS workflows define splitting rules at the level of **data content**, often reaching the granularity of:

```
dataset
   │
   ▼
block
   │
   ▼
file
   │
   ▼
run
   │
   ▼
luminosity section
```

DIRAC transformations generally operate at the level of **files or datasets**, not at run or luminosity section boundaries.

Because of this difference, the bookkeeping logic originally implemented in **WMBS** must be preserved during translation.

---


# Design Goals

The Translation IR was designed with the following objectives.

### 1 System independence

The representation must not depend on:

```text
WMCore internal structures
DIRAC transformation internals
```

This ensures the workflow semantics can be reused across multiple execution systems.

---

### 2 Explicit workflow semantics

The IR must explicitly represent:

```text
workflow structure
task dependencies
runtime configuration
data interaction
job splitting policies
```

These elements are implicit or distributed across multiple components in the original systems.

---

### 3 Compatibility with multiple execution backends

The IR must support translation into:

```text
DIRAC transformations
CWL workflows
```

Future workflow engines could also consume the same representation.

---


# Translation IR Architecture

The Translation IR organizes workflow information into a small set of canonical entities.

```text
Workflow
   │
   ├── Task
   │      ├── RuntimeDefinition
   │      ├── SplittingPolicy
   │      └── DataReference
   │
   └── Dependency Graph
```

Each entity captures a distinct aspect of the workflow semantics.

---


# Conceptual Structure of the Translation IR

The Translation IR is composed of several canonical objects that represent the structure of a workflow.

```
CanonicalWorkflow
        │
        ▼
CanonicalTask
        │
        ▼
CanonicalSplitting
        │
        ▼
CanonicalDataset
```

Each object represents a layer of workflow semantics independent of the execution system.

---

# Canonical Workflow Object

The CanonicalWorkflow object represents the top-level workflow definition.

```
┌──────────────────────────────┐
│ CanonicalWorkflow            │
├──────────────────────────────┤
│ workflow_name                │
│ campaign                     │
│ processing_string            │
│ workflow_type                │
│ request_priority             │
└──────────────────────────────┘
```

This object corresponds to the high-level workflow definition stored in WMCore.

It provides metadata describing the processing campaign and workflow context.

---

# Canonical Task Object

Each workflow contains one or more tasks describing processing steps.

```
┌──────────────────────────────┐
│ CanonicalTask                │
├──────────────────────────────┤
│ task_name                    │
│ input_dataset                │
│ output_dataset               │
│ processing_step              │
│ software_version             │
└──────────────────────────────┘
```

Tasks represent the logical units of workflow processing.

In CMS workflows these correspond to WMCore task objects that define processing stages.

---

# Canonical Splitting Description

The splitting object describes how data should be partitioned into jobs.

```
┌──────────────────────────────┐
│ CanonicalSplitting           │
├──────────────────────────────┤
│ splitting_algorithm          │
│ files_per_job                │
│ lumis_per_job                │
│ events_per_job               │
└──────────────────────────────┘
```

This object captures the logic required to generate job boundaries.

The information in this object later drives the **CMS-specific splitting plugin inside DIRAC transformations**.

---

# Dataset Resolution

CMS workflows typically reference datasets rather than individual files.

Dataset resolution therefore occurs during the translation phase.

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

This resolution is performed using the CMS Data Aggregation System (DAS).

The resulting list of logical file names (LFNs) becomes the input for transformation splitting.

---

# Translation Pipeline

The full translation process implemented in CMSDiracAux can be summarized as:

```
WMCore workflow
        │
        ▼
Workflow extraction (wmcGet.py)
        │
        ▼
Workflow normalization
        │
        ▼
Canonical Translation IR
        │
        ▼
DIRAC materialization
```

The Translation IR therefore sits at the **center of the translation pipeline**.

---

# Mapping Between WMCore and Translation IR

The Translation IR is constructed by mapping WMCore workflow fields into canonical objects.

| WMCore Field  | Translation IR Field | Description                       |
| ------------- | -------------------- | --------------------------------- |
| RequestName   | workflow_name        | Workflow identifier               |
| TaskName      | task_name            | Task identifier                   |
| InputDataset  | input_dataset        | Primary dataset                   |
| SplittingAlgo | splitting_algorithm  | Splitting method                  |
| FilesPerJob   | files_per_job        | File partition size               |
| LumisPerJob   | lumis_per_job        | Luminosity section partition size |

This mapping captures the workflow semantics while removing WMCore-specific implementation details.

---


# Mapping to DIRAC

When exporting the IR to DIRAC the entities are mapped as follows.

| Translation IR      | DIRAC                               |
| ------------------- | ----------------------------------- |
| Workflow            | Production                          |
| Task                | Transformation                      |
| RuntimeDefinition   | WorkflowStep                        |
| SplittingPolicy     | Transformation plugin configuration |
| DataReference.files | LFN list                            |

The IR therefore provides all information required to construct a DIRAC transformation.

---

# Mapping to CWL

When exporting workflows to CWL the entities are mapped differently.

| Translation IR    | CWL             |
| ----------------- | --------------- |
| Workflow          | Workflow        |
| Task              | CommandLineTool |
| RuntimeDefinition | baseCommand     |
| DataReference     | File inputs     |
| DependencyGraph   | Workflow DAG    |

This enables portable workflow descriptions compatible with CWL execution engines.

---

# Translation IR and DIRAC Materialization

Once the workflow has been translated into the canonical IR, the execution structures required by DIRAC can be generated.

```
Translation IR
        │
        ▼
DIRAC Transformation
        │
        ▼
CMS Splitting Plugin
        │
        ▼
Job definitions
```

The CMS splitting plugin reconstructs the job boundaries defined by the original CMS workflow splitting rules.

This ensures that CMS workflow semantics are preserved.

---

# Relationship to WMBS

An important architectural observation arises from the design of the Translation IR.

The CMS workflow system originally relied on the **Workload Management Bookkeeping System (WMBS)** to maintain the mapping between workflow tasks, data partitions, and jobs.

Even when workflows are executed in DIRAC, the system must still maintain this relationship.

```
workflow task
      │
      ▼
data partitions
      │
      ▼
jobs
```

Therefore the Translation IR and the DIRAC splitting plugin effectively reproduce the functionality originally implemented by WMBS.

---

# Role in the CMSDiracAux Architecture

The Translation IR sits at the center of the CMSDiracAux architecture.

```text
WMCore workflow
        │
        ▼
Translation IR
        │
        ├── DIRAC transformation
        │
        └── CWL workflow
```

This design isolates the **workflow semantics** from the **execution system**, allowing workflows to be translated and reused across different distributed computing frameworks.

---

# Importance of the Translation IR

The Translation IR solves the three main interoperability problems identified earlier in the report.

```text
workflow semantic mismatch
workflow–data interaction mismatch
runtime environment mismatch
```

By capturing workflow semantics in a system-independent form, the IR enables deterministic translation between heterogeneous workflow management systems.

# Design Advantages

The Translation IR provides several advantages:

### Decoupling

Workflow semantics are separated from execution infrastructure.

### Portability

Workflows can potentially be materialized into different execution systems.

### Stability

Changes in either WMCore or DIRAC implementations do not require rewriting the translation logic.

### Extensibility

Additional workflow systems could be integrated by implementing new translators.

---

# Summary

The Translation IR represents the core architectural concept of CMSDiracAux.

It provides a canonical representation of CMS workflows that preserves the semantics of workflow definitions, task structures, and data splitting policies while allowing the workflows to be executed within the DIRAC distributed computing infrastructure.

By introducing this abstraction layer, CMSDiracAux demonstrates that workflows defined within WMCore can be systematically translated into execution structures compatible with DIRAC without losing the fine-grained workflow semantics required by CMS computing workflows.
