# WMCore → DIRAC Translation Architecture

## Goal

The goal of this prototype is to demonstrate that serialized WMCore workflows
can be translated into a DIRAC-compatible form and executed under DIRAC-style
workflow management semantics.

This stage targets interoperability first, not full replacement.

## Source artifacts

The translator consumes serialized workflow objects:

- `WMRequest.json`
- `WMWorkload.json`
- `WMTask.json`
- `WMStep.json`
- `WMSplitting.json`

These represent different abstraction layers of the WMCore workflow model.

## Target model

The DIRAC-side model used in this prototype is:

- Production
- Transformation
- Transformation Plugin
- Tasks / Jobs

Conceptual mapping:

- `WMWorkload` → Production
- `WMTask` → Transformation
- `WMStep` → execution template / job body
- `WMSplitting` → transformation plugin configuration

## Translation flow

```text
Serialized WMCore JSON
    ↓
Canonical translation objects
    ↓
DIRAC-oriented transformation description
    ↓
CMSWMCoreSplittingPlugin
    ↓
Task groups
```

## Why canonical translation objects are used

A neutral canonical representation is used between WMCore JSON and DIRAC objects
because the two systems do not expose identical concepts at identical boundaries.

The canonical layer helps with:

- semantic normalization,
- provenance preservation,
- isolation from serializer changes,
- separation between translation and task materialization.

## Current implementation scope

The current implementation is intentionally narrow:

- one example workflow family,
- one primary executable task,
- one minimal translation path,
- plugin-driven grouping using normalized parameters.

This is sufficient for a stage-1 proof of concept.

## Current outputs

The translator emits:

- a translation document,
- a transformation specification,
- a plugin-input sidecar for stage-1 plugin testing,
- a translation report.
