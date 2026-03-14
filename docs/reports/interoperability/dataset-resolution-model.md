# Dataset Resolution Model

## Purpose

CMS workflows operate primarily on **datasets**, while execution infrastructures ultimately process **files**.

The CMSDiracAux translation layer must therefore resolve dataset-level workflow definitions into **file-level execution units** before jobs can be created.

This section describes the dataset resolution model used in the CMS workflow management system and the mechanism implemented in the CMSDiracAux proof-of-concept to translate dataset references into executable workload inputs.

---

# CMS Data Hierarchy

CMS data are organized according to a hierarchical structure.

```text id="cms_data_hierarchy"
dataset
   │
   ▼
block
   │
   ▼
file
   │
   ▼
run
   │
   ▼
lumi
   │
   ▼
events
```

Each level represents a progressively finer partition of the data.

| Level   | Description                                     |
| ------- | ----------------------------------------------- |
| Dataset | logical collection of data files                |
| Block   | dataset subdivision used for storage management |
| File    | physical storage unit                           |
| Run     | data-taking period identifier                   |
| Lumi    | luminosity section within a run                 |
| Event   | individual recorded event                       |

In most workflow definitions the **dataset is the primary input abstraction**.

---

# Dataset References in Workflow Definitions

In CMS workflows the input data are typically specified using a dataset identifier.

Example:

```text
/PrimaryDataset/ProcessingString/DataTier
```

This identifier represents a logical dataset registered in the CMS data bookkeeping systems.

Workflow tasks therefore define input data at the dataset level.

```text id="workflow_dataset_reference"
┌────────────────────────────┐
│ Workflow Task              │
│                            │
│ InputDataset = dataset_id  │
└───────────────┬────────────┘
                │
                ▼
        dataset resolution
```

Before jobs can be created, the dataset must be resolved into the underlying files.

---

# Dataset Discovery Infrastructure

Dataset resolution relies on the CMS data discovery infrastructure.

Two primary services are used:

| Service                       | Purpose                               |
| ----------------------------- | ------------------------------------- |
| DBS (Data Bookkeeping System) | stores dataset metadata               |
| DAS (Data Aggregation System) | query interface for dataset discovery |

These services provide information about:

* dataset existence
* file membership
* run/lumi metadata
* storage locations

---

# Data Representation in DIRAC

DIRAC transformations operate differently.

Jobs are typically generated using **explicit file-level inputs**.

These files are identified using their Logical File Names stored in the **DIRAC File Catalog**.

A transformation therefore defines:

```
input data query
```

which returns a set of LFNs.

The transformation system then generates jobs based on this file list.

Typical job splitting occurs at the level of:

```
file
```

or groups of files.

Unlike CMS workflows, DIRAC transformations generally do not operate directly on dataset abstractions.

---


# Dataset Resolution Pipeline

The dataset resolution process converts a dataset identifier into a list of logical file names (LFNs).

```text id="dataset_resolution_pipeline"
┌────────────────────────────┐
│ Workflow Task              │
│ InputDataset               │
└───────────────┬────────────┘
                │
                ▼
┌────────────────────────────┐
│ DAS Query                  │
│ dataset → file records     │
└───────────────┬────────────┘
                │
                ▼
┌────────────────────────────┐
│ File Metadata              │
│ run / lumi information     │
└───────────────┬────────────┘
                │
                ▼
┌────────────────────────────┐
│ Logical File Name List     │
│ (LFNs)                     │
└────────────────────────────┘
```

The resulting file list becomes the input to the job generation stage.

---

# Example DAS Query

Dataset file discovery is typically performed using `dasgoclient`.

Example:

```text
dasgoclient --query="file dataset=/ExampleDataset/Processing/DataTier"
```

The query returns metadata describing the files belonging to the dataset.

Example output fields include:

| Field        | Description         |
| ------------ | ------------------- |
| file.name    | logical file name   |
| file.size    | file size           |
| file.nevents | number of events    |
| run          | run identifier      |
| lumi         | luminosity sections |

These metadata fields are later used for job partitioning.

---

# Dataset Resolution in CMSDiracAux

The CMSDiracAux proof-of-concept implements dataset resolution as part of the **translator stage**.

```text id="dataset_resolution_architecture"
┌───────────────────────────────┐
│ WMCore Workflow               │
│ dataset references            │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│ Translator Layer              │
│ dataset resolution            │
│ DAS queries                   │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│ File List                     │
│ used for splitting            │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│ DIRAC Transformation Inputs   │
└───────────────────────────────┘
```

Dataset resolution therefore occurs **before DIRAC job generation**.

---

# Handling Large Datasets

CMS datasets often contain very large numbers of files.

Typical dataset sizes may include:

| Dataset                    | Approximate file count     |
| -------------------------- | -------------------------- |
| small analysis dataset     | tens of files              |
| typical production dataset | thousands of files         |
| large reprocessing dataset | tens of thousands of files |

For development purposes the CMSDiracAux proof-of-concept applies a temporary limit.

```text
maximum_files_per_dataset = 20
```

This limit prevents the generation of excessively large local artifacts during testing.

---

# Integration with Splitting

Once files are resolved, job generation can proceed using splitting policies.

```text id="resolution_splitting_flow"
dataset
   │
   ▼
file discovery
   │
   ▼
file list
   │
   ▼
splitting policy
   │
   ▼
job definitions
```

Splitting policies determine how files are partitioned into jobs.

Examples include:

* file-based splitting
* run-based splitting
* lumi-based splitting
* event-aware splitting

These policies are implemented within the job generation stage.

---

# Architectural Role in the CMSDiracAux System

Dataset resolution is located in the **translation layer of the CMSDiracAux architecture**.

```
WMCore workflow
        │
        ▼
workflow extraction
        │
        ▼
Translation IR  <── dataset resolution
        │
        ├── DIRAC transformation
        └── CWL workflow
```

By resolving datasets at this stage, the Translation IR becomes independent of the CMS metadata infrastructure.

This ensures that downstream execution systems only receive the **concrete file-level inputs required for execution**.

---

# Implications for DIRAC Execution

DIRAC transformations typically operate on file-level inputs.

Therefore the dataset resolution stage produces the input structure required by DIRAC workflows.

```text id="dataset_dirac_mapping"
dataset
   │
   ▼
file list
   │
   ▼
DIRAC transformation tasks
   │
   ▼
DIRAC jobs
```

This conversion bridges the difference between CMS dataset abstractions and DIRAC execution units.

---

# Importance for Workflow Interoperability

The dataset resolution model is essential for interoperability because it bridges two fundamentally different data abstractions.

```
CMS workflow → dataset abstraction
DIRAC workflow → file-level inputs
```


# Summary

CMS workflows define input data at the **dataset level**, while execution infrastructures require **file-level processing units**.

The dataset resolution model therefore performs the following steps:

1. resolve dataset identifiers using DAS queries
2. obtain file-level metadata
3. construct logical file name lists
4. provide these lists to the job generation stage

This process enables CMS workflows defined in WMCore to be translated into executable jobs compatible with DIRAC workflow infrastructures.
