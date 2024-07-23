from ulto_parser import Assign, Print, Num, Var, BinOp


class Interpreter:
    def __init__(self):
        self.variables = {}
        self.history = []

    def interpret(self, nodes):
        for node in nodes:
            self.visit(node)

    def visit(self, node):
        if isinstance(node, Num):
            return node.value
        elif isinstance(node, Var):
            return self.variables.get(node.name, 0)
        elif isinstance(node, BinOp):
            left_val = self.visit(node.left)
            right_val = self.visit(node.right)
            if node.op == 'PLUS':
                return left_val + right_val
            elif node.op == 'MINUS':
                return left_val - right_val
            elif node.op == 'MULTIPLY':
                return left_val * right_val
            elif node.op == 'DIVIDE':
                return left_val / right_val
        elif isinstance(node, Assign):
            value = self.visit(node.value)
            self.history.append((node.name, self.variables.get(node.name, None)))
            self.variables[node.name] = value
        elif isinstance(node, Print):
            value = self.visit(node.value)
            print(value)

    def reverse(self):
        if self.history:
            var_name, old_value = self.history.pop()
            if old_value is None:
                del self.variables[var_name]
            else:
                self.variables[var_name] = old_value

