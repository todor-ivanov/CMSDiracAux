# Early Report Notes

This directory contains early report-oriented notes collected during the
development of the WMCore → DIRAC interoperability proof of concept.

These notes are intentionally written early, while technical reasoning and
design trade-offs are still fresh. They will later evolve into the final
technical report.

## Current focus areas

- translation architecture
- WMCore ↔ DIRAC execution model differences
- CMS runtime construction challenges
- limitations of the current test environment
- DIRAC materialization milestone
- CWL export milestone
- future compatibility with DIRACX

## Active report follow-up items

The report workstream continues in parallel with the implementation.

The following items must be preserved in the report:

- update the complete architecture diagram so it reflects the three-stage layout:
  - WMCore.fetched.d
  - DIRAC.transf.d
  - DIRAC.cwl.d
- include the parameter-mapping tables between WMCore, canonical IR, and DIRAC
- preserve the rationale for choosing CWL as the next milestone after local DIRAC-style materialization
- preserve the design notes on WMBS granularity, CMS runtime bootstrap, static splitting, and the server-side limitations of the current environment
- preserve the architectural decision that data discovery belongs inside the translator layer
- preserve the architectural decision that CWL export is a central sibling branch and not a runtime step
- preserve the rendering findings for Markdown diagrams:
  - box-drawing diagrams must be enclosed in explicit fenced code blocks
  - indentation alone is not reliable for long diagrams
  - every connector line in a diagram must terminate in a real downstream element

## Deferred technical branch

After stabilizing the artifact layout and CWL export:

- query DBS and DAS to resolve LFNs from serialized WM objects per task
