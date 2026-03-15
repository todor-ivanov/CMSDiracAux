# Limitations

The CMSDiracAux project is currently a proof-of-concept implementation designed to explore the interoperability between the CMS workflow management system and the DIRAC distributed computing framework.

Several limitations exist in the current prototype.

---

# Dataset Size Limitation

The prototype limits dataset materialization to a small number of files.

Typical CMS datasets may contain thousands of files.

In the current proof-of-concept implementation the number of files processed during testing is restricted.

This limitation exists to keep generated job structures manageable during experimentation.

---

# Incomplete Run/Lumi Support

The prototype demonstrates run and luminosity section splitting concepts but does not fully implement all possible CMS splitting modes.

Some workflow configurations used in production CMS computing are therefore not yet supported.

---

# Runtime Environment Distribution

CMS runtime environments depend on both:

```
WMCore runtime artifacts
CMSSW software environment
```

Reconstructing this environment within the DIRAC execution model remains an open challenge.

Future work will explore improved runtime environment distribution strategies.

---

# DIRAC Server Integration

The current implementation performs transformation materialization locally.

Full integration with the DIRAC server infrastructure is not yet implemented.

This includes:

* server-side transformation agents
* persistent task queues
* production-scale scheduling.

---

# Experimental CWL Export

The CWL export stage is currently experimental and intended for demonstration purposes.

It does not yet represent the full complexity of CMS workflows.

---

# Summary

Despite these limitations, the CMSDiracAux prototype successfully demonstrates the feasibility of translating CMS workflows into execution structures compatible with the DIRAC distributed computing framework.
