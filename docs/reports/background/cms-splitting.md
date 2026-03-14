# CMS Workflow Splitting Model — Storage vs Content Hierarchy

### 1. CMS Data Hierarchy

CMS workflows operate on a data model that separates **storage entities** from **physics/content entities**.

**Storage hierarchy**

```
Dataset
 └ Block
    └ File
```

Datasets are logical collections of data.
Files within datasets are grouped into **blocks** to support scalable data management and placement across distributed storage systems.

**Content hierarchy**

```
Run
 └ Lumi Section
    └ Event
```

* **Run** – period of detector operation with consistent configuration
* **Luminosity section (lumi)** – small time slice within a run (~23 seconds)
* **Event** – individual collision record

The two hierarchies intersect but are not identical.

Key containment relations:

```
File ⊃ Lumi ⊃ Event
```

However:

```
Run groups lumisections but is not a storage container
```

Runs therefore **span multiple files**, while lumisections and events remain contained within a single file.

---

### 2. Workflow Splitting as Partitioning

CMS workflow splitting algorithms determine how input data are partitioned into independent processing jobs.

Conceptually, splitting can be modeled as a **partition operator**:

```
Split(level, size)
```

where

| Parameter | Meaning                                      |
| --------- | -------------------------------------------- |
| level     | hierarchy level at which partitioning occurs |
| size      | job sizing metric                            |

The splitting algorithm determines which objects are grouped into each job.

---

### 3. Confirmed CMS Splitting Algorithms

The commonly used CMS workflow splitting modes are:

| Algorithm           | Partition Level | Job Size Metric                      |
| ------------------- | --------------- | ------------------------------------ |
| FileBased           | File            | files per job                        |
| LumiBased           | Lumisection     | lumisections per job                 |
| EventAwareLumiBased | Lumisection     | events per job                       |
| EventBased          | Event           | events per job (primarily PrivateMC) |

The first three are the dominant modes used in CMS production and analysis workflows.

---

### 4. Example Partitions

#### FileBased

```
Jobs = partition(Files, files_per_job)
```

Example:

```
[FileA FileB] → Job1
[FileC FileD] → Job2
```

Each job processes a fixed number of input files.

---

#### LumiBased

```
Jobs = partition(Lumis, lumis_per_job)
```

Example:

```
[L1 L2 L3] → Job1
[L4 L5 L6] → Job2
```

Because lumisections are contained within files, file boundaries must still be respected.

---

#### EventBased

```
Jobs = partition(Events, events_per_job)
```

Jobs process a specified number of events regardless of lumisection boundaries.
This mode is primarily used in Monte-Carlo generation workflows.

---

#### EventAwareLumiBased

This hybrid algorithm partitions by lumisection but sizes jobs according to the total number of events.

```
Jobs = partition(Lumis)
subject to

Σ events(lumi_i) ≈ events_per_job
```

Thus:

```
split_unit = lumi
job_size_metric = events
```

Each job still processes **complete lumisections**, but the grouping is determined by event counts.

---

### 5. Projection onto File-Based Execution

Although splitting may be defined at the **lumi or event level**, actual execution requires **file inputs**.

Therefore each job description must be expressed as a set of files containing the required content.

Conceptually this is a **projection problem**:

```
Projection:
Split(Level X) → File-based job description
```

Examples:

**LumiBased**

```
job files = files containing the selected lumisections
```

**EventBased**

```
job files = files containing the selected events
```

**EventAwareLumiBased**

```
job files = files containing the selected lumisections
job size determined by summed event counts
```

---

### 6. Translation IR Representation

A useful intermediate representation for workflow translation can therefore be expressed as:

```
Job = {
  files,
  lumis,
  event_range
}
```

Where:

* `files` represent the physical execution input
* `lumis` and `event_range` act as selection constraints

This representation cleanly separates **storage objects** from **content filters**.

---

### 7. Minimal Formal Model

CMS splitting can be normalized into a three-parameter abstraction:

```
Split(level, weight, boundary)
```

| Parameter | Meaning                           |
| --------- | --------------------------------- |
| level     | hierarchy level of the split unit |
| weight    | metric used to size jobs          |
| boundary  | containment constraint            |

Example mappings:

| Algorithm           | level | weight | boundary |
| ------------------- | ----- | ------ | -------- |
| FileBased           | File  | files  | file     |
| LumiBased           | Lumi  | lumis  | file     |
| EventAwareLumiBased | Lumi  | events | file     |
| EventBased          | Event | events | lumi     |

---

### 8. Structural Insight

The hierarchy implies the following relationships:

```
File ⊃ Lumi ⊃ Event
Run ⊃ Lumi
```

Consequences:

* File-level splitting is always compatible with storage organization.
* Lumi and event splitting require projection onto files.
* Run boundaries do not align with storage units.

---

### 9. Implications for Workflow Translation

Any system translating CMS workflows to another execution model must therefore handle the mapping:

```
content-level splitting
        ↓
file-level execution units
```

The translation layer must project run/lumi/event constraints onto the files that contain the corresponding data.

This separation between **storage hierarchy** and **content hierarchy** is the key architectural constraint governing CMS workflow splitting.
