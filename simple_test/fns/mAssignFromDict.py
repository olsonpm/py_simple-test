#
# like 'mAssign' except assigns the key/value pairs of a dict onto secondaryObj
#   ** mutates secondaryObj
#


def mAssignFromDict(primaryDict):
    def mAssignFromDict_inner(secondaryObj):
        for k, v in primaryDict.items():
            setattr(secondaryObj, k, v)

        return secondaryObj

    return mAssignFromDict_inner
