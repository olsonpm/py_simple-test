from .decorators.argIsCallable import argIsCallable
from .internal.makeCallFn import makeCallFn
from .not_ import not_


@argIsCallable
def negate(predicate):
    return makeCallFn(predicate, negate.__name__, modifyResult=not_)
