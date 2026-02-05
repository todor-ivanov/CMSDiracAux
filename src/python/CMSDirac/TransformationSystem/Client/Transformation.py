"""
This is a placeholder for an extension to the DIRAC Transformation module in analogy
to the one developed by LHCbDIRAC at: https://gitlab.cern.ch/lhcb-dirac/LHCbDIRAC
"""

from DIRAC import gLogger, S_OK, S_ERROR
from DIRAC.TransformationSystem.Client.Transformation import Transformation as DIRACTransformation

from CMSDirac.TransformationSystem.Client.TransformationClient import TransformationClient


class Transformation(DIRACTransformation):
    def __init__(self, transID=0, transClientIn=None):

        if not transClientIn:
            self.transClient = TransformationClient()
        else:
            self.transClient = transClientIn

        super().__init__(transID=transID, transClient=self.transClient)
