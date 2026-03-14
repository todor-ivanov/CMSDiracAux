# DIRAC Production System

## Purpose of this section

The DIRAC Production System provides a framework for executing **large-scale production workflows** across distributed computing infrastructures.

While the Transformation System focuses on **data-driven job generation**, the Production System provides **higher-level workflow orchestration**, allowing complex multi-step production chains to be executed across the grid.

Understanding the Production System is important for evaluating how experiment workflows are structured in DIRAC and how they compare with CMS workflow management systems.

---

# Role of the Production System in DIRAC

The Production System was originally designed to support the large production campaigns of the LHCb experiment.

It provides functionality for:

* defining production workflows
* orchestrating multi-step processing chains
* tracking production status
* managing large sets of related jobs

Conceptually, the Production System sits above the workload management layer.

```
┌──────────────────────────────┐
│        Production System     │
│  (workflow orchestration)    │
└───────────────┬──────────────┘
                │
                ▼
┌──────────────────────────────┐
│     Workload Management      │
│      (DIRAC WMS)             │
└───────────────┬──────────────┘
                │
                ▼
┌──────────────────────────────┐
│     Pilot Execution Layer    │
└──────────────────────────────┘
```

---

# Concept of Productions

A **production** represents a coordinated set of jobs that process large volumes of data according to a defined workflow.

Conceptually:

```
┌─────────────────────────────┐
│        Production           │
│ (processing campaign)       │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│      Workflow Steps         │
│  (processing chain)         │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│      Job Generation         │
│  (tasks distributed)        │
└─────────────────────────────┘
```

A production may involve multiple stages such as:

* simulation
* reconstruction
* data reduction
* analysis preparation

Each stage produces output data used by the next stage.

---

# Production Workflow Structure

Production workflows in DIRAC are typically represented as **sequences of processing steps**.

```
┌─────────────┐
│  Step 1     │
│ Simulation  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Step 2     │
│ Reconstruction │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Step 3     │
│ Data Reduction │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Step 4     │
│ Analysis Data │
└─────────────┘
```

Each step may generate thousands of distributed jobs.

---

# Relationship Between Productions and Transformations

In many DIRAC deployments, productions are implemented internally using **transformations**.

Conceptually:

```
┌────────────────────────────┐
│       Production           │
│  (workflow orchestration)  │
└──────────────┬─────────────┘
               │
               ▼
┌────────────────────────────┐
│       Transformation       │
│   (job generation layer)   │
└──────────────┬─────────────┘
               │
               ▼
┌────────────────────────────┐
│         Jobs               │
│  executed via pilots       │
└────────────────────────────┘
```

Thus the Transformation System often acts as the **execution engine** for production workflows.

---

# Job Creation within a Production

Within a production step, the system generates jobs that process input data.

```
┌──────────────────────────┐
│ Production Step          │
│ (processing definition)  │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│ Input Data Discovery     │
│ (dataset or file query)  │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│ Job Generation           │
│ (large job set created)  │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│ Distributed Execution    │
│ via pilot infrastructure │
└──────────────────────────┘
```

Each production may generate **tens or hundreds of thousands of jobs**.

---

# Monitoring and Bookkeeping

The Production System includes services for tracking workflow progress.

These services maintain information about:

* job status
* data produced
* workflow step completion
* production progress

Conceptually:

```
┌──────────────────────────────┐
│     Production Monitoring    │
│                              │
│  job status                  │
│  step completion             │
│  output data tracking        │
└──────────────────────────────┘
```

This bookkeeping functionality is critical for large production campaigns.

---

# Comparison with CMS Workflow Management

The DIRAC Production System differs from CMS workflow management in several important ways.

| Property            | CMS Workflow System          | DIRAC Production System |
| ------------------- | ---------------------------- | ----------------------- |
| Workflow definition | explicit multi-step workflow | production steps        |
| Job generation      | predefined during splitting  | generated dynamically   |
| Data abstraction    | dataset + run/lumi splitting | file-level processing   |
| Bookkeeping         | WMBS                         | production monitoring   |

These differences highlight the conceptual gap between CMS workflows and DIRAC execution models.

---

# Implications for CMSDiracAux

The CMSDiracAux project aims to express CMS workflows within DIRAC infrastructure.

This requires mapping CMS workflow concepts onto DIRAC constructs.

Conceptually:

```
┌──────────────────────┐
│    CMS Workflow      │
│ (WMCore definition)  │
└───────────┬──────────┘
            │
            ▼
┌──────────────────────┐
│    Translation IR    │
│ workflow abstraction │
└───────────┬──────────┘
            │
            ▼
┌──────────────────────┐
│ DIRAC Production     │
│ or Transformation    │
│ execution model      │
└──────────────────────┘
```

The Translation IR acts as the layer that reconciles the different workflow abstractions used by the two systems.

---

# Summary

The DIRAC Production System provides high-level orchestration for large-scale distributed processing campaigns.

It manages multi-step workflows and coordinates the generation and monitoring of large numbers of distributed jobs.

In modern DIRAC deployments, the Production System often relies on the Transformation System to generate and execute individual jobs.

Understanding the relationship between these systems is essential for integrating CMS workflows within DIRAC infrastructures, as explored by the CMSDiracAux project.
