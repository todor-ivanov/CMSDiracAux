# CMS Runtime Construction Challenges

The CMS runtime model is substantially more complex than a plain DIRAC job
template.

## Inputs to runtime behavior

Runtime behavior depends on at least two major sources:

1. the actual data assigned to the current job,
2. the physics software configuration and parameter set used by the job.

In practice, the physics configuration often needs to be tweaked at runtime so
that it reflects the exact boundaries inside the data that the current job is
supposed to process.

This is necessary to preserve CMS data uniqueness guarantees.

## Runtime dependency layers

The effective runtime environment is built from multiple dependency layers:

- WMCore runtime code distributed with the job sandbox,
- CMSSW runtime code mounted through CVMFS,
- worker-node architecture and hardware properties.

These layers are linked through workload/job description objects such as the
serialized WMWorkload and WMBS job definitions.

## Why this matters

DIRAC is not naturally built around this exact runtime construction model.

This is one of the reasons why removing static early splitting is difficult:
the runtime boundary logic and the workload/job description objects are tightly
connected.

## Current PoC approach

The current stage materializes local DIRAC-like Job and Transformation objects
that explicitly preserve:

- CMS runtime bootstrap steps,
- carried WMBS job parameters,
- the link back to serialized WMCore objects.

This is an intermediate executable representation rather than the final target
architecture.

## Future direction

A later stage may express these workflow objects in a more portable workflow
language aligned with future DIRACX directions, while using the current DIRAC
Python object model only as an intermediate representation.
