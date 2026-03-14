# CMS Workflow Management System Architecture

## Purpose of this section

The CMS Workflow Management System provides the infrastructure used to define, orchestrate, and execute large-scale data processing workflows across the distributed computing resources of the Worldwide LHC Computing Grid.

The CMS workflow system is designed to support complex multi-stage data processing campaigns, including:

* detector data reconstruction
* Monte Carlo simulation
* data reprocessing
* analysis data preparation

Unlike the DIRAC workflow architecture, which emphasizes dynamic job generation driven by available data, the CMS workflow management system relies on **explicit workflow descriptions and predefined job splitting strategies**.

Understanding the CMS workflow architecture is essential for evaluating how CMS workflows can be translated into DIRAC-compatible execution models.

---

# Overview of CMS Workflow Architecture

The CMS workflow management architecture is composed of several subsystems that together transform workflow definitions into distributed jobs.

At a high level the system can be represented as:

```text id="b1j8th"
┌──────────────────────────────────────────────┐
│      CMS Workflow Definition Layer           │
│       (Request / Workflow specification)     │
└───────────────────────────┬──────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────┐
│            WMCore Framework                  │
│     (workflow description and orchestration) │
└───────────────────────────┬──────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────┐
│     WMBS (Workload Management Bookkeeping)   │
│      job generation and data bookkeeping     │
└───────────────────────────┬──────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────┐
│        Submission Infrastructure (SI)        │
│    job submission to distributed resources   │
└───────────────────────────┬──────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────┐
│       Distributed Computing Resources        │
│       (Grid / Cloud / HPC infrastructure)    │
└──────────────────────────────────────────────┘
```

Each layer progressively converts the workflow definition into executable jobs.

---

# Workflow Definition Layer

CMS workflows begin as **workflow requests** describing the processing to be performed.

These requests define:

* input datasets
* processing steps
* software configuration
* output datasets
* resource requirements

Conceptually:

```text id="fr8z91"
┌──────────────────────────────┐
│      Workflow Request        │
│                              │
│  input dataset               │
│  processing steps            │
│  CMSSW configuration         │
│  output datasets             │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       Workflow Object        │
│  internal WMCore structure   │
└──────────────────────────────┘
```

These workflow definitions are typically created and managed through CMS request management systems.

---

# WMCore Framework

The **WMCore framework** provides the internal data structures and software components used to represent and manage CMS workflows.

WMCore defines:

* workflow objects
* task hierarchies
* data dependencies
* execution parameters

Conceptually a workflow is represented as a tree of tasks:

```text id="qps6b9"
┌──────────────────────────┐
│       Workflow           │
└─────────────┬────────────┘
              │
              ▼
     ┌─────────────────┐
     │      Task       │
     │ (processing)    │
     └──────┬──────────┘
            │
            ▼
     ┌─────────────────┐
     │   Subtask       │
     │ (optional)      │
     └──────┬──────────┘
            │
            ▼
     ┌─────────────────┐
     │   Processing    │
     │   Step          │
     └─────────────────┘
```

Tasks represent logical processing stages applied to input datasets.

---

# Workflow Task Structure

Each task within a CMS workflow defines the processing applied to a subset of data.

Tasks specify:

* input dataset
* processing configuration
* splitting policy
* resource requirements

Example task structure:

```text id="ct0zj1"
┌─────────────────────────────┐
│ Task                        │
│                             │
│ Input dataset               │
│ CMSSW configuration         │
│ Splitting policy            │
│ Output dataset              │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Job definitions generated   │
│ by splitting algorithms     │
└─────────────────────────────┘
```

Tasks are therefore the primary abstraction used to represent workflow processing steps.

---

# WMBS: Job Generation and Bookkeeping

The **Workload Management Bookkeeping System (WMBS)** is responsible for generating jobs and tracking the association between jobs and data.

WMBS performs several key functions:

* dataset resolution
* file discovery
* job splitting
* job bookkeeping
* workflow progress tracking

Conceptually:

```text id="xb5z9a"
┌──────────────────────────────┐
│ Workflow Task                │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Dataset discovery            │
│ (DAS queries)                │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ File resolution              │
│ dataset → files              │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Job splitting                │
│ run / lumi / event policies  │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Job definitions              │
│ recorded in WMBS             │
└──────────────────────────────┘
```

WMBS maintains the mapping between:

```
workflow tasks
      ↓
jobs
      ↓
data units
```

This bookkeeping is critical for large-scale workflow execution.

---

# Splitting and Workload Partitioning

CMS workflows typically partition data using **splitting algorithms**.

These algorithms define how data are divided into jobs.

Typical splitting modes include:

* FileBased
* RunBased
* LumiBased
* EventAware

Conceptually:

```text id="p16ayk"
Input dataset
      │
      ▼
┌───────────────────────┐
│ Splitting algorithm   │
│ (run/lumi/event)      │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Job definitions       │
│ each processes data   │
└───────────────────────┘
```

These splitting strategies allow workflows to maintain predictable job runtimes despite heterogeneous data content.

---

# Job Submission Infrastructure

Once jobs are generated by WMBS, they are submitted to distributed computing resources.

```text id="sy0fdi"
┌──────────────────────────┐
│ Generated Jobs           │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│ Submission Infrastructure│
│ (grid job submission)    │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│ Distributed Worker Nodes │
└──────────────────────────┘
```

Jobs execute within the CMS runtime environment, typically provided through CVMFS.

---

# CMS Workflow Abstraction Levels

The CMS workflow management system operates across several abstraction levels.

| Layer            | Workflow abstraction     |
| ---------------- | ------------------------ |
| Workflow request | full processing campaign |
| Workflow         | structured set of tasks  |
| Task             | processing step          |
| Job              | executable workload unit |

Conceptually:

```text id="u0k0h0"
Processing campaign
        ↓
Workflow
        ↓
Tasks
        ↓
Jobs
```

These abstractions allow CMS workflows to manage large processing campaigns consisting of millions of jobs.

---

# Architectural Characteristics

Several characteristics distinguish the CMS workflow architecture:

* workflows are **explicitly defined before execution**
* job boundaries are **determined by splitting algorithms**
* bookkeeping tracks job-data relationships
* workflow state is maintained centrally

This architecture provides strong control over workflow execution and data processing.

---

# Relationship to DIRAC Workflow Systems

The CMS workflow architecture differs from the DIRAC workflow stack.

Conceptually:

```text id="h7sj1e"
CMS workflow architecture

Workflow
   ↓
Task
   ↓
WMBS splitting
   ↓
Jobs
```

versus

```text id="o0uwm4"
DIRAC workflow architecture

Production
   ↓
Transformation
   ↓
WMS scheduling
   ↓
Jobs
```

These differences explain why CMS workflows cannot be directly expressed using DIRAC workflow constructs.

---

# Implications for CMSDiracAux

The CMSDiracAux project introduces an intermediate abstraction layer that bridges the CMS workflow system and the DIRAC execution model.

Conceptually:

```text id="qydfzc"
CMS workflow (WMCore)
        │
        ▼
Translation IR
        │
        ▼
DIRAC workflow systems
(production / transformation / WMS)
```

This translation layer preserves workflow semantics while enabling execution within the DIRAC infrastructure.

---
# Detailed architecture

```text
                     CMS Workflow Management System
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  CENTRAL SERVICES                                                            │
│                                                                              │
│  ┌──────────────────────┐   ┌──────────────────────┐   ┌──────────────────┐  │
│  │ Request / ReqMgr     │   │ DBS / DAS            │   │ CouchDB /        │  │
│  │ workflow definition  │   │ data discovery       │   │ workflow state   │  │
│  └──────────┬───────────┘   └──────────┬───────────┘   └────────┬─────────┘  │
│             │                          │                        │            │
│             └───────────────┬──────────┴──────────┬─────────────┘            │
│                             │                     │                          │
│                             ▼                     ▼                          │
│                     ┌──────────────────────────────────────┐                 │
│                     │          WorkQueue Service           │                 │
│                     │   workflow / task distribution       │                 │
│                     └──────────────────┬───────────────────┘                 │
│                                        │                                     │
│                                        ▼                                     │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │ AGENTS                                                                 │  │
│  │                                                                        │  │
│  │  ┌──────────────────────┐      ┌──────────────────────┐                │  │
│  │  │ WMAgent              │      │ Auxiliary Agents     │                │  │
│  │  │                      │      │ monitoring / cleanup │                │  │
│  │  │  ┌────────────────┐  │      │ retries / state sync │                │  │
│  │  │  │ WMBS           │  │      └──────────────────────┘                │  │
│  │  │  │ bookkeeping    │  │                                              │  │
│  │  │  │ + splitting    │  │                                              │  │
│  │  │  └───────┬────────┘  │                                              │  │
│  │  │          │           │                                              │  │
│  │  │          ▼           │                                              │  │
│  │  │  ┌────────────────┐  │                                              │  │
│  │  │  │ Job creation   │  │                                              │  │
│  │  │  │ run/lumi/file  │  │                                              │  │
│  │  │  └───────┬────────┘  │                                              │  │
│  │  │          │           │                                              │  │
│  │  │          ▼           │                                              │  │
│  │  │  ┌────────────────┐  │                                              │  │
│  │  │  │ Job packaging  │  │                                              │  │
│  │  │  │ + submission   │  │                                              │  │
│  │  │  └───────┬────────┘  │                                              │  │
│  │  └──────────┼───────────┘                                              │  │
│  │             │                                                          │  │
│  └─────────────┼──────────────────────────────────────────────────────────┘  │
│                │                                                             │
│                ▼                                                             │
│        ┌──────────────────────┐                                              │
│        │ Submission           │                                              │
│        │ Infrastructure       │                                              │
│        │ grid / batch / condor│                                              │
│        └──────────┬───────────┘                                              │
│                   │                                                          │
│                   ▼                                                          │
│        ┌──────────────────────┐                                              │
│        │ Worker Nodes         │                                              │
│        │ CMS jobs execute     │                                              │
│        └──────────────────────┘                                              │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

# Summary

The CMS Workflow Management System provides a structured architecture for defining and executing large distributed workflows across the CMS computing infrastructure.

Key architectural components include:

* workflow definitions
* WMCore workflow objects
* WMBS job generation and bookkeeping
* distributed job submission

These components collectively transform high-level workflow requests into millions of distributed jobs executed across grid resources.

Understanding this architecture is essential for designing interoperability mechanisms such as the Translation IR used in the CMSDiracAux project.
