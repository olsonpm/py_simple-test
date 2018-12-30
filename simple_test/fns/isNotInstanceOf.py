from .decorators.argIsClass import argIsClass


@argIsClass
def isNotInstanceOf(aType):
    def isNotInstanceOf_inner(something):
        return not isinstance(something, aType)

    return isNotInstanceOf_inner
