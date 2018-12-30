# ------- #
# Imports #
# ------- #

from ordered_set import OrderedSet

from ..fns import (
    discardWhen,
    get,
    isEmpty,
    isInstanceOf,
    isLaden,
    isSomething,
    join,
    map_,
    passThrough,
    raise_,
    sort,
    toType,
)


# ---- #
# Main #
# ---- #


def validateRunParams(filesAndDirs, globStr, report, rootDir, silent):
    if isSomething(globStr):
        if not isinstance(globStr, str):
            raise_(
                ValueError,
                f"""\
                'globStr' must be an instance of str
                type: {type(globStr).__name__}
                """,
            )

        if isEmpty(globStr):
            raise ValueError("'globStr' cannot be empty")

    if isSomething(report) and not callable(report):
        raise ValueError("'report' must be callable")

    if isSomething(rootDir) and not isinstance(rootDir, str):
        raise_(
            ValueError,
            f"""\
            'rootDir' must be an instance of str
            type: {type(rootDir).__name__}
            """,
        )

    if isSomething(silent) and not isinstance(silent, bool):
        raise_(
            ValueError,
            f"""\
            'silent' must be an instance of bool
            type: {type(silent).__name__}
            """,
        )

    if isSomething(filesAndDirs):
        if not isinstance(filesAndDirs, list):
            raise_(
                ValueError,
                f"""\
                'filesAndDirs' must be an instance of list
                type: {type(filesAndDirs).__name__}
                """,
            )

        if isEmpty(filesAndDirs):
            raise ValueError("'filesAndDirs' cannot be empty")

        invalidFilesAndDirs = discardWhen(isInstanceOf(str))(filesAndDirs)
        if isLaden(invalidFilesAndDirs):
            invalidTypes = passThrough(
                invalidFilesAndDirs,
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
                'filesAndDirs' contains non-string elements
                invalid types passed: {invalidTypes}
                """,
            )

    if isSomething(filesAndDirs) and isSomething(globStr):
        raise ValueError("you cannot pass both 'filesAndDirs' and 'globStr'")
