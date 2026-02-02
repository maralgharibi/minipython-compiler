# ast.py

from abc import ABC, abstractmethod

class ASTNode(ABC):
    """Abstract base class for all AST nodes"""
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor (Visitor Pattern)"""
        pass
    
    def __repr__(self):
        return f"{self.__class__.__name__}()"
    
# ast.py (continued)

# ============ EXPRESSIONS ============
class Expression(ASTNode):
    """Base class for all expressions"""
    @abstractmethod
    def accept(self, visitor):
        pass



class Literal(Expression):
    """Literal value (int, float, string)"""
    def __init__(self, value, type_name="Literal"):
        self.value = value
        self.type_name = type_name
    
    def accept(self, visitor):
        return visitor.visit_literal(self)
    
    def __repr__(self):
         return f"{self.type_name}Literal({self.value})"

class IntegerLiteral(Literal):
    """Integer literal"""
    def __init__(self, value):
        super().__init__(value, "Integer")

class FloatLiteral(Literal):
    """Float literal"""
    def __init__(self, value):
        super().__init__(value, "Float")

class StringLiteral(Literal):
    """String literal"""
    def __init__(self, value):
        super().__init__(value, "String")

class Identifier(Expression):
    """Variable identifier"""
    def __init__(self, name):
        self.name = name
    
    def accept(self, visitor):
        return visitor.visit_identifier(self)
    
    def __repr__(self):
        return f"Identifier('{self.name}')"

class BinaryOp(Expression):
    """Binary operation (e.g., a + b)"""
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    
    def accept(self, visitor):
        return visitor.visit_binary_op(self)
    
    def __repr__(self):
        return f"BinaryOp({self.left} {self.op} {self.right})"

class UnaryOp(Expression):
    """Unary operation (e.g., -x)"""
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr
    
    def accept(self, visitor):
        return visitor.visit_unary_op(self)
    
    def __repr__(self):
        return f"UnaryOp({self.op} {self.expr})"

class CallExpression(Expression):
    """Function call"""
    def __init__(self, func_name, arguments):
        self.func_name = func_name
        self.arguments = arguments  # List of expressions
    
    def accept(self, visitor):
        return visitor.visit_call_expression(self)
    
    def __repr__(self):
        args = ', '.join(str(arg) for arg in self.arguments)
        return f"CallExpression({self.func_name}, [{args}])"
    
# ast.py (continued)

# ============ STATEMENTS ============

class Statement(ASTNode):
    """Base class for all statements"""
    @abstractmethod
    def accept(self, visitor):
        pass

class Program(Statement):
    """Root node: contains list of statements"""
    def __init__(self, statements):
        self.statements = statements  # List of statements
    
    def accept(self, visitor):
        return visitor.visit_program(self)
    
    def __repr__(self):
        stmts = '\n  '.join(str(stmt) for stmt in self.statements)
        return f"Program([\n  {stmts}\n])"

class VarDeclaration(Statement):
    """Variable declaration: var x = 10;"""
    def __init__(self, var_name, value):
        self.var_name = var_name
        self.value = value  # Expression
    
    def accept(self, visitor):
        return visitor.visit_var_declaration(self)
    
    def __repr__(self):
        return f"VarDeclaration('{self.var_name}', {self.value})"

class Assignment(Statement):
    """Assignment: x = 10;"""
    def __init__(self, var_name, value):
        self.var_name = var_name
        self.value = value  # Expression
    
    def accept(self, visitor):
        return visitor.visit_assignment(self)
    
    def __repr__(self):
        return f"Assignment('{self.var_name}', {self.value})"

class Block(Statement):
    """Block of statements: { stmt1; stmt2; }"""
    def __init__(self, statements):
        self.statements = statements  # List of statements
    
    def accept(self, visitor):
        return visitor.visit_block(self)
    
    def __repr__(self):
        stmts = '\n    '.join(str(stmt) for stmt in self.statements)
        return f"Block([\n    {stmts}\n  ])"

class IfStatement(Statement):
    """If statement: if (condition) { ... } else { ... }"""
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition  # Expression
        self.then_block = then_block  # Block
        self.else_block = else_block  # Block or None
    
    def accept(self, visitor):
        return visitor.visit_if_statement(self)
    
    def __repr__(self):
        else_part = f", else={self.else_block}" if self.else_block else ""
        return f"IfStatement({self.condition}, {self.then_block}{else_part})"

class WhileStatement(Statement):
    """While loop: while (condition) { ... }"""
    def __init__(self, condition, body):
        self.condition = condition  # Expression
        self.body = body  # Block
    
    def accept(self, visitor):
        return visitor.visit_while_statement(self)
    
    def __repr__(self):
        return f"WhileStatement({self.condition}, {self.body})"

class FunctionDeclaration(Statement):
    """Function declaration: def func(x, y) { ... }"""
    def __init__(self, func_name, params, body):
        self.func_name = func_name
        self.params = params  # List of parameter names
        self.body = body  # Block
    
    def accept(self, visitor):
        return visitor.visit_function_declaration(self)
    
    def __repr__(self):
        params = ', '.join(self.params)
        return f"FunctionDeclaration('{self.func_name}', [{params}], {self.body})"

class ReturnStatement(Statement):
    """Return statement: return value;"""
    def __init__(self, value):
        self.value = value  # Expression
    
    def accept(self, visitor):
        return visitor.visit_return_statement(self)
    
    def __repr__(self):
        return f"ReturnStatement({self.value})"

class ExpressionStatement(Statement):
    """Expression as statement: x + 5;"""
    def __init__(self, expression):
        self.expression = expression
    
    def accept(self, visitor):
        return visitor.visit_expression_statement(self)
    
    def __repr__(self):
        return f"ExpressionStatement({self.expression})"