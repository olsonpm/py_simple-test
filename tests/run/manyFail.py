#
# README
#  - These tests further inspect the expected suite and test state after "run"
#    is called.  The fixtures here will be more involved compared to the others.
#


# ------- #
# Imports #
# ------- #

from num2words import num2words
from simple_test import run
from simple_test.fns import noop
from .utils import makeGetPathToFixture


# ---- #
# Init #
# ---- #

getPathToFixture = makeGetPathToFixture("many")

fail = getPathToFixture("fail")


# ---- #
# Main #
# ---- #


def runTests(r):
    code = "run(globStr='**/*.py', rootDir=fail, report=noop)"
    result = run(globStr="**/*.py", rootDir=fail, report=noop)
    passed = (
        not result.succeeded
        and result.testsFound
        and hasExpectedRootTests(result)
        and hasExpectedRootSuites(result)
    )
    if not passed:
        r.addError(code)

    return r


# ------- #
# Helpers #
# ------- #


def hasExpectedRootTests(state):
    failedTests = {1, 4}

    for i in range(1, 6):
        test = state.rootTests[i - 1]
        succeeded = i not in failedTests
        testIsCorrect = (
            test.label == num2words(i) + " test"
            and test.fn.__name__ == num2words(i) + "Test"
            and test.parentSuite is None
            and test.rootState is state
            and test.succeeded == succeeded
        )

        if i in failedTests:
            testIsCorrect = testIsCorrect and test.label in str(test.exception)

        if not testIsCorrect:
            return False

    return True


def hasExpectedRootSuites(state):
    suite1 = state.rootSuites[0]
    suite2 = state.rootSuites[1]

    return (
        suite1.label == "one suite"
        and suite1.fn.__name__ == "oneSuite"
        and suite1.parentSuite is None
        and suite1.rootState is state
        and not suite1.succeeded
        and suite2.label == "two suite"
        and suite2.fn.__name__ == "twoSuite"
        and suite2.parentSuite is None
        and suite2.rootState is state
        and not suite2.succeeded
        and hasExpectedNestedTests(state)
        and hasExpectedNestedSuites(state)
    )


def hasExpectedNestedTests(state):
    suite1 = state.rootSuites[0]
    suite2 = state.rootSuites[1]
    subSuite1 = state.rootSuites[1].suites[0]

    subTest1 = suite1.tests[0]
    subTest2 = suite1.tests[1]
    subTest3 = suite2.tests[0]
    subSubTest1 = suite2.suites[0].tests[0]
    subSubTest2 = suite2.suites[0].tests[1]

    return (
        subTest1.label == "sub test 1"
        and subTest1.fn.__name__ == "subTest1"
        and subTest1.parentSuite is suite1
        and subTest1.rootState is state
        and not subTest1.succeeded
        and subTest1.label in str(subTest1.exception)
        and subTest2.label == "sub test 2"
        and subTest2.fn.__name__ == "subTest2"
        and subTest2.parentSuite is suite1
        and subTest2.rootState is state
        and subTest2.succeeded
        and subTest3.label == "sub test 3"
        and subTest3.fn.__name__ == "subTest3"
        and subTest3.parentSuite is suite2
        and subTest3.rootState is state
        and subTest3.succeeded
        and subSubTest1.label == "sub-sub test 1"
        and subSubTest1.fn.__name__ == "subSubTest1"
        and subSubTest1.parentSuite is subSuite1
        and subSubTest1.rootState is state
        and not subSubTest1.succeeded
        and subSubTest1.label in str(subSubTest1.label)
        and subSubTest2.label == "sub-sub test 2"
        and subSubTest2.fn.__name__ == "subSubTest2"
        and subSubTest2.parentSuite is subSuite1
        and subSubTest2.rootState is state
        and subSubTest2.succeeded
    )


def hasExpectedNestedSuites(state):
    subSuite1 = state.rootSuites[1].suites[0]

    return (
        subSuite1.label == "sub suite 1"
        and subSuite1.fn.__name__ == "subSuite1"
        and len(subSuite1.tests) == 2
        and subSuite1.suites == []
        and subSuite1.parentSuite is state.rootSuites[1]
        and subSuite1.rootState is state
        and not subSuite1.succeeded
    )
