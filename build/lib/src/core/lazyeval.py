# Ulto - Imperative Reversible Programming Language
#
# lazyeval.py
#
# Aman Thapa Magar <at719@sussex.ac.uk>


class LazyEval:
    def __init__(self, expression, engine):
        """
        Initializes the LazyEval instance.

        Args:
        expression (any): The expression to be lazily evaluated.
        engine (ExecutionEngine): The engine to evaluate the expression.
        """
        self.expression = expression
        self.engine = engine
        self.value = None
        self.evaluated = False

    def evaluate(self):
        """
        Evaluates the expression if it hasn't been evaluated yet.

        Returns:
        The evaluated value of the expression.
        """
        if not self.evaluated:
            self.value = self.engine.evaluate_expression(self.expression)
            self.evaluated = True
        return self.value