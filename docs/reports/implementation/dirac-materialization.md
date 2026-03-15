# DIRAC Materialization

## Overview

After the Translation IR has been constructed, the workflow must be materialized into execution structures compatible with the DIRAC distributed computing framework.

This stage converts canonical workflow descriptions into DIRAC execution constructs such as transformations and jobs.

---

# Materialization Pipeline

The materialization stage transforms canonical objects into DIRAC execution entities.

```
Translation IR
      │
      ▼
Transformation definition
      │
      ▼
CMS splitting plugin
      │
      ▼
Job generation
```

---

# DIRAC Transformation System

The DIRAC Transformation System is responsible for generating jobs from data inputs and workflow definitions.

```
Transformation
      │
      ▼
Input datasets
      │
      ▼
Tasks
      │
      ▼
Jobs
```

In CMSDiracAux, transformations are created using metadata derived from the Translation IR.

---

# CMS Splitting Plugin

CMS workflows require splitting policies that operate at fine data granularity.

Typical splitting levels include:

```
dataset
   │
   ▼
file
   │
   ▼
run
   │
   ▼
luminosity section
```

DIRAC normally performs splitting at the file level.

To preserve CMS workflow semantics, a CMS-specific splitting plugin is introduced.

```
Transformation
      │
      ▼
CMS Splitting Plugin
      │
      ▼
Job definitions
```

This plugin reproduces the logic originally implemented in WMBS.

---

# Job Description Construction

Once jobs are generated, the job description must be constructed.

A typical DIRAC job description includes:

```
Executable
Arguments
InputSandbox
OutputSandbox
CPUTime
```

CMSDiracAux extends the job description to include CMS-specific runtime parameters.

These parameters correspond to the configuration required by the CMS runtime environment.

---

# Runtime Parameter Injection

CMS jobs require runtime configuration artifacts.

Typical parameters include:

```
__CMSJobParameter__dataset
__CMSJobParameter__runRange
__CMSJobParameter__lumiMask
__CMSJobParameter__psetTweaks
```

These parameters ensure that the job processes the correct portion of the dataset.

---

# Worker Node Execution

Once jobs are scheduled they execute on worker nodes.

Runtime reconstruction pipeline:

```
DIRAC job starts
      │
      ▼
Bootstrap script
      │
      ▼
Runtime environment preparation
      │
      ▼
cmsRun execution
```

The bootstrap stage prepares the CMS runtime environment.

---

# Summary

DIRAC materialization converts canonical workflow descriptions into executable job structures.

This stage preserves CMS workflow semantics while enabling execution through the DIRAC workload management infrastructure.
