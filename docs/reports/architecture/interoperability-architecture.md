# CMS-DIRAC hybrid system

This section provides a view of which pieces would be substituted from the current CMS Workflow management system
once a **CMS-DIRAC** hybrid system is implemented with **CMSDiracAux** serving as an interoperable layer.

The idea is that CMSDiracAux does **not replace the whole CMS workflow system**. Instead it **cuts the system at two conceptual boundaries**:

1. **Workflow extraction boundary** – where WMCore workflows are intercepted.
2. **Execution backend boundary** – where the CMS Submission Infrastructure would normally generate and dispatch jobs.

These boundaries correspond to replacing the **WMBS + SI execution path** with the **Translation IR + DIRAC execution path**.

This approach is consistent with how large workflow systems are typically layered, where workflow definition and execution infrastructure can be decoupled through intermediate abstractions. ([arXiv][1])

---

# Current CMS Workflow management system

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
--------------------------------------------------------------------------------
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
--------------------------------------------------------------------------------
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
> **Figure X:** Current CMS Workflow Management system architecture


# Hybrid CMS-DIRAC Workflow System with CMSDiracAux as transitional layer/system

```text
                    CMS WORKFLOW MANAGEMENT SYSTEM
┌──────────────────────────────────────────────────────────────────────────────┐
│                              CMSWEB SERVICES                                 │
│                                              X---------+      X---------+    │
│   ReqMgr2      DBS/DAS          Rucio        | WMStats |      | CouchDB |    │
│                                              +---------+      +---------+    │
└───────────────┬──────────────────────────────────────────────────────────────┘
                │
                ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                         WORKFLOW MANAGEMENT (WMCore)                         │
│                                                                              │
│   Workflow Definition                                                        │
│   Task Graph                                                                 │
│   Splitting Policies                                                         │
└─────────────────────────────────────────────────────┬────────────────────────┘
                                                      │
══════════════════════════════════════════════════════╪═════════════════════════
                CMSDiracAux intercepts workflows here │
══════════════════════════════════════════════════════╪═════════════════════════
                                                      │
                                                      ▼

X-------------------------------+      ┌──────────────────────────────────────┐
│ WMBS                          │      │ DIRAC-like CMS Splitting Plugin      │
  (inside WMAgents)                    │ (WMBS logic reborn)                  │
│                               │      │                                      │
  Job bookkeeping                      │ Job ↔ data-content mapping           │
│ Run/Lumi splitting            │  →   │ Run/Lumi splitting                   │
  Job definitions                      │ Job definitions                      │
+-------------------------------+      └──────────────────────────────────────┘
                                                      │
                                                      ▼
                                     ┌─────────────────────────────────────────┐
                                     │      DIRAC TRANSFORMATION SYSTEM        │
                                     │                                         │
                                     │   Transformation                        │
                                     │          │                              │
                                     │          ▼                              │
                                     │        Jobs                             │
                                     └───────────────┬─────────────────────────┘
                                                     │
═════════════════════════════════════════════════════╪══════════════════════════
                        CMSDiracAux replaces execution backend here
═════════════════════════════════════════════════════╪══════════════════════════
                                                     │
                                                     ▼
┌──────────────────────────────────────────┐   ┌──────────────────────────────┐
│ CMS Submission Infrastructure            │   │ DIRAC WORKLOAD MANAGEMENT    │
│                                          │   │                              │
│ HTCondor                                 │   │ Job Queue                    │
│ GlideinWMS pilot system                  │◄──┤ Pilot / workload control     │
│ (planned substitute for DIRAC pilots)    │   │ Worker-node dispatch logic   │
└───────────────────────┬──────────────────┘   └──────────────┬───────────────┘
                        │                                     │
                        └──────────────────┬──────────────────┘
                                           │
                                           ▼
                              ┌──────────────────────────────┐
                              │         Worker Nodes         │
                              │                              │
                              │   CMS jobs / cmsRun execute  │
                              └──────────────────────────────┘
```
> **Figure X:** CMS workflow system architecture showing the integration points of CMSDiracAux. The project intercepts workflows after WMCore workflow definition and replaces the traditional CMS submission infrastructure with a DIRAC-based execution backend while preserving CMS workflow semantics.

---

# Interpretation of the Two Systems

A future hybrid system assembled between CMS-DIRAC should follow few principles. It should:

* Not break communication APIs with stakeholders systems
* Not imply or require conceptual changes to external systems
* Not break operational patterns
* Be backwards compatible

This is the reason why the initial Workflow construction from the current WMCore system should remains as is.
It serves as a bridge between other stakeholder systems and the main Workflow management system. It may by itself
evolve in the future or in the process of creating the new system, but nevertheless, should still follow the same principles as above.

This is the layer which provides the full hierarchical assembly  of a CMS workflow.

## First cut and new inter system communication line — workflow extraction

CMSDiracAux intercepts the system **after workflow definition but before WMBS job materialization**.

Meaning:

```
WMCore workflows
        ↓
Translation IR
```

Instead of letting WMBS produce job definitions directly, the workflow is translated into a **canonical representation**.

This is the **semantic decoupling point**.

---

## Second cut and new inter system communication line — execution backend

CMSDiracAux replaces the **CMS job construction and submission infrastructure**:

```
WMBS → SI → HTCondor → GlideinWMS
```

with

```
Translation IR → DIRAC Transformation → DIRAC WMS + GlideinWMS/HTCondor
```

This means the **execution backend changes**, but the **workflow semantics remain CMS-native**.

---

# Key Architectural Insight

```text
CMSDiracAux does not eliminate WMBS logic.
```

Instead:

```
WMBS functionality
        ↓
reappears in the DIRAC splitting plugin
```

This is necessary because CMS splitting operates **below the storage abstraction level** (run/lumi/event).

1. CMS workflow semantics remain intact.
2. Execution infrastructure becomes interchangeable.
3. The system can evolve toward DIRAC or DIRACX without rewriting the CMS workflow model.

Conceptually:

```text
CMS workflow semantics
        ↓
Translation IR
        ↓
execution backend (DIRAC / DIRACX)
```

---

[1]: https://arxiv.org/abs/0910.0626?utm_source=chatgpt.com "Towards a Grid Platform for Scientific Workflows Management"
