# System Architecture

## Overview

This document describes the overall architecture of the WMCore → DIRAC
interoperability proof of concept implemented in CMSDiracAux.

The architecture bridges two different workflow systems:

WMCore (CMS workflow management)

and

DIRAC (distributed workload management).

The CMSDiracAux project demonstrates how workflows defined in the CMS workflow management system (WMCore) can be translated into execution structures compatible with the DIRAC distributed computing framework.

The architecture introduced by CMSDiracAux separates the workflow description from the execution infrastructure by introducing a **canonical Translation Intermediate Representation (IR)**. This allows CMS workflow semantics to be preserved while enabling execution within a different distributed workload management system.

The overall architecture therefore consists of several layers:

```
CMS Workflow Definition
        │
        ▼
Translation Layer (CMSDiracAux)
        │
        ▼
DIRAC Execution Infrastructure
        │
        ▼
Worker Node Runtime Environment
```


Each layer serves a different purpose and represents a different abstraction level in the workflow execution pipeline.

---

# Architectural Layers

The CMSDiracAux architecture can be divided into four major layers.

```
┌───────────────────────────────────────────┐
│ CMS Workflow Management                   │
│ (WMCore Central Services)                 │
└───────────────────────────┬───────────────┘
                            │
                            ▼
┌───────────────────────────────────────────┐
│ CMSDiracAux Translation Layer             │
│ (Translation IR)                          │
└───────────────────────────┬───────────────┘
                            │
                            ▼
┌───────────────────────────────────────────┐
│ DIRAC Execution Infrastructure            │
│ (Transformation + WMS)                    │
└───────────────────────────┬───────────────┘
                            │
                            ▼
┌───────────────────────────────────────────┐
│ Worker Node Runtime                       │
│ (CMSSW / cmsRun execution)                │
└───────────────────────────────────────────┘
```

Each layer is described in detail below.

---

# CMS Workflow Management Layer

The first layer of the architecture is the CMS workflow management system.

In CMS, workflows are defined and managed by **WMCore**, which orchestrates the entire data processing pipeline for CMS computing tasks.

A CMS workflow typically consists of:

```
Workflow
   │
   ▼
Tasks
   │
   ▼
Splitting rules
   │
   ▼
Jobs
```

This model emphasizes **explicit workflow definition** before execution.

A CMS workflow definition includes:

* processing steps
* input datasets
* splitting policies
* runtime parameters
* job configuration templates.

The splitting policies determine how a dataset is divided into units of work that can be processed independently.

The CMS data hierarchy underlying this process is:

```
Dataset
   │
   ▼
Block
   │
   ▼
File
   │
   ▼
Run
   │
   ▼
Luminosity section
```

The important aspect of this hierarchy is that CMS jobs often operate on **run or luminosity section ranges**, rather than directly on files.

This means that the storage hierarchy alone does not uniquely determine job boundaries.

To maintain the relationship between workflow tasks, data partitions, and jobs, CMS relies on the **Workload Management Bookkeeping System (WMBS)**.

WMBS stores the association:

```
Workflow task
      │
      ▼
Run / Lumi partitions
      │
      ▼
Job definitions
```

This bookkeeping layer ensures that each job processes the correct portion of the dataset.

---

# CMSDiracAux Translation Layer

The central component of the CMSDiracAux architecture is the **translation layer**.

This layer extracts workflow information from WMCore and converts it into a canonical representation that can later be materialized into DIRAC execution structures.

The translation pipeline can be summarized as:

```
WMCore Workflow
      │
      ▼
Workflow Extraction
      │
      ▼
Canonical Translation IR
      │
      ▼
DIRAC Materialization
```

The canonical Translation IR acts as the semantic bridge between the two systems.

The purpose of the IR is to decouple:

```
CMS workflow semantics
        from
DIRAC execution infrastructure
```

Without this layer, the translation would require a direct one-to-one mapping between WMCore objects and DIRAC objects, which is difficult because the two systems follow different architectural philosophies.

---

# Canonical Translation IR

The Translation IR provides structured objects representing the essential components of a workflow.

```
┌─────────────────────────────┐
│ CanonicalWorkflow           │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ CanonicalTasks              │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ CanonicalSplitting          │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ CanonicalProduction         │
└─────────────────────────────┘
```

These objects capture the essential workflow semantics:

* task hierarchy
* splitting rules
* dataset relationships
* resource hints
* executable definitions.

The IR therefore becomes the **canonical description of the workflow independent of execution infrastructure**.

---

# DIRAC Execution Infrastructure

Once the workflow has been translated into the IR, it can be materialized into structures understood by DIRAC.

The primary mechanism for large-scale processing in DIRAC is the **Transformation System**.

A DIRAC transformation is responsible for generating jobs based on data inputs and defined processing rules.

```
Transformation
      │
      ▼
Task queues
      │
      ▼
Jobs
```

In the CMSDiracAux architecture, CMS-specific splitting behavior must be implemented inside a transformation plugin.

```
Transformation
      │
      ▼
CMS Splitting Plugin
      │
      ▼
Job Definitions
```

This plugin effectively reproduces WMBS functionality within the DIRAC environment.

This is necessary because CMS workflows require splitting at a granularity that is finer than the storage abstraction used by DIRAC.

---

# DIRAC Workload Management

Once jobs have been generated, they are handled by the DIRAC Workload Management System (WMS).

The WMS uses a **pilot-based scheduling model**.

```
Job Queue
     │
     ▼
Pilot Jobs
     │
     ▼
Worker Nodes
```

Pilots are generic worker agents that start on computing resources and request work from the central system.

This model improves reliability and resource utilization on heterogeneous distributed computing infrastructures.

---

# Worker Node Runtime Environment

When a job reaches a worker node, the runtime environment must be reconstructed before the CMS job can execute.

The runtime process typically follows these steps:

```
Worker Node
     │
     ▼
Bootstrap script
     │
     ▼
Runtime environment preparation
     │
     ▼
Job configuration reconstruction
     │
     ▼
cmsRun execution
```

The final processing is performed by the **CMSSW framework executable `cmsRun`**.

The behavior of `cmsRun` is determined entirely by its Python configuration (PSet).

```
cmsRun
   │
   ▼
Python configuration (PSet)
   │
   ▼
Processing pipeline
```

Each job therefore requires a configuration that reflects the dataset partition assigned to it.

---

# Runtime Environment Constraints

A CMS job depends on two different runtime domains.

```
        CMS Runtime Environment
               │
      ┌────────┴────────┐
      ▼                 ▼
 WMCore runtime      CMSSW framework
```

WMCore provides:

* workflow context
* job packages
* runtime parameters
* PSet tweaks.

CMSSW provides:

* physics algorithms
* framework libraries
* module execution environment.

Both layers must be available for successful job execution.

---

# Runtime Distribution Strategy

The architecture must also account for constraints in the DIRAC job sandbox model.

The input sandbox is intended to carry small files required for execution.

```
┌─────────────────────────────┐
│ Input Sandbox               │
│                             │
│ small scripts               │
│ configuration files         │
│ runtime parameters          │
└─────────────────────────────┘
```

Large runtime bundles are not suitable for sandbox transport.

CMSDiracAux therefore uses a bootstrap approach where the worker node reconstructs the runtime environment.

```
DIRAC Job
   │
   ▼
Bootstrap execution
   │
   ▼
Environment reconstruction
   │
   ▼
cmsRun
```

---

# Architectural Summary

The CMSDiracAux architecture provides a layered interoperability model.

```
CMS Workflow System
      │
      ▼
Translation IR
      │
      ▼
DIRAC Transformation
      │
      ▼
DIRAC WMS
      │
      ▼
Worker Node Runtime
      │
      ▼
cmsRun
```

This architecture preserves CMS workflow semantics while allowing execution within the DIRAC distributed computing framework.

The Translation IR serves as the key abstraction layer enabling this interoperability.

# Detailed view

```
                        CMSDiracAux Architecture Overview


        CMS Workflow System             CMSDiracAux        DIRAC Execution System
   ─────────────────────────────  ─────────────────────  ───────────────────────────


   ┌────────────────────────────┐
   │        ReqMgr / WMCore     │
   │                            │
   │  Workflow definition       │
   │  Task graph                │
   │  Splitting policies        │
   └─────────────┬──────────────┘
                 │
                 │ workflow extraction
                 ▼
                ┌──────────────────────────┐
                │  Workflow serialization  │
                │      (wmcGet.py)         │
                └─────────────┬────────────┘
                              │
                              ▼
                            ┌───────────────────────────────┐
                            │        Translation IR         │
                            │                               │
                            │  CanonicalWorkflow            │
                            │  CanonicalTasks               │
                            │  CanonicalSplitting           │
                            │  CanonicalDatasetRefs         │
                            └─────────────┬─────────────────┘
                                          │
                                          │ materialization
                                          ▼
                             ┌─────────────────────────────┐
                             │     DIRAC Transformation    │
                             │                             │
                             │  CMS Splitting Plugin       │
                             │  (WMBS logic reborn)        │
                             └───────────────────────┬─────┘
                                                     │
                                                     ▼
                                  ┌──────────────────────────────────────────┐
                                  │  +------------+   +-------------------+  │
                                  │  | GlideinWMS | + | DIRAC Workload    |  │
                                  │  | HTCondor   |   | Management System |  │
                                  │  +------------+   +-------------------+  │
                                  │                                          │
                                  │  Job queue                               │
                                  │  Pilot matching                          │
                                  └────────────────────┬─────────────────────┘
                                                       │
                                                       ▼
                                            ┌──────────────────────┐
                                            │     Worker Nodes     │
                                            │                      │
                                            │  runtime bootstrap   │
                                            │  cmsRun execution    │
                                            └──────────────────────┘
```
> **Figure:** Detailed CMSDiracAux Functional overview. The system extracts workflows from the CMS WMCore infrastructure and translates them into a canonical intermediate representation (Translation IR). The IR is then materialized into DIRAC transformations that reproduce CMS splitting semantics through dedicated plugins. Jobs are executed through the DIRAC workload management system while preserving CMS runtime behavior.

---

# Key Architectural Insight

One of the central conclusions of the CMSDiracAux architecture is that CMS-specific workload bookkeeping cannot be eliminated.

Even when workflows are executed through DIRAC, the system must maintain a mapping between jobs and the data content they process.

```
Workflow task
      │
      ▼
Data partitions
      │
      ▼
Jobs
```

This functionality, originally provided by WMBS, must therefore be implemented inside the DIRAC execution layer through CMS-aware transformation plugins.

---

This document forms the **central architectural description of the CMSDiracAux system** and should be read together with:

```
architecture-diagram.md
translation-ir-design.md
wmcore-dirac-mismatch.md
```
