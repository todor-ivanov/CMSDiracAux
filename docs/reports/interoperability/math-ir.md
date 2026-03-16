# 14. Formal System Model


## 14.1 System Overview

We model a distributed workflow execution system as a tuple:

```
S = (D, W, P, E)
```

where

```
D  = data model
W  = workflow model
P  = processing model
E  = execution infrastructure
```

CMS and DIRAC instantiate this system differently.

---

# 14.2 CMS Data Model

CMS data is organized as a hierarchical structure.

Let

```
Dataset = { Block₁, Block₂, … }
```

Each block contains files:

```
Block = { File₁, File₂, … }
```

Files contain luminosity sections:

```
Lumi ⊂ File
```

Luminosity sections contain events:

```
Event ⊂ Lumi
```

Runs are collections of events but are **not constrained by file boundaries**.

Thus:

```
Run ⊄ File
File ⊄ Run
```

Formally:

```
∃ r ∈ Run , f₁,f₂ ∈ File : Event(r) ∩ Event(f₁) ≠ ∅
                         ∧ Event(r) ∩ Event(f₂) ≠ ∅
```

meaning a single run may span multiple files.

---

# 14.3 CMS Workflow Model

A CMS workflow is defined as:

```
Wcms = (T, S, R)
```

where

```
T = set of tasks
S = set of processing steps
R = splitting rules
```

The execution hierarchy is:

```
workflow
   ↓
tasks
   ↓
steps
   ↓
jobs
```

Formally:

```
Workflow = { Task₁, Task₂, … }
Task = { Step₁, Step₂, … }
Step → Job*
```

where

```
Job* = set of jobs produced by splitting.
```

---

# 14.4 Job Splitting

Job splitting partitions input data according to workflow parameters.

Define:

```
Split : Data × Parameters → Partition(Data)
```

Thus:

```
Split(D, p) = { D₁, D₂, …, Dn }
```

Each partition produces a job:

```
Jobᵢ processes Dᵢ
```

In CMS the partitioning may occur at several levels:

```
File-level
Run-level
Lumi-level
Event-level
```

Therefore:

```
Split(D) ⊆ PowerSet(Event)
```

meaning partitions may operate on event subsets.

---

# 14.5 DIRAC Workflow Model

DIRAC represents workflows through **transformations**.

A DIRAC production is defined as:

```
Wdirac = (Tr, J)
```

where

```
Tr = set of transformations
J  = set of generated jobs
```

Each transformation generates jobs according to input datasets.

```
Transformation → Task → Job
```

Formally:

```
Tr : Dataset → Job*
```

DIRAC typically partitions data at **file granularity**.

```
SplitDIRAC(D) ⊆ PowerSet(File)
```

---

# 14.6 Workflow Model Mismatch

The mismatch between CMS and DIRAC can be expressed formally.

CMS splitting:

```
SplitCMS(D) ⊆ PowerSet(Event)
```

DIRAC splitting:

```
SplitDIRAC(D) ⊆ PowerSet(File)
```

Since

```
Event ⊂ Lumi ⊂ File
```

we obtain

```
SplitDIRAC(D) ⊆ SplitCMS(D)
```

but not vice versa.

Thus some CMS workflows **cannot be represented directly in DIRAC**.

---

# 14.7 Translation Layer

To bridge the mismatch, we introduce an intermediate representation.

Let

```
IR = canonical workflow representation
```

Translation becomes:

```
TCMS : Wcms → IR
TDIRAC : IR → Wdirac
```

The full pipeline becomes:

```
Wcms
  ↓ TCMS
IR
  ↓ TDIRAC
Wdirac
```

This abstraction separates:

```
workflow semantics
execution infrastructure
```

---

# 14.8 CMS Splitting Plugin

DIRAC transformations must be extended with CMS splitting logic.

Define a transformation plugin:

```
PluginCMS : Dataset × Parameters → Job*
```

such that:

```
PluginCMS(D, p) = SplitCMS(D, p)
```

Thus the DIRAC transformation system can reproduce CMS job partitions.

---

# 14.9 Execution Model

The execution system is defined as:

```
E = (Scheduler, Resources)
```

For CMS:

```
SchedulerCMS = GlideinWMS + HTCondor
```

For DIRAC:

```
SchedulerDIRAC = DIRAC WMS + Pilot System
```

A hybrid architecture integrates the two:

```
SchedulerHybrid =
   DIRAC Transformation
   + GlideinWMS resource management
```

---

# 14.10 Complete Interoperability Model

The complete system can be expressed as:

```
S* = (Dcms, Wcms, IR, Wdirac, Ehybrid)
```

with translation pipeline:

```
Wcms
   ↓
IR
   ↓
Wdirac
   ↓
Ehybrid
```

This model preserves:

```
CMS workflow semantics
DIRAC execution infrastructure
CMS resource management
```

---

# 14.11 Future Extension

If workflow descriptions are expressed in **Common Workflow Language (CWL)**, the translation pipeline becomes:

```
Wcms
   ↓
IR
   ↓
CWL
   ↓
DIRACX
```

This would provide **infrastructure-independent workflow definitions**.

---

## 14.12 Theorem-Style Result: Necessity of an Intermediate Representation

We now formalize the central architectural claim of this work.

### Definition 1 — Direct translation

A **direct workflow translation** is a mapping

```id="3yn7rj"
F : Wcms → Wdirac
```

such that for every CMS workflow `w ∈ Wcms`, the translated workflow `F(w)` preserves the relevant execution semantics of `w`.

---

### Definition 2 — Semantic preservation

Let

```id="2jlwm0"
SemCMS(w)
```

denote the execution semantics of a CMS workflow `w`, including:

* task structure
* step ordering
* data partitioning
* runtime constraints
* job-to-data association

Let

```id="xfm9r0"
SemDIRAC(w')
```

denote the execution semantics of a DIRAC workflow `w'`.

A translation is **semantics-preserving** if for every workflow `w`:

```id="mkwm8r"
SemDIRAC(F(w)) ≃ SemCMS(w)
```

where `≃` denotes equivalence up to accepted implementation-level differences.

---

### Definition 3 — Native DIRAC expressibility

A CMS workflow `w` is **natively DIRAC-expressible** if there exists a DIRAC workflow `w' ∈ Wdirac` such that:

```id="ay4be1"
SemDIRAC(w') ≃ SemCMS(w)
```

without introducing external semantics beyond the native DIRAC workflow model.

---

## Theorem 1 — Direct semantics-preserving translation is not possible in general

For the class of CMS workflows that use sub-file splitting semantics or CMS-specific runtime packaging, there does not exist a total direct translation

```id="6azvb9"
F : Wcms → Wdirac
```

that is semantics-preserving for all workflows in that class.

---

## Proof sketch

We prove this by identifying semantic features present in CMS workflows but absent from the native DIRAC model.

### 1. Splitting mismatch

CMS permits splitting rules at or below file granularity:

```id="m72v4v"
SplitCMS(D) ⊆ PowerSet(Event)
```

In contrast, native DIRAC splitting is file-based:

```id="r9hfgu"
SplitDIRAC(D) ⊆ PowerSet(File)
```

Since:

```id="8rg4jc"
Event ⊂ Lumi ⊂ File
```

there exist CMS partitions that separate data contained within the same file into different jobs.

Such partitions cannot, in general, be represented by a native DIRAC transformation if file is the smallest schedulable data unit.

Hence, there exists a CMS workflow `w₁` such that no `w' ∈ Wdirac` satisfies:

```id="hzzh2y"
SemDIRAC(w') ≃ SemCMS(w₁)
```

---

### 2. Run/file boundary mismatch

CMS data obeys:

```id="9zkgt4"
Run ⊄ File
File ⊄ Run
```

Therefore run-based splitting may require jobs whose logical input partitions intersect files non-trivially.

A DIRAC transformation defined only over file-level partitions cannot directly encode this relation.

Thus there exists a CMS workflow `w₂` using run-based semantics that is not natively DIRAC-expressible.

---

### 3. Runtime packaging mismatch

CMS workflows may require runtime artifacts such as:

```id="mnv3nl"
WMWorkload.pkl
JobPackage.pkl
PSet files
WMCore runtime code
```

with workflow-level and job-level payload distinctions.

Native DIRAC transformations assume execution logic is available through shared infrastructure and job description, rather than arbitrary CMS-specific workflow reconstruction payloads.

Therefore there exists a CMS workflow `w₃` whose runtime semantics cannot be represented as a native DIRAC workflow object alone.

---

### 4. Structural mismatch

CMS workflows may contain constructs such as:

```id="szzr2x"
TaskChain
StepChain
```

whose semantics involve differences in pilot reuse, intermediate data movement, and execution locality.

These are not first-class native objects in the DIRAC workflow model.

Thus there exists a CMS workflow `w₄` for which no native DIRAC workflow captures the same structural semantics directly.

---

### Conclusion

Since there exist workflows `w₁, w₂, w₃, w₄ ∈ Wcms` for which no semantics-preserving native DIRAC image exists, no total direct semantics-preserving mapping

```id="3k7hv1"
F : Wcms → Wdirac
```

can exist for the general CMS workflow class under consideration.

Therefore, direct translation is impossible in general.

∎

---

## Corollary 1 — An intermediate representation is necessary

If direct semantics-preserving translation is impossible in general, then interoperability requires a representation that captures workflow semantics independently of either native execution model.

Hence an intermediate representation

```id="stwl8n"
IR
```

is necessary, together with mappings

```id="xmzwkq"
TCMS   : Wcms → IR
TDIRAC : IR → Wdirac_ext
```

where `Wdirac_ext` denotes DIRAC extended with CMS-specific plugins, annotations, or auxiliary services.

---

## Interpretation

This result is the formal justification for the CMSDiracAux architecture.

The project is not merely converting one workflow syntax into another.
It is constructing a **semantic mediation layer**.

That mediation layer is needed because the two systems differ in:

* data partitioning model
* runtime packaging model
* workflow structure model
* execution infrastructure assumptions

---

## Stronger practical formulation

The theorem can be restated in engineering terms as follows:

```id="w5l5ko"
WMCore workflows cannot be translated directly into native DIRAC workflows
while preserving CMS execution semantics in the general case.

Therefore any viable interoperability solution must introduce:
1. a semantic intermediate representation, and
2. DIRAC-side extensions that reintroduce CMS-specific semantics.
```

---

## Consequence for CMSDiracAux

This directly motivates the architecture:

```id="yd9t4k"
WMCore
   ↓
Translation IR
   ↓
DIRAC + CMS extensions
   ↓
Hybrid execution
```

and, in the longer term:

```id="gv5aan"
WMCore
   ↓
Translation IR
   ↓
CWL
   ↓
DIRACX
```

---

## Optional stronger proposition for the report

If you want a more publication-style statement, you can include this version.

### Proposition

```id="lvpsuz"
The Translation IR is not an implementation convenience.
It is an architectural necessity imposed by the non-isomorphism
between the WMCore and DIRAC workflow models.
```
