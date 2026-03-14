# CMS vs DIRAC Workflow Execution Models

Comparison diagram that visualizes the **conceptual difference between CMS and DIRAC workflow execution models** and supports the **Schrödinger vs Heisenberg analogy**

```text
                        CMS Workflow Model
                 (Explicit Workflow Evolution)

      Workflow Definition
              │
              ▼
        Task Graph
              │
              ▼
        Splitting Rules
              │
              ▼
      Job Definitions Created
              │
              ▼
      Jobs Submitted to Grid
              │
              ▼
      Worker Node Execution


      Interpretation:

      Workflow evolution is defined
      before runtime execution.



────────────────────────────────────────────────────────────────────────



                        DIRAC Execution Model
                   (Dynamic Data-Driven Execution)

      Production / Transformation
              │
              ▼
       Task Queues Created
              │
              ▼
         Pilot Jobs Start
              │
              ▼
       Worker Node Requests Job
              │
              ▼
        Job Assigned Dynamically
              │
              ▼
        Payload Execution



      Interpretation:

      Workload is assigned dynamically
      during runtime execution.
```

---

# Data Interaction Comparison

Another useful view highlights how workflows interact with data.

```text
                 CMS Workflow Interaction with Data

        Workflow
            │
            ▼
       Dataset Definition
            │
            ▼
      Files Discovered
            │
            ▼
     Run / Lumi Partitioning
            │
            ▼
        Jobs Created


────────────────────────────────────────


                 DIRAC Workflow Interaction with Data

       Transformation
            │
            ▼
        Files Discovered
            │
            ▼
        Job Created
            │
            ▼
        File Processed
```

> **Figure X:** Conceptual comparison between CMS and DIRAC workflow execution models. CMS workflows explicitly define the job structure before execution, while DIRAC assigns work dynamically through a pilot-based execution model. The CMSDiracAux Translation IR bridges these two execution philosophies.

---

# Conceptual Interpretation

The difference can be summarized as follows.

### CMS

```text
Workflow → Data → Jobs
```

The workflow evolves explicitly and determines the job set before execution.

---

### DIRAC

```text
Data → Jobs during runtime
```

The system dynamically creates and schedules jobs based on available resources and data.

---

# Physics Analogy

This conceptual difference is similar to two equivalent formulations of quantum mechanics.

```text
CMS workflow model
        ↔
Schrödinger picture

The system state evolves explicitly.


DIRAC execution model
        ↔
Heisenberg picture

Operators evolve while the state
remains implicitly defined.
```

This analogy is not exact but provides an intuitive mental model for understanding the architectural distinction.

---

# Implication for CMSDiracAux

The interoperability layer must bridge these two philosophies.

```text
CMS explicit workflow model
            │
            ▼
        Translation IR
            │
            ▼
DIRAC dynamic execution model
```

The Translation IR allows CMS workflow semantics to be preserved while adapting them to the DIRAC execution infrastructure.
