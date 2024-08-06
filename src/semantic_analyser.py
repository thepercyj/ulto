# Ulto - Imperative Reversible Programming Language
#
# semantic_analyser.py
#
# Aman Thapa Magar <at719@sussex.ac.uk>

class SemanticAnalyser:
    def __init__(self, ast):
        """
        Initializes the SemanticAnalyser with the given AST.

        Args:
        ast (list): The abstract syntax tree.
        """
        self.ast = ast
        self.symbol_table = {}

    def analyse(self):
        """
        Analyzes the AST for semantic correctness.
        """
        for node in self.ast:
            self.analyse_node(node)

    def analyse_node(self, node):
        """
        Analyzes a single node in the AST.

        Args:
        node (tuple): The node to be analyzed.
        """
        if node[0] == 'assign':
            self.process_assignment(node)
        elif node[0] == 'reverse':
            self.process_reverse(node)
        elif node[0] == 'revtrace':
            self.process_revtrace(node)
        elif node[0] == 'if':
            self.process_if(node)
        elif node[0] == 'while':
            self.process_while(node)
        elif node[0] == 'print':
            self.process_print(node)
        elif node[0] == 'import':
            self.process_import(node)
        elif node[0] == 'class':
            self.process_class(node)
        else:
            self.error(f'Unknown node type: {node[0]}')

    def process_revtrace(self, node):
        """
        Processes a revtrace node.

        Args:
        node (tuple): The revtrace node.
        """
        _, var_name, index = node
        if var_name not in self.symbol_table:
            self.error(f'Variable "{var_name}" used before declaration')

    def process_assignment(self, node):
        """
        Processes an assignment node.

        Args:
        node (tuple): The assignment node.
        """
        _, var_name, value = node
        self.symbol_table[var_name] = self.inline_expression(value)

    def inline_expression(self, expr):
        """
        Inlines an expression.

        Args:
        expr (tuple): The expression to be inlined.

        Returns:
        The inlined expression.
        """
        if isinstance(expr, tuple):
            left, op, right = expr
            left = self.inline_expression(left)
            right = self.inline_expression(right)
            if isinstance(left, int) and isinstance(right, int):
                return self.evaluate_operation(op, left, right)
            return (left, op, right)
        return expr

    def evaluate_operation(self, op, left, right):
        """
        Evaluates a simple arithmetic operation.

        Args:
        op (str): The operation to be performed.
        left (int): The left operand.
        right (int): The right operand.

        Returns:
        int: The result of the operation.
        """
        if op == 'plus':
            return left + right
        elif op == 'minus':
            return left - right
        elif op == 'times':
            return left * right
        elif op == 'over':
            return left / right
        return None

    def process_reverse(self, node):
        """
        Processes a reverse node.

        Args:
        node (tuple): The reverse node.
        """
        _, var_name = node
        if var_name not in self.symbol_table:
            self.error(f'Variable "{var_name}" used before declaration')

    def process_if(self, node):
        """
        Processes an if node.

        Args:
        node (tuple): The if node.
        """
        _, condition, true_branch, false_branch = node
        self.evaluate_expression(condition)
        for stmt in true_branch:
            self.analyse_node(stmt)
        for stmt in false_branch:
            self.analyse_node(stmt)

    def process_while(self, node):
        """
        Processes a while node.

        Args:
        node (tuple): The while node.
        """
        _, condition, body = node
        self.evaluate_expression(condition)
        for stmt in body:
            self.analyse_node(stmt)

    def process_print(self, node):
        """
        Processes a print node.

        Args:
        node (tuple): The print node.
        """
        _, values = node
        for value in values:
            self.evaluate_expression(value)

    def process_import(self, node):
        """
        Processes an import node.

        Args:
        node (tuple): The import node.
        """
        _, module_name = node

    def process_class(self, node):
        """
        Processes a class node.

        Args:
        node (tuple): The class node.
        """
        _, class_name, methods = node
        self.symbol_table[class_name] = {
            'type': 'class',
            'methods': {method[1]: method for method in methods}
        }

    def evaluate_expression(self, expr):
        """
        Evaluates an expression.

        Args:
        expr (tuple): The expression to be evaluated.
        """
        if isinstance(expr, list):
            for item in expr:
                self.evaluate_expression(item)
        elif isinstance(expr, tuple):
            left, op, right = expr
            self.evaluate_expression(left)
            self.evaluate_expression(right)
        elif isinstance(expr, str):
            # Skip string literals and backtick-enclosed comments
            if expr.startswith('`') and expr.endswith('`'):
                return
            if isinstance(expr, str) and expr.isnumeric() is False and (
                    expr.startswith('"') and expr.endswith('"')) == False:
                if expr not in self.symbol_table:
                    self.error(f'Variable "{expr}" used before declaration')
        elif not isinstance(expr, int):
            self.error(f'Invalid expression type: {type(expr)}')

    def error(self, message):
        """
        Raises an error with the given message.

        Args:
        message (str): The error message.
        """
        raise Exception(f'Semantic error: {message}')
