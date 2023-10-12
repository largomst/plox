import sys

from lox.Expr import *
from lox.scanner import TokenType


class AstPrinter(Visitor):
    def print(self, expr: Expr):
        return expr.accept(self)

    def visitBinaryExpr(self, expr: Binary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visitGroupingExpr(self, expr: Grouping) -> str:
        return self.parenthesize('group', expr.expression)

    def visitLiteralExpr(self, expr: Literal) -> str:
        if expr.value == None:
            return 'nil'
        return str(expr.value)

    def visitUnaryExpr(self, expr: Unary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name: str, *exprs: [Expr]):
        str_list = []
        str_list.append('(')
        str_list.append(name)
        for expr in exprs:
            str_list.append(' ')
            str_list.append(expr.accept(self))
        str_list.append(')')
        return ''.join(str_list)


def main(args):
    expression = Binary(
        Unary(
            Token(TokenType.MINUS, '-', None, 1),
            Literal(123),
        ),
        Token(TokenType.STAR, '*', None, 1),
        Grouping(
            Literal(45.67),
        ),
    )
    print(AstPrinter().print(expression))


if __name__ == '__main__':
    main(sys.argv)
