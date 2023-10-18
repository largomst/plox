from lox.error import report
from lox.Expr import Assign, Binary, Expr, Grouping, Literal, Unary, Variable
from lox.scanner import Token, TokenType
from lox.Stmt import Expression, Print, Stmt, Var


class Parser:
    def __init__(self, tokens: [Token]):
        self.tokens = tokens

        self.current = 0

    def expression(self) -> Expr:
        return self.assignment()

    def assignment(self) -> Expr:
        """
        这里使用了一个技巧来实现赋值表达式
        """
        expr = self.equality()
        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()
            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)
            error(equals, 'Invalid assignment target.')
        return expr

    def declaration(self) -> Stmt:
        try:
            if self.match(TokenType.VAR):
                return self.var_declaration()
            return self.statement()
        except ParserError as e:
            self.synchronize()
            return None

    def var_declaration(self) -> Stmt:
        name = self.consume(TokenType.IDENTIFIER, 'Expect variable name.')
        initializer = self.expression() if self.match(TokenType.EQUAL) else None
        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Var(name, initializer)

    def equality(self) -> Expr:
        expr = self.comparsion()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparsion()
            expr = Binary(expr, operator, right)
        return expr

    def comparsion(self) -> Expr:
        expr = self.term()
        while self.match(
            TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL
        ):

            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr

    def term(self) -> Expr:
        expr = self.factor()
        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr

    def factor(self) -> Expr:
        expr = self.unary()
        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def unary(self) -> Expr:
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()

    def primary(self) -> Expr:
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NIL):
            return Literal(None)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            previous = self.previous()
            literal = previous.literal
            return Literal(literal)

        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        raise self.error(self.peek(), 'Expect epxression.')

    def match(self, *types: [TokenType]) -> bool:
        for type_ in types:
            if self.check(type_):
                self.advance()
                return True

        return False

    def consume(self, type_: TokenType, message: str):
        if self.check(type_):
            return self.advance()
        raise self.error(self.peek(), message)

    def check(self, type_: TokenType):
        return False if self.is_at_end() else self.peek().type == type_

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek().type == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def error(self, token: Token, message: str):
        error(token, message)
        return ParserError()

    def synchronize(self):
        self.advance()
        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return
            match self.peek().type:
                case TokenType.CLASS | TokenType.FUN | TokenType.VAR | TokenType.FOR | TokenType.IF | TokenType.WHILE | TokenType.PRINT | TokenType.RETURN:
                    return
            self.advance()

    def parse(self):
        statements = []
        while not self.is_at_end():
            statements.append(self.declaration())
        return statements

    def statement(self):
        if self.match(TokenType.PRINT):
            return self.print_statement()
        return self.expression_statement()

    def print_statement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    def expression_statement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return Expression(expr)


def error(token: Token, message: str):
    if token.type == TokenType.EOF:
        report(token.line, ' at end', message)
    else:
        report(token.line, f' at {token.lexeme} ', message)


class ParserError(RuntimeError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tokens = []
