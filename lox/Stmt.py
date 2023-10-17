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

    @abstractmethod
    def visitVarStmt(stmt: 'Var'):
        pass


class Expression(Stmt):
    def __init__(self, expression: 'Expr'):
        self.expression = expression

    def accept(self, visitor: 'Visitor'):
        return visitor.visitExpressionStmt(self)


class Print(Stmt):
    def __init__(self, expression: 'Expr'):
        self.expression = expression

    def accept(self, visitor: 'Visitor'):
        return visitor.visitPrintStmt(self)


class Var(Stmt):
    def __init__(self, name: 'Token', initializer: 'Expr'):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor: 'Visitor'):
        return visitor.visitVarStmt(self)
