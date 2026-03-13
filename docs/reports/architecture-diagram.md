# System Architecture Diagram

The following diagram shows the current architecture of the
WMCore → DIRAC interoperability proof of concept.

```
                    ┌───────────────────────────────┐
                    │         WMCore world          │
                    │                               │
                    │  WMRequest.json               │
                    │  WMWorkload.json              │
                    │  WMTask.json                  │
                    │  WMStep.json                  │
                    │  WMSplitting.json             │
                    └──────────────┬────────────────┘
                                   │
                                   ▼
                    ┌───────────────────────────────┐
                    │       wmcGet.py / fetch       │
                    │                               │
                    │  workflow fetch               │
                    │  workflow serialization       │
                    │  request-scoped layout        │
                    └──────────────┬────────────────┘
                                   │
                                   ▼
                    ┌───────────────────────────────┐
                    │      WMCore.fetched.d         │
                    │                               │
                    │  serialized WMCore artifacts  │
                    └──────────────┬────────────────┘
                                   │
                                   ▼
                    ┌───────────────────────────────┐
                    │   WMCore→DIRAC Translator     │
                    │        wmc2transf.py          │
                    │                               │
                    │  loader                       │
                    │  normalizer                   │
                    │  dataset resolution (DAS)     │
                    │  task/step mapper             │
                    │  splitting mapper             │
                    │  report generator             │
                    └──────────────┬────────────────┘
                                   │
                    Translation IR │
                                   ▼
              ┌───────────────────────────────────────────┐
              │            DIRAC Interop Layer            │
              │                                           │
              │  ProductionSpec                           │
              │  TransformationSpecs                      │
              │  Workflow XML / JDL bodies                │
              │  PluginParams                             │
              │  PluginInput                              │
              └──────────────┬────────────────────────────┘
                             │
              ┌──────────────┼────────────────────────────┐
              │              │                            │
              ▼              ▼                            ▼
┌────────────────────┐  ┌──────────────────────┐  ┌─────────────────────┐
│ Production System  │  │ Transformation System│  │ CMSDirac Plugin     │
│                    │  │                      │  │                     │
│ Production         │  │ Transformations      │  │ CMSWMCoreSplitting  │
│ metadata           │  │ Task creation        │  │ Plugin              │
└──────────┬─────────┘  └──────────┬───────────┘  └──────────┬──────────┘
           │                       │                         │
           └──────────────┬────────┴──────────────┬──────────┘
                          │                       │
                          ▼                       ▼
                 ┌────────────────┐      ┌──────────────────┐
                 │ DIRAC WMS      │      │ Data discovery   │
                 │ (local PoC)    │      │ + file metadata  │
                 │                │      │ resolver         │
                 │ Jobs           │      │ DAS today        │
                 │ TaskJobs       │      │ DBS later        │
                 └───────┬────────┘      └──────────────────┘
                         │
                         ▼
                 ┌────────────────┐
                 │  CMS execution │
                 │  cmsRun steps  │
                 │  CMSSW env     │
                 └───────┬────────┘
                         │
                         ▼
                 ┌────────────────┐
                 │  CWL export    │
                 │ transf2cwl.py  │
                 │                │
                 │  workflow.cwl  │
                 │  tool.cwl      │
                 │  inputs/       │
                 │  metadata/     │
                 └────────────────┘
```

Additional context:
```
                    ┌───────────────────────────────┐
                    │      Request output root      │
                    │                               │
                    │  WMCore.fetched.d             │
                    │  DIRAC.transf.d               │
                    │  DIRAC.cwl.d                  │
                    └───────────────────────────────┘

```
CMS data hierarchy:
```
                    ┌───────────────────────────────┐
                    │          CMS data             │
                    │                               │
                    │  dataset                      │
                    │    ↓                          │
                    │  block                        │
                    │    ↓                          │
                    │  file                         │
                    └───────────────────────────────┘
```

PoC scalability limit:
```
                    ┌───────────────────────────────┐
                    │        Current PoC cap        │
                    │                               │
                    │  first 20 files per dataset   │
                    │  are materialized             │
                    └───────────────────────────────┘
```
