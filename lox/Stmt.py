from abc import ABC, abstractmethod

from lox.scanner import Token


class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor: 'Visitor'):
        pass


class Visitor(ABC):
    @abstractmethod
    def visitBlockStmt(stmt: 'Block'):
        pass

    @abstractmethod
    def visitExpressionStmt(stmt: 'Expression'):
        pass

    @abstractmethod
    def visitIfStmt(stmt: 'If'):
        pass

    @abstractmethod
    def visitPrintStmt(stmt: 'Print'):
        pass

    @abstractmethod
    def visitVarStmt(stmt: 'Var'):
        pass

    @abstractmethod
    def visitWhileStmt(stmt: 'While'):
        pass


class Block(Stmt):
    def __init__(self, statements: 'List[Stmt]'):
        self.statements = statements

    def accept(self, visitor: 'Visitor'):
        return visitor.visitBlockStmt(self)


class Expression(Stmt):
    def __init__(self, expression: 'Expr'):
        self.expression = expression

    def accept(self, visitor: 'Visitor'):
        return visitor.visitExpressionStmt(self)


class If(Stmt):
    def __init__(self, condition: 'Expr', thenBranch: 'Stmt', elseBranch: 'Stmt'):
        self.condition = condition
        self.thenBranch = thenBranch
        self.elseBranch = elseBranch

    def accept(self, visitor: 'Visitor'):
        return visitor.visitIfStmt(self)


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


class While(Stmt):
    def __init__(self, condition: 'Expr', body: 'Stmt'):
        self.condition = condition
        self.body = body

    def accept(self, visitor: 'Visitor'):
        return visitor.visitWhileStmt(self)
