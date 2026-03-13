# ⚠️ AI-Assisted Content Notice

Parts of the code, documentation, and generated reports contained in this
repository include **AI-assisted or AI-altered content**.

Some sections were produced with the help of **OpenAI ChatGPT (GPT-5 series)**
during the development of the WMCore → DIRAC interoperability prototype.

All AI-generated or AI-assisted material included in this repository has been
**reviewed and curated by a human maintainer** before inclusion.

The purpose of using AI assistance in this repository is to accelerate
prototyping and documentation while maintaining full human oversight of
technical correctness and architectural decisions.

If you encounter inconsistencies or potential issues in AI-assisted sections,
please open an issue in the repository.

# CMSDiracAux
Auxiliary scripts and tests for running CMS workflows within Dirac distributed computing system for the CMS experiment at CERN

## Design and report notes

Architecture notes are kept under `docs/architecture/`.

Early report-oriented notes and preserved design reasoning are kept under
`docs/reports/`.


## Running CMS jobs with Dirac

These are notes collected during the process of initial tests of running CMS speciiffic jobs/workflows wihthin the Dirac distributed computing system.

### CMS Workflow type chosen:
 * Relval Workflow
 * Montecarlo from scratch
 * No Input
 * No Pileup

### Goals:
 * Run a minimal workflow within a minimal Dirac instance setup (hopefully provided by the Dirac Team)
 * Run the workflow, monitor the jobs progress, collect the output
 * If needed dissect the workflow on a joblevel basis and
 * Investigate how Dirac expects the payload to be packaged
 * Investigate how is the payload sent and monitored during runtime at the workernodes
 * Investigate how the jobs accounting works
 * Investigate what are the regular mechanisms for jobs and workflows debugging
 * Investigate the advanced job managing mechanisms
 * Create deterministic translation layer (a PoC) between the CMS workflow management system and DIRAC
 * Express the complexity of the workflows abstractions between the two systems
 * Mark needed changes/developments to the CMS workflows

## PoC Objectives:

---

### Objective 1

Create a **deterministic WMCore → DIRAC translation PoC**.

This includes:

```
WMCore workflow extraction
dataset resolution
translation IR construction
DIRAC transformation materialization
```

---

### Objective 2

Create a **workflow abstraction bridge** between the systems.

This bridge must explain:

```
workflow structure differences
splitting semantics
runtime environment differences
data hierarchy
```

This is the **core scientific value** of the project.

---

### Objective 3

Demonstrate how CMS workflows could **theoretically run under DIRAC**.

Not necessarily fully production-ready, but:

```
structurally compatible
architecturally explainable
```

---

### Objective 4

Export workflows into **CWL representation**.

Purpose:

```
future DIRACX compatibility
workflow portability
DAG representation
```

---

### Objective 5

Produce **architectural documentation** explaining:

```
why the systems differ
what translation layer is required
which components are experiment-specific
```
---

## Objective Completion Matrix:

| Objective                                 | Status                           | Completion |
| ----------------------------------------- | -------------------------------- | ---------- |
| WMCore workflow extraction                | implemented                      | **85%**    |
| Dataset discovery via DAS                 | implemented (prototype)          | **70%**    |
| Canonical Translation IR                  | partially implemented implicitly | **45%**    |
| WMCore → DIRAC transformation translation | implemented prototype            | **65%**    |
| Local DIRAC transformation simulation     | implemented                      | **70%**    |
| CMS splitting plugin simulation           | implemented                      | **60%**    |
| CWL workflow export                       | early prototype                  | **40%**    |
| DIRAC runtime job modeling                | partially explored               | **35%**    |
| Workflow abstraction bridge               | conceptual only                  | **25%**    |
| Architecture documentation                | in progress                      | **30%**    |
