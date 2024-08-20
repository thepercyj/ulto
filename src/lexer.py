# Ulto - Imperative Reversible Programming Language
#
# lexer.py
#
# Aman Thapa Magar <at719@sussex.ac.uk>

import re

def tokenize(code):
    """
    Tokenizes the given code into a list of tokens.

    Args:
    code (str): The source code to be tokenized.

    Returns:
    list: A list of tokens.
    """
    tokens = []
    token_specification = [
        ('PLUS_ASSIGN', r'\+='),  # Addition assignment
        ('MINUS_ASSIGN', r'-='),  # Subtraction assignment
        ('TIMES_ASSIGN', r'\*='),  # Multiplication assignment
        ('OVER_ASSIGN', r'/='),  # Division assignment
        ('MODULO', r'%'),  # Modulo operator
        ('INT_DIV', r'//'),  # Integer division
        ('EQ', r'=='),  # Equality
        ('NEQ', r'!='),  # Not equal
        ('LTE', r'<='),  # Less than or equal
        ('GTE', r'>='),  # Greater than or equal
        ('LT', r'<'),  # Less than
        ('GT', r'>'),  # Greater than
        ('NUMBER', r'\d+'),  # Integer
        ('ASSIGN', r'='),  # Assignment
        ('ID', r'[A-Za-z_][A-Za-z0-9_]*'),  # Identifiers
        ('PLUS', r'\+'),  # Addition
        ('MINUS', r'-'),  # Subtraction
        ('TIMES', r'\*'),  # Multiplication
        ('OVER', r'/'),  # Division
        ('LPAREN', r'\('),  # Left parenthesis
        ('RPAREN', r'\)'),  # Right parenthesis
        ('LBRACKET', r'\['),  # Left bracket
        ('RBRACKET', r'\]'),  # Right bracket
        ('COLON', r':'),  # Colon
        ('IF', r'if'),  # If keyword
        ('ELIF', r'elif'),  # 'elif' keyword
        ('ELSE', r'else'),  # Else keyword
        ('FOR', r'for'),  # For loop keyword
        ('IN', r'in'),  # In keyword for iteration
        ('RANGE', r'range'),  # Range keyword for numeric ranges
        ('WHILE', r'while'),  # While keyword
        ('PRINT', r'print'),  # Print keyword
        ('REV', r'rev'),  # Reverse keyword
        ('REVTRACE', r'revtrace'),  # reverse tracepath for accessing history
        ('STRING', r'(?:"[^"]*"|`[^`]*`)'),  # String literals with both " and `
        ('COMMA', r','),  # Comma for parameter separation
        ('COMMENT', r'#.*'),  # Comment
        ('SKIP', r'[ \t]+'),  # Skip over spaces / tabs
        ('NEWLINE', r'\n'),  # Line end
        ('MISMATCH', r'.'),  # Any other character
        ('AND', r'and'),  # Logical AND
        ('OR', r'or'),  # Logical OR
        ('TRUE', r'True'),  # Boolean True
        ('FALSE', r'False'),  # Boolean False
        ('BREAK', r'break')  # Break keyword
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
            value = value  # Keep backticks for interpreter to handle
        elif kind == 'COMMENT':
            continue
        elif kind == 'ID' and value in ('if', 'else', 'while', 'print', 'rev', 'revtrace', 'for', 'in', 'range', 'and', 'or', 'break', 'True', 'False'):
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

