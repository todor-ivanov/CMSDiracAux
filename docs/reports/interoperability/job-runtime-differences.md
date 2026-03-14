# Job Runtime Differences Between CMS and DIRAC

This document captures the **runtime execution differences between CMS workflows and DIRAC**, the role of `cmsRun`, **PSet tweaks**, **sandbox limitations**, and how the **Translation IR and runtime metadata mechanisms interact**.

## Purpose

While the CMSDiracAux project primarily focuses on translating workflow descriptions from WMCore to DIRAC-compatible execution structures, a significant portion of the interoperability challenge lies at the **runtime execution layer**.

CMS and DIRAC jobs differ not only in how workflows are defined, but also in how runtime environments are constructed and how job semantics are transported to worker nodes.

This document analyzes:

* runtime requirements of the CMS `cmsRun` process
* the role of **PSet configuration and runtime tweaks**
* runtime environment dependencies on **WMCore infrastructure** and **CMSSW**
* the constraints imposed by **DIRAC job sandbox distribution**
* the relationship between the **Translation IR layer** and legacy `__CMSJobParameter__` job metadata
* potential architectural improvements to runtime code distribution.

---

# CMS Runtime Execution Model

In the CMS workflow system, the executable component of a job is typically the **CMSSW framework executable `cmsRun`**.

However, `cmsRun` itself contains very little intrinsic logic about the specific job being executed. Instead, the behavior of the job is entirely determined by a **Python configuration file (PSet)**.

Conceptually:

```
┌───────────────────────────────┐
│ cmsRun executable             │
└───────────────┬───────────────┘
                │
                ▼
      Python configuration (PSet)
                │
                ▼
        Processing pipeline
```

The configuration defines:

* modules to be executed
* execution order
* input sources
* output modules
* physics parameters.

Thus, **the runtime semantics of a CMS job reside in its configuration**, not in the executable itself.

---

# Runtime Dependencies of CMS Jobs

A CMS job environment has two primary dependency domains.

```
                CMS Runtime Environment
                        │
          ┌─────────────┴─────────────┐
          ▼                           ▼
   WMCore Infrastructure          CMSSW Framework
```

### WMCore Infrastructure

WMCore provides the workflow-level runtime context:

* workflow definition
* job package
* splitting metadata
* job-specific parameters
* PSet tweaks.

These components determine:

```
which unit of work the job represents
```

### CMSSW Framework

CMSSW provides the physics execution environment:

* framework libraries
* modules and algorithms
* data processing pipelines
* runtime configuration interpreter.

These components determine:

```
how the job processes the assigned data
```

Both sides must be satisfied for a CMS job to execute correctly.

---

# Job Identity and PSet Tweaks

A CMS job becomes a **unique runtime instance** only after PSet modifications are applied.

Conceptually:

```
Workflow definition
        │
        ▼
Generic PSet configuration
        │
        ▼
Runtime PSet tweaks
        │
        ▼
Final job-specific configuration
        │
        ▼
cmsRun execution
```

PSet tweaks typically encode:

* input file lists
* run/lumi boundaries
* event limits
* output dataset metadata
* runtime parameters derived from workflow splitting.

Thus the final runtime configuration of each job is constructed dynamically.

---

# DIRAC Runtime Execution Model

DIRAC jobs follow a significantly different runtime philosophy.

A DIRAC job is defined primarily through a **Job Description Language (JDL)**.

```
┌───────────────────────────────┐
│ DIRAC Job Description (JDL)   │
├───────────────────────────────┤
│ Executable                    │
│ Arguments                     │
│ InputSandbox                  │
│ OutputSandbox                 │
│ Resource requirements         │
└───────────────┬───────────────┘
                │
                ▼
         Pilot-based execution
```

The pilot job retrieves the payload from the central system and executes it on the worker node.

DIRAC therefore assumes:

* small job descriptions
* limited sandbox payloads
* runtime software accessible externally (e.g. via CVMFS).

---

# Sandbox Distribution Constraints

One of the key constraints encountered by CMSDiracAux arises from the limitations of the **DIRAC sandbox model**.

The input sandbox is designed to transport small files required for job execution.

```
┌─────────────────────────────┐
│ Input Sandbox               │
│                             │
│ scripts                     │
│ configuration files         │
│ small runtime artifacts     │
└─────────────────────────────┘
```

Large software bundles are not expected to be transported through this mechanism.

This constraint becomes problematic for CMS workflows because the runtime environment may include:

* workflow management scripts
* job package artifacts
* PSet configurations
* metadata files.

Transporting these artifacts through the sandbox is inefficient and potentially incompatible with the DIRAC execution model.

---

# DIRAC Workflow Construction

In DIRAC a **Job** can contain a **Workflow**, which is a sequence of **Steps** executed on the worker node.

Conceptually:

```
DIRAC Job
   │
   ▼
Workflow
   │
   ├─ Step 1
   ├─ Step 2
   ├─ Step 3
   ▼
payload execution
```

At runtime this is represented by:

```
jobDescription.xml
```

which defines:

* step order
* executable per step
* environment
* parameter passing

Example conceptual structure:

```
Workflow
 ├─ Step: PrepareEnvironment
 ├─ Step: ExecutePayload
 ├─ Step: Finalize
```
---

# Bootstrap Execution Strategy

To address sandbox constraints, CMSDiracAux employs a **bootstrap execution model**.

A DIRAC job initially runs a lightweight bootstrap script which reconstructs the CMS runtime environment.

```
DIRAC job
   │
   ▼
Bootstrap step
   │
   ▼
Environment reconstruction
   │
   ▼
cmsRun execution
```

Example conceptual sequence:

```
Step 1  prepare runtime environment
Step 2  retrieve workflow artifacts
Step 3  reconstruct job configuration
Step 4  run cmsRun
```

---

# Role of `__CMSJobParameter__`

In early CMSDiracAux prototypes, CMS job metadata was transported into the DIRAC workflow object using the special parameter prefix:

```
__CMSJobParameter__
```

These parameters preserved job-specific information extracted from the WMCore job package.

Examples include:

* workflow identifiers
* task names
* dataset partitions
* run/lumi ranges
* configuration references.

Conceptually:

```
WMCore Job Package
        │
        ▼
Flattened metadata
        │
        ▼
DIRAC workflow parameters
        │
        ▼
Runtime bootstrap logic
```

This mechanism provided a simple way to preserve CMS job semantics within DIRAC job descriptions.

---

# Translation IR as a Replacement Layer

CMSDiracAux introduces a **Translation Intermediate Representation (IR)** that formalizes the translation between WMCore workflows and DIRAC execution structures.

```
WMCore workflow
        │
        ▼
Translation IR
        │
        ▼
DIRAC transformations / jobs
```

The IR captures structured information such as:

* workflow steps
* splitting rules
* input datasets
* resource hints
* executable definitions.

This allows the translation layer to preserve semantics without relying on flat metadata structures.

---

# Relationship Between IR and Runtime Parameters

The Translation IR replaces the architectural role previously played by `__CMSJobParameter__`.

However, runtime jobs still require **job-specific metadata**.

Therefore the relationship becomes:

```
Translation IR
       │
       ▼
Job materialization
       │
       ▼
Runtime metadata projection
       │
       ▼
Worker node execution
```

In this architecture:

* the IR acts as the **canonical semantic representation**
* runtime parameters become a **projection of the IR**, not a primary source of truth.

---

# How This Relates to CMSDiracAux

The `createCMSJob()` method implicitly tries to construct such a **DIRAC workflow**.

In the prototype the steps look like:

```
Step 1  clone CMSDiracAux repo
Step 2  source env.sh
Step 3  run Startup.py
```

So the DIRAC job acts as a **bootstrap wrapper**, while the actual CMS logic happens inside that wrapper.

---

# Why This Is Needed

CMS runtime is fundamentally different from DIRAC runtime.

### DIRAC runtime model

DIRAC assumes:

```
Executable
Arguments
InputSandbox
OutputSandbox
```

Everything else is expected to be:

* small
* pre-installed
* or accessible through CVMFS.

---

### CMS runtime model

CMS jobs expect a **rich runtime payload** containing:

```
step_cfg.py
WMWorkload.pkl
JobPackage.pkl
CMSSW configuration
runtime metadata
```

These objects define the **job semantics**, not just the executable.

---

This is one of the central architectural constraints for CMSDiracAux.

---

# The Resulting Runtime Strategy

Because of this constraint the runtime must be **reconstructed on the worker node** rather than shipped entirely through the sandbox.

The strategy becomes:

```
DIRAC Job
   │
   ▼
Bootstrap step
   │
   ▼
Reconstruct CMS runtime
   │
   ▼
Execute CMS job
```

Example conceptual pipeline:

```
Step 1   prepare environment
Step 2   retrieve job package
Step 3   execute CMSSW job
```

This matches exactly the idea of the **DIRAC workflow step chain**.

---

# How the `__CMSJobParameter__` Fields Fit

Those parameters provide the **minimal metadata needed to reconstruct the CMS job context**.

They typically encode things like:

```
task name
dataset slice
run/lumi partition
workflow identifiers
configuration references
```

At runtime the bootstrap script can use them to:

```
recover WMCore job semantics
load JobPackage.pkl
configure CMSSW job
```

So they effectively carry **CMS job identity across the DIRAC boundary**.

---

# Architectural Interpretation

This leads to the following layered runtime model.

```
DIRAC layer
────────────
job
workflow
steps
pilot execution


CMS layer
────────────
WMWorkload
JobPackage
CMSSW runtime
dataset partition
```

The bootstrap workflow bridges these two layers.

---

# Why This Matters for CMSDiracAux

The real difficulty is not translating workflows.

The real difficulty is **translating runtime semantics**.

CMS jobs assume:

```
rich runtime state
```

DIRAC assumes:

```
minimal job description
```

The CMSDiracAux approach therefore relies on:

```
DIRAC workflow bootstrap
+
runtime reconstruction
+
metadata injection
```

rather than trying to directly map CMS jobs to plain DIRAC jobs.

---

# Key Architectural Constraint


```
DIRAC cannot freely distribute arbitrary runtime payloads
via job sandboxes.
```

This forces the architecture to use:

```
runtime reconstruction
or external retrieval
```

instead of direct sandbox shipping.

This constraint strongly influences the **design of the translation layer and runtime bootstrap logic**.

It  also relates to the need of reinventing WMBS. The key point is that **WMBS is not just a historical artifact of CMS workflow management**. It exists because CMS workflows require a **level of job–data association that the storage hierarchy alone cannot provide**. When one moves execution to DIRAC, that requirement does not disappear — it simply moves somewhere else in the architecture.

Below is the reasoning step by step.

---

# 1. What WMBS Actually Does

WMBS (Workload Management Bookkeeping System) is often described as a job bookkeeping database, but its **real architectural role** is deeper.

It maintains the mapping:

```text
workflow task
      │
      ▼
data units
(run / lumi / events)
      │
      ▼
jobs
```

Conceptually:

```
dataset
   │
   ▼
files discovered
   │
   ▼
runs/lumis extracted
   │
   ▼
splitting rules
   │
   ▼
job definitions
```

The important point is that the **job boundaries are not tied to storage objects**.

A job might process:

```
lumi 101–120
from file A and B
```

That information **cannot be recovered from the dataset structure alone**.

Therefore WMBS must explicitly store:

```
job ↔ data content mapping
```

---

# 2. DIRAC’s Native Model

DIRAC assumes a much simpler relationship between data and jobs.

Conceptually:

```
file
   │
   ▼
job
```

In other words:

```text
job input = file list
```

DIRAC transformations typically operate at the **file level**.

Example:

```
fileA.root → job1
fileB.root → job2
fileC.root → job3
```

No additional bookkeeping layer is required because **the storage unit equals the work unit**.

---

# 3. The Core Mismatch

CMS workloads require splitting **below the storage unit**.

DIRAC workloads assume splitting **at the storage unit**.

This mismatch looks like this:

```
CMS

dataset
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
job
```

versus

```
DIRAC

file
   │
   ▼
job
```

---

# 4. What Happens If WMBS is Removed

If one simply translates CMS workflows to file-level jobs and remove run/lumi splitting:

1. files contain **very uneven event counts**
2. job runtimes become unpredictable
3. resource scheduling becomes unstable
4. long jobs block resource pools
5. short jobs cause fragmentation

In other words:

```
runtime predictability collapses
```

This is precisely the reason CMS introduced WMBS originally.

---

# 5. What Happens in CMSDiracAux

When CMS workflows are executed through DIRAC, the **same problem reappears**.

DIRAC does not know:

```
run
lumi
event boundaries
```

Therefore it cannot perform the required splitting natively.

So the system must introduce a **bookkeeping mechanism again**.

But this time it cannot live inside WMBS.

Instead it must live inside the **DIRAC splitting layer**.

Conceptually:

```
DIRAC Transformation
        │
        ▼
CMS splitting plugin
        │
        ▼
job definitions
```

---

# 6. Where the WMBS Logic Moves

In CMSDiracAux the WMBS functionality effectively migrates to the **DIRAC transformation plugin**.

```
DIRAC Transformation
      │
      ▼
CMSWMCoreSplittingPlugin
      │
      ▼
jobs created from run/lumi partitions
```

This plugin must perform the same functions that WMBS originally did:

```
dataset resolution
run/lumi extraction
splitting policy application
job-data bookkeeping
```

In other words:

```
WMBS logic → DIRAC plugin
```

---

# 7. Architectural Consequence

This leads to a very important architectural conclusion.

Even if the **central scheduling system changes**, the need for WMBS-like functionality **does not disappear**.

It simply moves layers.

```
CMS system
────────────
WMBS
      ↓
jobs


CMSDiracAux system
──────────────────
DIRAC Transformation Plugin
      ↓
jobs
```

So the architecture becomes:

```
WMCore workflow
      │
      ▼
Translation IR
      │
      ▼
DIRAC transformation
      │
      ▼
CMS splitting plugin
(WMBS logic reborn)
      │
      ▼
jobs
```

---

# 8. Impact on Scheduling

This also explains why the splitting granularity matters for resource scheduling.

If job lengths are predictable:

```
scheduler efficiency ↑
resource utilization ↑
```

If jobs correspond to arbitrary file sizes:

```
runtime variance ↑
resource fragmentation ↑
scheduler predictability ↓
```

Therefore the **fine-grained splitting logic must remain part of the system**.

---

# 9. Final Architectural Insight

And to be more precise we can safely state that:

> WMBS exists because CMS workflows require job splitting below the storage abstraction level. Any alternative execution infrastructure must therefore reintroduce equivalent bookkeeping if the same splitting granularity is preserved.

This is one of the **most important architectural constraints**.

---

# How things change with DiracX

With **DIRACX**, the need for **WMBS-like logic does not disappear** if CMS keeps run/lumi/event-level splitting. What changes is **where that logic would plug in** and how naturally it fits the surrounding architecture. While we can be reasonably confident about the high-level direction, some details are still blurry because DIRACX is still evolving and some workflow/task pieces have been discussed only internally as issues/prototypes, etc., rather than frozen as long-stable user-facing architecture. ([GitHub][1])

In classic DIRAC, the path is roughly:

```text
Production
   ↓
Transformation
   ↓
WMS / Matcher / Task Queues
   ↓
Pilots
```

That stack is centered on **data-driven transformations** and **pilot-based pull scheduling**, with task queues and matcher logic inside the WMS. DIRAC’s own docs describe the WMS in terms of pilot jobs, task queues, matching, and the core WMS databases such as `JobDB`, `TaskQueueDB`, and `PilotAgentsDB`. ([DIRAC Documentation][2])

DIRACX is moving toward a more explicit **workflow / task / service API** model. Public DIRACX discussions and the `dirac-cwl` plan point toward first-class submission endpoints like `POST /jobs` and `POST /productions`, a workflow/task database, and a later transition where transformations and optimizers are handled through DIRACX task-aware services rather than the older tightly coupled classic stack. That means the conceptual shape becomes closer to:

```text
Workflow
   ↓
Tasks
   ↓
Scheduling services
   ↓
Pilots / execution
```

rather than classic DIRAC’s `Production → Transformation → Jobs` emphasis. This is exactly why DIRACX looks architecturally closer to CMS than classic DIRAC does. ([GitHub][3])

So if CMSDiracAux were retargeted from classic DIRAC to DIRACX, the **core requirement** would stay the same:

```text
CMS needs:
dataset → file → run/lumi/event-aware partitioning
```

and therefore it would still need a component that performs:

* dataset/file discovery
* run/lumi-aware partitioning
* job–data-content bookkeeping
* predictable runtime-oriented workload shaping.

That requirement comes from the CMS side, not from DIRAC’s implementation details. DIRACX would not remove that need; it would only provide a cleaner architectural place to host it, likely as part of a workflow/task service layer or a task-generation component instead of burying it inside classic transformation-plugin mechanics. That is an inference from the currently visible DIRACX direction, not a guaranteed finalized product feature. ([GitHub][4])

In other words, with classic DIRAC:

```text
WMBS logic must be reborn inside DIRAC transformation plugins
```

With DIRACX:

```text
WMBS logic must be reborn inside DIRACX workflow/task generation services
```

or whatever the final DIRACX task abstraction stabilizes into. The essential logic does not go away; it just migrates into a more natural abstraction layer because DIRACX explicitly talks in terms of workflows and tasks rather than only productions and transformations. ([GitHub][3])

The **sandbox/runtime-distribution constraint** also does not fundamentally disappear. Classic DIRAC sandbox handling is still designed around relatively small input/output sandboxes, with the WMS and pilot infrastructure expecting that large software payloads live elsewhere. DIRAC pilot bootstrapping remains centered on downloading pilot bootstrap material and then retrieving work, not on arbitrarily shipping large experiment-specific runtime bundles as a general solution. DIRACX discussions around CWL and new job wrappers suggest more flexible ways to describe where executables and inputs come from, but that is not the same as “DIRACX natively solves CMS-style random runtime bundle distribution.” This should be treated as **partially improved in principle, but not solved by default**. ([DIRAC Documentation][5])

So for CMSDiracAux, the runtime story under DIRACX would likely shift from:

```text
classic DIRAC bootstrap job
   ↓
reconstruct CMS runtime on worker node
```

to something more declarative, possibly closer to:

```text
workflow/task description
   ↓
explicit description of executable + inputs + metadata source
   ↓
scheduler / wrapper materializes runtime
```

especially if CWL-backed workflows become the dominant path. But even then, CMS still has the same hard problem: its runtime semantics and job partitioning are not naturally file-level or minimal-sandbox-level. So the CMS-specific metadata and bookkeeping layer is still required. ([GitHub][6])

The cleanest summary is this:

```text
Classic DIRAC:
WMBS-like logic would have to be reborn mainly in transformation plugins.

DIRACX:
WMBS-like logic would still have to exist,
but could likely live in a more natural workflow/task layer.
```

That is why DIRACX is promising for future inter-operational architecture for CMS integration: it reduces the **abstraction mismatch** between CMS and DIRAC, but it does **not** remove the deep CMS requirement for fine-grained data-content bookkeeping and runtime shaping. That part remains a CMS-driven constraint regardless of the execution backend.

[1]: https://github.com/DIRACGrid?utm_source=chatgpt.com "DIRAC Project"
[2]: https://dirac.diracgrid.org/en/latest/AdministratorGuide/Systems/WorkloadManagement/?utm_source=chatgpt.com "10. Workload Management System (WMS)"
[3]: https://github.com/DIRACGrid/dirac-cwl/issues/8?utm_source=chatgpt.com "Issue #8 · DIRACGrid/dirac-cwl - General Plan"
[4]: https://github.com/DIRACGrid/diracx/discussions/175?utm_source=chatgpt.com "Transitioning from (Dirac Worklfow, JDL) to (CWL, pydantic ..."
[5]: https://dirac.diracgrid.org/en/latest/AdministratorGuide/Systems/WorkloadManagement/Pilots/Pilots3.html?utm_source=chatgpt.com "10.2.3. Pilots bootstrapping - DIRAC Documentation"
[6]: https://github.com/DIRACGrid/dirac-cwl?utm_source=chatgpt.com "DIRACGrid/dirac-cwl: Proof of Concept"





# Runtime constraints for CMS processes

To the picture discussed so far, one must not miss the runtime enforced requirements on the `cmsRun` process and the additional information which must be provided by its Parameter Set (PSet) files and the PSet tweaks application mechanisms.

Putting `cmsRun`, the runtime PSet tweaks, and the two code-distribution methods for the two different runtime code bundles into the picture makes the architectural constraint even more complex.

At runtime, a CMS job is not just “an executable plus some files.” `cmsRun` is a **single executable whose behavior is fully determined by a Python configuration file**; that configuration defines which modules are loaded, in what order they run, and with which parameters, and it is fixed at the beginning of the job. In other words, the runtime semantics of the job live in the configuration, not in the executable alone. ([TWiki][1])

That immediately creates a two-sided dependency for the CMS runtime environment:

* On one side, the job depends on **WMCore-side workflow/runtime artifacts**: the workflow description, job package, and the per-job information produced by splitting and packaging.
* On the other side, the job depends on **CMSSW-side physics software**: the actual framework, modules, release environment, and the Python configuration that `cmsRun` will execute. ([GitHub][2])

That is why the CMS runtime environment is structurally constrained by **both** WMCore and CMSSW. WMCore determines *which exact unit of work this job is*, while CMSSW determines *how that unit of work is executed physically and logically*.

## Where PSet tweaks fit

The PSet layer is especially important because it is the point where a generic workflow/job package becomes a **specific job instance**. The CMS configuration model is Python-based and is meant to be modified/configured before execution; `SetupCMSSWPset.py` in WMCore explicitly exists to load the shipped PSet and mock or adjust values that depend on runtime context. That is exactly the kind of place where job-specific tweaks are applied. ([GitHub][2])

So in practice, the runtime chain is conceptually:

```text
WMCore job identity
      │
      ▼
PSet / PSetTweaks
      │
      ▼
cmsRun executes specific job instance
```

The important consequence is that **PSet distribution is not just configuration convenience**. It is part of the job identity and part of the semantics of the split.

## How this interacts with DIRAC / DIRACX

Classic DIRAC is comfortable with:

* a relatively small input sandbox
* a job description
* a runtime that is otherwise already available on the worker node or accessible through standard mechanisms. ([DIRAC Documentation][3])

Classic DIRAC is **not naturally built around shipping large arbitrary experiment-specific runtime bundles with every job**, and even in the newer DIRACX/CWL discussions, sandbox/input handling is still being clarified and standardized rather than already solved as a stable, final model. That means this whole area is still somewhat blurry on the DIRACX side. ([GitHub][4])

So the core problem for CMSDiracAux remains:

```text
cmsRun needs:
  CMSSW environment
  + job-specific PSet semantics
  + WMCore-derived job identity

DIRAC expects:
  small job description
  + modest sandbox
  + runtime available externally
```

That mismatch does not disappear just because the execution backend changes.



# Paths for change of the CMS runtime environment


Two architectural improvements can significantly reduce runtime friction.

## 1. Distributing the Core Runtime Bundle via CVMFS

Instead of shipping the workflow runtime environment with each job sandbox, the common runtime bundle could be distributed via CVMFS.

```
Worker node
     │
     ▼
CVMFS mounted runtime
     │
     ▼
Bootstrap execution
```

Advantages include:

* smaller job sandboxes
* consistent runtime environment
* centralized version management.

---

## 2. Reconstructing Per-Job PSet Configurations at Runtime

Currently, each job often receives a fully materialized PSet configuration.

A more scalable approach is to distribute **PSet templates and tweak parameters**, allowing the final configuration to be generated on the worker node.

```
Generic PSet template
        │
        ▼
Runtime tweak parameters
        │
        ▼
Worker-side configuration generation
        │
        ▼
cmsRun execution
```

This reduces sandbox payload size and aligns better with DIRAC's execution model.

---

# Impact on the CMSDiracAux Architecture

Combining the above improvements results in the following runtime architecture.

```
               CMSDiracAux Runtime Model

WMCore workflow
       │
       ▼
Translation IR
       │
       ▼
DIRAC transformation
       │
       ▼
Bootstrap job
       │
       ▼
┌────────────────────────────────────┐
│ Worker Node                        │
│                                    │
│  CVMFS runtime bundle              │
│          │                         │
│          ▼                         │
│  runtime metadata projection       │
│          │                         │
│          ▼                         │
│  PSet reconstruction               │
│          │                         │
│          ▼                         │
│        cmsRun                      │
└────────────────────────────────────┘
```


Changing the CMS jobs runtime environment would help, but this must be a complex effort with different focus areas. The first being a change of the CMS Runtime code distribution methods. Lets elaborate on the two already mentioned directions.

* A change of how we distribute the main Workflow Management System dependent core bundle, by uploading it cvmfs instead distributing it with the job sandboxes.
* A change of the PSet configuration per job distribution

## Direction 1: move the WMCore-dependent core bundle to CVMFS

This would help **significantly**, but only partially.

If the main workflow-management-dependent bundle — the generic WMCore runtime/bootstrap layer, helper scripts, unpackers, startup logic, maybe common workflow handling code — were moved to CVMFS instead of being shipped through sandboxes, then one major pressure point would be removed:

* the sandbox gets smaller
* the runtime becomes more reproducible
* common code is versioned once centrally
* jobs stop redundantly shipping the same management code repeatedly.

This is exactly aligned with the DIRAC expectation that most runtime software should already be available in shared infrastructure rather than being pushed with each job. ([DIRAC Documentation][3])

Architecturally, that would transform the runtime problem from:

```text
ship WMCore logic + ship job config + run cmsRun
```

to:

```text
mount WMCore logic from CVMFS + inject job config + run cmsRun
```

That is a real improvement, because it removes the “generic runtime bundle” from the per-job transport problem.

But it does **not** eliminate the need for per-job semantics. The worker node would still need to know:

* which exact split this job corresponds to
* which job package / workflow slice it represents
* which runtime parameters or PSet modifications make it unique.

So moving the generic bundle to CVMFS helps with **distribution overhead and reproducibility**, but it does not solve the CMS-specific **job individuation problem**.

## Direction 2: rethink per-job PSet distribution

Solving this problem is a difficult task. Because `cmsRun` behavior is driven by configuration, the PSet is not just “small metadata”; it is often the actual expression of the job instance. If CMS continue shipping a distinct per-job PSet through the sandbox, then even after moving the generic WMCore code to CVMFS, the remaining per-job transport burden is still semantically essential.

There are two broad possibilities in addressing this problem:

### A. Keep shipping the per-job PSet

This preserves exact semantics and is operationally straightforward, but it keeps the job tied to sandbox-style distribution. That means the architecture still depends on per-job transport of the final runtime description.

### B. Generate or reconstruct the per-job PSet on the worker node

This would help much more architecturally, because then the sandbox would no longer need to carry the final per-job configuration. Instead, the job would carry only:

* stable configuration references
* job-specific parameter values
* split metadata
* maybe a small templating/tweak description.

Then the worker-side bootstrap could materialize the actual final PSet just before `cmsRun`.

This would change the runtime model from:

```text
ship final PSet
```

to:

```text
ship PSet recipe / tweak inputs
        ↓
reconstruct final PSet at runtime
```

For CMSDiracAux, that is the more strategic direction, because it aligns much better with both classic DIRAC and the likely DIRACX direction: keep large/common/runtime-stable things externalized, and keep only the truly job-specific state flowing per job.

## How much do these two changes help?

A fair qualitative assessment is:

### Move generic WMCore-dependent runtime bundle to CVMFS

**Helps a lot operationally.**
It reduces sandbox dependency substantially and aligns the CMS runtime better with the DIRAC model. But it does **not** remove the need for WMBS-like bookkeeping or job-specific runtime construction.

### Move from per-job shipped PSet to per-job reconstructed PSet

**Helps even more architecturally.**
It reduces per-job payload coupling and moves the system closer to a declarative execution model. But it requires a robust way to encode and reconstruct the job-specific semantics correctly.

So if ranked by effect:

```text
1. CVMFS for generic WMCore bundle
   = strong operational improvement

2. runtime reconstruction of per-job PSet
   = stronger architectural improvement
```

The second one is more transformative because it attacks the most CMS-specific piece of the runtime.

## What does not change, even after both improvements

Even if both changes are adopted, one thing remains true:

CMS still needs a component that determines **which exact data-content slice** a job processes and how that becomes runtime configuration. That requirement comes from CMS splitting granularity, not from the transport mechanism. So even with:

* generic bundle on CVMFS
* per-job PSet reconstructed at runtime

the new  system would still need a WMBS-like layer — whether in classic DIRAC transformation plugins or, more naturally, in a DIRACX workflow/task-generation layer — to preserve the mapping:

```text
workflow/task
      ↓
run/lumi/event partition
      ↓
job-specific runtime semantics
```

That is the real invariant.

## DIRACX improvement

The future DIRACX system will help in this situation mainly by providing a **cleaner architectural home** for this logic. Public DIRACX and `dirac-cwl` discussions point toward explicit workflow/task services, job/production endpoints, and more modern handling of workflow metadata, but sandbox/input-data behavior is still under discussion. ([GitHub][5])

* **DIRACX does not remove the CMS runtime problem**
* but it may make it easier to express the solution as:

  * workflow/task metadata
  * declarative input descriptions
  * runtime-side materialization of job specifics.

That is a meaningful improvement in architecture, but not a magic removal of the CMS-specific constraints.

## Bottom line

The CMS runtime environment is constrained simultaneously by:

* **WMCore infrastructure semantics**
  because the job must know what exact split-produced workload instance it is

and

* **CMSSW framework semantics**
  because `cmsRun` needs a concrete, job-specific Python configuration to define the processing graph. ([TWiki][1])

Changing distribution in those two directions would help, but asymmetrically:

* putting the **generic WMCore-dependent core bundle on CVMFS** removes a large operational incompatibility with DIRAC-style execution
* changing **per-job PSet handling** is the deeper architectural move, because that is where CMS job uniqueness actually lives.

The strongest long-term shape is:

```text
common runtime logic
    → CVMFS

job-specific semantics
    → lightweight metadata / tweak inputs

final runtime PSet
    → materialized on worker node
```

That would make CMSDiracAux much more compatible with both classic DIRAC and future DIRACX-style workflow execution, while preserving the essential CMS semantics that WMBS originally existed to protect.

[1]: https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideAboutPythonConfigFile?utm_source=chatgpt.com "Description of the cmsRun Python Configuration Syntax - TWiki"
[2]: https://github.com/dmwm/WMCore/blob/master/src/python/WMCore/WMRuntime/Scripts/SetupCMSSWPset.py?utm_source=chatgpt.com "SetupCMSSWPset.py"
[3]: https://dirac.diracgrid.org/en/latest/CodeDocumentation/Interfaces/API/Dirac.html?utm_source=chatgpt.com "Dirac — DIRAC Documentation"
[4]: https://github.com/aldbr/dirac-cwl-proto/issues/25?utm_source=chatgpt.com "Input/Output Sandbox/Data Management · Issue #25"
[5]: https://github.com/DIRACGrid/dirac-cwl/issues/8?utm_source=chatgpt.com "Issue #8 · DIRACGrid/dirac-cwl - General Plan"



# CMSDiracAux

In an early attempt to address this problem in the CMSDiracAux project was implemented  a mechanism of taking any WMBS defined job parameter and attach them to the DIRAC job as external attribute and mark them accordingly with a label as `__CMSJobParameter`

The main method for creating the classical DIRAC jobs called `createCMSJob()` is using `__CMSJobParameter__` to take a flat WMCore job dictionary from the CMS `JobPackage` (A bundle of CMS jobs predefined at WMBS) and inject each entry into the DIRAC workflow object as a workflow/job parameter. In the code, every CMS job field except `name` is added through `job._addParameter(job.workflow, parName, value, f"__CMSJobParameter__: {parName}")`. That means the function is not merely building a runnable DIRAC job shell; it is also trying to preserve the WMCore job identity and per-job runtime metadata inside the DIRAC-side workflow description. ([GitHub][1])

Architecturally, those parameters are needed because the CMS job model carries far more job-specific state than a normal DIRAC file-driven job. In CMS, the executable is not enough: the job also needs the information that tells it which exact workload slice it is responsible for, how that slice was produced by splitting, and how it relates back to the workflow/task context. In the PoC, the parameters are the simplest way to carry that WMCore job state across the WMCore → DIRAC boundary without losing it during translation. They are effectively a compatibility payload attached to the DIRAC workflow object. ([GitHub][1])

Within the DIRAC runtime model, this fits at the level of the job description rather than at the pure JDL level. DIRAC JDL describes the executable, arguments, input sandbox, output sandbox, and resource requirements such as `Executable`, `Arguments`, `InputSandbox`, and `OutputSandbox`. That is enough for generic grid execution, but not enough by itself to encode the richer CMS job semantics. The extra `__CMSJobParameter__` values therefore belong to the workflow/job-description layer, where they can travel with the job definition and be available to the runtime logic that interprets that definition. This is consistent with DIRAC’s model, where JDL is the submission envelope and the runtime behavior can depend on richer job metadata beyond those basic submission attributes. ([DIRAC Documentation][2])

In the specific `createCMSJob()` prototype, those parameters coexist with a very CMS-specific three-step runtime chain: first clone the `CMSDiracAux` repo, then source `env.sh`, then call `Startup.py`. So the intention is clear: the DIRAC job is being used as a bootstrap shell for executing a CMS-style runtime environment, and the injected CMS job parameters are there so the CMS bootstrap layer can recover the WMCore job semantics from inside the DIRAC execution container. The code currently shows the bootstrap stage more clearly than the final parameter consumption stage, but the design intent is explicit. ([GitHub][1])

That is also why these parameters matter in the broader CMSDiracAux concept. The project is not trying to submit ordinary DIRAC user jobs; it is trying to preserve enough CMS semantics that a DIRAC-executed payload can still behave like a CMS job. The canonical code in the newer `Interop` layer shows the same overall direction: preserve CMS workflow/task/splitting information in translation objects and then materialize them into local DIRAC-like jobs and transformations. The `CanonicalTask`, `CanonicalStep`, and `CanonicalSplitting` dataclasses explicitly preserve request name, task path, input dataset, splitting mode, resource hints, executable, arguments, and related metadata. The older `__CMSJobParameter__` approach in `wmcGet.py` is the direct, flat, early prototype version of that same preservation strategy. ([GitHub][3])

So the purpose of the `__CMSJobParameter__` fields is not cosmetic and not redundant with the JDL. They are there to smuggle CMS-specific job semantics into a DIRAC workflow object, because the plain DIRAC submission description cannot by itself represent everything a CMS job needs. In the CMSDiracAux bundle and concept, they are needed in the use cases where the runtime must know not only “what executable to run” but also “which exact WMCore-generated unit of work this job represents.” That includes reconstructing job identity, reconnecting to `WMWorkload.pkl` and `JobPackage.pkl`, preserving splitting outcomes, and eventually allowing a DIRAC-side runtime or plugin layer to behave in a WMBS-like way rather than as a purely file-based DIRAC job. ([GitHub][1])

The most important conceptual point is this: in classic DIRAC, job metadata usually supports execution; in CMSDiracAux, these `__CMSJobParameter__` entries are trying to preserve workflow semantics. That is why they are needed, and that is where they fit. ([GitHub][1])

[1]: https://raw.githubusercontent.com/todor-ivanov/CMSDiracAux/main/bin/wmcGet.py "raw.githubusercontent.com"
[2]: https://dirac.diracgrid.org/en/latest/UserGuide/GettingStarted/UserJobs/JDLReference/?utm_source=chatgpt.com "Job Description Language Reference - DIRAC Documentation"
[3]: https://raw.githubusercontent.com/todor-ivanov/CMSDiracAux/main/src/python/CMSDirac/Interop/model.py "raw.githubusercontent.com"



## Relation to the IR layer of CMSDiracAux

Yet another layer of CMSDiracAux which relates to the problem of distributing job specific parameters to the runtime environment is the IR layer. The both methods, though, are **not strict alternatives**.

The best way to think about this is:

```text
Translation IR
    = canonical architecture-level representation

__CMSJobParameter__
    = runtime/job-level transport mechanism
```

In principle:

* the **IR layer replaces the architectural role** that the flat `__CMSJobParameter__` bundle was playing in the early prototype
* but it does **not automatically eliminate** the need for some **runtime-carried per-job metadata**.

Shortly:

```text
IR layer ≠ direct drop-in replacement for __CMSJobParameter__
```

More precisely:

```text
IR replaces their role as the main translation abstraction,
but some job-level metadata still has to reach runtime.
```

Unless runtime reconstruction is redesigned further, those two mechanisms will likely need to work in a **coupled or successor relationship**, not as mutually exclusive options.


The old `__CMSJobParameter__` mechanism is essentially:

```text
flat WMCore job metadata
        ↓
attached directly to DIRAC job/workflow
        ↓
available at runtime
```

It is an **early prototype bridge**.

The IR layer does something more structured:

```text
WMCore workflow
        ↓
canonical normalized objects
        ↓
materialized DIRAC jobs / transformations
```

The IR is a **better place to preserve meaning**, but the worker node still needs some of that meaning at runtime.

That means the question becomes:

```text
How does IR information get projected into runtime-consumable form?
```

And there are only a few possibilities:

### 1. Flat job parameters

Equivalent to the old `__CMSJobParameter__` idea.

### 2. Structured sidecar artifact

For example, a job-local JSON/YAML/pkl emitted from the IR.

### 3. Runtime reconstruction from references

The job receives only IDs / minimal metadata and reconstructs the rest.

---

# Current architectural interpretation

Given how CMSDiracAux is evolving, the most likely correct interpretation is:

```text
IR layer
    = source of truth

__CMSJobParameter__-like payload
    = one possible projection of IR into runtime
```

So if kept, the parameter bundle will become:

```text
derived runtime view of the IR
```

rather than an independent parallel truth source.

That is the important distinction.

---

# In practice

If the project stays close to the current bootstrap model, then some coupling is still needed:

```text
IR
  ↓
job materialization
  ↓
runtime metadata injection
  ↓
bootstrap / Startup.py / cmsRun
```

In that case, `__CMSJobParameter__` or its successor still exists, but only as a **runtime transport layer**.

If the project later moves toward:

* CVMFS-hosted common runtime
* runtime-side PSet reconstruction
* structured per-job metadata artifacts

then the old flat parameter bundle can likely be **reduced or replaced**.

---

# In Conclusion

> The Translation IR in CMSDiracAux should replace `__CMSJobParameter__` as the **primary semantic representation**, but it does not automatically replace the need for **runtime-delivered per-job metadata**. Therefore, at the current conceptual stage, they should be viewed as working in a coupled manner, with `__CMSJobParameter__`-like data becoming a runtime projection of the IR rather than an alternative to it.

So:

```text
today: coupled
future ideal state: IR primary, runtime projection minimized
```


# Summary

CMS and DIRAC differ fundamentally in how jobs are defined and executed.

CMS jobs rely on runtime configuration and workflow semantics derived from WMCore, while DIRAC jobs rely on minimal job descriptions executed through a pilot-based infrastructure.

CMSDiracAux bridges this gap by introducing a Translation IR and by reconstructing CMS runtime semantics inside DIRAC jobs through bootstrap mechanisms and metadata projection.

Moving common runtime components to CVMFS and reconstructing per-job PSet configurations dynamically can significantly improve compatibility between CMS runtime requirements and DIRAC execution constraints.

