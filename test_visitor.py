# test_visitor.py - FIXED VERSION

from lexer import Lexer
from parser import Parser
from visitor import PrintVisitor

test_code = """
var x = 10;
var y = x + 20;
if (x > 5) {
    print("x is greater than 5");
} else {
    print("x is 5 or less");
}
while (y < 100) {
    y = y + 10;
}
def add(a, b) {
    return a + b;
}
"""

print("=== Source Code ===")
print(test_code)

print("\n=== Lexing ===")
lexer1 = Lexer(test_code)  # First lexer for token display
tokens = lexer1.tokenize()
for token in tokens[:10]:  # Show first 10 tokens
    print(token)

print("\n=== Parsing ===")
lexer2 = Lexer(test_code)  # FRESH lexer for parser
parser = Parser(lexer2)
ast = parser.parse()
print(f"Parsed successfully! {len(ast.statements)} statements")

print("\n=== AST Structure (Visitor Output) ===")
print("=" * 50)
visitor = PrintVisitor()
ast.accept(visitor)
print("=" * 50)