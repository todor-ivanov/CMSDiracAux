# Knowledge Base

The ultimate goal of the project is not only to create a deterministic translation PoC
between the CMS workflow management system and DIRAC, but also to express the complexity
of the workflows description and make and explain a transition layer of workflow level abstractions
between the two systems, which is inevitably connected with the two system's internals.
(reflecting the fact that Non of the two systems' workflows descriptions are agnostic to their own architectures)


# 1. Abstraction layers

The earlier discussion correctly identified the following conceptual mapping.

```
WMCore
│
├─ WMWorkload
│     workflow container
│
├─ WMTask
│     processing stage
│
├─ WMStep
│     runtime execution definition
│
└─ WMSplitting
      job generation rules
```

DIRAC equivalent:

```
DIRAC
│
├─ Production
│
├─ Transformation
│
├─ Job template (JDL)
│
└─ TransformationPlugin
      job generation logic
```

This mapping was already reconstructed in the restored conversation PDF.

---

# 2. Translation pipeline

The PoC architecture is therefore:

```
WMCore workflow
        │
        ▼
Canonical Translation IR
        │
        ├──────────► DIRAC Transformation
        │
        └──────────► CWL workflow export
```

Important:

The **Translation IR is not optional**.
It is the **architectural bridge** between the two systems.

---

# 3. Major architectural mismatch discovered

The discussions with DIRAC developers confirmed several **structural mismatches**.

## Runtime code distribution

CMS:

```
job sandbox
│
├─ WMCore runtime
├─ workflow structure
├─ parameter sets
└─ job.pkl
```

DIRAC:

```
runtime code → CVMFS
job description → jobDescription.xml
```

DIRAC transformations **normally do not distribute runtime sandboxes**. 

This is a major incompatibility with CMS workflows.

---

## Job execution model

DIRAC runtime:

```
Executable: dirac-jobexec
Arguments: jobDescription.xml
```

All workflow steps are interpreted **inside the XML description**, not the JDL.

This means:

```
JDL → bootstrap
XML → workflow logic
```

---

## Job splitting model

DIRAC splitting constraints:

```
file = lowest granularity
```

Sub-file splitting is not supported in vanilla DIRAC.

Workarounds suggested:

```
1) split dataset into multiple transformations
2) pre-split files externally
```

This limitation directly affects CMS **event-level splitting models**.

---

# 4. DIRAC architecture relevant to the PoC

From the developer discussions we learned the following key details.

### Transformation plugins

Plugins generate tasks based on input data.

Examples:

```
Standard
BySize
ByShare
```

But **real experiments implement custom plugins**.

Example:

```
LHCbDIRAC TransformationSystem
```

This is important because CMS will likely need its own plugin.

---

### Agent/plugin roles

DIRAC uses different agents for different operations:

```
RequestTaskAgent
    data movement

Transformation agents
    job generation

TaskManager plugins
    job placement
```

These are separate concerns.

---

### Extension architecture

DIRAC is extended experiment-side.

Example:

```
DIRAC
└── LHCbDIRAC
        plugin systems
        bookkeeping
        production system
```

This confirms the feasibility of a **CMSDIRAC-like extension**.

# 5. CMS workflow complexity (critical insight)

The conversations revealed an important property of CMS workflows.

They are **not purely data-driven**.

Job splitting depends on:

```
data volume
+
CMSSW runtime requirements
+
workflow structure
+
data tiers
+
processing chains
```

Meaning:

```
splitting = multi-dimensional
```

This explains why simple data-based splitting cannot replicate CMS workflows.

---

# 6. Workflow structure in CMS

CMS workflows contain chains:

```
StepChain
TaskChain
```

Difference:

StepChain

```
single pilot
multiple sequential steps
no intermediate transfers
```

TaskChain

```
multiple pilots
intermediate data movement
```

This concept does **not exist directly in DIRAC**.

Therefore it must be represented in the Translation IR.

---
# Important insight discovered

The PoC is not merely a **translator**.

It is effectively creating a **meta-workflow representation**.

Which means your project is really building:

```
WMCore
   ↓
Workflow IR
   ↓
DIRAC
   ↓
CWL
```

This is **very close to a workflow interoperability layer**.

That makes the project conceptually much stronger.


# WMCore vs DIRAC Workflow Model Comparison

This table will become the **foundation of the report section**:

```
docs/reports/interoperability/wmcore-dirac-mismatch.md
```

---

# Workflow Architecture Comparison

| Concept                        | WMCore (CMS)                       | DIRAC                       |
| ------------------------------ | ---------------------------------- | --------------------------- |
| Workflow container             | `WMWorkload`                       | Production / Transformation |
| Processing stage               | `WMTask`                           | Transformation              |
| Execution step                 | `WMStep`                           | Workflow Step               |
| Job definition                 | `WMBSJob`                          | Job (JDL)                   |
| Job runtime definition         | CMSSW configuration (`pset`)       | jobDescription.xml          |
| Job bootstrap                  | CMSRun                             | `dirac-jobexec`             |
| Job parameters                 | JobPackage.pkl                     | JobParameters               |
| Job splitting                  | WMBS splitting plugins             | Transformation plugins      |
| Splitting granularity          | file / event / runtime constraints | file only                   |
| Dataset abstraction            | dataset → block → file             | LFN list                    |
| Data discovery                 | DAS                                | DIRAC File Catalog          |
| Workflow orchestration         | WMAgent                            | DIRAC Agents                |
| Runtime code distribution      | job sandbox                        | CVMFS                       |
| Workflow DAG                   | implicit in TaskChain/StepChain    | implicit workflow XML       |
| Future workflow representation | none standardized                  | CWL                         |

---

# Key Architectural Differences

## 1 Runtime environment

```
WMCore
payload aware
deeply coupled to CMSSW
```

```
DIRAC
payload agnostic
execution wrapper
```

---

## 2 Workflow semantics

```
WMCore workflow
= physics workflow
```

```
DIRAC workflow
= workload orchestration
```

---

## 3 Job splitting model

WMCore:

```
multi-dimensional
data
+
runtime requirements
+
data tiers
```

DIRAC:

```
primarily data driven
```

---

## 4 Runtime entry point

DIRAC jobs:

```
Executable: dirac-jobexec
Arguments: jobDescription.xml
```

Everything else is interpreted **inside the workflow XML**.

---

# 3. Formal Translation IR Schema

This is the **most important architectural artifact** in the project.

The Translation IR must represent **workflow semantics independent of both systems**.

---

# Translation IR Layer

```
WMCore
   │
   ▼
Translation IR
   │
   ├── DIRAC Transformation
   │
   └── CWL Workflow
```

---

# Translation IR Core Entities

## Workflow

Top-level container.

```
Workflow
  id
  name
  tasks[]
  datasets[]
  metadata
```

---

## Task

Represents a **processing stage**.

```
Task
  id
  name
  input_dataset
  output_dataset
  runtime
  splitting
  dependencies[]
```

---

## RuntimeDefinition

Abstract runtime description.

```
RuntimeDefinition
  executable
  environment
  parameter_sets
  software_stack
```

Examples:

```
CMSSW runtime
container runtime
script runtime
```

---

## DataReference

Dataset abstraction.

```
DataReference
  dataset
  blocks[]
  files[]
```

---

## SplittingPolicy

Job generation model.

```
SplittingPolicy
  algorithm
  granularity
  events_per_job
  files_per_job
  runtime_constraints
```

---

## JobTemplate

Abstract job model.

```
JobTemplate
  runtime
  input_data
  parameters
  resources
```

---

# Translation IR Graph

The IR is naturally a **DAG**.

```
Workflow
   │
   ├── Task A
   │      │
   │      ▼
   │    Task B
   │
   └── Task C
```

Dependencies come from **data flow**.

---

# IR → DIRAC Mapping

| IR element          | DIRAC                |
| ------------------- | -------------------- |
| Workflow            | Production           |
| Task                | Transformation       |
| RuntimeDefinition   | WorkflowStep         |
| JobTemplate         | JDL                  |
| SplittingPolicy     | TransformationPlugin |
| DataReference.files | LFN list             |

---

# IR → CWL Mapping

| IR element        | CWL             |
| ----------------- | --------------- |
| Workflow          | Workflow        |
| Task              | CommandLineTool |
| RuntimeDefinition | baseCommand     |
| DataReference     | File inputs     |
| SplittingPolicy   | Scatter         |

---

# Why Translation IR is Essential

Without the IR the system becomes:

```
WMCore → DIRAC
```

Which fails because:

```
workflow semantics ≠ compatible
```

With IR:

```
WMCore
   │
   ▼
Workflow IR
   │
   ├─ DIRAC
   └─ CWL
```

Now both targets can evolve independently.

---

# Updated Architecture Diagram

```
WMCore Workflow
        │
        ▼
Translation IR
        │
        ├──────────────► DIRAC Transformation
        │                    │
        │                    ▼
        │               jobDescription.xml
        │
        └──────────────► CWL Workflow
                             │
                             ▼
                         DIRACX / other engines
```

---












# Important Insight for the Report

Your project is **not simply a translator**.

It is effectively building:

```
Workflow Interoperability Layer
```

Between two experiment computing systems.

That makes the report far stronger scientifically.

---
