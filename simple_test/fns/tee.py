def tee(msg):
    def tee_inner(something):
        print(msg)
        print(something)
        return something

    return tee_inner
