import re


def tokenize(code):
    tokens = []
    token_specification = [
        ('NUMBER', r'\d+'),
        ('ASSIGN', r'='),
        ('PLUS', r'\+'),
        ('MINUS', r'-'),
        ('MULTIPLY', r'\*'),
        ('DIVIDE', r'/'),
        ('EQ', r'=='),
        ('REV', r'rev'),
        ('IF', r'if'),
        ('ELSE', r'else'),
        ('ENDIF', r'endif'),
        ('NEWLINE', r'\n'),
        ('ID', r'[A-Za-z]+'),
        ('SKIP', r'[ \t]+'),  # Spaces and tabs are skipped
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
        elif kind == 'ID' and value in ('rev', 'if', 'else', 'endif'):
            kind = value.upper()
        elif kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
            tokens.append((kind, value, line_num, column))
            continue
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected on line {line_num}')
        tokens.append((kind, value, line_num, column))
    return tokens


# Example usage
if __name__ == '__main__':
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
    for token in tokens:
        print(token)
