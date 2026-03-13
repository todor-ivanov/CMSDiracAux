

                       +-----------------------+
                       |        WMCore         |
                       |   (CMS Workflow Mgmt) |
                       +-----------+-----------+
                                   |
                                   v
                       +-----------------------+
                       |       wmcGet.py       |
                       |  Fetch + serialize    |
                       |  WMCore workflow      |
                       +-----------+-----------+
                                   |
                                   v
                       +-----------------------+
                       |   WMCore.fetched.d    |
                       |                       |
                       |  WMTask.json          |
                       |  WMStep.json          |
                       |  WMSplitting.json     |
                       +-----------+-----------+




                       +-----------------------+
                       |     wmc2transf.py     |
                       |  Build canonical IR   |
                       +-----------+-----------+
                                   |
                                   v
                       +-----------------------+
                       |  Canonical Translation |
                       |          IR            |
                       |                       |
                       |  Production           |
                       |  Task                 |
                       |  Step                 |
                       |  Splitting            |
                       +-----------+-----------+


----------------------------------------------------------------------
                    DIRAC-style Materialization
----------------------------------------------------------------------

                       +-----------------------+
                       | emit_translation_doc  |
                       |                       |
                       | Generate local DIRAC  |
                       | transformation bundle |
                       +-----------+-----------+
                                   |
                                   v
                       +-----------------------+
                       |     DIRAC.transf.d    |
                       |                       |
                       | Transformations       |
                       | PluginInput           |
                       | Jobs                  |
                       | Reports               |
                       +-----------+-----------+
                                   |
                                   v
                       +-----------------------+
                       | runLocalTransformation|
                       |                       |
                       | Execute splitting     |
                       | plugin locally        |
                       +-----------+-----------+
                                   |
                                   v
                       +-----------------------+
                       | CMSWMCoreSplitting    |
                       | Plugin                |
                       +-----------+-----------+
                                   |
                                   v
                       +-----------------------+
                       | Task-specific jobs    |
                       |                       |
                       | jobDescription.xml    |
                       | job.jdl               |
                       +-----------+-----------+


----------------------------------------------------------------------
                     Workflow Language Export
----------------------------------------------------------------------

                       +-----------------------+
                       |     transf2cwl.py     |
                       |                       |
                       | Export transformation |
                       | to CWL representation |
                       +-----------+-----------+
                                   |
                                   v
                       +-----------------------+
                       |      DIRAC.cwl.d      |
                       |                       |
                       | workflow.cwl          |
                       | tool.cwl              |
                       | inputs                |
                       | metadata              |
                       +-----------------------+


----------------------------------------------------------------------
                    Data Discovery Path
----------------------------------------------------------------------

 WMCore Task
      |
      v
 dataset reference
      |
      v
 DAS query (dasgoclient)
      |
      v
 dataset file records
      |
      v
 LFN list
      |
      v
 PluginInput dataset


----------------------------------------------------------------------
                 CMS Data Hierarchy Context
----------------------------------------------------------------------

 dataset
    |
    v
 block
    |
    v
 file


Large CMS datasets may contain:

 thousands of files
 hundreds of blocks



# Human-Readable Architecture Diagram

# Human-Readable System Architecture Diagram

This diagram presents the full architecture of the WMCore → DIRAC
interoperability proof of concept in a visually structured form.


----------------------------------------------------------------------
                          CMS Workflow Layer
----------------------------------------------------------------------

```
┌─────────────────────────────┐
│ WMCore                      │
│ CMS workflow management     │
└───────────────┬─────────────┘
                │
                ▼
┌─────────────────────────────┐
│ wmcGet.py                   │
│ workflow fetch + serialize  │
└───────────────┬─────────────┘
                │
                ▼
┌─────────────────────────────┐
│ WMCore.fetched.d            │
│ serialized workflow objects │
└───────────────┬─────────────┘
```

----------------------------------------------------------------------
                        Translation Layer
----------------------------------------------------------------------

```
┌─────────────────────────────┐
│ wmc2transf.py               │
│ build canonical IR          │
│ + data discovery            │
└───────────────┬─────────────┘
                │
                ▼
┌─────────────────────────────┐
│ Canonical Translation IR    │
│ Production / Task / Step    │
│ Splitting                   │
└───────────────┬─────────────┘
```

----------------------------------------------------------------------
                    DIRAC-style Materialization
----------------------------------------------------------------------

```
        ┌─────────────────────────────┐
        │ DIRAC materialization       │
        │ DIRAC.transf.d              │
        └───────────────┬─────────────┘
                        │
                        ▼
        ┌─────────────────────────────┐
        │ runLocalTransformation.py   │
        │ splitting simulation        │
        └───────────────┬─────────────┘
                        │
                        ▼
        ┌─────────────────────────────┐
        │ CMSWMCoreSplittingPlugin    │
        └───────────────┬─────────────┘
                        │
                        ▼
        ┌─────────────────────────────┐
        │ Task-specific jobs          │
        │ jobDescription.xml / JDL    │
        └───────────────┬─────────────┘
                        │
                        ▼
        ┌─────────────────────────────┐
        │ DIRAC WMS / CMS execution   │
        └─────────────────────────────┘

        ┌─────────────────────────────┐
        │ CWL export                  │
        │ transf2cwl.py               │
        └───────────────┬─────────────┘
                        │
                        ▼
        ┌─────────────────────────────┐
        │ DIRAC.cwl.d                 │
        │ workflow bundle             │
        └─────────────────────────────┘
```

----------------------------------------------------------------------
                 PoC Scalability Limitation
----------------------------------------------------------------------

For development purposes the PoC currently materializes:

 20 files per dataset

This avoids generating extremely large transformation structures
while still validating the translation architecture.


