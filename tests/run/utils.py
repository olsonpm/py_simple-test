from os import path

fixturesDir = path.join(path.dirname(__file__), "fixtures")


def makeGetPathToFixture(baseDir):
    def getPathToFixture(rest):
        return path.join(fixturesDir, baseDir, rest)

    return getPathToFixture
