from WMCore.WMSpec.WMStep import WMStep
from WMCore.WMSpec.WMTask import WMTask
from WMCore.DataStructs.Job import Job as WMJob
from WMCore.WMSpec.WMWorkload import WMWorkload


class ParametersMap(dict):
    def __init__(self, obj=None, mapping=None, **kwargs):
        self.initObj = obj
        self.initMapping = mapping
        if mapping is not None:
            mapping = {
                str(key): value for key, value in mapping.items()
            }
        else:
            # Here comes the full parameters map between Dirac and WMCore objects
            # NOTE: Here the mapping is still a list of tuples, which is to be
            #       converted into a dictionary later, depending on the type of
            #       object provided for mapping
            if isinstance(obj, WMJob):
                    mapping = [
                        (),
                        (),
                    ]

            if isinstance(obj, WMStep):
                if obj.stepType() == 'CMSSW':
                    mapping = [
                        (),
                        (),
                    ]
                elif obj.stepType() == 'StageOut':
                    mapping = [
                        (),
                        ()
                    ]
                elif obj.stepType() == 'LogArchive':
                    mapping = [
                        (),
                        ()
                    ]

            if isinstance(obj, WMTask):
                if obj.data.taskType == 'Production':
                    mapping = [
                        (),
                        ()
                    ]

            if isinstance(obj, WMWorkload):
                mapping = [
                    (),
                    ()
                ]

            mapping = dict(mapping)

        if kwargs:
            mapping.update(
                {str(key): value for key, value in kwargs.items()}
            )
        super().__init__(mapping)

    # @staticmethod
    def __call__(self, parName):
        """

        """
        return self[parName]

    def getParam(self, parName):
        """
        parName: the target object parameter name
        """
        return {parName: self(parName)}, obj[self(parName)]
