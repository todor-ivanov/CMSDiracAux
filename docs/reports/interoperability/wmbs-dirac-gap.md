# WMBS, DIRAC, and the Granularity Gap

A core architectural issue in this project is the mismatch between the semantic
granularity used by CMS workflow management and the granularity naturally used by
lower-level workload systems.

## CMS workflow-management granularity

In CMS workflow management, the effective atomic unit is often a luminosity
section.

The CMS system must guarantee data uniqueness: no two jobs should reprocess the
same luminosity section.

This requirement pushes CMS workflow management toward finer bookkeeping and
assignment semantics than those naturally supported by most lower-level execution
systems.

## Lower-level scheduling granularity

Systems such as HTCondor and DIRAC naturally operate closer to file/job
granularity.

They can associate jobs with files well, but they do not naturally express
multiple jobs per file or lumi-level assignment semantics as first-class objects.

## Why WMBS exists

One role of WMBS (Workflow Management Bookkeeping System) is to bridge this
semantic mismatch.

WMBS performs a second-level bookkeeping and job/data association stage. It
exists in the WMAgents layer and supports:

- static early splitting,
- bookkeeping of job-to-data associations,
- finer-grained mapping needed by CMS processing semantics,
- insulation of higher-level workflow logic from lower-level scheduler details.

Historically, this also helped preserve flexibility with respect to the
underlying scheduling system.

## Relevance for the current PoC

This is one of the reasons why the current proof of concept cannot simply map
WMCore semantics directly to plain DIRAC file-level transformations and claim
full equivalence.

For the current stage, the project preserves and carries forward WMBS-style job
parameters where available, but does not yet resolve the deeper architectural
question of whether WMBS semantics should:

- remain present in some form,
- be emulated in DIRAC,
- be translated into a future workflow language,
- or be partially redesigned away.
