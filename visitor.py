from abc import ABC, abstractmethod
from ast import *

class ASTVisitor(ABC):
    """Abstract visitor interface for AST nodes"""
    
    @abstractmethod
    def visit_program(self, node: Program):
        pass
    
    @abstractmethod
    def visit_var_declaration(self, node: VarDeclaration):
        pass
    
    @abstractmethod
    def visit_assignment(self, node: Assignment):
        pass
    
    @abstractmethod
    def visit_if_statement(self, node: IfStatement):
        pass
    
    @abstractmethod
    def visit_while_statement(self, node: WhileStatement):
        pass
    
    @abstractmethod
    def visit_function_declaration(self, node: FunctionDeclaration):
        pass
    
    @abstractmethod
    def visit_return_statement(self, node: ReturnStatement):
        pass
    
    @abstractmethod
    def visit_expression_statement(self, node: ExpressionStatement):
        pass
    
    @abstractmethod
    def visit_block(self, node: Block):
        pass
    
    @abstractmethod
    def visit_binary_op(self, node: BinaryOp):
        pass
    
    @abstractmethod
    def visit_unary_op(self, node: UnaryOp):
        pass
    
    @abstractmethod
    def visit_call_expression(self, node: CallExpression):
        pass
    
    @abstractmethod
    def visit_identifier(self, node: Identifier):
        pass
    
    @abstractmethod
    def visit_literal(self, node: Literal):
        pass


# visitor.py (continued)

class PrintVisitor(ASTVisitor):
    """Visitor that prints AST structure with indentation"""
    
    def __init__(self):
        self.indent_level = 0
    
    def _indent(self):
        return "  " * self.indent_level
    
    def _print(self, text):
        print(f"{self._indent()}{text}")
    
    def visit_program(self, node: Program):
        self._print("Program:")
        self.indent_level += 1
        for stmt in node.statements:
            stmt.accept(self)
        self.indent_level -= 1
    
    def visit_var_declaration(self, node: VarDeclaration):
        self._print(f"VarDeclaration: {node.var_name}")
        self.indent_level += 1
        self._print("Value:")
        self.indent_level += 1
        node.value.accept(self)
        self.indent_level -= 2
    
    def visit_assignment(self, node: Assignment):
        self._print(f"Assignment: {node.var_name}")
        self.indent_level += 1
        self._print("Value:")
        self.indent_level += 1
        node.value.accept(self)
        self.indent_level -= 2
    
    def visit_if_statement(self, node: IfStatement):
        self._print("IfStatement:")
        self.indent_level += 1
        
        self._print("Condition:")
        self.indent_level += 1
        node.condition.accept(self)
        self.indent_level -= 1
        
        self._print("Then:")
        self.indent_level += 1
        node.then_block.accept(self)
        self.indent_level -= 1
        
        if node.else_block:
            self._print("Else:")
            self.indent_level += 1
            node.else_block.accept(self)
            self.indent_level -= 1
        
        self.indent_level -= 1
    
    def visit_while_statement(self, node: WhileStatement):
        self._print("WhileStatement:")
        self.indent_level += 1
        
        self._print("Condition:")
        self.indent_level += 1
        node.condition.accept(self)
        self.indent_level -= 1
        
        self._print("Body:")
        self.indent_level += 1
        node.body.accept(self)
        self.indent_level -= 1
        
        self.indent_level -= 1
    
    def visit_function_declaration(self, node: FunctionDeclaration):
        self._print(f"FunctionDeclaration: {node.func_name}")
        self.indent_level += 1
        
        self._print(f"Parameters: {', '.join(node.params)}")
        
        self._print("Body:")
        self.indent_level += 1
        node.body.accept(self)
        self.indent_level -= 1
        
        self.indent_level -= 1
    
    def visit_return_statement(self, node: ReturnStatement):
        self._print("ReturnStatement:")
        self.indent_level += 1
        node.value.accept(self)
        self.indent_level -= 1
    
    def visit_expression_statement(self, node: ExpressionStatement):
        self._print("ExpressionStatement:")
        self.indent_level += 1
        node.expression.accept(self)
        self.indent_level -= 1
    
    def visit_block(self, node: Block):
        self._print("Block:")
        self.indent_level += 1
        for stmt in node.statements:
            stmt.accept(self)
        self.indent_level -= 1
    
    def visit_binary_op(self, node: BinaryOp):
        self._print(f"BinaryOp: {node.op}")
        self.indent_level += 1
        
        self._print("Left:")
        self.indent_level += 1
        node.left.accept(self)
        self.indent_level -= 1
        
        self._print("Right:")
        self.indent_level += 1
        node.right.accept(self)
        self.indent_level -= 1
        
        self.indent_level -= 1
    
    def visit_unary_op(self, node: UnaryOp):
        self._print(f"UnaryOp: {node.op}")
        self.indent_level += 1
        node.expr.accept(self)
        self.indent_level -= 1
    
    def visit_call_expression(self, node: CallExpression):
        self._print(f"CallExpression: {node.func_name}")
        self.indent_level += 1
        
        if node.arguments:
            self._print("Arguments:")
            self.indent_level += 1
            for arg in node.arguments:
                arg.accept(self)
            self.indent_level -= 1
        
        self.indent_level -= 1
    
    def visit_identifier(self, node: Identifier):
        self._print(f"Identifier: {node.name}")
    
    def visit_literal(self, node: Literal):
        self._print(f"{node.type_name}Literal: {node.value}")