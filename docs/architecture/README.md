# Architecture Notes

This directory contains working architecture notes for the WMCore → DIRAC
interoperability prototype developed in this repository.

These documents are intentionally lightweight and evolving. Their purpose is to:

- capture architectural decisions early,
- document boundaries of the current proof of concept,
- record postponed topics for future implementation stages,
- support the preparation of a fuller technical report later.

## Current documents

- `wmcore-dirac-translation.md`  
  Overview of the translation architecture from serialized WMCore workflow
  objects to DIRAC-oriented transformation definitions.

- `splitting-design.md`  
  Notes on the `CMSWMCoreSplittingPlugin`, supported modes, and current limits.

- `data-management-future.md`  
  Future-facing notes on data discovery, catalogs, DBS/DAS, Rucio, and topics
  intentionally postponed beyond the current stage.

## Current scope

The current stage focuses on:

- WMCore workflow serialization,
- canonical translation to a DIRAC-oriented intermediate representation,
- minimal transformation emission,
- plugin-driven task grouping.

The current stage does **not** yet fully address:

- intra-file splitting,
- run/lumi masks,
- full DIRAC catalog integration,
- DBS/DAS-based discovery,
- Rucio-based data management integration.
