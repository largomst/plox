from abc import ABC, abstractmethod
from typing import List

from lox.error import LoxRuntimeError, runtime_error
from lox.Expr import Assign, Binary, Call, Expr, Grouping, Literal, Logical, Unary, Variable
from lox.Expr import Visitor as eVisitor
from lox.scanner import Token, TokenType
from lox.Stmt import Block, Expression, Function, If, Print, Stmt, Var
from lox.Stmt import Visitor as sVisitor
from lox.Stmt import While


class Environment:
    def __init__(self, enclosing=None):
        self.enclosing = enclosing
        self.values: dict[str, object] = {}

    def define(self, name: str, value: object):
        self.values[name] = value

    def get(self, name: Token):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        if self.enclosing is not None:
            return self.enclosing.get(name)
        raise LoxRuntimeError(name, f'Undefined variable "{name.lexeme}".')

    def assign(self, name: Token, value: object):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
        raise LoxRuntimeError(name, f'Undefined variable "{name.lexeme}".')


class Interpreter(eVisitor, sVisitor):
    def __init__(self):
        self.globals_ = Environment()
        self.environment = self.globals_

        import time

        class clock(LoxCallable):
            def arity(self):
                return 0

            def call(self, interpreter, arguments):
                return time.time()

            def __str__(self):
                return '<native fn>'

        self.globals_.define('clock', clock)

    def visitLiteralExpr(self, expr: Literal):
        return expr.value

    def visitGroupingExpr(self, expr: Grouping):
        return self.evaluate(expr.expression)

    def visitUnaryExpr(self, expr: Unary):
        right = self.evaluate(expr.right)
        match expr.operator.type:
            case TokenType.MINUS:
                self.check_number_operand(expr.operator, right)
                return -float(right)
            case TokenType.BANG:
                return not self.is_truthy(right)

    def check_number_operand(self, operator: Token, operand: object):
        if isinstance(operand, float):
            return
        else:
            raise LoxRuntimeError(operator, 'Operand must be a number.')

    def visitBinaryExpr(self, expr: Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        operator = expr.operator
        match expr.operator.type:
            case TokenType.MINUS:
                self.check_number_operands(operator, left, right)
                return float(left) - float(right)
            case TokenType.SLASH:
                self.check_number_operands(operator, left, right)
                return float(left) / float(right)
            case TokenType.STAR:
                self.check_number_operands(operator, left, right)
                return float(left) * float(right)
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) + float(right)
                if isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)
                raise LoxRuntimeError(expr.operator, 'Operands must be two numbers or strings.')
            case TokenType.GREATER:
                self.check_number_operands(operator, left, right)
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                self.check_number_operands(operator, left, right)
                return float(left) >= float(right)
            case TokenType.LESS:
                self.check_number_operands(operator, left, right)
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                self.check_number_operands(operator, left, right)
                return float(left) <= float(right)
            case TokenType.BANG_EQUAL:
                self.check_number_operands(operator, left, right)
                return not self.is_equal(left, right)
            case TokenType.EQUAL_EQUAL:
                self.check_number_operands(operator, left, right)
                return self.is_equal(left, right)

    def visitCallExpr(self, expr: Call):
        callee = self.evaluate(expr.callee)
        arguments = [self.evaluate(argument) for argument in expr.arguments]
        if not isinstance(callee, LoxCallable):
            raise LoxRuntimeError(expr.paren, 'Can only call functions and classes.')
        function = callee
        # 在函数调用之前检查函数参数的数量
        if len(arguments) != function.arity():
            raise LoxRuntimeError(
                f'Expected {function.arity()} arguments but got{len(arguments)}.'
            )
        return function.call(self, arguments)

    def check_number_operands(self, operator: Token, left: object, right: object):
        if isinstance(left, float) and isinstance(right, float):
            return
        else:
            raise LoxRuntimeError(operator, 'Operands must be a number.')

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def is_equal(self, a, b):
        if a is None and b is None:
            return True
        if a is None:
            return False
        return a == b

    def is_truthy(self, obj: object):
        if obj is None:
            return False
        elif isinstance(obj, bool):
            return bool(obj)
        return True

    def interpret(self, statements: [Stmt]):
        try:
            for statement in statements:
                self.execute(statement)
        except LoxRuntimeError as e:
            runtime_error(e)

    def execute(self, stmt: Stmt):
        stmt.accept(self)

    def stringify(self, obj: object):
        if obj is None:
            return 'nil'
        if isinstance(obj, float):
            text = str(obj)
            if text.endswith('.0'):
                text = text[: len(text) - 2]
            return text
        if isinstance(obj, bool):
            return 'true' if obj else 'false'
        return str(obj)

    def visitExpressionStmt(self, stmt: Expression):
        self.evaluate(stmt.expression)
        return None

    def visitFunctionStmt(self, stmt: Function):
        function = LoxFunction(stmt, self.environment)
        self.environment.define(stmt.name.lexeme, function)
        return None

    def visitPrintStmt(self, stmt: Print):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))
        return None

    def visitReturnStmt(self, stmt: 'Return'):
        value = self.evaluate(stmt.value) if stmt.value != None else None
        raise Return(value)

    def visitVarStmt(self, stmt: Var):
        value = None if stmt.initializer is None else self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)
        return None

    def visitVariableExpr(self, expr: Variable):
        return self.environment.get(expr.name)

    def visitAssignExpr(self, expr: Assign):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    def visitBlockStmt(self, stmt: Block):
        self.execute_block(stmt.statements, Environment(self.environment))
        return None

    def execute_block(self, statements: List[Stmt], environment: Environment):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    def visitIfStmt(self, stmt: If):
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.thenBranch)
        elif stmt.elseBranch is not None:
            self.execute(stmt.elseBranch)
        return None

    def visitLogicalExpr(self, expr: Logical):
        left = self.evaluate(expr.left)
        if expr.operator.type == TokenType.OR:
            if self.is_truthy(left):
                return left
        elif not self.is_truthy(left):   # TokenType.AND
            return left
        return self.evaluate(expr.right)

    def visitWhileStmt(self, stmt: While):
        while self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)
        return None


class LoxCallable(ABC):
    @abstractmethod
    def call(self, interpreter: Interpreter, arguments: List[object]):
        pass

    @abstractmethod
    def arity(self):
        pass


class LoxFunction(LoxCallable):
    def __init__(self, declaration: Function, closure: Environment):
        self.closure = closure
        self.declaration = declaration

    def call(self, interpreter: Interpreter, argument: List[object]) -> object:
        # Important!!! 每次函数调用都要创建新的环境
        environment = Environment(self.closure)
        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, argument[i])
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except Return as return_value:
            return return_value.value
        return None

    def arity(self):
        return len(self.declaration.params)

    def __str__(self):
        return f'<fn {self.declaration.name.lexeme}>'


class Return(LoxRuntimeError):
    def __init__(self, value: object):
        super().__init__(None, None)
        self.value = value
