from copy import copy
from types import SimpleNamespace as o

#
# like 'assign' except assigns the key/value pairs of a dict onto secondaryObj
# returns an instance of SimpleNamespace
#


def assignFromDict(primaryDict):
    primaryObj = o()
    for k, v in primaryDict.items():
        setattr(primaryObj, k, v)

    def assignFromDict_inner(secondaryObj):
        result = copy(primaryObj)

        for k, v in secondaryObj.__dict__.items():
            if k not in result.__dict__:
                setattr(result, k, v)

        return result

    return assignFromDict_inner
