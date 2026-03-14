# CMSDiracAux Main Architecture

```text
                                     CMS Workflow Layer
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│                          CMS Workflow Management                             │
│                                (WMCore)                                      │
│                                                                              │
│      Workflow Request                                                        │
│            │                                                                 │
│            ▼                                                                 │
│        Tasks                                                                 │
│            │                                                                 │
│            ▼                                                                 │
│      Splitting Policies                                                      │
│                                                                              │
└───────────────┬──────────────────────────────────────────────────────────────┘
                │
                │ workflow extraction
                ▼


                           CMSDiracAux Translation Layer
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│                     Canonical Translation IR                                 │
│                                                                              │
│     CanonicalWorkflow                                                        │
│            │                                                                 │
│            ▼                                                                 │
│       CanonicalTasks                                                         │
│            │                                                                 │
│            ▼                                                                 │
│      CanonicalSplitting                                                      │
│            │                                                                 │
│            ▼                                                                 │
│      CanonicalProduction                                                     │
│                                                                              │
└───────────────┬──────────────────────────────────────────────────────────────┘
                │
                │ transformation materialization
                ▼


                                DIRAC Execution Layer
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│                         DIRAC Transformation System                          │
│                                                                              │
│        Transformation                                                        │
│              │                                                               │
│              ▼                                                               │
│       CMS Splitting Plugin                                                   │
│              │                                                               │
│              ▼                                                               │
│           Jobs                                                               │
│                                                                              │
└───────────────┬──────────────────────────────────────────────────────────────┘
                │
                │ pilot scheduling
                ▼


                         DIRAC Workload Management System
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│                             Job Queue                                        │
│                                 │                                            │
│                                 ▼                                            │
│                            Pilot Jobs                                        │
│                                 │                                            │
│                                 ▼                                            │
│                            Worker Nodes                                      │
│                                                                              │
└───────────────┬──────────────────────────────────────────────────────────────┘
                │
                │ runtime execution
                ▼


                                  CMS Runtime
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│                           Worker Node Runtime                                │
│                                                                              │
│      Bootstrap                                                               │
│         │                                                                    │
│         ▼                                                                    │
│   Runtime Reconstruction                                                     │
│         │                                                                    │
│         ▼                                                                    │
│   PSet Tweaks Applied                                                        │
│         │                                                                    │
│         ▼                                                                    │
│      cmsRun                                                                  │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

> **Figure X:** CMSDiracAux architecture. CMS workflows defined in WMCore are translated into a canonical intermediate representation that decouples CMS workflow semantics from DIRAC execution infrastructure. The IR is materialized into DIRAC transformations, where CMS-specific splitting logic is implemented through transformation plugins. Jobs are executed via the DIRAC Workload Management System using pilot scheduling, while CMS runtime environments are reconstructed on worker nodes before executing the `cmsRun` application.

---

# Key Architectural Message of the Diagram

This diagram communicates the **core architectural idea of CMSDiracAux**:

```text
CMS workflows
      ↓
canonical Translation IR
      ↓
DIRAC transformations
      ↓
CMS-aware splitting plugin
      ↓
jobs executed through DIRAC pilots
      ↓
CMS runtime reconstructed on worker nodes
```

---

# Important Insight Highlighted

The diagram also illustrates the most important conclusion of the interoperability study:

```text
WMBS functionality does not disappear
when moving CMS workflows to DIRAC.
```

Instead it **reappears inside the DIRAC transformation layer**, where CMS-specific splitting logic must be implemented.

Conceptually:

```text
CMS WMBS
      ↓
CMSDiracAux splitting plugin
```
