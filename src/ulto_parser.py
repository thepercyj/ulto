# Ulto - Imperative Reversible Programming Language
#
# ulto_parser.py
#
# Aman Thapa Magar <at719@sussex.ac.uk>

class Parser:
    def __init__(self, tokens):
        """
        Initializes the parser with the given tokens.

        Args:
        tokens (list): The list of tokens.
        """
        self.tokens = tokens
        self.current_token = None
        self.pos = 0
        self.advance()

    def advance(self):
        """
        Advances to the next token.
        """
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
            self.pos += 1
        else:
            self.current_token = None

    def parse(self):
        """
        Parses the tokens into an abstract syntax tree (AST).

        Returns:
        list: The parsed AST.
        """
        statements = []
        while self.current_token is not None:
            if self.current_token[0] == 'CLASS':
                statements.append(self.parse_class())
            elif self.current_token[0] == 'ID' and self.peek_next_token()[0] == 'ASSIGN':
                statements.append(self.parse_assignment())
            elif self.current_token[0] == 'REV':
                statements.append(self.parse_reverse())
            elif self.current_token[0] == 'REVTRACE':
                statements.append(self.parse_revtrace())
            elif self.current_token[0] == 'IF':
                statements.append(self.parse_if())
            elif self.current_token[0] == 'WHILE':
                statements.append(self.parse_while())
            elif self.current_token[0] == 'PRINT':
                statements.append(self.parse_print())
            else:
                self.error()
        return statements

    def parse_class(self):
        """
        Parses a class definition.

        Returns:
        tuple: The parsed class node.
        """
        self.consume('CLASS')
        class_name = self.consume('ID')
        self.consume('COLON')
        methods = []
        while self.current_token and self.current_token[0] != 'NEWLINE':
            if self.current_token[0] == 'DEF':
                methods.append(self.parse_function())
        return ('class', class_name, methods)

    def parse_function(self):
        """
        Parses a function definition.

        Returns:
        tuple: The parsed function node.
        """
        self.consume('DEF')
        func_name = self.consume('ID')
        self.consume('LPAREN')
        params = []
        if self.current_token[0] != 'RPAREN':
            params.append(self.consume('ID'))
            while self.current_token[0] == 'COMMA':
                self.consume('COMMA')
                params.append(self.consume('ID'))
        self.consume('RPAREN')
        self.consume('COLON')
        body = []
        while self.current_token and self.current_token[0] != 'RETURN':
            body.append(self.parse_statement())
        return_value = self.parse_return()
        body.append(return_value)
        return ('function', func_name, params, body)

    def parse_return(self):
        """
        Parses a return statement.

        Returns:
        tuple: The parsed return node.
        """
        self.consume('RETURN')
        value = self.parse_expression()
        return ('return', value)

    def parse_statement(self):
        """
        Parses a single statement.

        Returns:
        tuple: The parsed statement node.
        """
        if self.current_token[0] == 'ID' and self.peek_next_token()[0] == 'ASSIGN':
            return self.parse_assignment()
        elif self.current_token[0] == 'REV':
            return self.parse_reverse()
        elif self.current_token[0] == 'REVTRACE':
            return self.parse_revtrace()
        elif self.current_token[0] == 'RETURN':
            return self.parse_return()
        elif self.current_token[0] == 'IF':
            return self.parse_if()
        elif self.current_token[0] == 'WHILE':
            return self.parse_while()
        elif self.current_token[0] == 'PRINT':
            return self.parse_print()
        else:
            self.error()

    def parse_assignment(self):
        """
        Parses an assignment statement.

        Returns:
        tuple: The parsed assignment node.
        """
        var_name = self.consume('ID')
        self.consume('ASSIGN')
        value = self.parse_expression()
        return ('assign', var_name, value)

    def parse_expression(self):
        """
        Parses an expression.

        Returns:
        tuple: The parsed expression node.
        """
        left = self.consume_value()
        while self.current_token and self.current_token[0] in ('PLUS', 'MINUS', 'TIMES', 'OVER', 'EQ', 'NEQ', 'LT', 'GT', 'LTE', 'GTE', 'DOT'):
            op = self.current_token[0].lower()
            self.advance()
            if op == 'dot':
                method_name = self.consume('ID')
                self.consume('LPAREN')
                args = []
                if self.current_token[0] != 'RPAREN':
                    args.append(self.consume_value())
                    while self.current_token[0] == 'COMMA':
                        self.consume('COMMA')
                        args.append(self.consume_value())
                self.consume('RPAREN')
                left = (left, 'call', method_name, args)
            else:
                right = self.consume_value()
                left = (left, op, right)
        return left

    def parse_reverse(self):
        """
        Parses a reverse statement.

        Returns:
        tuple: The parsed reverse node.
        """
        self.consume('REV')
        var_name = self.consume('ID')
        return ('reverse', var_name)

    def parse_revtrace(self):
        """
        Parses a revtrace statement.

        Returns:
        tuple: The parsed revtrace node.
        """
        self.consume('REVTRACE')
        var_name = self.consume('ID')
        index = self.consume('NUMBER')
        return ('revtrace', var_name, index)

    def parse_if(self):
        """
        Parses an if statement.

        Returns:
        tuple: The parsed if node.
        """
        self.consume('IF')
        condition = self.parse_expression()
        self.consume('COLON')
        true_branch = self.parse_block()
        false_branch = []
        if self.current_token and self.current_token[0] == 'ELSE':
            self.consume('ELSE')
            self.consume('COLON')
            false_branch = self.parse_block()
        return ('if', condition, true_branch, false_branch)

    def parse_while(self):
        """
        Parses a while statement.

        Returns:
        tuple: The parsed while node.
        """
        self.consume('WHILE')
        condition = self.parse_expression()
        self.consume('COLON')
        body = self.parse_block()
        return ('while', condition, body)

    def parse_print(self):
        """
        Parses a print statement.

        Returns:
        tuple: The parsed print node.
        """
        self.consume('PRINT')
        self.consume('LPAREN')
        values = [self.parse_expression()]
        while self.current_token[0] == 'COMMA':
            self.consume('COMMA')
            values.append(self.parse_expression())
        self.consume('RPAREN')
        return ('print', values)

    def parse_block(self):
        """
        Parses a block of statements.

        Returns:
        list: The list of parsed statements.
        """
        statements = []
        while self.current_token and self.current_token[0] != 'NEWLINE' and self.current_token[0] != 'ELSE':
            statements.append(self.parse_statement())
        return statements

    def consume(self, token_type):
        """
        Consumes the current token if it matches the expected type.

        Args:
        token_type (str): The expected token type.

        Returns:
        str: The value of the consumed token.
        """
        if self.current_token and self.current_token[0] == token_type:
            value = self.current_token[1]
            self.advance()
            return value
        else:
            self.error()

    def consume_value(self):
        """
        Consumes a value token (number, identifier, or string).

        Returns:
        The consumed value.
        """
        if self.current_token[0] == 'LBRACKET':
            self.consume('LBRACKET')
            elements = []
            while self.current_token[0] != 'RBRACKET':
                elements.append(self.consume_value())
                if self.current_token[0] == 'COMMA':
                    self.consume('COMMA')
            self.consume('RBRACKET')
            return elements
        elif self.current_token and self.current_token[0] in ('NUMBER', 'ID', 'STRING'):
            return self.consume(self.current_token[0])
        else:
            self.error()

    def peek_next_token(self):
        """
        Peeks at the next token without consuming it.

        Returns:
        tuple: The next token.
        """
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        else:
            return None

    def error(self):
        """
        Raises a syntax error with the current token.

        Raises:
        Exception: Indicates a syntax error.
        """
        raise Exception(f'Invalid syntax at token {self.current_token}')
