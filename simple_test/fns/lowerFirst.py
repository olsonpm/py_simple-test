from .decorators.argIsType import argIsType


@argIsType(str)
def lowerFirst(aString):
    return aString[:1].lower() + aString[1:]
