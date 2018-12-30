wasCalled = False


def report(*args, **kwargs):
    global wasCalled
    wasCalled = True
