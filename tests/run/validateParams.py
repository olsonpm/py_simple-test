from os import path
from po.simple_test import run


def runTests(r):
    try:
        code = "run(projectDir=1)"
        run(projectDir=1)
        r.shouldHaveRaisedAnError(code)
    except Exception as e:
        expectedSubString = "'projectDir' must be an instance of str"
        if expectedSubString not in str(e):
            r.raisedUnexpectedError(code)

    try:
        code = "run(projectDir='')"
        run(projectDir="")
        r.shouldHaveRaisedAnError(code)
    except Exception as e:
        expectedSubString = "'projectDir' cannot be an empty string"
        if expectedSubString not in str(e):
            r.raisedUnexpectedError(code)

    try:
        code = "run(projectDir='relative/path')"
        run(projectDir="relative/path")
        r.shouldHaveRaisedAnError(code)
    except Exception as e:
        expectedSubString = "'projectDir' must pass 'os.path.isabs'"
        if expectedSubString not in str(e):
            r.raisedUnexpectedError(code)

    try:
        code = "run(projectDir='/doesnt/exist')"
        run(projectDir="/doesnt/exist")
        r.shouldHaveRaisedAnError(code)
    except Exception as e:
        expectedSubString = "'projectDir' must pass 'os.path.isdir'"
        if expectedSubString not in str(e):
            r.raisedUnexpectedError(code)

    try:
        thisFilesDirectory = path.dirname(path.abspath(__file__))
        code = "run(projectDir=thisFilesDirectory)"
        run(projectDir=thisFilesDirectory)
        r.shouldHaveRaisedAnError(code)
    except Exception as e:
        expectedSubString = "projectDir must contain a directory 'tests'"
        if expectedSubString not in str(e):
            r.raisedUnexpectedError(code)

    try:
        code = "run(reporter=1)"
        run(reporter=1)
        r.shouldHaveRaisedAnError(code)
    except Exception as e:
        expectedSubString = "'reporter' must be an instance of str"
        if expectedSubString not in str(e):
            r.raisedUnexpectedError(code)

    try:
        code = "run(reporter='')"
        run(reporter="")
        r.shouldHaveRaisedAnError(code)
    except Exception as e:
        expectedSubString = "'reporter' cannot be an empty string"
        if expectedSubString not in str(e):
            r.raisedUnexpectedError(code)

    try:
        code = "run(reporter='.relative.not.supported')"
        run(reporter=".relative.not.supported")
        r.shouldHaveRaisedAnError(code)
    except Exception as e:
        expectedSubString = "relative reporter modules are not yet supported"
        if expectedSubString not in str(e):
            r.raisedUnexpectedError(code)

    try:
        code = "run(silent=1)"
        run(silent=1)
        r.shouldHaveRaisedAnError(code)
    except Exception as e:
        expectedSubString = "'silent' must be an instance of bool"
        if expectedSubString not in str(e):
            r.raisedUnexpectedError(code)

    return r
