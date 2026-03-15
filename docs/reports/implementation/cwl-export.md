# CWL Export

## Motivation

One of the objectives of CMSDiracAux is to demonstrate that workflows defined in WMCore can be expressed in a portable workflow representation.

The Common Workflow Language (CWL) provides a standardized description format for computational workflows.

Exporting workflows to CWL enables experimentation with modern workflow execution architectures.

---

# Export Pipeline

```
Translation IR
      │
      ▼
CWL generation
      │
      ▼
CWL workflow description
```

The Translation IR contains all information required to generate a CWL representation.

---

# Workflow Representation

The CWL export stage generates:

```
workflow.cwl
job.yaml
```

These files describe:

* workflow steps
* inputs and outputs
* runtime commands
* data dependencies

---

# Mapping IR Objects to CWL

| IR Object          | CWL Representation   |
| ------------------ | -------------------- |
| CanonicalWorkflow  | CWL workflow         |
| CanonicalTask      | CWL step             |
| CanonicalDataset   | CWL input            |
| CanonicalSplitting | CWL parameterization |

---

# Experimental Nature

The CWL export functionality is currently experimental.

Its main goal is to demonstrate that workflow descriptions can be expressed independently from both WMCore and DIRAC.

---

# Summary

The CWL export stage illustrates the portability of the Translation IR by demonstrating that workflows defined in WMCore can be expressed in a generic workflow language.
