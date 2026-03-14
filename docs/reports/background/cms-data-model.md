# **CMS data hierarchy**

* General overview
```text
┌───────────────────────────────────────────────┐
│                 CMS Data Model                │
└───────────────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│                   Dataset                     │
│  Logical collection of CMS event data         │
│  e.g. /PrimaryDataset/Processed/Tier          │
└───────────────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│                    Block                      │
│  Transfer / placement unit inside a dataset   │
│  Groups files for data management             │
└───────────────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│                     File                      │
│  Physical / logical file containing events    │
│  Usually the scheduling / catalog unit        │
└───────────────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│                  Lumi Section                 │
│  Subdivision of a run                         │
│  Common CMS processing / bookkeeping unit     │
└───────────────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│                     Event                     │
│  Atomic physics data record                   │
└───────────────────────────────────────────────┘


Additional orthogonal grouping / metadata dimensions:

┌───────────────────────┐      ┌───────────────────────┐
│          Run          │      │      Data Tier        │
│  Groups lumi sections │      │  RAW / RECO / AOD ... │
└───────────────────────┘      └───────────────────────┘
            │                              │
            └──────────────┬───────────────┘
                           │
                           ▼
               apply across dataset contents
```

* A more explicit CMS-style relation view:

```text
┌──────────┐
│ Dataset  │
└────┬─────┘
     │ contains
     ▼
┌──────────┐
│  Block   │
└────┬─────┘
     │ contains
     ▼
┌──────────┐
│   File   │
└────┬─────┘
     │ contains events from
     ├───────────────────────────────┐
     ▼                               ▼
┌──────────┐                   ┌──────────┐
│ Lumi     │  belongs to       │   Run    │
│ Section  ├──────────────────►│          │
└────┬─────┘                   └──────────┘
     │ contains
     ▼
┌──────────┐
│  Event   │
└──────────┘
```

* **Workflow/input semantics**:

```text
┌───────────────────────────────────────────────┐
│                 CMS Input Data                │
└───────────────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│ InputDataset                                  │
│ /PrimaryDataset/ProcessedDataset/DataTier     │
└───────────────────────────────────────────────┘
                        │
         ┌──────────────┼──────────────┐
         ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Block        │ │ Run whitelist│ │ Lumi mask    │
│ selection    │ │ / blacklist  │ │ / selection  │
└──────┬───────┘ └──────────────┘ └──────────────┘
       │
       ▼
┌──────────────┐
│ File list    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Events       │
└──────────────┘
```


* **Orthogonal relation between storage structure and physics content**.

```text
DATA STORAGE ENTITIES
┌───────── Dataset ─────────┐
│ ┌──────── Block ────────┐ │
│ │ ┌──── File A ───────┐ │ │
│ │ └───────────────────┘ │ │
│ │ ┌──── File B ───────┐ │ │
│ │ └───────────────────┘ │ │
│ │        ...            │ │
│ └───────────────────────┘ │
└───────────────────────────┘


DATA CONTENT OBJECTS
+ - - - - - - - - - - - - - - - +
. Run                           .
.  Lumi → Event → Event         .
.  Lumi → Event → Event         .
.  ...                          .
+ - - - - - - - - - - - - - - - +

Run spans multiple files
Files contain lumisections and events
```

1. **Storage hierarchy**

   ```
   Dataset → Block → File
   ```

2. **Content hierarchy**

   ```
   Run → Lumi Section → Event
   ```

3. **Key CMS property**

* Data contents relation

   * **Runs cross file boundaries**
   * **Files contain lumisections**
   * **Events belong to exactly one lumisection**
  *  **Luminosity sections do not cross file boundaries.**
---

### Correct compact relation

```text
Lumi ⊂ File
File ⊄ Lumi
Event ⊂ Lumi
Event ⊂ File
```

Meaning:

* **Lumi ⊂ File** → a lumi is fully contained in one file
* **File ⊄ Lumi** → a file may contain multiple lumis
* **Event ⊂ Lumi** → events belong to a lumi
* **Event ⊂ File** → events are stored in files


* Run-Files relation

   * **A run can span multiple files**
   * **Run boundaries are not required to coincide with file boundaries**
   * **Therefore a file may contain events from multiple runs**

```
Run ⊄ File
File ⊄ Run
Event ⊂ Run
Event ⊂ File
```


```
┌──────────────────────────────────────────────────────────────┐
│ Dataset                                                      │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Block                                                    │ │
│ │  +-----------------------------------------------------+ │ │
│ │  . Run                                                 . │ │
│ │  .  ┌──────────────┐   ┌──────────────┐   ...          . │ │
│ │  .  │ File A       │   │ File B       │                . │ │
│ │  .  │ ┌──────────┐ │   │ ┌──────────┐ │                . │ │
│ │  .  │ │ Lumi     │ │   │ │ Lumi     │ │                . │ │
│ │  .  │ │ E → E    │ │   │ │ E → E    │ │                . │ │
│ │  .  │ └──────────┘ │   │ └──────────┘ │                . │ │
│ │  .  │ ┌──────────┐ │   │ ┌──────────┐ │                . │ │
│ │  .  │ │ Lumi     │ │   │ │ Lumi     │ │                . │ │
│ │  .  │ │ E → E    │ │   │ │ E → E    │ │                . │ │
│ │  .  │ └──────────┘ │   │ └──────────┘ │                . │ │
│ │  .  │ ...          │   │ ...          │                . │ │
│ │  .  └──────────────┘   └──────────────┘                . │ │
│ │  +-----------------------------------------------------+ │ │
│ └──────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```


# CMS Job Splitting Algorithms

* **Complete list of CMS workflow job-splitting algorithms** used in the **WMCore / WMAgent splitting framework**:

---

| Algorithm            | Unit       | Typical use           |
| -------------------- | ---------- | --------------------- |
| FileBased            | File       | most production       |
| LumiBased            | Lumi       | data reconstruction   |
| EventBased           | Event      | MC                    |
| EventAwareLumiBased  | Lumi       | modern CMS production |
| RunBased             | Run        | rare workflows        |
| BlockBased           | Block      | dataset management    |
| DatasetBased         | Dataset    | special workflows     |
| ProductionEventBased | Event      | MC generation         |
| EventRangeBased      | EventRange | event service         |

---

## **Splitting dimension**

1. **canonical splitting algorithms implemented in WMCore**, and
2. **variants / configuration-driven hybrids** that appear in production workflows.

## 1. File-level splitting

These operate purely on **storage entities** (Files).

### 1. FileBased

Most common.

Splits jobs by **number of input files**.

Typical parameters:

```
files_per_job
max_files_per_job
```

Used for:

* MC processing
* reprocessing
* workflows where file boundaries are safe units

Properties:

```
job_unit = File
```

---

## 2. Lumi-based splitting

Operates on **lumisections**, which are **content objects inside files**.

### 2. LumiBased

Splits jobs by **number of lumisections**.

Parameters:

```
lumis_per_job
```

Used for:

* prompt reconstruction
* skims
* workflows that must preserve lumi boundaries

Properties:

```
job_unit = LumiSection
```

Important constraint:

```
Lumi ∈ File
```

---

## 3. Event-based splitting

Splits purely by **number of events processed**.

### 3. EventBased

Splits jobs by **event count**.

Parameters:

```
events_per_job
```

Used for:

* Monte Carlo generation
* some simulation steps

Properties:

```
job_unit = Event
```

---

## 4. Event-aware lumi splitting

Hybrid splitting.

### 4. EventAwareLumiBased

Splits by **lumisections**, but uses **event counts to size jobs**.

Parameters:

```
events_per_job
max_events_per_lumi
```

Purpose:

* avoid large lumis producing oversized jobs
* maintain lumi integrity

Properties:

```
job_unit = LumiSection
size_metric = EventCount
```

This is very common in CMS production.

---

## 5. Run-based splitting

Rare but supported.

### 5. RunBased

Splits by **run number**.

Used when workflows must **preserve run boundaries**.

Properties:

```
job_unit = Run
```

---

## 6. Lumi-run hybrid splitting

### 6. LumiBased with run whitelist

A configuration-driven variant.

Splits by lumis but **restricted by run masks**.

Used for:

* re-reconstruction
* partial dataset reprocessing

Properties:

```
job_unit = LumiSection
constraint = Run
```

---

## 7. Dataset-level splitting

### 7. DatasetBased

One job processes **entire dataset partitions**.

Rare.

Mostly used for:

* merge workflows
* cleanup steps

---

## 8. Block-based splitting

Splits by **dataset block**.

### 8. BlockBased

Units:

```
job_unit = Block
```

Use cases:

* data placement
* replication workflows
* some large merge steps

---

## 9. Production-style event generation splitting

### 9. ProductionEventBased

Special variant used for MC generation.

Properties:

```
events_per_job
events_per_lumi
```

Important because **MC generation must synthesize lumisections**.

---

## 10. Event-range splitting

Used internally in some generation workflows.

### 10. EventRangeBased

Units:

```
event_range
```

Used in:

* event service
* opportunistic computing

---

## The three *most important* in CMS production

In practice **~95% of CMS workflows use only three**:

```
FileBased
LumiBased
EventAwareLumiBased
```

Everything else is niche.

---


## CMS splitting visualized

```
✂ = job split boundary
```
---

# 1. FileBased splitting

**Jobs are groups of files**

```
┌──────────────────────────────────────────────────────────────┐
│ Dataset                                                      │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Block                                                    │ │
│ │  +-----------------------------------------------------+ │ │
│ │  . Run                                                 . │ │
│ │  .  ✂──────────────┐   ✂──────────────┐   ...          . │ │
│ │  .  │ File A       │   │ File B       │                . │ │
│ │  .  │ ┌──────────┐ │   │ ┌──────────┐ │                . │ │
│ │  .  │ │ Lumi     │ │   │ │ Lumi     │ │                . │ │
│ │  .  │ │ E → E    │ │   │ │ E → E    │ │                . │ │
│ │  .  │ └──────────┘ │   │ └──────────┘ │                . │ │
│ │  .  └──────────────┘   └──────────────┘                . │ │
│ │  +-----------------------------------------------------+ │ │
│ └──────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

Meaning

```
job = N files
```

---

# 2. LumiBased splitting

**Jobs split at lumisection boundaries**

```
┌──────────────────────────────────────────────────────────────┐
│ Dataset                                                      │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Block                                                    │ │
│ │  +-----------------------------------------------------+ │ │
│ │  . Run                                                 . │ │
│ │  .  ┌──────────────┐   ┌──────────────┐   ...          . │ │
│ │  .  │ File A       │   │ File B       │                . │ │
│ │  .  │ ✂──────────┐ │   │ ✂──────────┐ │                . │ │
│ │  .  │ │ Lumi     │ │   │ │ Lumi     │ │                . │ │
│ │  .  │ │ E → E    │ │   │ │ E → E    │ │                . │ │
│ │  .  │ └──────────┘ │   │ └──────────┘ │                . │ │
│ │  .  │ ✂──────────┐ │   │ ✂──────────┐ │                . │ │
│ │  .  │ │ Lumi     │ │   │ │ Lumi     │ │                . │ │
│ │  .  │ │ E → E    │ │   │ │ E → E    │ │                . │ │
│ │  .  │ └──────────┘ │   │ └──────────┘ │                . │ │
│ │  .  └──────────────┘   └──────────────┘                . │ │
│ │  +-----------------------------------------------------+ │ │
│ └──────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

Meaning

```
job = N lumisections
```

---

# 3. EventBased splitting

**Events themselves define the boundary**

```
┌──────────────────────────────────────────────────────────────┐
│ Dataset                                                      │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Block                                                    │ │
│ │  +-----------------------------------------------------+ │ │
│ │  . Run                                                 . │ │
│ │  .  ┌──────────────┐                                   . │ │
│ │  .  │ File A       │                                   . │ │
│ │  .  │ ┌──────────┐ │                                   . │ │
│ │  .  │ │ Lumi     │ │                                   . │ │
│ │  .  │ │ E ✂ E ✂ E│ │                                   . │ │
│ │  .  │ └──────────┘ │                                   . │ │
│ │  .  │ ┌──────────┐ │                                   . │ │
│ │  .  │ │ Lumi     │ │                                   . │ │
│ │  .  │ │ E ✂ E ✂ E│ │                                   . │ │
│ │  .  │ └──────────┘ │                                   . │ │
│ │  .  └──────────────┘                                   . │ │
│ │  +-----------------------------------------------------+ │ │
│ └──────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

Meaning

```
job = N events
```

---

# 4. EventAwareLumiBased splitting

**Jobs split by lumis but sized by events**

```
┌──────────────────────────────────────────────────────────────┐
│ Dataset                                                      │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Block                                                    │ │
│ │  +-----------------------------------------------------+ │ │
│ │  . Run                                                 . │ │
│ │  .  ┌──────────────┐   ┌──────────────┐                . │ │
│ │  .  │ File A       │   │ File B       │                . │ │
│ │  .  │ ✂──────────┐ │   │ ✂──────────┐ │                . │ │
│ │  .  │ │ Lumi     │ │   │ │ Lumi     │ │                . │ │
│ │  .  │ │ E → E    │ │   │ │ E → E    │ │                . │ │
│ │  .  │ │ E → E    │ │   │ │ E → E    │ │                . │ │
│ │  .  │ └──────────┘ │   │ └──────────┘ │                . │ │
│ │  .  │ ✂──────────┐ │   │ ✂──────────┐ │                . │ │
│ │  .  │ │ Lumi     │ │   │ │ Lumi     │ │                . │ │
│ │  .  │ │ E → E    │ │   │ │ E → E    │ │                . │ │
│ │  .  │ └──────────┘ │   │ └──────────┘ │                . │ │
│ │  .  └──────────────┘   └──────────────┘                . │ │
│ │  +-----------------------------------------------------+ │ │
│ └──────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

Meaning

```
split_unit = lumi
job_size ≈ events_per_job
```

---

# 5. RunBased splitting (rare)

Cuts along **Run boundary**.

```
+-----------------------------------------------------+
. Run 1                                               .
.                                                     .
+-----------------------------------------------------+

+-----------------------------------------------------+
. Run 2                                               .
.                                                     .
+-----------------------------------------------------+
```

---

# Importance for the CMS vs. DIRAC interoperability

This immediately exposes the **core mismatch** between CMS and DIRAC:

CMS splitting units:

```
File
Lumi
Event
```

But **Run spans files**.

So when translating CMS workflows to DIRAC transformations:

```
run constraints
must be projected onto file-level job units
```

—which is exactly the architectural tension your **translation layer must resolve**.

