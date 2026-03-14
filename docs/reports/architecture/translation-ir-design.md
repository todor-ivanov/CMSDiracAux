# Translation IR Design

## Purpose of the Translation IR

The CMSDiracAux project introduces a **canonical Translation Intermediate Representation (Translation IR)** to bridge the architectural differences between the CMS workflow management system and the DIRAC workload management framework.

Direct translation between the two systems is not possible because their workflow models operate at **different abstraction levels**.

```text
CMS WMCore → experiment-aware workflow system
DIRAC      → distributed workload orchestration system
```

The Translation IR provides a **system-independent workflow representation** that captures the essential workflow semantics while remaining decoupled from the execution framework.

The role of the Translation IR can be summarized as:

```text
WMCore workflow
        ↓
Translation IR
        ↓
DIRAC transformation
or
CWL workflow
```

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

# Workflow Entity

The **Workflow** object represents the complete processing pipeline.

It contains:

```text
workflow identifier
task list
dependency graph
workflow metadata
```

The workflow object therefore defines the **top-level orchestration structure**.

---

# Task Entity

A **Task** represents a processing stage within the workflow.

It corresponds conceptually to:

```text
WMCore → WMTask
DIRAC  → Transformation
```

Each task contains:

```text
runtime definition
input dataset reference
output dataset reference
splitting policy
resource requirements
```

Tasks are connected through the workflow dependency graph.

---

# RuntimeDefinition

The **RuntimeDefinition** entity describes how the task should execute.

This includes:

```text
executable
software environment
configuration parameters
runtime scripts
```

Examples of runtime definitions include:

```text
CMSSW cmsRun execution
container execution
generic script execution
```

This abstraction allows the IR to represent workflows without embedding experiment-specific execution logic.

---

# DataReference

The **DataReference** entity describes the data consumed or produced by a task.

It captures dataset information independently of the storage system.

Typical fields include:

```text
dataset identifier
block identifiers
file list
metadata
```

The IR does not assume a specific data catalog implementation.

---

# SplittingPolicy

The **SplittingPolicy** entity defines how tasks are partitioned into jobs.

This entity captures the semantics that differ most strongly between CMS and DIRAC.

Fields include:

```text
splitting algorithm
files per job
events per job
resource constraints
```

The splitting policy therefore defines the transformation from **task-level work to executable jobs**.

---

# Dependency Graph

The workflow structure is represented as a **directed acyclic graph (DAG)**.

Tasks are connected through data dependencies.

```text
Task A
  │
  ▼
Task B
```

This representation is compatible with both:

```text
DIRAC workflow steps
CWL workflow DAGs
```

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
