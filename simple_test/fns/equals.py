def equals(right):
    def equals_inner(left):
        return left == right

    return equals_inner
