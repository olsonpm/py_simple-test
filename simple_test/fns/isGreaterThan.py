def isGreaterThan(right):
    def isGreaterThan_inner(left):
        return left > right

    return isGreaterThan_inner
