"""
This is a placeholder for an extension to the DIRAC Transformation client in analogy
to the one developed by LHCbDIRAC at: https://gitlab.cern.ch/lhcb-dirac/LHCbDIRAC
"""
from DIRAC import S_OK, gLogger
from DIRAC.TransformationSystem.Client.TransformationClient import TransformationClient as DIRACTransformationClient


class TransformationClient(DIRACTransformationClient):

    def __init__(self, **kwargs):
        DIRACTransformationClient.__init__(self, **kwargs)
