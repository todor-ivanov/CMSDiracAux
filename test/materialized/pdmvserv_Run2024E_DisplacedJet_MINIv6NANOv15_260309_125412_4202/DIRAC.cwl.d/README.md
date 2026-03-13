# CWL Export Bundle

This bundle was generated from a local CMSDiracAux transformation materialization.

Transformation name: DataProcessing
Exported task count: 4

Contents

- tool.cwl
  Generic stage-1 CommandLineTool representing the CMS runtime bootstrap.

- workflow.cwl
  Single-step CWL workflow wrapping tool.cwl.

- inputs
  One YAML input file per generated task.

- metadata/job.metadata.yaml
  Minimal job-style metadata.

- metadata/transformation.metadata.yaml
  Minimal transformation-style metadata.

Typical local validation

cwltool workflow.cwl inputs/task_0001.yaml

This bundle is intended as a stage-1 CWL representation aligned with the
dirac-cwl direction, not as a final CMS runtime model.
