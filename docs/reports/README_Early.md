# Early Report Notes

This directory contains early report-oriented notes collected during the
development of the WMCore to DIRAC interoperability proof of concept.

These notes are intentionally written early, while technical reasoning and
design trade-offs are still fresh. They are expected to be refined later into a
more formal report.

## Current focus areas

- the translation architecture
- the gap between WMCore, WMBS, and DIRAC execution semantics
- CMS runtime construction challenges
- limitations of the current test environment
- the local materialization milestone
- the CWL export milestone
- future directions toward DIRACX and workflow-language portability

## Active report follow-up items

The report workstream is active and should continue in parallel with coding.

The following items must be propagated into the report:

- update the complete architecture diagram so it reflects the three-stage layout:
  - WMCore.fetched.d
  - DIRAC.transf.d
  - DIRAC.cwl.d
- include the parameter-mapping tables between WMCore, canonical IR, and DIRAC
- preserve the rationale for choosing CWL as the next milestone after local DIRAC-style materialization
- preserve the design notes on WMBS granularity, CMS runtime bootstrap, static splitting, and the server-side limitations of the current environment

## Deferred technical note to keep visible

After the current output-layout and CWL-export stage, the next technical branch is:

- query DBS and DAS to resolve LFNs from serialized WM objects per task
