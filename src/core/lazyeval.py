# Ulto - Imperative Reversible Programming Language
#
# lazyeval.py
#
# Aman Thapa Magar <at719@sussex.ac.uk>


class LazyEval:
    """
    A class for lazy evaluation of expressions.

    The `LazyEval` class is used to defer the evaluation of an expression until its value is actually needed.
    This can be useful in scenarios where evaluating the expression is expensive and might not be required
    unless certain conditions are met. The class ensures that the expression is evaluated only once, caching
    the result for subsequent accesses.

    Attributes:
        expression (any): The expression to be lazily evaluated.
        engine (ExecutionEngine): The engine used to evaluate the expression.
        value (any): The evaluated value of the expression, initialized to `None`.
        evaluated (bool): A flag indicating whether the expression has been evaluated, initialized to `False`.
    """
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