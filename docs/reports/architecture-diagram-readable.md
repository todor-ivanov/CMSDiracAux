# Human-Readable System Architecture Diagram

This diagram presents the full architecture of the WMCore → DIRAC
interoperability proof of concept in a visually structured form.


----------------------------------------------------------------------
                          CMS Workflow Layer
----------------------------------------------------------------------

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


----------------------------------------------------------------------
                        Translation Layer
----------------------------------------------------------------------

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


----------------------------------------------------------------------
                 PoC Scalability Limitation
----------------------------------------------------------------------

For development purposes the PoC currently materializes:

 20 files per dataset

This avoids generating extremely large transformation structures
while still validating the translation architecture.
