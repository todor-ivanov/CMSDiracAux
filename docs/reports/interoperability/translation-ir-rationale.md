# Translation IR Rationale

## Purpose

The CMSDiracAux project introduces a **Translation Intermediate Representation (Translation IR)** to bridge the architectural and conceptual differences between the CMS Workflow Management System (WMCore) and the DIRAC workflow execution stack.

The Translation IR serves as a **canonical workflow description layer** that allows workflows defined in WMCore to be represented in a system-agnostic form before being materialized into DIRAC execution structures.

This section explains:

* why the Translation IR is necessary
* how the IR abstracts workflow definitions
* how workflow parameters and data structures are mapped
* how IR objects translate into DIRAC constructs

---

# Motivation

CMS workflows and DIRAC workflows are based on fundamentally different execution philosophies.

CMS workflows define the **entire job structure before execution**, whereas DIRAC workflows generate jobs dynamically as data becomes available.

```text
CMS Workflow Model

Workflow
   ↓
Tasks
   ↓
WMBS splitting
   ↓
Jobs
```

```text
DIRAC Workflow Model

Production
   ↓
Transformation
   ↓
Tasks
   ↓
Jobs
```

These models cannot be mapped directly because they operate at different abstraction layers.

The Translation IR provides a stable intermediate layer between the two systems.

---

# Position of the Translation IR

The IR sits between the CMS workflow description and the DIRAC execution model.

```text
┌─────────────────────────────┐
│ CMS Workflow (WMCore)       │
│ workflow / task structure   │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Translation IR              │
│ canonical workflow model    │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ DIRAC Execution Structures  │
│ transformation / jobs       │
└─────────────────────────────┘
```

The Translation IR therefore performs two roles:

1. **semantic normalization**
2. **execution preparation**

---

# Why Direct Field Mapping Is Insufficient

A naïve approach might attempt to translate workflow definitions by mapping field names from WMCore objects directly to DIRAC job definitions.

Rationale behind using a direct mapping would be the follwoing rule of thumb: Direct field-name mapping is valid when all three are true:

1. the meaning is the same,
2. the cardinality is the same,
3. the lifecycle role is the same.

However this approach fails because:

1. **workflow abstractions differ**
2. **splitting models differ**
3. **job definitions occur at different layers**

```text
WMCore workflow
       ↓
task definitions
       ↓
splitting policies
       ↓
job definitions
```

versus

```text
DIRAC workflow
       ↓
transformation
       ↓
file discovery
       ↓
job generation
```

### Different abstraction boundaries

WMCore:

* request
* workload
* task
* step
* splitting

DIRAC:

* production
* transformation
* transformation plugin
* tasks/jobs
* workflow/job body

Those are similar, but not identical. Some WMCore fields map:

* directly,
* indirectly,
* after aggregation,
* after splitting normalization,
* or after inheritance resolution.

So many mappings are actually **semantic transforms**, not simple field copies.

---

### One WMCore field may affect several DIRAC fields

Example pattern:

A WMCore step’s runtime/resource configuration may influence:

* body executable arguments,
* CPU requirement,
* memory requirement,
* tags,
* plugin annotations.

That is not “copy one field to one field.”

---

### Several WMCore fields may collapse into one normalized concept

For example, splitting information may come from several places in the WMCore material, but in DIRAC there should be one normalized plugin payload such as:

```json
{
  "Mode": "EventAwareLumiBased",
  "EventsPerJob": 5000,
  "LumisPerJob": 10,
  "RespectRunBoundaries": true
}
```

The IR is where those multiple inputs collapse into one stable representation.

---

### IR gives a reusable contract for future phases

A canonical translation object should be looked as  a compiler layer:

```text
WMCore JSON = source language
Translation IR = abstract syntax / normalized program form
DIRAC objects = target language
```

A compiler that directly rewrites source tokens into machine instructions is usually brittle.

A compiler with an IR is usually much more maintainable.

This is the same architectural reason.



## Field-level schema with more concrete names


| WMCore object            | WMCore field name                              | Canonical IR field      | DIRAC object                     | DIRAC field name                     | Notes                                                |
| ------------------------ | ---------------------------------------------- | ----------------------- | -------------------------------- | ------------------------------------ | ---------------------------------------------------- |
| `WMRequest.json`         | `RequestName`                                  | `ProductionName`        | Production                       | `ProductionName`                     | Main workflow identity                               |
| `WMRequest.json`         | `RequestType`                                  | `ProductionType`        | Production                       | `ProductionType`                     | May need normalization to DIRAC production semantics |
| `WMRequest.json`         | `Campaign`                                     | `CampaignName`          | Production                       | `Campaign` or metadata field         | Production-level metadata                            |
| `WMRequest.json`         | `AcquisitionEra`                               | `AcquisitionEra`        | Production                       | metadata field                       | Useful for provenance and output naming              |
| `WMRequest.json`         | `ProcessingString`                             | `ProcessingString`      | Production / Transformation      | metadata field                       | May be used in output or lineage                     |
| `WMRequest.json`         | `PrepID`                                       | `PrepId`                | Production                       | metadata field                       | Provenance / bookkeeping                             |
| `WMRequest.json`         | `Priority`                                     | `Priority`              | Production / Transformation      | `Priority`                           | Could propagate downward                             |
| `WMWorkload.json`        | `RequestName` or workload name                 | `ProductionName`        | Production                       | `ProductionName`                     | If not already taken from request                    |
| `WMWorkload.json`        | task graph / task list                         | `TaskGraph`             | Production                       | step/dependency structure            | Used to create linked transformations                |
| `WMWorkload.json`        | global policy values                           | `GlobalPolicy`          | Production                       | metadata / defaults                  | Defaults inherited by tasks                          |
| `WMTask.json`            | `TaskName`                                     | `TaskName`              | Transformation                   | `TransformationName`                 | Usually 1:1 in phase 1                               |
| `WMTask.json`            | task path, often hierarchical                  | `TaskPath`              | Transformation                   | metadata field                       | Important for traceability                           |
| `WMTask.json`            | task type / step type                          | `TransformationType`    | Transformation                   | `Type`                               | Needs normalization, not raw copy                    |
| `WMTask.json`            | input dataset refs                             | `InputDataset`          | Transformation                   | `InputDataQuery` or equivalent       | Exact implementation may vary in PoC                 |
| `WMTask.json`            | output dataset intent                          | `OutputDataset`         | Transformation                   | `OutputData`                         | Often constructed, not copied verbatim               |
| `WMTask.json`            | parent task refs                               | `ParentTasks`           | Production step / Transformation | dependency links                     | Used to build transformation graph                   |
| `WMTask.json`            | site whitelist / blacklist                     | `SitePolicy`            | Transformation                   | `Site`, `SiteMask`, or metadata      | Depends on DIRAC integration style                   |
| `WMTask.json`            | task-level priority                            | `Priority`              | Transformation                   | `Priority`                           | May override production default                      |
| `WMTask.json`            | splitting section or ref                       | `SplittingPolicy`       | Transformation                   | `Plugin` + `PluginParams`            | Main bridge into plugin                              |
| `WMStep.json`            | step name                                      | `StepName`              | Job body / Transformation        | metadata field                       | For traceability                                     |
| `WMStep.json`            | `CMSSWVersion`                                 | `SoftwareVersion`       | Job body                         | `SoftwareVersion` or env field       | Runtime environment                                  |
| `WMStep.json`            | `ScramArch`                                    | `SoftwareArchitecture`  | Job body                         | `SoftwareArchitecture`               | Runtime environment                                  |
| `WMStep.json`            | step config / `ConfigCacheID` / cfg ref        | `StepConfiguration`     | Job body                         | `Executable` + `Arguments` + sandbox | Usually expanded, not copied directly                |
| `WMStep.json`            | executable semantics, usually `cmsRun`         | `Executable`            | Job body                         | `Executable`                         | Typically `cmsRun`                                   |
| `WMStep.json`            | runtime args                                   | `Arguments`             | Job body                         | `Arguments`                          | Derived from cfg / runtime settings                  |
| `WMStep.json`            | memory requirement                             | `MemoryMB`              | Job body                         | `Memory` or `MemoryMB`               | Resource requirement                                 |
| `WMStep.json`            | cores / threads                                | `CpuCores`              | Job body                         | `CPUCores` or requirement field      | Depends on body representation                       |
| `WMStep.json`            | estimated wallclock / time                     | `CpuTime`               | Job body                         | `CPUTime`                            | Runtime estimate / requirement                       |
| `WMStep.json`            | GPU requirement flag                           | `GpuRequired`           | Job body / Transformation        | tag / requirement / metadata         | Important for CMS GPU workflows                      |
| `WMStep.json`            | input files/modules                            | `InputArtifacts`        | Job body                         | `InputSandbox`                       | Sandbox or external data refs                        |
| `WMStep.json`            | output modules/files                           | `OutputArtifacts`       | Job body                         | `OutputSandbox` / output metadata    | Depends on handling style                            |
| `WMSplitting.json`       | algorithm name, e.g. `FileBased`               | `SplitMode`             | Transformation                   | `Plugin` / `PluginParams["Mode"]`    | Normalized, not copied raw                           |
| `WMSplitting.json`       | `files_per_job`                                | `FilesPerJob`           | Plugin params                    | `FilesPerJob`                        | File-count grouping                                  |
| `WMSplitting.json`       | `events_per_job`                               | `EventsPerJob`          | Plugin params                    | `EventsPerJob`                       | Event-count grouping                                 |
| `WMSplitting.json`       | `lumis_per_job`                                | `LumisPerJob`           | Plugin params                    | `LumisPerJob`                        | Lumi-count grouping                                  |
| `WMSplitting.json`       | `max_events_per_lumi` or similar               | `MaxEventsPerLumi`      | Plugin params                    | `MaxEventsPerLumi`                   | Only if needed by algorithm                          |
| `WMSplitting.json`       | `halt_job_on_file_boundaries` / similar policy | `RespectFileBoundaries` | Plugin params                    | `RespectFileBoundaries`              | Normalize policy flags                               |
| `WMSplitting.json`       | run-boundary policy                            | `RespectRunBoundaries`  | Plugin params                    | `RespectRunBoundaries`               | Important for lumi/run-safe grouping                 |
| `WMSplitting.json`       | lumi-boundary policy                           | `RespectLumiBoundaries` | Plugin params                    | `RespectLumiBoundaries`              | Important for event-aware lumi splitting             |
| `WMSplitting.json`       | runtime/resource-aware hints                   | `SplitResourceHints`    | Plugin params                    | `ResourceHints`                      | Optional extension for PoC                           |
| any WMCore source object | source object path/id                          | `SourceRef`             | any DIRAC object                 | metadata field                       | Provenance back-link                                 |
| any WMCore source object | original JSON fragment                         | `SourcePayload`         | report only                      | report artifact                      | Useful for debugging, not runtime                    |

---

## What this table is really saying

The important pattern is:

* some fields are **copied directly**
* some are **renamed**
* some are **normalized**
* some are **constructed**
* some are **carried only for provenance**

That is exactly why a canonical translation layer is useful.

---

## A more realistic mini-example

Instead of this brittle direct mapping:

```text
WMTask["TaskName"] -> Transformation["TransformationName"]
WMSplitting["events_per_job"] -> Transformation["EventsPerJob"]
WMStep["CMSSWVersion"] -> Job["CMSSWVersion"]
```

The IR should do this:

```text
WMCore JSON
   -> CanonicalTask {
        TaskName,
        TransformationType,
        Executable,
        Arguments,
        SoftwareVersion,
        MemoryMB,
        SplitMode,
        EventsPerJob,
        SourceRef
      }
   -> DIRAC objects
```

That gives one place to resolve:

* inheritance,
* defaults,
* naming cleanup,
* semantic conversion,
* unsupported cases.

---


**Therefore the translation process must introduce a *canonical intermediate model*.**

---

# Translation IR Architecture

The Translation IR defines the canonical objects used to represent workflows.

```text
┌───────────────────────────────┐
│ IRWorkflow                    │
│ workflow metadata             │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│ IRTask                        │
│ processing step               │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│ IRDataset                     │
│ dataset reference             │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│ IRSplittingPolicy             │
│ job partitioning rules        │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│ IRJobTemplate                 │
│ executable job description    │
└───────────────────────────────┘
```

Each object encapsulates a different part of the workflow semantics.

---

# Canonical Translation Objects

The Translation IR introduces canonical objects independent of both WMCore and DIRAC.

| IR Object         | Purpose                     |
| ----------------- | --------------------------- |
| IRWorkflow        | describes overall workflow  |
| IRTask            | processing step             |
| IRDataset         | input dataset reference     |
| IRSplittingPolicy | job splitting configuration |
| IRJobTemplate     | executable job description  |

These objects provide a stable interface for both systems.

---

# Workflow Parameter Mapping

The following table describes how key workflow parameters map between WMCore and the Translation IR.

| WMCore Parameter   | Translation IR       | Description                 |
| ------------------ | -------------------- | --------------------------- |
| RequestName        | workflow_name        | workflow identifier         |
| InputDataset       | dataset              | input dataset               |
| ProcessingString   | processing_tag       | processing stage identifier |
| CMSSWVersion       | software_release     | CMSSW environment           |
| GlobalTag          | conditions_tag       | detector conditions         |
| ConfigCacheID      | configuration_ref    | job configuration           |
| SplittingAlgo      | splitting_policy     | splitting strategy          |
| SplittingArguments | splitting_parameters | parameters of splitting     |

---

# Dataset Representation Mapping

| WMCore Object | Translation IR | Description        |
| ------------- | -------------- | ------------------ |
| Dataset       | dataset_name   | dataset identifier |
| Block         | block_name     | dataset block      |
| File          | file_lfn       | logical file name  |
| Run           | run_number     | run identifier     |
| Lumi          | lumi_section   | luminosity section |

CMS datasets follow the hierarchy:

```text
dataset
   ↓
block
   ↓
file
   ↓
run
   ↓
lumi
```

The Translation IR stores these relationships in a normalized form.

---

# Task Definition Mapping

The following table maps task definitions between WMCore and the Translation IR.

| WMCore Field       | IR Field                | Description             |
| ------------------ | ----------------------- | ----------------------- |
| TaskName           | task_name               | name of task            |
| InputDataset       | input_dataset           | dataset used            |
| SplittingAlgo      | splitting_algorithm     | splitting strategy      |
| SplittingArguments | splitting_parameters    | splitting configuration |
| ConfigCacheID      | configuration_reference | CMSSW configuration     |
| OutputDataset      | output_dataset          | produced dataset        |

---

# Job Definition Mapping

The Translation IR job template captures the information required to generate DIRAC jobs.

| IR Field         | DIRAC Equivalent | Description        |
| ---------------- | ---------------- | ------------------ |
| executable       | job executable   | application        |
| arguments        | job arguments    | runtime parameters |
| input_files      | InputSandbox     | input files        |
| output_files     | OutputSandbox    | produced files     |
| software_release | environment      | runtime software   |

---

# Splitting Policy Representation

CMS workflows define explicit job partitioning policies.

```text
dataset
      ↓
splitting algorithm
      ↓
job definitions
```

Example splitting modes:

* FileBased
* LumiBased
* RunBased
* EventAware

The Translation IR represents these policies using the IRSplittingPolicy object.

| Splitting Mode | IR Representation |
| -------------- | ----------------- |
| FileBased      | files_per_job     |
| LumiBased      | lumis_per_job     |
| RunBased       | runs_per_job      |
| EventAware     | events_per_job    |

---

# DIRAC Materialization

Once the Translation IR is constructed, it can be converted into DIRAC workflow structures.

```text
IRWorkflow
     ↓
IRTask
     ↓
DIRAC Transformation
     ↓
DIRAC Jobs
```

This allows the CMS workflow to be executed through the DIRAC workload infrastructure.

---

# Role of the Translation IR in CMSDiracAux

The Translation IR is the **core abstraction layer** in the CMSDiracAux architecture.

```text
WMCore workflow
      ↓
Translation IR
      ↓
DIRAC execution
```

The IR therefore enables:

* workflow portability
* architecture decoupling
* execution model translation

---

# Summary

The Translation IR provides a canonical representation of workflows that separates **workflow semantics from execution infrastructure**.

This abstraction allows CMS workflows to be expressed in a form compatible with DIRAC while preserving the workflow structure and data processing semantics.

The Translation IR is therefore the key architectural component that enables interoperability between the CMS workflow management system and DIRAC execution environments.
