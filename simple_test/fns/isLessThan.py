def isLessThan(right):
    def isLessThan_inner(left):
        return left < right

    return isLessThan_inner
