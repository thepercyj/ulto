class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.pos = 0
        self.advance()

    def advance(self):
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
            self.pos += 1
        else:
            self.current_token = None

    def parse(self):
        statements = []
        while self.current_token is not None:
            if self.current_token[0] == 'ASSIGN':
                statements.append(self.parse_assignment())
            elif self.current_token[0] == 'REVERSE':
                statements.append(self.parse_reverse())
            elif self.current_token[0] == 'IF':
                statements.append(self.parse_if())
            else:
                self.error()
        return statements

    def parse_assignment(self):
        self.consume('ASSIGN')
        var_name = self.consume('ID')
        self.consume('TO')
        value = self.parse_expression()
        return ('assign', var_name, value)

    def parse_expression(self):
        left = self.consume_value()
        while self.current_token and self.current_token[0] in ('PLUS', 'MINUS', 'TIMES', 'OVER', 'EQ'):
            op = self.current_token[0].lower()
            if op == 'times':
                op = 'multiply'
            elif op == 'over':
                op = 'divide'
            elif op == 'eq':
                op = '=='
            self.advance()
            right = self.consume_value()
            left = (left, op, right)
        return left

    def parse_if(self):
        self.consume('IF')
        condition = self.parse_expression()
        true_branch = []
        false_branch = []
        while self.current_token and self.current_token[0] not in ('ELSE', 'ENDIF'):
            true_branch.append(self.parse_statement())
        if self.current_token and self.current_token[0] == 'ELSE':
            self.consume('ELSE')
            while self.current_token and self.current_token[0] != 'ENDIF':
                false_branch.append(self.parse_statement())
        self.consume('ENDIF')
        return ('if', condition, true_branch, false_branch)

    def parse_reverse(self):
        self.consume('REVERSE')
        var_name = self.consume('ID')
        return ('reverse', var_name)

    def parse_statement(self):
        if self.current_token[0] == 'ASSIGN':
            return self.parse_assignment()
        elif self.current_token[0] == 'REVERSE':
            return self.parse_reverse()
        elif self.current_token[0] == 'IF':
            return self.parse_if()
        else:
            self.error()

    def consume(self, token_type):
        if self.current_token and self.current_token[0] == token_type:
            value = self.current_token[1]
            self.advance()
            return value
        else:
            self.error()

    def consume_value(self):
        if self.current_token and (self.current_token[0] == 'NUMBER' or self.current_token[0] == 'ID'):
            return self.consume(self.current_token[0])
        else:
            self.error()

    def error(self):
        raise Exception(f'Invalid syntax at token {self.current_token}')


# Example usage
if __name__ == '__main__':
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
