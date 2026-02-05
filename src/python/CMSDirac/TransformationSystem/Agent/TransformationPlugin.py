# from DIRAC
from DIRAC import gLogger, gConfig, S_OK, S_ERROR
from DIRAC.TransformationSystem.Client.TransformationClient import TransformationClient
from DIRAC.TransformationSystem.Agent.TransformationPlugin import TransformationPlugin as DIRACTransformationPlugin


class TransformationPlugin(DIRACTransformationPlugin):
    """
    A minimal CMS Transformation extension
    """
    def __init__(self, plugin, transClient=None):
        """
        Constructor of the minimal CMSTransformation class.
        """
        super().__init__(plugin)

        if transClient is None:
            self.transClient = TransformationClient()
        else:
            self.transClient = transClient

    def _groupByLumi(self, lfn):
        """
        __groupByLumi__
        This is a placeholder method
        """
        # ...
        return S_OK([('SE_1', lfn)])

    def _ByLumi(self, lfn):
        """ByLumi"""
        return self._groupByLumi(lfn)
