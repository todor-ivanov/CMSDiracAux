# CMSDiracAux Technical Report

This directory contains the evolving technical report for the
WMCore → DIRAC interoperability proof of concept implemented in
CMSDiracAux.

The report is organized as follows.

# CMSDiracAux Report

This report documents the architecture, design, and proof-of-concept implementation of **CMSDiracAux**, a translation layer that enables interoperability between the CMS workflow management system (WMCore) and the DIRAC distributed computing framework.

---

# Table of Contents

## Introduction

- [Report Overview](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/README.md)
- [Early Draft Notes](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/README_Early.md)

---

# Background

## CMS Computing Architecture

- [CMS Workflow Management](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/background/cms-workflow-management.md)
- [CMS Workflow Management System](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/background/cms-workflow-management-system.md)
- [CMS Data Model](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/background/cms-data-model.md)
- [CMS Splitting Model](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/background/cms-splitting.md)
- [WMBS Splitting Model](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/background/wmbs-splitting-model.md)

## WMCore Architecture

- [WMCore Architecture](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/background/wmcore-architecture.md)
- [WMCore–DIRAC High-Level Comparison](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/background/wmcore-dirac-high-level.md)

## DIRAC Computing Architecture

- [DIRAC Architecture](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/background/dirac-architecture.md)
- [DIRAC Production System](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/background/dirac-production-system.md)
- [DIRAC Transformation System](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/background/dirac-transformation-system.md)
- [DIRAC Workload Management System](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/background/dirac-worload-management-system.md)
- [DIRAC Workflow Systems Architecture](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/background/dirac-workflow-systems-architecture.md)

## DIRACX Evolution

- [DIRAC → DIRACX Architectural Changes](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/background/dirac-to-diracx-changes.md)
- [DIRACX and CMS Integration](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/background/dirac-diracx-cms.md)

---

# Architecture

- [CMSDiracAux Main Architecture](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/architecture/cmsdiracaux-main-architecture.md)
- [System Architecture](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/architecture/system-architecture.md)
- [Interoperability Architecture](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/architecture/interoperability-architecture.md)
- [Architecture Diagram](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/architecture/architecture-diagram.md)

## Execution Models

- [CMS vs DIRAC Execution Model](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/architecture/cms-vs-dirac-execution-model.md)
- [WMCore vs DIRAC Execution Model](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/architecture/wmcore-vs-dirac-execution-model.md)

---

# Interoperability Analysis

## Workflow Model Differences

- [WMCore–DIRAC Workflow Mismatch](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/interoperability/wmcore-dirac-mismatch.md)
- [WMBS–DIRAC Gap Analysis](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/interoperability/wmbs-dirac-gap.md)

## Translation Layer

- [Translation IR Rationale](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/interoperability/translation-ir-rationale.md)
- [Translation IR Design](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/interoperability/translation-ir-design.md)

## Runtime and Job Translation

- [CMS Runtime Construction](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/interoperability/cms-runtime-construction.md)
- [Job Runtime Differences](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/interoperability/job-runtime-differences.md)
- [Job Description Translation](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/interoperability/job-description-translation.md)
- [WMCore–DIRAC Parameter Mapping](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/interoperability/wmcore-dirac-parameter-mapping.md)

## Dataset Handling

- [Dataset Resolution Model](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/interoperability/dataset-resolution-model.md)

---

# Implementation

- [Translator Design](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/implementation/translator-design.md)
- [DIRAC Materialization](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/implementation/dirac-materialization.md)
- [CWL Export](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/implementation/cwl-export.md)

---

# Evaluation

- [Proof-of-Concept Evaluation](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/evaluation/poc-evaluation.md)
- [Current Stage Limitations](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/evaluation/current-stage-limitations.md)
- [System Limitations](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/evaluation/limitations.md)

---

# Development Checkpoints

- [Local Transformation Materialization](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/checkpoints/2026-03-12-local-materialization.md)
- [DAS LFN Resolution](https://github.com/todor-ivanov/CMSDiracAux/blob/main/docs/reports/checkpoints/2026-03-13-das-lfn-resolution.md)

---


## Current major PoC limitations

- only the first 20 files per dataset are materialized
- no full run/lumi support
- no server-side DIRAC transformation agent integration yet

## Current request-scoped output layout
```
REQUEST_ROOT
|
|-- WMCore.fetched.d
|
|-- DIRAC.transf.d
|
`-- DIRAC.cwl.d
```
## Active follow-up items

- update the architecture diagram whenever the pipeline structure changes
- preserve the parameter mapping tables
- preserve the DIRAC InputSandbox vs jobDescription.xml analysis
- preserve the DAS/DBS data discovery branch notes
