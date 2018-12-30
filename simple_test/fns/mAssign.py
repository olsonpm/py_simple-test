#
# assigns attributes of primaryObj over secondaryObj
# return secondaryObj
#   ** mutates secondaryObj
#


def mAssign(primaryObj):
    def mAssign_inner(secondaryObj):
        for k, v in primaryObj.__dict__.items():
            setattr(secondaryObj, k, v)

        return secondaryObj

    return mAssign_inner
