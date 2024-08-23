# Ulto - Imperative Reversible Programming Language
#
# semantic_analyser.py
#
# Aman Thapa Magar <at719@sussex.ac.uk>

class SemanticAnalyser:
    """
    A semantic analyzer for the Ulto programming language.

    The `SemanticAnalyser` class is responsible for checking the abstract syntax tree (AST) of an Ulto program
    for semantic correctness. It ensures that variables are declared before use, validates operations and
    control structures, and tracks the program's symbol table. The class processes various nodes in the AST,
    including assignments, loops, conditionals, and expressions, to enforce the language's semantic rules.

    Attributes:
        ast (list): The abstract syntax tree to be analyzed.
        symbol_table (dict): A symbol table to track variable declarations and their values during analysis.
    """
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
        elif node[0] == 'for':
            self.process_for(node)
        elif node[0] == 'while':
            self.process_while(node)
        elif node[0] == 'print':
            self.process_print(node)
        elif node[0] == 'plus_assign':
            self.process_plus_assign(node)
        elif node[0] == 'minus_assign':
            self.process_minus_assign(node)
        elif node[0] == 'times_assign':
            self.process_times_assign(node)
        elif node[0] == 'over_assign':
            self.process_over_assign(node)
        elif node[0] == 'break':
            self.process_break(node)
        elif node[0] == 'len':
            self.process_len(node)
        else:
            self.error(f'Unknown node type: {node[0]}')

    def process_len(self, node):
        """
        Processes a len function node.

        Args:
        node (tuple): The len function node.
        """
        _, expr = node
        self.inline_expression(expr)

    def process_break(self, node):
        """
        Processes a break statement node.

        Args:
        node (tuple): The break statement node.
        """
        # Ensure that the break statement is used inside a loop
        if not self.is_inside_loop():
            self.error("Break statement not inside a loop")

    def is_inside_loop(self):
        """
        Checks if the current context is inside a loop.
        This function would need to track the current context
        to ensure 'break' is within a loop.

        Returns:
        bool: True if inside a loop, False otherwise.
        """
        return True

    def process_assignment(self, node):
        """
        Processes an assignment node.

        Args:
        node (tuple): The assignment node.
        """
        _, var_name, value = node
        self.symbol_table[var_name] = self.inline_expression(value)

    def process_revtrace(self, node):
        """
        Processes a revtrace node.

        Args:
        node (tuple): The revtrace node.
        """
        _, var_name, index = node
        if var_name not in self.symbol_table:
            self.error(f'Variable "{var_name}" used before declaration')

    def process_plus_assign(self, node):
        _, var_name, value = node
        if var_name not in self.symbol_table:
            self.error(f'Variable "{var_name}" used before declaration')
        self.inline_expression(value)

    def process_minus_assign(self, node):
        _, var_name, value = node
        if var_name not in self.symbol_table:
            self.error(f'Variable "{var_name}" used before declaration')
        self.inline_expression(value)

    def process_times_assign(self, node):
        _, var_name, value = node
        if var_name not in self.symbol_table:
            self.error(f'Variable "{var_name}" used before declaration')
        self.inline_expression(value)

    def process_over_assign(self, node):
        _, var_name, value = node
        if var_name not in self.symbol_table:
            self.error(f'Variable "{var_name}" used before declaration')
        self.inline_expression(value)

    def inline_expression(self, expr):
        """
        Inlines an expression.

        Args:
        expr (tuple or any): The expression to be inlined.

        Returns:
        The inlined expression.
        """
        if isinstance(expr, tuple):
            if len(expr) == 3:
                left, op, right = expr
                left = self.inline_expression(left)
                right = self.inline_expression(right)
                if isinstance(left, int) and isinstance(right, int):
                    return self.evaluate_operation(op, left, right)
                return (left, op, right)
            elif len(expr) == 2:  # Handle tuples with 2 elements
                left, op = expr
                left = self.inline_expression(left)
                if isinstance(left, int):
                    return (left, op)
                return (left, op)
            else:
                # Handle a single value tuple (or malformed expression)
                return expr[0] if len(expr) == 1 else expr
        elif isinstance(expr, list):
            return [self.inline_expression(item) for item in expr]
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
        elif op == 'modulo':
            return left % right
        elif op == 'int_div':
            return left // right
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
        if node[0] != 'if':
            self.error("Expected 'if' node")

        condition, true_branch, elif_branches, false_branch = node[1], node[2], node[3], node[4]

        self.evaluate_expression(condition)

        for stmt in true_branch:
            self.analyse_node(stmt)

        for elif_condition, elif_branch in elif_branches:
            self.evaluate_expression(elif_condition)
            for stmt in elif_branch:
                self.analyse_node(stmt)

        for stmt in false_branch:
            self.analyse_node(stmt)

    def process_for(self, node):
        """
        Processes a for loop node.

        Args:
        node (tuple): The for loop node.
        """
        _, var_name, iterable, body = node

        if iterable[0] == 'range':
            _, start_value, end_value, step_value = iterable
            self.inline_expression(start_value)
            self.inline_expression(end_value)
            if step_value:
                self.inline_expression(step_value)
        elif isinstance(iterable, list):
            for element in iterable:
                if isinstance(element, int) or isinstance(element, str):
                    continue
                else:
                    self.error(f'Invalid type in iterable: {element}')
        else:
            self.inline_expression(iterable)
            if isinstance(iterable, str) and iterable not in self.symbol_table:
                self.error(f'Variable "{iterable}" used before declaration')

        # Ensure the loop variable is added to the symbol table
        if var_name in self.symbol_table:
            # Optionally handle or track shadowed variables
            shadowed = True
        else:
            shadowed = False
        self.symbol_table[var_name] = None

        for stmt in body:
            self.analyse_node(stmt)

        # Remove the loop variable from the symbol table after the loop is processed
        if not shadowed:
            del self.symbol_table[var_name]

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
            if expr[0] == 'len':
                _, value = expr
                self.evaluate_expression(value)
            elif len(expr) == 3:
                left, op, right = expr
                self.evaluate_expression(left)
                self.evaluate_expression(right)
            else:
                self.error(f"Unexpected tuple structure: {expr}")
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
