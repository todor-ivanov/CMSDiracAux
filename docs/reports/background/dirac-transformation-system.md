# DIRAC Transformation System

## Purpose of this section

The DIRAC Transformation System provides a framework for executing large-scale distributed workloads across heterogeneous computing resources.

Unlike the CMS workflow system, which constructs jobs based on predefined splitting of datasets, the DIRAC Transformation System operates using **dynamic job generation driven by available input data**.

Understanding the DIRAC Transformation System is essential for evaluating how CMS workflows can be executed within a DIRAC-based infrastructure.

---

# DIRAC Architecture Context

DIRAC (Distributed Infrastructure with Remote Agent Control) is a distributed computing framework originally developed by the LHCb experiment and later adopted by other experiments and communities.

DIRAC provides services for:

* workload management
* data management
* distributed resource integration
* pilot-based job execution

Within the workload management layer, the **Transformation System** is responsible for orchestrating large production campaigns.

---

# Concept of Transformations

A **transformation** in DIRAC represents a high-level description of a processing task that must be executed over a set of input data.

Conceptually:

```
┌───────────────────────────┐
│        Transformation     │
│   (processing definition) │
└──────────────┬────────────┘
               │
               ▼
┌───────────────────────────┐
│      Input Data Query     │
│  (dataset / file query)   │
└──────────────┬────────────┘
               │
               ▼
┌───────────────────────────┐
│         File List         │
│  (LFNs discovered)        │
└──────────────┬────────────┘
               │
               ▼
┌───────────────────────────┐
│      Job Generation       │
│  (tasks created)          │
└───────────────────────────┘
```

The transformation defines:

* the executable application
* input data selection
* job parameters
* output data handling

Jobs are then generated dynamically based on the discovered input data.

---

# Transformation Lifecycle

The lifecycle of a DIRAC transformation typically follows the sequence below.

```
┌───────────────────────────┐
│ Transformation Definition │
│  (workflow description)   │
└──────────────┬────────────┘
               │
               ▼
┌───────────────────────────┐
│   Input Data Discovery    │
│ (File Catalog queries)    │
└──────────────┬────────────┘
               │
               ▼
┌───────────────────────────┐
│      Task Generation      │
│ (internal transformation) │
└──────────────┬────────────┘
               │
               ▼
┌───────────────────────────┐
│        Job Creation       │
│  (payload definitions)    │
└──────────────┬────────────┘
               │
               ▼
┌───────────────────────────┐
│      Distributed Jobs     │
│ executed via pilot jobs   │
└───────────────────────────┘
```

Each transformation therefore results in **large numbers of jobs** executed across distributed computing sites.

---

# Data-Driven Job Generation

A defining property of the DIRAC Transformation System is that job generation is **driven by available input data**.

```
┌─────────────────────────┐
│   Input Data Appears    │
│   (files in catalog)    │
└─────────────┬───────────┘
              │
              ▼
┌─────────────────────────┐
│ Transformation Evaluator│
│  scans available files  │
└─────────────┬───────────┘
              │
              ▼
┌─────────────────────────┐
│     Job Generation      │
│ create tasks per file   │
└─────────────┬───────────┘
              │
              ▼
┌─────────────────────────┐
│ Jobs submitted to DIRAC │
│ pilot execution system  │
└─────────────────────────┘
```

This dynamic behaviour contrasts with workflow systems that precompute all jobs before execution.

---

# File-Level Processing Model

DIRAC transformations generally operate on **file-level input units**.

Typical mapping between files and jobs:

```
┌──────────────┐
│  File A      │
└──────┬───────┘
       ▼
   ┌────────┐
   │ Job 1  │
   └────────┘

┌──────────────┐
│  File B      │
└──────┬───────┘
       ▼
   ┌────────┐
   │ Job 2  │
   └────────┘

┌──────────────┐
│  File C      │
└──────┬───────┘
       ▼
   ┌────────┐
   │ Job 3  │
   └────────┘
```

This model assumes that files represent reasonable units of work.

However, it implicitly assumes **uniform file workloads**, which is not always true for CMS data.

---

# Pilot Job Execution Model

DIRAC employs a **pilot job model** for workload execution.

```
┌──────────────────────────┐
│   Pilot Job Submitted    │
│   to computing site      │
└──────────────┬───────────┘
               │
               ▼
┌──────────────────────────┐
│  Pilot Starts on Worker  │
│        Node              │
└──────────────┬───────────┘
               │
               ▼
┌──────────────────────────┐
│ Pilot Contacts DIRAC     │
│ Central Services         │
└──────────────┬───────────┘
               │
               ▼
┌──────────────────────────┐
│ Payload Job Retrieved    │
│ from job queue           │
└──────────────┬───────────┘
               │
               ▼
┌──────────────────────────┐
│      Job Execution       │
│ within pilot environment │
└──────────────────────────┘
```

This mechanism improves resource utilization by separating **resource acquisition** from **job scheduling**.

---

# Job Execution Description

Jobs executed by DIRAC are typically described using the **Job Description Language (JDL)**.

The JDL specifies:

* executable
* runtime arguments
* input sandbox
* output sandbox
* environment configuration

The actual execution workflow may also be described using:

```
jobDescription.xml
```

which defines the internal job workflow executed by the worker node.

---

# Transformation Plugins

The Transformation System supports **plugins** responsible for defining how input data is partitioned into jobs.

Conceptually:

```
┌───────────────────────────┐
│ Transformation Definition │
└──────────────┬────────────┘
               │
               ▼
┌───────────────────────────┐
│  Splitting Plugin         │
│ (job generation policy)   │
└──────────────┬────────────┘
               │
               ▼
┌───────────────────────────┐
│ Jobs Created              │
│ according to plugin logic │
└───────────────────────────┘
```

These plugins determine:

* job granularity
* data partitioning
* runtime parameterization

The plugin architecture is particularly relevant for implementing CMS-specific splitting logic.

---

# Comparison with CMS Workflow Execution

The DIRAC Transformation System differs fundamentally from the CMS workflow model.

| Property              | CMS WMCore                             | DIRAC                              |
| --------------------- | -------------------------------------- | ---------------------------------- |
| Job generation        | predefined during workflow preparation | dynamic based on data availability |
| Data abstraction      | dataset oriented                       | file oriented                      |
| Splitting granularity | run / lumi / event possible            | typically file level               |
| Bookkeeping           | WMBS                                   | transformation tasks               |

---

# Implications for CMSDiracAux

The CMSDiracAux project introduces a **Translation IR** that bridges the conceptual gap between the CMS workflow model and the DIRAC Transformation System.

The translation process can be summarized as:

```
┌──────────────────────┐
│    WMCore Workflow   │
└───────────┬──────────┘
            │
            ▼
┌──────────────────────┐
│     Translation IR   │
│ workflow abstraction │
└───────────┬──────────┘
            │
            ▼
┌──────────────────────┐
│ DIRAC Transformation │
│ executed via pilots  │
└──────────────────────┘
```

This architecture allows CMS workflows to be executed within DIRAC while preserving workflow semantics.

---

# Summary

The DIRAC Transformation System provides a flexible infrastructure for executing large-scale distributed workloads through **dynamic job generation and pilot-based execution**.

However, its **file-oriented processing model** differs from the fine-grained data abstractions used in CMS workflows.

Bridging this difference requires an intermediate abstraction layer, implemented in CMSDiracAux as the **Translation IR**.
