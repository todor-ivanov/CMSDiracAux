# Dataset Resolution Model

## Purpose of this section

The CMS workflow management system and the DIRAC workload management framework operate with **different abstractions for data selection and job input definition**.

CMS workflows typically refer to **datasets**, while DIRAC transformations operate on **explicit lists of files**.

Therefore, when translating workflows from WMCore to DIRAC, it is necessary to introduce a **dataset resolution stage** that converts dataset references into concrete file-level inputs.

This section describes the dataset resolution model implemented in the CMSDiracAux prototype and explains its role in the workflow translation pipeline.

---

# Data Representation in CMS

CMS workflows are defined at the level of **datasets**, which represent logical collections of files.

The CMS data hierarchy follows a structured model.

```
dataset
   │
   ▼
block
   │
   ▼
file
```

Each level serves a specific purpose.

| Level   | Purpose                                |
| ------- | -------------------------------------- |
| dataset | logical data collection                |
| block   | distribution unit across storage sites |
| file    | physical processing unit               |

Workflow definitions typically reference datasets rather than individual files.

For example, a workflow step may declare:

```
input dataset
```

without specifying the individual files that should be processed.

The actual file lists are resolved dynamically during workflow preparation.

---

# Dataset Discovery via DAS

Dataset resolution in CMS relies on the **Data Aggregation System (DAS)**.

DAS provides a unified interface for querying CMS metadata services.

Typical queries include:

```
dataset → blocks
dataset → files
block → files
```

In practice, dataset resolution is often performed using the command-line tool:

```
dasgoclient
```

Example query:

```
dasgoclient --query="file dataset=/A/B/C"
```

The result of this query is a list of **Logical File Names (LFNs)** that represent the files belonging to the dataset.

These LFNs become the **actual processing units for job execution**.

---

# Dataset Resolution in CMS Workflows

In the CMS workflow system, dataset resolution happens during **job creation inside WMBS**.

The process is conceptually:

```
dataset reference
        ↓
block discovery
        ↓
file discovery
        ↓
job splitting
```

The WMBS subsystem uses this information to determine how jobs should be generated.

The final jobs therefore receive:

```
subset of dataset files
```

rather than the dataset itself.

This resolution process is normally hidden from the workflow description.

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

# Dataset Resolution in the CMSDiracAux Pipeline

In the CMSDiracAux prototype, dataset resolution is performed in the **translation layer**.

This stage occurs between:

```
WMCore workflow extraction
and
Translation IR construction
```

The dataset resolution process is shown below.

```
WMCore workflow
        │
        ▼
dataset reference
        │
        ▼
DAS query
        │
        ▼
file list (LFNs)
        │
        ▼
Translation IR DataReference
```

The resulting file list is then stored inside the **DataReference entity** of the Translation IR.

---

# Dataset Resolution Pipeline

The dataset resolution workflow implemented in the prototype can be summarized as follows.

```
dataset identifier
        │
        ▼
dasgoclient query
        │
        ▼
block discovery
        │
        ▼
file discovery
        │
        ▼
LFN list
        │
        ▼
Translation IR DataReference
```

This step converts CMS dataset abstractions into **file-level inputs compatible with DIRAC transformations**.

---

# Limiting Dataset Materialization in the Prototype

CMS datasets may contain extremely large numbers of files.

For example:

```
dataset size ≈ thousands of files
```

Materializing all files during development would produce extremely large artifacts.

Therefore the CMSDiracAux prototype introduces a temporary constraint:

```
maximum files per dataset = 20
```

This limit allows the prototype to demonstrate the translation process while keeping the generated artifacts manageable.

The limit is purely a development constraint and is not inherent to the architecture.

---

# Representation in the Translation IR

Once resolved, dataset information is represented in the Translation IR as a **DataReference object**.

Conceptually:

```
DataReference
   dataset identifier
   block identifiers
   file list
```

Only the **file list** is required by the DIRAC execution model, but retaining the dataset and block identifiers provides additional context for workflow translation and debugging.

---

# Interaction with Job Splitting

Dataset resolution is tightly coupled with the **job splitting stage**.

After resolving the file list, the workflow translator can apply the splitting policy defined in the Translation IR.

The resulting process becomes:

```
dataset reference
        │
        ▼
file resolution
        │
        ▼
splitting policy
        │
        ▼
job generation
```

This sequence mirrors the logic implemented in the CMS WMBS subsystem.

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
dataset resolution
        │
        ▼
Translation IR
        │
        ├── DIRAC transformation
        └── CWL workflow
```

By resolving datasets at this stage, the Translation IR becomes independent of the CMS metadata infrastructure.

This ensures that downstream execution systems only receive the **concrete file-level inputs required for execution**.

---

# Importance for Workflow Interoperability

The dataset resolution model is essential for interoperability because it bridges two fundamentally different data abstractions.

```
CMS workflow → dataset abstraction
DIRAC workflow → file-level inputs
```

The translation layer therefore converts **dataset semantics into file semantics** while preserving the workflow structure.

This conversion is a key step in enabling deterministic translation between the two workflow systems.
