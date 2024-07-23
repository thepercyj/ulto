class ASTNode:
    pass


class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Num(ASTNode):
    def __init__(self, value):
        self.value = value


class Var(ASTNode):
    def __init__(self, name):
        self.name = name


class Assign(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Print(ASTNode):
    def __init__(self, value):
        self.value = value


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.lexer.next_token()

    def parse(self):
        nodes = []
        while self.lexer.current_token[0] != 'EOF':
            nodes.append(self.statement())
        return nodes

    def statement(self):
        if self.lexer.current_token[0] == 'ID':
            var_name = self.lexer.current_token[1]
            self.lexer.next_token()
            if self.lexer.current_token[0] == 'ASSIGN':
                self.lexer.next_token()
                value = self.expr()
                return Assign(var_name, value)
        elif self.lexer.current_token[0] == 'PRINT':
            self.lexer.next_token()
            value = self.expr()
            return Print(value)
        else:
            raise RuntimeError('Invalid statement')

    def expr(self):
        node = self.term()
        while self.lexer.current_token[0] in ('PLUS', 'MINUS'):
            token = self.lexer.current_token
            self.lexer.next_token()
            node = BinOp(node, token[0], self.term())
        return node

    def term(self):
        node = self.factor()
        while self.lexer.current_token[0] in ('MULTIPLY', 'DIVIDE'):
            token = self.lexer.current_token
            self.lexer.next_token()
            node = BinOp(node, token[0], self.factor())
        return node

    def factor(self):
        token = self.lexer.current_token
        if token[0] in ('PLUS', 'MINUS'):
            self.lexer.next_token()
            node = BinOp(Num(0), token[0], self.factor())
        elif token[0] == 'NUMBER':
            self.lexer.next_token()
            return Num(token[1])
        elif token[0] == 'ID':
            self.lexer.next_token()
            return Var(token[1])
        elif token[0] == 'LPAREN':
            self.lexer.next_token()
            node = self.expr()
            if self.lexer.current_token[0] != 'RPAREN':
                raise RuntimeError('Missing closing parenthesis')
            self.lexer.next_token()
            return node
        else:
            raise RuntimeError('Invalid factor')
