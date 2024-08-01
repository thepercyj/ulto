# Ulto - Imperative Reversible Programming Language
#
# semantic_analyser.py
#
# Aman Thapa Magar <at719@sussex.ac.uk>

class SemanticAnalyser:
    def __init__(self, ast):
        self.ast = ast
        self.symbol_table = {}

    def analyse(self):
        for node in self.ast:
            self.analyse_node(node)
        print("Semantic analysis passed")

    def analyse_node(self, node):
        if node[0] == 'assign':
            self.process_assignment(node)
        elif node[0] == 'reverse':
            self.process_reverse(node)
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

    def process_assignment(self, node):
        _, var_name, value = node
        self.evaluate_expression(value)
        self.symbol_table[var_name] = None  # Mark the variable as declared

    def process_reverse(self, node):
        _, var_name = node
        if var_name not in self.symbol_table:
            self.error(f'Variable "{var_name}" used before declaration')

    def process_if(self, node):
        _, condition, true_branch, false_branch = node
        self.evaluate_expression(condition)
        for stmt in true_branch:
            self.analyse_node(stmt)
        for stmt in false_branch:
            self.analyse_node(stmt)

    def process_while(self, node):
        _, condition, body = node
        self.evaluate_expression(condition)
        for stmt in body:
            self.analyse_node(stmt)

    def process_print(self, node):
        _, value = node
        self.evaluate_expression(value)

    def process_import(self, node):
        _, module_name = node
        # Handle imports as needed, e.g., importing Python standard library modules

    def process_class(self, node):
        _, class_name, methods = node
        self.symbol_table[class_name] = {
            'type': 'class',
            'methods': {method[1]: method for method in methods}
        }

    def evaluate_expression(self, expr):
        if isinstance(expr, list):
            for item in expr:
                self.evaluate_expression(item)
        elif isinstance(expr, tuple):
            left, op, right = expr
            self.evaluate_expression(left)
            self.evaluate_expression(right)
        elif isinstance(expr, str):
            if expr.startswith('"') and expr.endswith('"'):
                return  # It's a string literal
            elif expr not in self.symbol_table:
                self.error(f'Variable "{expr}" used before declaration')
        elif not isinstance(expr, int):
            self.error(f'Invalid expression type: {type(expr)}')

    def error(self, message):
        raise Exception(f'Semantic error: {message}')
