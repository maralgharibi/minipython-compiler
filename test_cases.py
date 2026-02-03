from lexer import Lexer
from parser import Parser
from visitor import PrintVisitor

def run_test(name, code, expected_errors=0):
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print(f"{'='*60}")
    print("Input code:")
    print(code)
    print("\n" + "-"*40)
    
    lexer = Lexer(code)
    parser = Parser(lexer)
    
    try:
        ast = parser.parse()
        
        if parser.had_error:
            print(f"\n❌ Test FAILED - Expected {expected_errors} errors")
        else:
            print(f"\n✅ Test PASSED")
            print(f"AST has {len(ast.statements)} statements")
            
            # Show AST structure
            if len(ast.statements) > 0:
                print("\nAST Structure:")
                visitor = PrintVisitor()
                ast.accept(visitor)
    
    except Exception as e:
        print(f"\n💥 UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()

# ============ TEST CASE 1: Valid code covering all features ============
test1 = """
var x = 10;
var y = x * 2 + 5;

if (x > y) {
    print("x is greater");
} else {
    print("y is greater or equal");
}

while (x < 100) {
    x = x + 10;
}

def multiply(a, b) {
    return a * b;
}

result = multiply(5, 3);
"""

# ============ TEST CASE 2: Valid code with nested structures ============
test2 = """
var i = 0;
var j = 0;

while (i < 3) {
    j = 0;
    while (j < 3) {
        if (i == j) {
            print("Diagonal");
        } else {
            if (i > j) {
                print("Below diagonal");
            } else {
                print("Above diagonal");
            }
        }
        j = j + 1;
    }
    i = i + 1;
}

def factorial(n) {
    if (n == 0) {  # Changed from n <= 1
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}
"""

# ============ TEST CASE 3: Invalid code (syntax errors) ============
test3 = """
var x = 10              # 1. Missing semicolon
if (x > 5 {             # 2. Missing closing paren
    print("Hello");
else {                  # 3. else without if
    print("World")
}                       # 4. Missing semicolon in block

def func( {              # 5. Invalid function declaration
    return 42;
}

y = ;                    # (OPTIONAL extra error if you want 6)

"""


# ============ TEST CASE 4: Complex expressions and function calls ============
test4 = """
# Complex arithmetic
var a = 10 * (2 + 3) - 4 / 2;
var b = -a + 5 * 2;

# Nested function calls
def max(x, y) {
    if (x > y) {
        return x;
    } else {
        return y;
    }
}

def min(x, y) {
    if (x < y) {
        return x;
    } else {
        return y;
    }
}

result = max(min(10, 20), min(15, 25));
print("Result is: ", result);

# Chained comparisons
if (a > 0 && a < 100) {
    print("a is between 0 and 100");
}
"""

if __name__ == "__main__":
    print("MINIPYTHON PARSER TEST SUITE")
    print("="*60)
    
    run_test("1. Valid code with all features", test1)
    run_test("2. Nested structures", test2)
    run_test("3. Invalid code (error handling)", test3, expected_errors=10)
    run_test("4. Complex expressions", test4)
    
    print(f"\n{'='*60}")
    print("TEST SUITE COMPLETE")
    print(f"{'='*60}")