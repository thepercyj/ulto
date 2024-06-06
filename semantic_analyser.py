class SemanticAnalyser:
    def __init__(self, ast):
        self.ast = ast
        self.symbol_table = {}

    def analyse(self):
        for node in self.ast:
            if node[0] == 'assign':
                self.process_assignment(node)
            elif node[0] == 'reverse':
                self.process_reverse(node)
            elif node[0] == 'if':
                self.process_if(node)
            else:
                self.error(f'Unknown node type: {node[0]}')
        print("Semantic analysis passed")

    def process_assignment(self, node):
        _, var_name, value = node
        self.evaluate_expression(value)
        self.symbol_table[var_name] = None

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

    def evaluate_expression(self, expr):
        if isinstance(expr, tuple):
            left, op, right = expr
            self.evaluate_expression(left)
            self.evaluate_expression(right)
        else:
            if not isinstance(expr, int) and expr not in self.symbol_table:
                self.error(f'Variable "{expr}" used before declaration')

    def analyse_node(self, node):
        if node[0] == 'assign':
            self.process_assignment(node)
        elif node[0] == 'reverse':
            self.process_reverse(node)
        elif node[0] == 'if':
            self.process_if(node)
        else:
            self.error(f'Unknown node type: {node[0]}')

    def error(self, message):
        raise Exception(f'Semantic error: {message}')


if __name__ == '__main__':
    from ulto_parser import Parser
    from lexer import tokenize

    code = """
    assign x to 5
    assign y to x plus 3
    reverse y
    assign z to x minus 2
    assign w to x times 4
    assign v to x over 2
    if x == 5
    assign a to 1
    else
    assign a to 2
    endif
    """

    tokens = tokenize(code)
    parser = Parser(tokens)
    ast = parser.parse()
    print(ast)

    analyser = SemanticAnalyser(ast)
    analyser.analyse()
