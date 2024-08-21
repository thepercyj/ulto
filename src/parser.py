# Ulto - Imperative Reversible Programming Language
#
# parser.py
#
# Aman Thapa Magar <at719@sussex.ac.uk>

# Ulto - Imperative Reversible Programming Language
#
# parser.py
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
            if self.current_token[0] == 'ID':
                next_token_type = self.peek_next_token()[0]
                if next_token_type in ['ASSIGN', 'PLUS_ASSIGN', 'MINUS_ASSIGN', 'TIMES_ASSIGN', 'OVER_ASSIGN']:
                    statements.append(self.parse_assignment())
                else:
                    self.error()
            elif self.current_token[0] == 'REV':
                statements.append(self.parse_reverse())
            elif self.current_token[0] == 'REVTRACE':
                statements.append(self.parse_revtrace())
            elif self.current_token[0] == 'IF':
                statements.append(self.parse_if())
            elif self.current_token[0] == 'FOR':
                statements.append(self.parse_for())
            elif self.current_token[0] == 'WHILE':
                statements.append(self.parse_while())
            elif self.current_token[0] == 'PRINT':
                statements.append(self.parse_print())
            elif self.current_token[0] == 'INDENT':
                self.consume('INDENT')
                statements.extend(self.parse_block())
                self.consume('DEDENT')
            else:
                self.error()
        return statements


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
        if self.current_token[0] == 'ID':
            next_token = self.peek_next_token()[0]
            if next_token in ['ASSIGN', 'PLUS_ASSIGN', 'MINUS_ASSIGN', 'TIMES_ASSIGN', 'OVER_ASSIGN']:
                return self.parse_assignment()
            elif next_token == 'LPAREN':
                return self.parse_expression()
        elif self.current_token[0] == 'LBRACKET':
            return self.consume_value()
        elif self.current_token[0] == 'REV' and self.peek_next_token()[0] == 'ID':
            return self.parse_reverse()
        elif self.current_token[0] == 'REVTRACE':
            return self.parse_revtrace()
        elif self.current_token[0] == 'RETURN':
            return self.parse_return()
        elif self.current_token[0] == 'IF':
            return self.parse_if()
        elif self.current_token[0] == 'FOR':
            return self.parse_for()
        elif self.current_token[0] == 'WHILE':
            return self.parse_while()
        elif self.current_token[0] == 'PRINT':
            return self.parse_print()
        elif self.current_token[0] == 'BREAK':
            return self.parse_break()
        else:
            self.error()

    def parse_assignment(self):
        """
        Parses an assignment statement.

        Returns:
        tuple: The parsed assignment node.
        """
        var_name = self.consume('ID')
        if self.current_token[0] == 'ASSIGN':
            self.consume('ASSIGN')
            value = self.parse_expression()
            return ('assign', var_name, value)
        elif self.current_token[0] == 'PLUS_ASSIGN':
            self.consume('PLUS_ASSIGN')
            value = self.parse_expression()
            return ('plus_assign', var_name, value)
        elif self.current_token[0] == 'MINUS_ASSIGN':
            self.consume('MINUS_ASSIGN')
            value = self.parse_expression()
            return ('minus_assign', var_name, value)
        elif self.current_token[0] == 'TIMES_ASSIGN':
            self.consume('TIMES_ASSIGN')
            value = self.parse_expression()
            return ('times_assign', var_name, value)
        elif self.current_token[0] == 'OVER_ASSIGN':
            self.consume('OVER_ASSIGN')
            value = self.parse_expression()
            return ('over_assign', var_name, value)
        else:
            self.error()

    def parse_expression(self):
        """
        Parses an expression.

        Returns:
        tuple: The parsed expression node.
        """
        if self.current_token[0] == 'LEN':
            self.advance()
            self.consume('LPAREN')
            expr = self.parse_expression()  # Parse the expression inside len()
            self.consume('RPAREN')
            return ('len', expr)
        else:
            left = self.parse_primary_expression()

            while self.current_token and self.current_token[0] in (
                    'PLUS', 'MINUS', 'TIMES', 'OVER', 'EQ', 'NEQ', 'LT', 'GT', 'LTE', 'GTE', 'DOT', 'AND', 'OR', 'MODULO', 'INT_DIV'):
                op = self.current_token[0].lower()
                self.advance()

                right = self.parse_primary_expression()

                left = (left, op, right)

            return left

    def parse_primary_expression(self):
        """
        Parses a primary expression (number, identifier, or parenthesized expression).
        Returns:
        The parsed expression.
        """
        if self.current_token[0] == 'LPAREN':
            self.consume('LPAREN')
            expr = self.parse_expression()  # Parse the entire sub-expression within parentheses
            self.consume('RPAREN')
            return expr
        elif self.current_token[0] == 'LEN':
            self.advance()
            self.consume('LPAREN')
            expr = self.parse_expression()
            self.consume('RPAREN')
            return ('len', expr)
        elif self.current_token[0] == 'ID':
            id_token = self.consume('ID')

            if self.current_token and self.current_token[0] == 'LBRACKET':
                self.consume('LBRACKET')
                index_expr = self.parse_expression()  # Parse the expression inside the brackets
                self.consume('RBRACKET')
                return (id_token, 'index', index_expr)

            return id_token

        else:
            return self.consume_value()

    def parse_break(self):
        """
        Parses a break statement.

        Returns:
        tuple: The parsed break node.
        """
        self.consume('BREAK')
        return ('break',)

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
        index = self.parse_expression()
        return ('revtrace', var_name, index)

    def parse_if(self):
        """
        Parses an if statement.

        Returns:
        tuple: The parsed if node.
        """
        self.consume('IF')
        condition = self.parse_expression()

        # Handle compound conditions
        while self.current_token and self.current_token[0] in ['AND', 'OR']:
            op = self.current_token[0].lower()
            self.advance()
            right_condition = self.parse_expression()
            condition = (condition, op, right_condition)

        self.consume('COLON')
        true_branch = self.parse_block()

        elif_branches = []
        false_branch = []

        # Handle elif branches
        while self.current_token and self.current_token[0] == 'ELIF':
            self.advance()  # Move past 'elif'
            elif_condition = self.parse_expression()
            self.consume('COLON')
            elif_branch = self.parse_block()
            elif_branches.append((elif_condition, elif_branch))

        # Handle else branch
        if self.current_token and self.current_token[0] == 'ELSE':
            self.consume('ELSE')
            self.consume('COLON')
            false_branch = self.parse_block()

        result = ('if', condition, true_branch, elif_branches, false_branch)
        print("Parsed if structure:", result)  # Debugging output
        return result

    def parse_for(self):
        """
        Parses a for loop statement.

        Returns:
        tuple: The parsed for loop node.
        """
        self.consume('FOR')
        var_name = self.consume('ID')
        self.consume('IN')

        if self.current_token[0] == 'LBRACKET':
            iterable = self.consume_value()  # This will consume the entire list

        elif self.current_token[0] == 'RANGE':
            self.consume('RANGE')
            self.consume('LPAREN')
            start_value = self.parse_expression()

            if self.current_token[0] == 'COMMA':
                self.consume('COMMA')
                end_value = self.parse_expression()
                step_value = None
                if self.current_token[0] == 'COMMA':
                    self.consume('COMMA')
                    step_value = self.parse_expression()
            else:
                end_value = start_value  # Treat single parameter as range(end)
                start_value = ('NUMBER', 0)  # Default start at 0
                step_value = None

            self.consume('RPAREN')
            iterable = ('range', start_value, end_value, step_value)

        else:
            # Assume it's a variable holding an iterable
            iterable = self.parse_expression()

        self.consume('COLON')
        body = self.parse_block()
        return ('for', var_name, iterable, body)

    def parse_while(self):
        """
        Parses a while statement.

        Returns:
        tuple: The parsed while node.
        """
        self.consume('WHILE')
        condition = self.parse_expression()
        # support for both { } and indent/dedent codeblocks
        if self.current_token[0] == 'COLON':
            self.consume('COLON')
            body = self.parse_block()
        elif self.current_token[0] == 'LBRACE':
            body = self.parse_block()
        else:
            self.error()

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
        if self.current_token[0] == 'LBRACE':
            self.consume('LBRACE')  # '{'
            while self.current_token and self.current_token[0] != 'RBRACE':
                stmt = self.parse_statement()
                statements.append(stmt)
                if self.current_token and self.current_token[0] == 'NEWLINE':
                    self.advance()
            self.consume('RBRACE')  # '}'
        elif self.current_token[0] == 'INDENT':
            self.consume('INDENT')  # INDENT
            while self.current_token and self.current_token[0] != 'DEDENT':
                stmt = self.parse_statement()
                statements.append(stmt)
                if self.current_token and self.current_token[0] == 'NEWLINE':
                    self.advance()
            self.consume('DEDENT')  # DEDENT
        else:
            while self.current_token and self.current_token[0] not in ('ELIF', 'ELSE', 'NEWLINE'):
                stmt = self.parse_statement()
                statements.append(stmt)
                if self.current_token and self.current_token[0] == 'NEWLINE':
                    self.advance()
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
        if self.current_token is None:
            raise SyntaxError("Unexpected end of input")

        if self.current_token[0] == 'LBRACKET':
            self.consume('LBRACKET')
            elements = []
            while self.current_token and self.current_token[0] != 'RBRACKET':
                elements.append(self.consume_value())
                if self.current_token[0] == 'COMMA':
                    self.consume('COMMA')
            self.consume('RBRACKET')
            return elements
        elif self.current_token[0] in ('NUMBER', 'ID', 'STRING'):
            return self.consume(self.current_token[0])
        elif self.current_token[0] == 'TRUE':
            self.consume('TRUE')
            return True
        elif self.current_token[0] == 'FALSE':
            self.consume('FALSE')
            return False
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


