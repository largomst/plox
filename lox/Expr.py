from abc import ABC, abstractmethod

from lox.scanner import Token


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: 'Visitor'):
        pass


class Visitor(ABC):
    @abstractmethod
    def visitAssignExpr(expr: 'Assign'):
        pass

    @abstractmethod
    def visitBinaryExpr(expr: 'Binary'):
        pass

    @abstractmethod
    def visitGroupingExpr(expr: 'Grouping'):
        pass

    @abstractmethod
    def visitLiteralExpr(expr: 'Literal'):
        pass

    @abstractmethod
    def visitUnaryExpr(expr: 'Unary'):
        pass

    @abstractmethod
    def visitVariableExpr(expr: 'Variable'):
        pass


class Assign(Expr):
    def __init__(self, name: 'Token', value: 'Expr'):
        self.name = name
        self.value = value

    def accept(self, visitor: 'Visitor'):
        return visitor.visitAssignExpr(self)


class Binary(Expr):
    def __init__(self, left: 'Expr', operator: 'Token', right: 'Expr'):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: 'Visitor'):
        return visitor.visitBinaryExpr(self)


class Grouping(Expr):
    def __init__(self, expression: 'Expr'):
        self.expression = expression

    def accept(self, visitor: 'Visitor'):
        return visitor.visitGroupingExpr(self)


class Literal(Expr):
    def __init__(self, value: 'object'):
        self.value = value

    def accept(self, visitor: 'Visitor'):
        return visitor.visitLiteralExpr(self)


class Unary(Expr):
    def __init__(self, operator: 'Token', right: 'Expr'):
        self.operator = operator
        self.right = right

    def accept(self, visitor: 'Visitor'):
        return visitor.visitUnaryExpr(self)


class Variable(Expr):
    def __init__(self, name: 'Token'):
        self.name = name

    def accept(self, visitor: 'Visitor'):
        return visitor.visitVariableExpr(self)
