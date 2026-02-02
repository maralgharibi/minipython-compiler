# test_parser.py

from lexer import Lexer
from parser import Parser

test_code = """
var x = 10;
var y = x + 5;
if (x > 5) {
    print("Hello");
}
"""

lexer = Lexer(test_code)
parser = Parser(lexer)

try:
    ast = parser.parse()
    print("Parsing successful!")
    print(f"AST Root: {ast}")
    print(f"Number of statements: {len(ast.statements)}")
    
    for i, stmt in enumerate(ast.statements):
        print(f"\nStatement {i}: {stmt}")
        
except Exception as e:
    print(f"Parsing error: {e}")