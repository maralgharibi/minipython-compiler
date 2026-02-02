# test_ast.py (create new file or add to main.py temporarily)

from ast import *

# Create some sample nodes
int_lit = IntegerLiteral(42)
str_lit = StringLiteral("hello")
id_node = Identifier("x")
binary_op = BinaryOp(id_node, "+", int_lit)

var_decl = VarDeclaration("y", binary_op)
assign = Assignment("x", int_lit)
block = Block([var_decl, assign])

if_stmt = IfStatement(id_node, block)

# Print them
print("AST Nodes created:")
print(f"  IntegerLiteral: {int_lit}")
print(f"  StringLiteral: {str_lit}")
print(f"  Identifier: {id_node}")
print(f"  BinaryOp: {binary_op}")
print(f"  VarDeclaration: {var_decl}")
print(f"  IfStatement: {if_stmt}")