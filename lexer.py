import re

def tokenize(code):
    tokens = []
    token_specification = [
        ('NUMBER', r'\d+'),
        ('ASSIGN', r'assign'),
        ('TO', r'to'),
        ('ID', r'[A-Za-z]+'),
        ('PLUS', r'plus'),
        ('MINUS', r'minus'),
        ('MULTIPLY', r'times'),
        ('DIVIDE', r'over'),
        ('REVERSE', r'reverse'),
        ('IF', r'if'),
        ('ELSE', r'else'),
        ('ENDIF', r'endif'),
        ('EQ', r'=='),
        ('SKIP', r'[ \t]+'),
        ('NEWLINE', r'\n'),
        ('MISMATCH', r'.'),
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
    line_start = 0
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        if kind == 'NUMBER':
            value = int(value)
        elif kind == 'ID' and value in ('assign', 'to', 'reverse', 'plus', 'minus', 'times', 'over', 'if', 'else', 'endif'):
            kind = value.upper()
        elif kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
            continue
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected on line {line_num}')
        tokens.append((kind, value, line_num, column))
    return tokens


# if __name__ == '__main__':
#     code = """
#     assign x to 5
#     assign y to x plus 3
#     reverse y
#     assign z to x minus 2
#     assign w to x times 4
#     assign v to x over 2
#     if x == 5
#     assign a to 1
#     else
#     assign a to 2
#     endif
#     """
#
#     tokens = tokenize(code)
#     for token in tokens:
#         print(token)
