# Architectural Comparison: CMS Workflow System, DIRAC, and DIRACX

## Purpose

This section compares the architectural organization of three workflow execution models:

* the **CMS Workflow Management System (WMCore)**
* the **classic DIRAC workflow stack**
* the **DIRACX architecture**

The comparison focuses on how each system transforms **workflow descriptions into executable jobs** and how the abstraction layers differ.

Understanding these differences is important for evaluating the design of interoperability layers such as the **Translation IR introduced in the CMSDiracAux project**.

---

# Workflow Architecture Comparison

The diagram below illustrates the conceptual workflow pipeline implemented by each system.

```text
┌────────────────────────────────────┬────────────────────────────────────┬────────────────────────────────────┐
│           CMS WMCore               │            DIRAC (classic)         │               DIRACX               │
├────────────────────────────────────┼────────────────────────────────────┼────────────────────────────────────┤
│                                    │                                    │                                    │
│   WORKFLOW DEFINITION              │   PRODUCTION SYSTEM                │   WORKFLOW SERVICES                │
│   (request / workflow object)      │   (processing campaigns)           │   (workflow APIs)                  │
│                                    │                                    │                                    │
│            │                       │            │                       │            │                       │
│            ▼                       │            ▼                       │            ▼                       │
│   TASK STRUCTURE                   │   TRANSFORMATION SYSTEM            │   TASK SERVICES                    │
│   (task tree / processing steps)   │   (data-driven job generation)     │   (workflow task graph)            │
│                                    │                                    │                                    │
│            │                       │            │                       │            │                       │
│            ▼                       │            ▼                       │            ▼                       │
│   WMBS                              │   WORKLOAD MANAGEMENT SYSTEM       │   SCHEDULING SERVICES             │
│   (dataset discovery               │   (job queues / matching)          │   (resource matchmaking)           │
│    + splitting + bookkeeping)      │                                    │                                    │
│                                    │                                    │                                    │
│            │                       │            │                       │            │                       │
│            ▼                       │            ▼                       │            ▼                       │
│   JOB GENERATION                   │   PILOT DIRECTORS                  │   PILOT SERVICES                   │
│   (run/lumi/event jobs)            │   (pilot submission)               │   (pilot orchestration)            │
│                                    │                                    │                                    │
│            │                       │            │                       │            │                       │
│            ▼                       │            ▼                       │            ▼                       │
│   SUBMISSION INFRASTRUCTURE        │   PILOT INFRASTRUCTURE             │   EXECUTION PLANE                  │
│   (grid / batch systems)           │   (grid / batch)                   │   (grid / cloud / HPC)             │
│                                    │                                    │                                    │
│            │                       │            │                       │            │                       │
│            ▼                       │            ▼                       │            ▼                       │
│   WORKER NODES                     │   WORKER NODES                     │   WORKER NODES                     │
│   (CMS payload jobs)               │   (pilot executes payload)         │   (pilot executes payload)         │
│                                    │                                    │                                    │
└────────────────────────────────────┴────────────────────────────────────┴────────────────────────────────────┘
```

Each column represents a complete workflow processing stack from workflow definition to execution.

---

# Workflow Abstraction Layers


```
Abstraction Layers

CMS WMCore        : Workflow → Tasks → Jobs
DIRAC (classic)   : Production → Transformation → Jobs
DIRACX            : Workflow → Tasks → Jobs
```

```
Scheduling Model

CMS WMCore        : push scheduling
DIRAC (classic)   : pilot pull scheduling
DIRACX            : pilot pull scheduling (decoupled services)
```

```
Data Granularity

CMS WMCore        : dataset → run → lumi → event
DIRAC (classic)   : file-oriented processing
DIRACX            : file-oriented (but workflow abstractions available)
```

```
Key Structural Difference

CMS
workflow semantics defined BEFORE execution

DIRAC
jobs generated dynamically from data

DIRACX
workflow services define tasks,
but execution remains pilot-driven
```

The three systems organize workflow abstractions differently.

```text
CMS WMCore
Workflow
   ↓
Tasks
   ↓
Jobs


DIRAC (classic)
Production
   ↓
Transformation
   ↓
Jobs


DIRACX
Workflow
   ↓
Tasks
   ↓
Jobs
```

The CMS and DIRACX models expose workflow tasks explicitly, whereas classic DIRAC expresses workflows through production and transformation constructs.

---

# Scheduling Model

The systems also differ in how jobs are scheduled and dispatched.

```text
CMS WMCore        : push scheduling
DIRAC (classic)   : pilot pull scheduling
DIRACX            : pilot pull scheduling with decoupled scheduling services
```

In the CMS system, jobs are generated and submitted explicitly to computing resources.
In DIRAC systems, resources obtain work dynamically through pilot jobs that pull workloads from the central system.

---

# Data Processing Granularity

Another important difference concerns the granularity of workload partitioning.

```text
CMS WMCore        : dataset → run → lumi → event
DIRAC (classic)   : file-oriented processing
DIRACX            : file-oriented execution with higher-level workflow abstractions
```

CMS workflows frequently operate on data partitions defined by **run, luminosity section, or event counts**, whereas DIRAC typically partitions workloads at the **file level**.

---

# Structural Differences

The key architectural distinction between the systems lies in how workflows are defined relative to execution.

```text
CMS workflow system
workflow semantics defined before execution


DIRAC (classic)
jobs generated dynamically from input data


DIRACX
workflow services define tasks,
while execution remains pilot-driven
```

This difference reflects two different workflow philosophies:

* **CMS:** workflows are explicitly defined and decomposed into jobs before execution.
* **DIRAC:** jobs are generated dynamically as data becomes available.

---

# Relevance for CMSDiracAux

The CMSDiracAux project introduces a **Translation IR** that bridges the conceptual gap between these architectures.

Conceptually:

```text
CMS Workflow (WMCore)
        │
        ▼
Translation IR
        │
        ▼
DIRAC workflow stack
(production / transformation / WMS)
```

This intermediate abstraction allows workflows defined in the CMS system to be expressed in terms compatible with the DIRAC execution infrastructure.

---

# Summary

The CMS workflow system, classic DIRAC, and DIRACX represent three distinct approaches to distributed workflow execution:

* CMS emphasizes **explicit workflow definition and fine-grained data partitioning**.
* Classic DIRAC focuses on **dynamic job generation and pilot-based scheduling**.
* DIRACX introduces **modern workflow abstractions and service-oriented architecture**, while retaining pilot-based execution.

Understanding these architectural differences is essential for designing interoperability mechanisms between the two systems.





































```text
                         Workflow System Architectures (Conceptual Comparison)

┌────────────────────────────────────┬────────────────────────────────────┬────────────────────────────────────┐
│           CMS WMCore               │            DIRAC (classic)         │               DIRACX               │
├────────────────────────────────────┼────────────────────────────────────┼────────────────────────────────────┤
│                                    │                                    │                                    │
│   WORKFLOW DEFINITION              │   PRODUCTION SYSTEM                │   WORKFLOW SERVICES                │
│   (Request / Workflow object)      │   (processing campaigns)           │   (workflow APIs)                  │
│                                    │                                    │                                    │
│            │                       │            │                       │            │                       │
│            ▼                       │            ▼                       │            ▼                       │
│   TASK STRUCTURE                   │   TRANSFORMATION SYSTEM            │   TASK SERVICES                    │
│   (task tree / processing steps)   │   (data-driven job generation)     │   (workflow task graph)            │
│                                    │                                    │                                    │
│            │                       │            │                       │            │                       │
│            ▼                       │            ▼                       │            ▼                       │
│   WMBS                              │   WORKLOAD MANAGEMENT SYSTEM       │   SCHEDULING SERVICES              │
│   (dataset discovery               │   (job queues / matching)          │   (resource matchmaking)           │
│    + splitting + bookkeeping)      │                                    │                                    │
│                                    │                                    │                                    │
│            │                       │            │                       │            │                       │
│            ▼                       │            ▼                       │            ▼                       │
│   JOB GENERATION                   │   PILOT DIRECTORS                  │   PILOT SERVICES                   │
│   (run/lumi/event jobs)            │   (pilot submission)               │   (pilot orchestration)            │
│                                    │                                    │                                    │
│            │                       │            │                       │            │                       │
│            ▼                       │            ▼                       │            ▼                       │
│   SUBMISSION INFRASTRUCTURE        │   PILOT INFRASTRUCTURE             │   EXECUTION PLANE                  │
│   (grid / batch systems)           │   (grid / batch)                   │   (grid / cloud / HPC)             │
│                                    │                                    │                                    │
│            │                       │            │                       │            │                       │
│            ▼                       │            ▼                       │            ▼                       │
│   WORKER NODES                     │   WORKER NODES                     │   WORKER NODES                     │
│   (CMS payload jobs)               │   (pilot executes payload)         │   (pilot executes payload)         │
│                                    │                                    │                                    │
└────────────────────────────────────┴────────────────────────────────────┴────────────────────────────────────┘
```
