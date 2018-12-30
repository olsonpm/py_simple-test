from simple_test import run


def runTests(r):
    try:
        code = "run(globStr=1)"
        run(globStr=1)
        r.shouldHaveRaisedAnError(code)
    except Exception as e:
        expectedSubString = "'globStr' must be an instance of str"
        if expectedSubString not in str(e):
            r.raisedUnexpectedError(code)

    try:
        code = 'run(globStr="")'
        run(globStr="")
        r.shouldHaveRaisedAnError(code)
    except Exception as e:
        expectedSubString = "'globStr' cannot be empty"
        if expectedSubString not in str(e):
            r.raisedUnexpectedError(code)

    try:
        code = "run(report=1)"
        run(report="")
        r.shouldHaveRaisedAnError(code)
    except Exception as e:
        expectedSubString = "'report' must be callable"
        if expectedSubString not in str(e):
            r.raisedUnexpectedError(code)

    try:
        code = "run(rootDir=1)"
        run(rootDir=1)
        r.shouldHaveRaisedAnError(code)
    except Exception as e:
        expectedSubString = "'rootDir' must be an instance of str"
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

    try:
        code = "run(filesAndDirs=1)"
        run(filesAndDirs=1)
        r.shouldHaveRaisedAnError(code)
    except Exception as e:
        expectedSubString = "'filesAndDirs' must be an instance of list"
        if expectedSubString not in str(e):
            r.raisedUnexpectedError(code)

    try:
        code = "run(filesAndDirs=[])"
        run(filesAndDirs=[])
        r.shouldHaveRaisedAnError(code)
    except Exception as e:
        expectedSubString = "'filesAndDirs' cannot be empty"
        if expectedSubString not in str(e):
            r.raisedUnexpectedError(code)

    try:
        code = "run(filesAndDirs=[1])"
        run(filesAndDirs=[1])
        r.shouldHaveRaisedAnError(code)
    except Exception as e:
        expectedSubString = "'filesAndDirs' contains non-string elements"
        if expectedSubString not in str(e):
            r.raisedUnexpectedError(code)

    try:
        code = 'run(filesAndDirs=["someFile"], globStr="someGlob")'
        run(filesAndDirs=["someFile"], globStr="someGlob")
        r.shouldHaveRaisedAnError(code)
    except Exception as e:
        expectedSubString = "you cannot pass both 'filesAndDirs' and 'globStr'"
        if expectedSubString not in str(e):
            r.raisedUnexpectedError(code)

    return r
