from case_conversion import separate_words
from ..Results import Results, o
from ..utils import getModuleBasename
from simple_test.fns import forEach, invokeAttr, isLaden, keepWhen

from . import validateParams, withProcess

modules = [validateParams, withProcess]


def runTests():
    resultsList = []
    for m in modules:
        moduleName = separate_words(getModuleBasename(m))
        r = Results(moduleName, level=1)
        results = m.runTests(r)
        resultsList.append(results)

    unsuccessfulResults = keepWhen(hasErrors)(resultsList)
    if isLaden(unsuccessfulResults):
        print(f"run")
        forEach(invokeAttr("printResults"))(unsuccessfulResults)
    else:
        print(f"{o} run")


__all__ = ["runTests"]


# ------- #
# Helpers #
# ------- #


def hasErrors(result):
    return isLaden(result.errors)
