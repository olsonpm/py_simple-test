from .raise_ import raise_


def invoke(aCallable):
    if callable(aCallable):
        return aCallable()
    else:
        raise_(ValueError, "'invoke' requires its argument to be callable")
