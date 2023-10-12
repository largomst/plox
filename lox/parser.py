from lox.error import report
from lox.Expr import Binary, Expr, Grouping, Literal, Unary
from lox.scanner import Token, TokenType


class Parser:
    def __init__(self, tokens: [Token]):
        self.tokens = tokens

        self.current = 0

    def expression(self) -> Expr:
        return self.equality()

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
            right = term()
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

    def unary(self) -> Expr:
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = previous()
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
            return Literal(self.previous().literal)

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        raise error(self.peek(), 'Expect epxression.')

    def match(self, *types: [TokenType]) -> bool:
        for type_ in types:
            if self.check(type_):
                self.advance()
                return True

        return False

    def consume(self, type_: TokenType, message: str):
        if self.check(type_):
            return True
        raise MyException(f'{self.peek()}, message')

    def check(self, type_: TokenType):
        return False if self.is_at_end() else self.peek().type == type_

    def advance(self):
        if self.is_at_end():
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
        return PraerError()

    def synchronize(self):
        self.advance()
        while self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return
            match self.peek().type:
                case TokenType.CLASS | TokenType.FUN | TokenType.VAR | TokenType.FOR | TokenType.IF | TokenType.WHILE | TokenType.PRINT | TokenType.RETURN:
                    return
            self.advance()

    def parse(self):
        try:
            return self.expression()
        except ParserError as e:
            return None


def error(token: Token, message: str):
    if token.type == TokenType.EOF:
        report(token.line, ' at end', message)
    else:
        report(token.line, f' at {token.lexeme} ', message)


class ParserError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tokens = []


class MyExcpetion(Exception):
    pass
