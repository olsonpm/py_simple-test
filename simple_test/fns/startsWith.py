from .decorators.argIsType import argIsType


@argIsType(str)
def startsWith(prefix):
    @argIsType(str)
    def startsWith_inner(fullStr):
        return fullStr.startswith(prefix)

    return startsWith_inner
