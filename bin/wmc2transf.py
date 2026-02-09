#!/usr/bin/env python
"""
Minimal WMCore task/workflow/ to Dirac Transformation/Production test converter
"""

import argparse
import logging
import pickle
import os
import sys
import json
import xmltodict
from pprint import pprint, pformat

# from WMCore
from WMCore.DataStructs.JobPackage import JobPackage
from WMCore.WMSpec.WMWorkload import WMWorkloadHelper

# from DIRAC
from DIRAC import gLogger, gConfig, S_OK, S_ERROR
from DIRAC.ProductionSystem.Client.ProductionClient import ProductionClient
from DIRAC.ProductionSystem.Client.ProductionStep import ProductionStep
from DIRAC.Interfaces.API.Job import Job
from DIRAC.Core.Workflow.Parameter import Parameter
from DIRAC.Resources.Catalog.FileCatalog import FileCatalog
from DIRAC.TransformationSystem.Client.Transformation import Transformation as DIRACTransformation
from DIRAC.TransformationSystem.Client.TransformationClient import TransformationClient as DIRACTransformationClient
from DIRAC.TransformationSystem.Agent.TransformationPlugin import TransformationPlugin as DIRACTransformationPlugin

# from CMSDirac
from UtilsAux.Serialize import serializeObj_
from CMSDirac.TransformationSystem.Agent.TransformationPlugin import TransformationPlugin as CMSTransformationPlugin
from CMSDirac.TransformationSystem.Client.Transformation import Transformation
from CMSDirac.TransformationSystem.Client.TransformationClient import TransformationClient

parseWmTaskPath = lambda p: [x for x in p.split('/') if x.strip() != '']

class OptionParser():
    """Class to parse the command line arguments"""
    def __init__(self):
        """User based option parser"""
        exampleStr="""
        Examples:

        * interactive mode:

        ipython -i bin/wmc2transf.py -- \
             -j test/CMSWorkflows.d/pdmvserv_RVCMSSW_16_0_0_pre2QCD__STD_GPU_Pix_202_PU_KIT_251125_103426_8717/run_job_219128/job/WMSandbox/JobPackage.pcl  \
             -w test/CMSWorkflows.d/pdmvserv_RVCMSSW_16_0_0_pre2QCD__STD_GPU_Pix_202_PU_KIT_251125_103426_8717/run_job_219128/job/WMSandbox/WMWorkload.pkl  \
             -i 219128 \
             -o test/
        """

        helpStr = """
        Simple WMC task/workflow/ to Dirac Transformation/Production converter script
        """

        self.parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                               description=helpStr,
                               epilog=exampleStr)
        self.parser.add_argument("-i", "--wmJobIndex", action="store",
                                 dest="wmJobIndex", default="", help="WMCore Job index (int)")
        self.parser.add_argument("-j", "--wmJobPkg", action="store",
                                 dest="wmJobPkgFile", default="", help="WMCore Job Definition (in *.pkl format)")
        self.parser.add_argument("-w", "--wmWorkload", action="store",
                                 dest="wmWorkloadFile", default="", help="WMCore Workload Definition (in *.pkl format)")
        self.parser.add_argument("-o", "--outDir", action="store",
                                 dest="outDir", default="/tmp", help="Output directory (Default: /tmp)")


def main():
    pass

def createCMSJob(cmsJob):
    job = Job()
    job.setName("CMS test job")
    job.setOutputSandbox(["*log"])

    # Translate all CMS job parameters into Dirac job parameters:
    # NOTE: We follow a flat dictionary approach:
    for parName, value in cmsJob.items():
        job._addParameter(job.workflow,
                          parName,
                          "CMSJobParameter",
                          value,
                          f"__CMSJobParameter__: {parName}")

    # job step1: setup CMS runtime required software
    job.setExecutable("/bin/git", arguments="clone -b runtime https://github.com/todor-ivanov/CMSDiracAux.git")

    # job step2: Source the CMSDiracAux repository environments
    job.setExecutable("source ./CMSDiracAux/env.sh")

    # job step3: properly Call CMSRun through Startup.py
    # NOTE: This should go through the steps:
    #       * CMSSW runtime area build
    #       * ....
    job.setExecutable(
        "./CMSDiracAux/bin/Startup.py",
        arguments=f"",
    )

    # NOTE: Alternative would be to dall CMSDiracAux/bin/run-job.sh
    #       job.setExecutable("./CMSDiracAux/bin/Startup.py")

    # return job.workflow.toXML()
    return job


if __name__ == '__main__':
    optmgr = OptionParser()
    opts = optmgr.parser.parse_args()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logging.basicConfig()

    # Parse the input files paths
    opts.wmJobPkgFile = os.path.realpath(opts.wmJobPkgFile)
    opts.wmWorkloadFile = os.path.realpath(opts.wmWorkloadFile)

    opts.wmJobPkgFileName = os.path.basename(opts.wmJobPkgFile)
    opts.wmWorkloadFileName = os.path.basename(opts.wmWorkloadFile)

    opts.wmJobPkgFileExt = os.path.splitext(opts.wmJobPkgFileName)[1]
    opts.wmJobPkgFileName = os.path.splitext(opts.wmJobPkgFileName)[0]

    opts.wmWorkloadFileExt = os.path.splitext(opts.wmWorkloadFileName)[1]
    opts.wmWorkloadFileName = os.path.splitext(opts.wmWorkloadFileName)[0]

    opts.wmJobPkgFileDir = os.path.dirname(opts.wmJobPkgFile)
    opts.wmWorkloadFileDir = os.path.dirname(opts.wmWorkloadFile)

    # Set the output dir
    if opts.outDir == "/tmp":
        opts.outDir = os.path.join(opts.outDir, f"job_{opts.wmJobIndex}")
        opts.outDir = os.path.abspath(opts.outDir)
        opts.wmJobPkgFileSerOut = f"{os.path.join(opts.wmJobPkgFileDir, opts.wmJobPkgFileName)}.json"
        opts.wmWorkloadFileSerOut = f"{os.path.join(opts.wmWorkloadFileDir, opts.wmWorkloadFileName)}.json"
    else:
        opts.outDir = os.path.join(opts.outDir, f"job_{opts.wmJobIndex}")
        opts.outDir = os.path.abspath(opts.outDir)
        opts.wmJobPkgFileSerOut = f"{os.path.join(opts.outDir, opts.wmJobPkgFileName)}.json"
        opts.wmWorkloadFileSerOut = f"{os.path.join(opts.outDir, opts.wmWorkloadFileName)}.json"

    # Create the output dir if missing:
    if not os.path.exists(opts.outDir):
        os.mkdir(opts.outDir)

    # Load all WMCore definitions
    wmJobPkg = JobPackage()
    wmJobPkg.load(opts.wmJobPkgFile)
    wmJob = wmJobPkg[int(opts.wmJobIndex)]

    with open(opts.wmWorkloadFile, 'rb') as fd:
        wmWorkloadDef = pickle.load(fd)

    wmWorkload = WMWorkloadHelper(wmWorkloadDef)
    wmWorkloadTree = wmWorkload.data.dictionary_whole_tree_()

    wmJobTask = parseWmTaskPath(wmJob['task'])[1]
    wmTask = wmWorkload.getTask(wmJobTask)
    # wmTask = wmWorkload.getTask('GenSimFull')
    wmTaskDict = wmTask.data.dictionary_whole_tree_()

    # Serialize and write them to the output dir:
    with open(opts.wmWorkloadFileSerOut, "w") as fd:
        json.dump(serializeObj_(wmWorkloadDef.dictionary_whole_tree_()), fd, indent=4)

    with open(opts.wmJobPkgFileSerOut, "w") as fd:
        json.dump(serializeObj_(wmJobPkg), fd, indent=4)

    # ------------------------------------------------------
    # Create all DIRAC objects:

    # First create a job
    job = createCMSJob(wmJob)
    jobXml = xmltodict.parse(job.workflow.toXML())
    jobJDL=pformat(job._toJDL())

    with open(f'{opts.outDir}/jobDescription.xml.json', 'w') as fd:
        json.dump(jobXml, fd, indent=4)

    with open(f'{opts.outDir}/jobDescription.xml', 'w') as fd:
        json.dump(job.workflow.toXML(), fd, indent=4)

    with open(f'{opts.outDir}/job.jdl', 'w') as fd:
        fd.write(job._toJDL())

    # Second create a vanila transformation
    trans = Transformation()

    trans = Transformation()

    trans.setTransformationName = "CMS Test transformation"
    trans.setTransformationGroup("Test")
    trans.setTransformationFamily("Test")
    trans.setType("Production")
    trans.setDescription("A simple test transformation out of the simplest CMS test job" )
    trans.setPlugin("ByLumi")
    trans.setBody(job.workflow.toXML())
    # transXml = xmltodict.parse(transformation.getTransformationsByUser('tivanov')['Value'][0]['Body'])
    transXml = xmltodict.parse(trans.paramValues['Body'])

    with open(f'{opts.outDir}/transformation.xml.json', 'w') as fd:
        json.dump(transXml, fd, indent=4)

    # Try to create an instance of the minimal CMSTransformationPlugin
    cmsTransPlugin = CMSTransformationPlugin('ByLumi')

    """Executes everything"""
    main()
