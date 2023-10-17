from abc import ABC, abstractmethod

from lox.scanner import Token


class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor: 'Visitor'):
        pass


class Visitor(ABC):
    @abstractmethod
    def visitExpressionStmt(stmt: 'Expression'):
        pass

    @abstractmethod
    def visitPrintStmt(stmt: 'Print'):
        pass


class Expression(Stmt):
    def __init__(self, expressoin: 'Expr'):
        self.expressoin = expressoin

    def accept(self, visitor: 'Visitor'):
        return visitor.visitExpressionStmt(self)


class Print(Stmt):
    def __init__(self, expression: 'Expr'):
        self.expression = expression

    def accept(self, visitor: 'Visitor'):
        return visitor.visitPrintStmt(self)
