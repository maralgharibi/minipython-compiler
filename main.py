import sys
from lexer import Lexer
from parser import Parser
from visitor import PrintVisitor

def main():
    if len(sys.argv) > 1:
        # Read from file
        filename = sys.argv[1]
        try:
            with open(filename, 'r') as f:
                code = f.read()
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found")
            return
    else:
        # Interactive mode
        print("MiniPython Parser - Interactive Mode")
        print("Enter your code (end with empty line):")
        print("-" * 40)
        
        lines = []
        while True:
            line = input()
            if line.strip() == "":
                break
            lines.append(line)
        
        code = "\n".join(lines)
    
    if not code.strip():
        print("No input provided")
        return
    
    print("\n" + "="*60)
    print("PARSING RESULT:")
    print("="*60)
    
    # Lexing
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    print(f"\nTokens generated: {len(tokens)}")
    if len(tokens) <= 20:  # Don't flood output
        for token in tokens:
            print(f"  {token}")
    
    # Parsing
    parser = Parser(lexer)
    ast = parser.parse()
    
    # AST Output
    if not parser.had_error:
        print(f"\n✅ Parsing successful!")
        print(f"AST contains {len(ast.statements)} statements")
        
        print("\n" + "-"*40)
        print("AST STRUCTURE:")
        print("-"*40)
        
        visitor = PrintVisitor()
        ast.accept(visitor)
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()