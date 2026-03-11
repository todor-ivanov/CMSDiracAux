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
import random
import string
from pprint import pprint, pformat

# from WMCore
from WMCore.DataStructs.JobPackage import JobPackage
from WMCore.WMSpec.WMWorkload import WMWorkloadHelper
from WMCore.Services.ReqMgr.ReqMgr import ReqMgr
from WMCore.Services.WorkQueue.WorkQueue import WorkQueue
from WMCore.Database.CMSCouch import CouchServer, CouchConflictError
from WMCore.Lexicon import splitCouchServiceURL

# from DIRAC
from DIRAC import gLogger, gConfig, S_OK, S_ERROR
from DIRAC.ProductionSystem.Client.ProductionClient import ProductionClient
from DIRAC.ProductionSystem.Client.ProductionStep import ProductionStep
from DIRAC.Interfaces.API.Job import Job
from DIRAC.Core.Workflow.Workflow import fromXMLFile
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
        self.exclArgs = self.parser.add_mutually_exclusive_group()
        self.exclArgs.add_argument("-w", "--wmWorkload", action="store",
                                 dest="wmWorkloadFile", default="", help="WMCore Workload Definition (in *.pkl format)")
        self.exclArgs.add_argument("-r", "--wmReqName", action="store",
                                 dest="wmReqName", default="", help="WMCore Request name to fetch from WMCore Request Manager")
        self.parser.add_argument("-m", "--wmReqMgr", action="store",
                                 dest="wmReqMgr", default="cmsweb-testbed.cern.ch", help="WMCore Request manager instance(Default: https://cmsweb-testbed.cern.ch/reqmgr2 )")
        self.parser.add_argument("-o", "--outDir", action="store",
                                 dest="outDir", default="/tmp", help="Output directory (Default: /tmp)")


def main():
    pass

def createCMSJob(cmsJob=None):
    job = Job()
    job.setName("CMS test job")
    job.setOutputSandbox(["*log"])

    # Translate all CMS job parameters into Dirac job parameters:
    # NOTE: We follow a flat dictionary approach:
    if cmsJob:
        for parName, value in cmsJob.items():
            if parName == "name":
                continue
            #     parName = "jobName"
            job._addParameter(job.workflow,
                              parName,
                              # "CMSJobParameter",
                              "parameter",
                              value,
                              f"__CMSJobParameter__: {parName}")

    # job step1: setup CMS runtime required software
    job.setExecutable("/bin/git", arguments="clone --depth 1 -b runtime https://github.com/todor-ivanov/CMSDiracAux.git")

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

def randStr(size=8):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))


if __name__ == '__main__':
    # Parse arguments:
    optmgr = OptionParser()
    opts = optmgr.parser.parse_args()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logging.basicConfig()

    # Load all WMCore definitions
    wmReqMgrUrl = f"https://{opts.wmReqMgr}/reqmgr2"
    wmCouchDb = f"https://{opts.wmReqMgr}/couchdb/reqmgr_workload_cache"
    wmCouchUrl = splitCouchServiceURL(wmCouchDb)[0]
    wmCouchDbName = splitCouchServiceURL(wmCouchDb)[1]
    wmReqMgr = ReqMgr(wmReqMgrUrl)

    if opts.wmReqName:
        wmWorkload = WMWorkloadHelper()
        wmWorkload.load(f"{wmCouchDb}/{opts.wmReqName}/spec")
    else:
        with open(opts.wmWorkloadFile, 'rb') as fd:
            wmWorkloadDef = pickle.load(fd)
            wmWorkload = WMWorkloadHelper(wmWorkloadDef)

    wmWorkloadTree = wmWorkload.data.dictionary_whole_tree_()
    wmRequest = wmReqMgr.getRequestByNames(wmWorkload.name())

    # Try to load the WMCore job from an eventual JobPackage
    wmJobPkg = JobPackage()
    wmJob = None
    if opts.wmJobPkgFile:
        wmJobPkg.load(opts.wmJobPkgFile)
        if not opts.wmJobIndex:
            wmJobPkg.pop('directory', None)
            if wmJobPkg:
                opts.wmJobIndex = list(wmJobPkg.keys())[0]
        if opts.wmJobIndex:
            wmJob = wmJobPkg[int(opts.wmJobIndex)]

    # Parse the input files paths
    opts.outDir = os.path.abspath(opts.outDir)
    if opts.wmJobPkgFile:
        wmJobPkgFilePath = os.path.realpath(opts.wmJobPkgFile)
        wmJobPkgFileName = os.path.basename(wmJobPkgFilePath)
        wmJobPkgFileExt = os.path.splitext(wmJobPkgFileName)[1]
        wmJobPkgFileName = os.path.splitext(wmJobPkgFileName)[0]
        wmJobPkgFileDir = os.path.dirname(opts.wmJobPkgFile)
    else:
        wmJobPkgFileName = "JobPackage"
        wmJobPkgFileDir = opts.outDir

    if opts.wmWorkloadFile:
        wmWorkloadFilePath = os.path.realpath(opts.wmWorkloadFile)
        wmWorkloadFileName = os.path.basename(wmWorkloadFilePath)
        wmWorkloadFileExt = os.path.splitext(wmWorkloadFileName)[1]
        wmWorkloadFileName = os.path.splitext(wmWorkloadFileName)[0]
        wmWorkloadFileDir = os.path.dirname(opts.wmWorkloadFile)
    else:
        wmWorkloadFileName = "WMWorkload"
        wmWorkloadFileDir = opts.outDir

    # Set the output dir
    if opts.outDir == "/tmp":
        opts.outDir = os.path.join(opts.outDir, f"wf_{wmWorkload.name()}")
        if opts.wmJobIndex:
            opts.outDir = os.path.join(opts.outDir, f"job_{opts.wmJobIndex}")
        wmJobPkgFileSerOut = f"{os.path.join(wmJobPkgFileDir, wmJobPkgFileName)}.json"
        wmWorkloadFileSerOut = f"{os.path.join(wmWorkloadFileDir, wmWorkloadFileName)}.json"
        wmRequestSerOut = f"{os.path.join(wmWorkloadFileDir, 'WMRequest')}.json"
    else:
        opts.outDir = os.path.join(opts.outDir, f"wf_{wmWorkload.name()}")
        if opts.wmJobIndex:
            opts.outDir = os.path.join(opts.outDir, f"job_{opts.wmJobIndex}")
        wmJobPkgFileSerOut = f"{os.path.join(opts.outDir, wmJobPkgFileName)}.json"
        wmWorkloadFileSerOut = f"{os.path.join(opts.outDir, wmWorkloadFileName)}.json"
        wmRequestSerOut = f"{os.path.join(opts.outDir, 'WMRequest')}.json"

    # Create the output dir if missing:
    if not os.path.exists(opts.outDir):
        os.makedirs(opts.outDir, exist_ok=True)

    if wmJob:
        wmJobTask = parseWmTaskPath(wmJob['task'])[1]
        wmTask = wmWorkload.getTask(wmJobTask)
    else:
        wmTask = wmWorkload.getTopLevelTask()[0]
    wmTaskTree = wmTask.data.dictionary_whole_tree_()

    # Serialize and write WMCore objects to the output dir:
    with open(wmWorkloadFileSerOut, "w") as fd:
        # json.dump(serializeObj_(wmWorkloadDef.dictionary_whole_tree_()), fd, indent=4)
        json.dump(serializeObj_(wmWorkloadTree), fd, indent=4)

    with open(wmRequestSerOut, "w") as fd:
        json.dump(serializeObj_(wmRequest), fd, indent=4)

    with open(wmJobPkgFileSerOut, "w") as fd:
        json.dump(serializeObj_(wmJobPkg), fd, indent=4)

    # walk all tasks' job splitting configurations:
    # for taskPath in wmWorkload.listAllTaskPathNames():
    #     taskSplitting = wmWorkload.listJobSplittingParametersByTask()[taskPath]
    wmSplittingTree = wmWorkload.listJobSplittingParametersByTask()

    # walk all tasks
    cmsRunTaskCounter = 0
    for taskPath in wmWorkload.listAllTaskPathNames():
        task = wmWorkload.getTaskByPath(taskPath)
        cmsRunStepsNames = task.listAllStepNames(cmsRunOnly=True)
        if cmsRunStepsNames:
            cmsRunTaskCounter += 1
        print(f"Task Name: {task.name()}")
        print(f"Task Path: {taskPath}")
        print(f"Task steps: {task.listAllStepNames(cmsRunOnly=False)}")
        print(f"cmsRun steps: {task.listAllStepNames(cmsRunOnly=True)}")
        for stepName in task.listAllStepNames(cmsRunOnly=False):
            step = task.getStepHelper(stepName)
            print(f"step Name: {step.name()}")
            print(f"step Config: {step.getConfigCacheID()}")

    cmsRunTasks = {}
    cmsRunTasksTree = {}
    for taskPath in wmWorkload.listAllTaskPathNames():
        task = wmWorkload.getTaskByPath(taskPath)
        if task.listAllStepNames(cmsRunOnly=True):
            cmsRunTasksTree[task.name()] = task.data.dictionary_whole_tree_()
            cmsRunTasks[task.name()] = task
            # for stepName in task.listAllStepNames(cmsRunOnly=False):
            #     step = task.getStepHelper(stepName)

    # Get all steps from the toplevel task
    wmTaskSteps = {}
    for stepName in wmTask.listAllStepNames(cmsRunOnly=False):
        step = wmTask.getStepHelper(stepName)
        wmTaskSteps[stepName] = step

    wmStepTree = wmTaskSteps['cmsRun1'].data.dictionary_whole_tree_()

    with open(f"{os.path.join(opts.outDir, 'WMTask')}.json", 'w') as fd:
        json.dump(serializeObj_(wmTaskTree), fd, indent=4)

    with open(f"{os.path.join(opts.outDir, 'WMStep')}.json", 'w') as fd:
        json.dump(serializeObj_(wmStepTree), fd, indent=4)

    # with open(f"{os.path.join(opts.outDir, 'WMJob_%s' % opts.wmJobIndex)}.json", 'w') as fd:
    with open(f"{os.path.join(opts.outDir, 'WMJob')}.json", 'w') as fd:
        json.dump(serializeObj_(wmJob), fd, indent=4)

    with open(f"{os.path.join(opts.outDir, 'WMSplitting')}.json", 'w') as fd:
        json.dump(serializeObj_(wmSplittingTree), fd, indent=4)

    # ------------------------------------------------------
    # Create all DIRAC objects:

    # First create a job
    # NOTE: If --wmJobPkg is not provided as an argument the script will break here
    job = createCMSJob(wmJob)
    jobXml = xmltodict.parse(job.workflow.toXML())
    jobJDL=pformat(job._toJDL())

    with open(f'{opts.outDir}/jobDescription.xml.json', 'w') as fd:
        json.dump(jobXml, fd, indent=4)

    # with open(f'{opts.outDir}/jobDescription.xml', 'w') as fd:
    #     json.dump(job.workflow.toXML(), fd, indent=4)
    jobDescrFile = f'{opts.outDir}/jobDescription.xml'
    job.workflow.toXMLFile(jobDescrFile)

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
