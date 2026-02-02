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

# from WMCore
from WMCore.DataStructs.JobPackage import JobPackage
from WMCore.WMSpec.WMWorkload import WMWorkloadHelper

# from DIRAC
from DIRAC import gLogger
from DIRAC.ProductionSystem.Client.ProductionClient import ProductionClient
from DIRAC.ProductionSystem.Client.ProductionStep import ProductionStep
from DIRAC.Interfaces.API.Job import Job
from DIRAC.Core.Workflow.Parameter import Parameter
from DIRAC.Resources.Catalog.FileCatalog import FileCatalog


class OptionParser():
    """Class to parse the command line arguments"""
    def __init__(self):
        """User based option parser"""
        exampleStr="""
        Examples:

        * interactive mode:
        ipython -i ....
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
    job.setExecutable("/bin/git", arguments="clone https://github.com/todor-ivanov/CMSDiracAux.git")

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

    # Load all WMCore definitions
    wmJobPkg = JobPackage()
    wmJobPkg.load(opts.wmJobPkgFile)
    wmJob = wmJobPkg[int(opts.wmJobIndex)]

    with open(opts.wmWorkloadFile, 'rb') as fd:
        wmWorkloadDef = pickle.load(fd)

    wmWorkload = WMWorkloadHelper(wmWorkloadDef)
    wmWorkloadTree = wmWorkload.data.dictionary_whole_tree_()

    # Create all DIRAC objects:
    job = createCMSJob(wmJob)


    """Executes everything"""
    main()
