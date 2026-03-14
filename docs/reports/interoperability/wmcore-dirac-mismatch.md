# WMCore–DIRAC Workflow Model Mismatch

## Purpose of this section

This section explains the **architectural mismatch between the CMS workflow management system (WMCore/WMBS)** and the **DIRAC workload management framework**.

Understanding this mismatch is critical for the CMSDiracAux project because the goal of the project is **not only to translate workflow descriptions**, but also to provide a **transition layer of workflow-level abstractions between the two systems**.

The following sections address specific aspects of this
interoperability challenge:

• dataset-resolution-model.md
• translation-ir-rationale.md
• job-description-translation.md


As stated in the project objectives:

> The ultimate goal of the project is not only to create a deterministic translation PoC between the CMS workflow management system and DIRAC, but also to express the complexity of the workflows description and make and explain a transition layer of workflow level abstractions between the two systems, which is inevitably connected with the two system's internals. (reflecting the fact that Non of the two systems' workflows descriptions are agnostic to their own architectures)

The mismatch originates from a fundamental difference:

```
WMCore workflows = experiment execution model
DIRAC workflows  = distributed workload orchestration
```

Therefore, **a direct translation between the two systems is not possible without introducing an intermediate abstraction layer**.


---

# CMS Workflow Execution Model

The CMS workflow system is implemented in **WMCore** and **WMBS** and is tightly coupled to the **CMSSW experiment framework**.

The system operates at multiple hierarchical levels:

* workflow definition
* task decomposition
* step execution
* dataset-aware splitting
* job creation

The execution model is shown below.

```
┌──────────────────────────────────────────────────────────┐
│                    CMS Workflow Request                  │
│                                                          │
│                 Physics workflow definition              │
│                    (WMWorkload object)                   │
└─────────────────────────────┬────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────┐
│                          Task                            │
│                       (WMTask)                           │
│                                                          │
│        Represents a processing stage in the workflow     │
└─────────────────────────────┬────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────┐
│                          Step                            │
│                        (WMStep)                          │
│                                                          │
│   Defines execution inside the CMSSW framework           │
│                                                          │
│   Runtime elements                                       │
│   • CMSSW release                                        │
│   • pset configuration                                   │
│   • processing parameters                                │
└─────────────────────────────┬────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────┐
│                     WMBS Splitting                       │
│                                                          │
│        Multi-dimensional splitting algorithm             │
│                                                          │
│   Splitting criteria may include                         │
│   • dataset / block / file structure                     │
│   • number of events                                     │
│   • runtime constraints                                  │
│   • CMSSW processing requirements                        │
└─────────────────────────────┬────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────┐
│                        Job Creation                      │
│                        (WMBSJob)                         │
│                                                          │
│   Job payload includes                                   │
│   • workflow runtime sandbox                             │
│   • parameter sets                                       │
│   • JobPackage.pkl                                       │
│   • input data references                                │
└──────────────────────────────────────────────────────────┘
```

---

# Key Characteristics of the CMS Workflow Model

### Workflow definitions are experiment-aware

CMS workflows are tightly integrated with the **CMSSW runtime environment**.

A workflow does not only describe scheduling logic.
It also contains:

```
• experiment software configuration
• physics processing parameters
• runtime environment assumptions
```

This makes CMS workflows **payload-aware**.

---

### Multi-dimensional job splitting

Job splitting in CMS is not purely data driven.

Splitting decisions may depend on:

```
data hierarchy
+
runtime configuration
+
processing chains
+
resource constraints
```

This leads to **multi-dimensional splitting**.

---

### Dataset hierarchy drives workflow execution

CMS data is structured hierarchically:

```
dataset
   │
   ▼
block
   │
   ▼
file
```

Workflow execution often depends on this hierarchy.

---

# DIRAC Workflow Execution Model

DIRAC is designed as a **general distributed workload management system**.

Unlike WMCore, DIRAC workflows are **payload-agnostic**.

The system focuses on:

* job orchestration
* resource scheduling
* distributed execution

The execution model is shown below.

```
┌──────────────────────────────────────────────────────────┐
│                        Production                        │
│                                                          │
│            High-level description of a workflow          │
└─────────────────────────────┬────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────┐
│                      Transformation                      │
│                                                          │
│     Defines how jobs should be generated from data       │
└─────────────────────────────┬────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────┐
│                   Transformation Plugin                  │
│                                                          │
│           Determines job creation logic                  │
│                                                          │
│        Typical splitting criteria                        │
│        • file                                            │
│        • file groups                                     │
└─────────────────────────────┬────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────┐
│                           Job                            │
│                                                          │
│  Executable                                              │
│  dirac-jobexec                                           │
│                                                          │
│  Input                                                   │
│  jobDescription.xml                                      │
│                                                          │
│  Runtime environment                                     │
│  CVMFS                                                   │
└──────────────────────────────────────────────────────────┘
```

---

# Key Characteristics of the DIRAC Workflow Model

### Payload-agnostic workflow definition

DIRAC does not assume knowledge of experiment-specific software.

Jobs are executed through a generic entry point:

```
dirac-jobexec
```

The job runtime logic is described in:

```
jobDescription.xml
```

---

### Runtime environment externalization

Unlike CMS workflows, DIRAC assumes runtime software is **already available on the worker node**.

Typically via:

```
CVMFS
```

Therefore jobs do not normally carry runtime code in a sandbox.

---

### Data-driven job splitting

DIRAC transformations typically split work based on **input data granularity**.

The most common granularity is:

```
file
```

This differs significantly from CMS workflows where splitting may depend on **processing parameters and runtime logic**.

---

# Architectural Comparison

The following diagram highlights the structural mismatch between the two workflow models.

```
┌─────────────────────────────────────────────┐
│                CMS WMCore                   │
│         Workflow Management System          │
└─────────────────────────────────────────────┘
                     │
                     ▼
        ┌───────────────────────────────┐
        │           Workflow            │
        │           WMWorkload          │
        └───────────────┬───────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │             Task              │
        │            WMTask             │
        └───────────────┬───────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │             Step              │
        │            WMStep             │
        │                               │
        │  Runtime: CMSSW / cmsRun      │
        │  Parameter sets (pset.py)     │
        └───────────────┬───────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │        WMBS Splitting         │
        │                               │
        │  Multi-dimensional splitting  │
        │                               │
        │  • dataset / block / file     │
        │  • runtime constraints        │
        │  • data tiers                 │
        └───────────────┬───────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │           Job                 │
        │          WMBSJob              │
        │                               │
        │  Input sandbox                │
        │  CMSSW runtime                │
        │  JobPackage.pkl               │
        └───────────────────────────────┘



                ARCHITECTURAL GAP



┌─────────────────────────────────────────────┐
│                    DIRAC                    │
│        Workload Management Framework        │
└─────────────────────────────────────────────┘
                     │
                     ▼
        ┌───────────────────────────────┐
        │          Production           │
        └───────────────┬───────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │        Transformation         │
        └───────────────┬───────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │  Transformation Plugin        │
        │                               │
        │  Splitting by input data      │
        │  granularity                  │
        └───────────────┬───────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │             Job               │
        │                               │
        │  Executable: dirac-jobexec    │
        │  jobDescription.xml input     │
        │  runtime via CVMFS            │
        └───────────────────────────────┘
```

---

# Why a Translation Layer is Necessary

The comparison shows that **the two systems operate at different abstraction levels**.

```
WMCore → experiment workflow system
DIRAC  → distributed execution framework
```

Direct translation would therefore lose essential information.

To resolve this problem, CMSDiracAux introduces a **canonical Translation IR**.

```
WMCore Workflow
        │
        ▼
Translation IR
        │
        ├── DIRAC transformation
        │
        └── CWL workflow
```

The Translation IR allows workflow semantics to be represented in a **system-independent form**.

This makes it possible to:

```
translate WMCore workflows
generate DIRAC transformations
export workflows to CWL
```

without coupling the workflow description to either system.

---



---

# Static vs Dynamic Workflow–Data Coupling

An important conceptual difference between the CMS workflow system (WMCore/WMBS) and DIRAC concerns **how workflows interact with data and how workload is distributed over the data space**.

Although both systems ultimately execute jobs on distributed computing resources, they approach the relationship between **workflow definition and data distribution** in fundamentally different ways.

This difference can be characterized as a contrast between **static workflow partitioning** and **dynamic workload expansion**.

---

# CMS Workflow Model: Static Workflow Partitioning

In the CMS workflow system, the workflow is **fully defined before runtime** and then distributed across the dataset during job creation.

The WMBS subsystem performs the following operations:

1. **Dataset discovery**
2. **Dataset partitioning**
3. **Job generation**
4. **Runtime configuration generation**

Once these steps are completed, the runtime jobs are already **fully defined units of work**.

Each job receives:

```text
• a well-defined subset of the dataset
• runtime configuration parameters
• a CMSSW execution configuration
```

The runtime configuration is generated using **PSetTweaks**, which determine the **exact processing boundaries of each job over the dataset**.

Conceptually, the system performs the following transformation:

```text
workflow definition
        +
dataset description
        ↓
explicit job list
```

The workflow management system therefore produces **all executable units of work ahead of execution**.

The runtime environment simply executes the predefined jobs.

This results in a **static workflow partitioning model**.

---

# DIRAC Workflow Model: Dynamic Workload Expansion

DIRAC follows a different philosophy.

Instead of producing a fully materialized set of jobs ahead of execution, DIRAC uses **workflow templates combined with transformation rules**.

A transformation describes:

```text
• job template
• input data selection criteria
• job splitting policy
```

The transformation system then **generates jobs dynamically as data becomes available**.

Conceptually, the transformation system performs:

```text
workflow template
        +
incoming data
        ↓
job generation
```

Jobs are therefore not necessarily enumerated in advance.

Instead, they are **spawned dynamically based on data discovery and transformation rules**.

This produces a **dynamic workload expansion model**.

---

# Comparison of the Two Models

The two approaches differ primarily in **when the workflow is resolved into executable jobs**.

| Aspect                | CMS WMCore                        | DIRAC                       |
| --------------------- | --------------------------------- | --------------------------- |
| Workflow definition   | full workflow graph defined       | workflow template defined   |
| Job generation moment | before execution                  | during execution            |
| Dataset interaction   | workflow distributed over dataset | jobs generated from data    |
| Runtime configuration | embedded in job                   | externalized in environment |
| Execution model       | static job set                    | dynamic job spawning        |

This difference significantly influences how each system manages data distribution and load balancing.

---

# Analogy Between Quantum Pictures and Workflow Management Models

## Context

When comparing the CMS Workflow Management System (WMCore) with the DIRAC workflow model, an analogy with different formulations of quantum mechanics can help explain the conceptual difference in how workflows are represented and executed.

---

# Schrödinger Picture

In the **Schrödinger picture**, the **state evolves with time**, while the operators remain fixed.

Conceptually:

```text
state(t) evolves
operators remain fixed
```

In this formulation, the entire evolution of the system is encoded in the **explicit time evolution of the state vector**.

---

## Analogy with CMS WMCore

The CMS workflow system behaves similarly to the Schrödinger picture.

In CMS:

* workflows are **fully defined in advance**
* job boundaries are **explicitly constructed**
* the entire evolution of the workflow is **pre-determined**

Conceptually:

```text
workflow definition
        ↓
explicit job splitting
        ↓
predefined jobs
        ↓
execution
```

Thus, the **state of the workflow evolves**, while the structure of the execution model remains fixed.

---

# Heisenberg Picture

In the **Heisenberg picture**, the situation is reversed:

```text
operators evolve
state remains fixed
```

The system state is fixed, while the **observables (operators)** evolve with time.

This formulation focuses on **transformations acting on the system rather than explicit evolution of the state**.

---

## Analogy with DIRAC

The DIRAC workflow model resembles the Heisenberg picture.

In DIRAC:

* the workflow definition acts as a **static template**
* jobs are generated dynamically as data becomes available
* the execution evolves through **operations applied to data**

Conceptually:

```text
workflow template
        ↓
data appears
        ↓
transformation generates tasks
        ↓
jobs executed dynamically
```

Thus, the **execution operators evolve**, while the workflow description remains largely static.

---

# Conceptual Summary

```text
CMS WMCore
Schrödinger-like model

workflow evolves explicitly
jobs defined in advance


DIRAC
Heisenberg-like model

workflow template fixed
execution generated dynamically
```

---

This analogy highlights the fundamental philosophical difference between the systems:

* **CMS workflows encode the full evolution of computation explicitly.**
* **DIRAC workflows encode transformations applied dynamically to available data.**

This conceptual distinction helps explain why an intermediate abstraction layer such as the **Translation IR** is required to bridge the two workflow models.

# Validity of the Analogy

The analogy is conceptually useful but should be treated carefully.

The systems do not literally implement physical time evolution models.
However, the analogy captures an important architectural difference.

The essential point is the **location of dynamism in the system**.

| System     | Dynamic component                     |
| ---------- | ------------------------------------- |
| CMS WMCore | workflow state over dataset           |
| DIRAC      | job generation from workflow template |

Thus:

```text
CMS → dynamic workflow over static job definitions
DIRAC → static workflow template generating dynamic jobs
```

This analogy serves as a **useful conceptual aid**, but it should be interpreted as an illustration rather than a strict formal equivalence.

---

# Implications for Workflow Translation

This difference has direct implications for interoperability.

Because the CMS system resolves workflows **before execution**, while DIRAC resolves workflows **during execution**, a translation between the two systems cannot simply map objects one-to-one.

Instead, a translation layer must represent:

```text
• workflow structure
• dataset interaction model
• job generation semantics
```

independently of the execution framework.

This requirement is one of the primary motivations for the **Translation IR** introduced in the CMSDiracAux project.

---

# Static vs Dynamic Workflow–Data Interaction Models

```text
                STATIC WORKFLOW PARTITIONING
                   (CMS WMCore / WMBS)


        Workflow Definition (WMWorkload / TaskChain)
                           │
                           │
                           ▼
                ┌───────────────────────┐
                │     Workflow Graph    │
                │   fully defined       │
                └──────────┬────────────┘
                           │
                           ▼
                ┌───────────────────────┐
                │    WMBS Splitting     │
                │                       │
                │  Pre-compute job      │
                │  boundaries over      │
                │  dataset              │
                └──────────┬────────────┘
                           │
                           ▼
                ┌───────────────────────┐
                │      Job Creation     │
                │                       │
                │  Explicit job list    │
                │  generated centrally  │
                └──────────┬────────────┘
                           │
                           ▼
                    Runtime Execution


        Dataset Structure
        dataset → block → file
                │
                ▼
        Workflow distributed
        over dataset partitions



-----------------------------------------------------------------------



                DYNAMIC WORKLOAD EXPANSION
                         (DIRAC)


        Workflow Template (Transformation)
                           │
                           │
                           ▼
                ┌───────────────────────┐
                │     Transformation    │
                │      definition       │
                │                       │
                │  job template         │
                │  splitting rules      │
                └──────────┬────────────┘
                           │
                           ▼
                ┌───────────────────────┐
                │  Transformation Agent │
                │                       │
                │  monitors available   │
                │  input data           │
                └──────────┬────────────┘
                           │
                           ▼
                ┌───────────────────────┐
                │   Dynamic Job Spawn   │
                │                       │
                │  jobs created when    │
                │  data is discovered   │
                └──────────┬────────────┘
                           │
                           ▼
                    Runtime Execution


        Incoming Data
             │
             ▼
        Jobs generated
        from data availability
```

---

### CMS model

```text
workflow → job set → runtime
```

The workflow is **expanded into explicit jobs before execution**.

Data is treated as a **space over which the workflow is distributed**.

---

### DIRAC model

```text
workflow template → dynamic job generation
```

The workflow remains a **template**, and jobs are **spawned dynamically from data**.

---

# WMBS necessity argument

Here is yet another place to mention why WMBS Exists, even though already explained in other sections of the report.

The CMS workflow system requires job splitting at a much finer
granularity than the storage hierarchy used for dataset management.

While datasets and files represent the storage organization of CMS data,
job boundaries are often defined using run, luminosity section,
or event counts.

This requirement necessitates an additional bookkeeping layer that
tracks the association between jobs and data units.

The Workload Management Bookkeeping System (WMBS) fulfills this role.

---

# DIRACX outlook

**DIRACX Perspective**

The DIRACX architecture introduces explicit workflow and task
abstractions that are conceptually closer to the CMS workflow model.

Classic DIRAC represents workflows using productions and transformations,
while DIRACX moves toward a workflow → task → job hierarchy.

This convergence reduces the conceptual distance between the CMS
workflow model and DIRAC execution infrastructure, which strengthens
the relevance of the Translation IR approach proposed in this work.

---

# Conceptual Interpretation

The diagram highlights where **dynamism resides in each system**.

| System     | Dynamic element                       |
| ---------- | ------------------------------------- |
| CMS WMCore | workflow state over dataset           |
| DIRAC      | job generation from workflow template |

This explains why **direct translation between the systems is difficult**.

The CMSDiracAux project therefore introduces a **Translation IR** that separates:

```text
workflow semantics
data distribution semantics
execution system semantics
```


---

# IR Layer placement

```
┌──────────────────────────────────────────────────────────────┐
│                        CMS Ecosystem                         │
│                                                              │
│                  WMCore Workflow Definitions                 │
│                                                              │
│      WMWorkload / TaskChain / StepChain JSON requests        │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                   Workflow Acquisition Layer                 │
│                                                              │
│                         wmcGet.py                            │
│                                                              │
│   Extract workflow definitions from WMCore request manager   │
│   Serialize workflow request objects                         │
│                                                              │
│                 Output → WMCore.fetched.d                    │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                       Translation Layer                      │
│                                                              │
│                         wmc2transf.py                        │
│                                                              │
│   Build canonical workflow representation                    │
│                                                              │
│                    Canonical Translation IR                  │
│                                                              │
│   Workflow                                                   │
│     ├── Tasks                                                │
│     │     ├── RuntimeDefinition                              │
│     │     ├── SplittingPolicy                                │
│     │     └── DataReference                                  │
│     │                                                        │
│     └── Dependency Graph                                     │
│                                                              │
│   Dataset discovery via DAS / dasgoclient                    │
└───────────────┬───────────────────────────────┬──────────────┘
                │                               │
                ▼                               ▼
┌──────────────────────────────┐      ┌──────────────────────────────┐
│     DIRAC Materialization    │      │          CWL Export          │
│                              │      │                              │
│  Construct DIRAC Transform   │      │          transf2cwl.py       │
│                              │      │                              │
│  CMSWMCoreSplittingPlugin    │      │  Convert Translation IR      │
│  (local simulation)          │      │  into CWL workflow           │
│                              │      │                              │
│      Output → DIRAC.transf.d │      │      Output → DIRAC.cwl.d    │
└───────────────┬──────────────┘      └───────────────┬──────────────┘
                │                                     │
                ▼                                     ▼
┌──────────────────────────────────────────────────────────────┐
│                        Execution Layer                       │
│                                                              │
│                         DIRAC Runtime                        │
│                                                              │
│                     dirac-jobexec                            │
│                                                              │
│                jobDescription.xml execution                  │
└──────────────────────────────────────────────────────────────┘
```
