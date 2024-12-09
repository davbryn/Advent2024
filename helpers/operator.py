class Operator:
    def __init__(self, func, name):
        self.func = func
        self.name = name

    def __call__(self, a, b):
        return self.func(a, b)


add = Operator(lambda a, b: a + b, "add")
multiply = Operator(lambda a, b: a * b, "multiply")
concatenate = Operator(lambda a, b: int(str(a) + str(b)), "concatenate")