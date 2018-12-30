from ordered_set import OrderedSet
import wrapt

from ..discardWhen import discardWhen
from ..get import get
from ..internal.getArgName import getArgName
from ..isLaden import isLaden
from ..isType import isType
from ..join import join
from ..map_ import map_
from ..passThrough import passThrough
from ..raise_ import raise_
from ..sort import sort
from ..toType import toType


def argIsListOfType(aType):
    @wrapt.decorator
    def wrapper(fn, _instance, args, kwargs):
        typePassed = type(args[0])

        fnName = fn.__name__
        typeName = aType.__name__

        if typePassed is not list:
            argName = getArgName(fn)
            raise_(
                ValueError,
                f"""\
                {fnName} requires {argName} to have the type list
                type passed: {typePassed.__name__}
                """,
            )

        invalidTypes = discardWhen(isType(aType))(args[0])
        if isLaden(invalidTypes):
            argName = getArgName(fn)
            invalidTypeNames = passThrough(
                invalidTypes,
                [
                    map_(toType),
                    OrderedSet,
                    list,
                    map_(get("__name__")),
                    sort,
                    join(", "),
                ],
            )
            raise_(
                ValueError,
                f"""\
                {fnName} requires {argName} to be a list of {typeName}
                invalid types passed: {invalidTypeNames}
                """,
            )

        return fn(*args, **kwargs)

    return wrapper
