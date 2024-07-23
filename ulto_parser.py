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
            if self.current_token[0] == 'NEWLINE':
                self.advance()
                continue
            elif self.current_token[0] == 'ID':
                statements.append(self.parse_assignment())
            elif self.current_token[0] == 'REV':
                statements.append(self.parse_reverse())
            elif self.current_token[0] == 'IF':
                statements.append(self.parse_if())
            else:
                self.error()
        return statements

    def parse_assignment(self):
        var_name = self.consume('ID')
        self.consume('ASSIGN')
        value = self.parse_expression()
        self.advance_newline()
        return ('assign', var_name, value)

    def parse_expression(self):
        left = self.consume_value()
        while self.current_token and self.current_token[0] in ('PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'EQ'):
            op = self.current_token[0].lower()
            self.advance()
            right = self.consume_value()
            left = (left, op, right)
        return left

    def parse_if(self):
        self.consume('IF')
        condition = self.parse_expression()
        self.advance_newline()
        true_branch = self.parse_block()
        false_branch = []
        if self.current_token and self.current_token[0] == 'ELSE':
            self.consume('ELSE')
            self.advance_newline()
            false_branch = self.parse_block()
        self.consume('ENDIF')
        self.advance_newline()
        return ('if', condition, true_branch, false_branch)

    def parse_reverse(self):
        self.consume('REV')
        var_name = self.consume('ID')
        self.advance_newline()
        return ('reverse', var_name)

    def parse_statement(self):
        if self.current_token[0] == 'ID':
            return self.parse_assignment()
        elif self.current_token[0] == 'REV':
            return self.parse_reverse()
        elif self.current_token[0] == 'IF':
            return self.parse_if()
        else:
            self.error()

    def parse_block(self):
        block = []
        while self.current_token and self.current_token[0] != 'ELSE' and self.current_token[0] != 'ENDIF':
            if self.current_token[0] == 'NEWLINE':
                self.advance()
                continue
            block.append(self.parse_statement())
        return block

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

    def advance_newline(self):
        if self.current_token and self.current_token[0] == 'NEWLINE':
            self.advance()

    def error(self):
        raise Exception(f'Invalid syntax at token {self.current_token}')


# Example usage
if __name__ == '__main__':
    from lexer import tokenize

    code = """
    x = 5
    y = x + 3
    rev y
    z = x - 2
    z = x
    rev z
    w = x * 4
    v = x / 2

    if x == 5
        a = 1
    else
        a = 2
    endif
    """

    tokens = tokenize(code)
    parser = Parser(tokens)
    ast = parser.parse()
    print(ast)
