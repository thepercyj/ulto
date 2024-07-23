import re


class Lexer:
    def __init__(self, input_code):
        self.tokens = []
        self.current_token = None
        self.position = 0
        self.input_code = input_code
        self.tokenize()

    def tokenize(self):
        token_specification = [
            ('NUMBER', r'\d+(\.\d*)?'),
            ('ASSIGN', r'='),
            ('PLUS', r'\+'),
            ('MINUS', r'-'),
            ('MULTIPLY', r'\*'),
            ('DIVIDE', r'/'),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('ID', r'[A-Za-z_]\w*'),
            ('SKIP', r'[ \t]+'),
            ('NEWLINE', r'\n'),
            ('MISMATCH', r'.'),
        ]
        tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
        for mo in re.finditer(tok_regex, self.input_code):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'NUMBER':
                value = float(value) if '.' in value else int(value)
            elif kind == 'ID' and value == 'print':
                kind = 'PRINT'
            elif kind == 'SKIP' or kind == 'NEWLINE':
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f'{value!r} unexpected')
            self.tokens.append((kind, value))
        self.tokens.append(('EOF', None))

    def next_token(self):
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
            self.position += 1
        else:
            self.current_token = ('EOF', None)
        return self.current_token
