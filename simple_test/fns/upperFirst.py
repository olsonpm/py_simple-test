from .decorators.argIsType import argIsType


@argIsType(str)
def upperFirst(maybeString):
    return maybeString[:1].upper() + maybeString[1:]
