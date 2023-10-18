from lox.error import LoxRuntimeError, runtime_error
from lox.Expr import Assign, Binary, Expr, Grouping, Literal, Unary, Variable
from lox.Expr import Visitor as eVisitor
from lox.scanner import Token, TokenType
from lox.Stmt import Expression, Print, Stmt, Var
from lox.Stmt import Visitor as sVisitor


class Environment:
    def __init__(self):
        self.values: dict[str, object] = {}

    def define(self, name: str, value: object):
        self.values[name] = value

    def get(self, name: Token):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        raise LoxRuntimeError(name, f'Undefined variable "{name.lexeme}".')

    def assign(self, name: Token, value: object):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        raise LoxRuntimeError(name, f'Undefined variable "{name.lexeme}".')


class Interpreter(eVisitor, sVisitor):
    def __init__(self):
        self.environment = Environment()

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

    def visitPrintStmt(self, stmt: Print):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))
        return None

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
