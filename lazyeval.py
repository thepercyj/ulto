class LazyEval:
    def __init__(self, expression, engine):
        self.expression = expression
        self.engine = engine
        self.value = None
        self.evaluated = False

    def evaluate(self):
        if not self.evaluated:
            self.value = self.engine.evaluate_expression(self.expression)
            self.evaluated = True
        return self.value