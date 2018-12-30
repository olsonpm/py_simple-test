from textwrap import dedent

#
# combines the attributes of obj1 and obj2 while ensuring none are overwritten
# this is intended to consume instances of SimpleNamespace, but not restricted
#   to such
#
#  ** mutates secondaryObj
#
# returns secondaryObj
#


def mCombine(primaryObj):
    def mCombine_inner(secondaryObj):
        for k, v in primaryObj.__dict__.items():
            if k in secondaryObj.__dict__:
                _raiseOverlappingKeysError(k)
            else:
                setattr(secondaryObj, k, v)

        return secondaryObj

    return mCombine_inner


def _raiseOverlappingKeysError(key):
    raise ValueError(
        dedent(
            f"""
            'mCombine' was passed two objects with matching attribute keys
            key: {key}
            """
        )
    )
