import re

def tokenize(code):
    # here we define all the operators and keywords to be tokenize for the language.
    tokens = []
    token_specification = [
        ('NUMBER', r'\d+'),  # Integer
        ('ASSIGN', r'='),  # Assignment 
        ('ID', r'[A-Za-z_][A-Za-z0-9_]*'),  # Identifiers
        ('PLUS', r'\+'),  # Addition 
        ('MINUS', r'-'),  # Subtraction 
        ('TIMES', r'\*'),  # Multiplication 
        ('OVER', r'/'),  # Division 
        ('EQ', r'=='),  # Equality 
        ('NEQ', r'!='),  # Not equal 
        ('LT', r'<'),  # Less than 
        ('GT', r'>'),  # Greater than 
        ('LTE', r'<='),  # Less than or equal 
        ('GTE', r'>='),  # Greater than or equal 
        ('LPAREN', r'\('),  # Left parenthesis
        ('RPAREN', r'\)'),  # Right parenthesis
        ('LBRACKET', r'\['),  # Left bracket
        ('RBRACKET', r'\]'),  # Right bracket
        ('COLON', r':'),  # Colon
        ('DEF', r'def'),  # Function definition keyword
        ('CLASS', r'class'),  # Class definition keyword
        ('RETURN', r'return'),  # Return keyword
        ('IF', r'if'),  # If keyword
        ('ELSE', r'else'),  # Else keyword
        ('WHILE', r'while'),  # While keyword
        ('PRINT', r'print'),  # Print keyword
        ('NEW', r'new'),  # Keyword for creating new instances
        ('REV', r'rev'),  # Reverse keyword
        ('STRING', r'"[^"]*"'),  # String literal
        ('COMMA', r','),  # Comma for parameter separation
        ('SKIP', r'[ \t]+'),  # Skip over spaces and tabs
        ('NEWLINE', r'\n'),  # Line endings
        ('MISMATCH', r'.'),  # Any other character
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
        elif kind == 'STRING':
            value = value[1:-1]
        elif kind == 'ID' and value in ('class', 'def', 'return', 'new', 'if', 'else', 'while', 'print', 'rev'):
            kind = value.upper()
        elif kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
            continue
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected on line {line_num}, column {column}')
        tokens.append((kind, value, line_num, column))
    return tokens
