# WMBS Splitting Model

## Purpose of this section

The CMS workflow management system includes a dedicated subsystem called **WMBS (Workload Management Bookkeeping System)** responsible for job generation and bookkeeping.

WMBS exists primarily because CMS workflows require **extremely fine-grained control over how workloads are distributed over data**.

Unlike many distributed computing systems that schedule work at the level of files or datasets, CMS workflows may split workloads at the level of:

* files
* runs
* luminosity sections
* events

This high-granularity splitting requires an explicit bookkeeping layer capable of associating **individual jobs with specific portions of the data content**.

---

# CMS Data Granularity

CMS data management separates **storage organization** from **physics content structure**.

### Storage hierarchy

```
Dataset
└─ Block
   ├─ File
   └─ File
```

### Physics content hierarchy

```
Run
└─ Lumi Section
   └─ Event
```

These hierarchies are orthogonal.

Files represent storage containers, while runs and luminosity sections represent the logical structure of recorded physics data.

Important structural properties:

```
Run ⊄ File
File ⊄ Run

Lumi ⊂ File
Event ⊂ Lumi
```

Consequently:

* runs may span multiple files
* files may contain events from multiple runs
* lumisections remain contained within files

This structural mismatch between storage units and physics units is the **primary reason CMS requires sophisticated splitting algorithms**.

---

# WMBS Role in Workflow Execution

WMBS is responsible for:

* associating workflows with datasets
* resolving datasets into file lists
* applying splitting algorithms
* generating job definitions
* tracking job–data associations

The workflow execution process in CMS can therefore be summarized as:

```
Workflow
   │
   ▼
Dataset discovery
   │
   ▼
File resolution
   │
   ▼
WMBS splitting
   │
   ▼
Job generation
```

The splitting stage determines the **runtime boundaries of each job**.

---

# Splitting Algorithms

CMS supports multiple splitting algorithms depending on the type of workload and the desired level of granularity.

Typical splitting modes include:

| Splitting mode | Description                      |
| -------------- | -------------------------------- |
| FileBased      | jobs process full files          |
| RunBased       | jobs process runs                |
| LumiBased      | jobs process luminosity sections |
| EventAware     | jobs process fixed event counts  |

These algorithms exist because **runs, lumisections and files are not aligned structures**.

For example:

* a run may span multiple files
* a file may contain events from multiple runs

Therefore splitting at the level of runs or lumisections requires **metadata inspection and bookkeeping beyond simple file lists**.

---

# Architectural Motivation for WMBS

The existence of WMBS is not merely an implementation choice.

It reflects a fundamental architectural property of CMS workflows: **workload scheduling must be tied to physics data granularity rather than storage containers**.

The following observation is therefore critical for understanding CMS workflow design.

> One of the reasons for WMBS existence at the first place is the fact that we have high granularity job splitting in CMS reaching as deep as data content (lumis/events) rather than only staying at data storage containers level (datasets/blocks/files), which means whatever central scheduling system we take we will still need to implement additional bookkeeping for associating jobs to data contents while distributing the workload over the data.
>
> This in the concept of CMSDiracAux would mean re-implementing WMBS functionalities in the plugin mechanisms for job splitting. WMBS itself, good or bad implemented as is currently would have to be reborn as long as we keep this level of granularity.

---

# Implications for CMSDiracAux

This architectural fact has direct implications for the CMSDiracAux project.

Even if CMS workflows are executed on top of DIRAC infrastructure, the system must still provide functionality equivalent to WMBS.

In particular:

* jobs must be associated with **specific lumisections or event ranges**
* splitting logic must preserve **deterministic mapping between jobs and data**
* bookkeeping must track which parts of a dataset have already been processed

Therefore the CMSDiracAux architecture effectively requires **re-implementing WMBS functionality inside DIRAC splitting plugins**.

---

# Impact on Scheduling and Resource Utilization

Fine-grained splitting is not only a bookkeeping concern.

It directly affects how distributed resources are utilized.

> How this impacts the lower levels of the system, such as Submission Infrastructure (SI) etc. It affects workload scheduling and resource pool utilization, because it delivers predictability of work entity at runtime, so that one may schedule based on projected runtime and fine-grained control over these parameters.

In CMS workflows:

* jobs process relatively uniform workloads
* runtime predictions are therefore reliable
* scheduling systems can distribute jobs efficiently

If splitting were performed only at the file level, this predictability would be lost.

> While if we lose this low level of granularity splitting and live only with file-based splitting, due to the extremely non-consistent event contents of different files, the effect would be a randomization of the projected runtime parameter, loss of predictability of the resource utilization in terms of time, loss of control over job lengths and resource pool fragmentation.

Thus the WMBS splitting model is also a mechanism for **maintaining stable resource scheduling behavior across heterogeneous datasets**.

---

# Consequences for Interoperability with DIRAC

DIRAC transformations typically operate at the **file level**.

However CMS workflows frequently require splitting at the **run or lumisection level**.

Therefore the CMSDiracAux translation layer must:

1. resolve datasets into files
2. inspect file metadata
3. map runs and lumisections to files
4. generate jobs respecting CMS splitting semantics

This functionality cannot be implemented purely through standard DIRAC transformations.

Instead it requires **extended splitting plugins capable of CMS-style bookkeeping**.

---

# Summary

WMBS exists because CMS workflows require **fine-grained workload distribution tied to the physics structure of the data**.

This leads to several important consequences:

* job splitting may occur at run, lumi, or event level
* data bookkeeping must track job–data associations
* runtime predictability depends on this fine granularity

Therefore any attempt to run CMS workflows on top of another distributed computing framework must **re-implement the WMBS splitting model in some form**.

The CMSDiracAux project addresses this requirement by embedding WMBS-like functionality inside the workflow translation layer and DIRAC splitting plugins.

---
