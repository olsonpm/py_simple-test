#
# assigns attributes of primaryObj over secondaryObj
# return secondaryObj
#   ** mutates secondaryObj
#


def mAssignAttrs(primaryObj):
    def mAssignAttrs_inner(secondaryObj):
        for k, v in primaryObj.__dict__.items():
            setattr(secondaryObj, k, v)

        return secondaryObj

    return mAssignAttrs_inner
