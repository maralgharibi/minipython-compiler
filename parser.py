from lexer import Lexer, Token, TokenType
from ast import *


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.tokens = lexer.tokenize()
        self.current_token_index = 0
        self.current_token = self.tokens[0] if self.tokens else None
        self.had_error = False 
    
    def error(self, message: str):
        """Report parsing error without crashing"""
        if self.current_token and self.current_token.type == TokenType.EOF:
            self.had_error = True
            return

        self.had_error = True
        line = self.current_token.line if self.current_token else 1
        col = self.current_token.column if self.current_token else 1
        
        print(f"\n❌ PARSER ERROR at line {line}, column {col}:")
        print(f"   {message}")
        
        if hasattr(self.lexer, 'text'):
            lines = self.lexer.text.split('\n')
            if line - 1 < len(lines):
                print(f"   {lines[line-1]}")
                print(f"   {' ' * (col-1)}^")
        
        self.synchronize()
    
    def synchronize(self):
        sync_tokens = {
            TokenType.SEMI,
            TokenType.RBRACE,
            TokenType.IF,
            TokenType.WHILE,
            TokenType.DEF,
            TokenType.RETURN,
            TokenType.VAR
        }

        while self.current_token and self.current_token.type not in sync_tokens:
            self.current_token_index += 1
            if self.current_token_index < len(self.tokens):
                self.current_token = self.tokens[self.current_token_index]
            else:
                self.current_token = None

        if self.current_token and self.current_token.type == TokenType.SEMI:
            self.current_token_index += 1
            if self.current_token_index < len(self.tokens):
                self.current_token = self.tokens[self.current_token_index]
            else:
                self.current_token = None

            
    
    def eat(self, token_type: TokenType):
        """Consume current token if it matches expected type"""
        if self.current_token and self.current_token.type == token_type:
            self.current_token_index += 1
            if self.current_token_index < len(self.tokens):
                self.current_token = self.tokens[self.current_token_index]
            else:
                self.current_token = None
        else:
            expected = token_type
            found = self.current_token.type if self.current_token else "EOF"
            self.error(f"Expected {expected}, found {found}")
    
    def peek(self, token_type: TokenType) -> bool:
        """Check next token without consuming it"""
        if self.current_token and self.current_token.type == token_type:
            return True
        return False
    
    def peek_ahead(self, n: int = 1) -> Token:
        """Look ahead n tokens"""
        idx = self.current_token_index + n
        if idx < len(self.tokens):
            return self.tokens[idx]
        return Token(TokenType.EOF, None, 0, 0)
    
    # ============ EXPRESSION PARSING ============
    
    def parse_factor(self) -> Expression:
        """factor → INT | FLOAT | STRING | ID | "(" expr ")" | call_expr"""
        token = self.current_token
        
        if token.type == TokenType.INT:
            self.eat(TokenType.INT)
            return IntegerLiteral(token.value)
        
        elif token.type == TokenType.FLOAT:
            self.eat(TokenType.FLOAT)
            return FloatLiteral(token.value)
        
        elif token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            return StringLiteral(token.value)
        
        elif token.type == TokenType.ID:
            # Check if it's a function call
            if self.peek_ahead().type == TokenType.LPAREN:
                return self.parse_call_expression()
            else:
                self.eat(TokenType.ID)
                return Identifier(token.value)
        
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            expr = self.parse_logical_or()

            self.eat(TokenType.RPAREN)
            return expr
        
        elif token.type in (TokenType.PLUS, TokenType.MINUS):
            op = token.value
            self.eat(token.type)
            expr = self.parse_factor()
            return UnaryOp(op, expr)
        
        else:
            self.error(f"Unexpected token in factor: {token.type}")
            self.eat(token.type)
            return IntegerLiteral(0)  

    
    def parse_call_expression(self) -> CallExpression:
        """call_expr → ID "(" arg_list? ")" """
        func_name = self.current_token.value
        self.eat(TokenType.ID)
        self.eat(TokenType.LPAREN)
        
        arguments = []
        if not self.peek(TokenType.RPAREN):
            arguments.append(self.parse_expression())
            while self.peek(TokenType.COMMA):
                self.eat(TokenType.COMMA)
                arguments.append(self.parse_expression())
        
        self.eat(TokenType.RPAREN)
        return CallExpression(func_name, arguments)
    
    def parse_term(self) -> Expression:
        """term → factor (("*" | "/") factor)*"""
        node = self.parse_factor()
        
        while self.current_token and self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            op = self.current_token.value
            self.eat(self.current_token.type)
            right = self.parse_factor()
            node = BinaryOp(node, op, right)
        
        return node
    
    def parse_expression(self) -> Expression:
        """expr → term (("+" | "-") term)*"""
        node = self.parse_term()
        
        while self.current_token and self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            op = self.current_token.value
            self.eat(self.current_token.type)
            right = self.parse_term()
            node = BinaryOp(node, op, right)
        
        return node
    
    def parse_comparison(self) -> Expression:
        """comparison → expr ((">" | "<" | "==" | "!=") expr)?"""
        node = self.parse_expression()
        
        while self.current_token and self.current_token.type in (
            TokenType.GT,
            TokenType.LT,
            TokenType.GTE,
            TokenType.LTE,
            TokenType.EQ,
            TokenType.NEQ,
        ):

            op = self.current_token.value
            self.eat(self.current_token.type)
            right = self.parse_expression()
            node = BinaryOp(node, op, right)
        
        return node
    
    def parse_logical_and(self) -> Expression:
        node = self.parse_comparison()

        while self.current_token and self.current_token.type == TokenType.AND:
            op = self.current_token.value
            self.eat(TokenType.AND)
            right = self.parse_comparison()
            node = BinaryOp(node, op, right)

        return node


    def parse_logical_or(self) -> Expression:
        node = self.parse_logical_and()

        while self.current_token and self.current_token.type == TokenType.OR:
            op = self.current_token.value
            self.eat(TokenType.OR)
            right = self.parse_logical_and()
            node = BinaryOp(node, op, right)

        return node

    # ============ STATEMENT PARSING ============
    
    def parse_var_declaration(self) -> VarDeclaration:
        """var_decl → "var" ID "=" expr ";" """
        self.eat(TokenType.VAR)
        var_name = self.current_token.value
        self.eat(TokenType.ID)
        self.eat(TokenType.ASSIGN)
        value = self.parse_expression()
        self.eat(TokenType.SEMI)
        return VarDeclaration(var_name, value)
    
    def parse_assignment(self) -> Assignment:
        var_name = self.current_token.value
        self.eat(TokenType.ID)
        self.eat(TokenType.ASSIGN)

        if self.peek(TokenType.SEMI):
            self.error("Missing expression in assignment")
            self.eat(TokenType.SEMI)
            return Assignment(var_name, IntegerLiteral(0))

        value = self.parse_expression()
        self.eat(TokenType.SEMI)
        return Assignment(var_name, value)

    
    def parse_if_statement(self) -> IfStatement:
        """if_stmt → "if" "(" expr ")" block ("else" block)? """
        self.eat(TokenType.IF)
        self.eat(TokenType.LPAREN)
        condition = self.parse_logical_or()
        self.eat(TokenType.RPAREN)
        
        then_block = self.parse_block()
        
        else_block = None
        if self.peek(TokenType.ELSE):
            self.eat(TokenType.ELSE)

            if self.peek(TokenType.IF):
                # else if → else { if (...) { ... } }
                else_block = Block([self.parse_if_statement()])
            else:
                else_block = self.parse_block()

        
        return IfStatement(condition, then_block, else_block)
    
    def parse_while_statement(self) -> WhileStatement:
        """while_stmt → "while" "(" expr ")" block """
        self.eat(TokenType.WHILE)
        self.eat(TokenType.LPAREN)
        condition = self.parse_logical_or()
        self.eat(TokenType.RPAREN)
        body = self.parse_block()
        return WhileStatement(condition, body)
    
    def parse_function_declaration(self) -> FunctionDeclaration:
        """func_decl → "def" ID "(" param_list? ")" block """
        self.eat(TokenType.DEF)
        func_name = self.current_token.value
        self.eat(TokenType.ID)
        self.eat(TokenType.LPAREN)
        
        params = []
        if not self.peek(TokenType.RPAREN):
            if not self.peek(TokenType.ID):
                self.error("Expected parameter name")
            else:
                params.append(self.current_token.value)
                self.eat(TokenType.ID)

            while self.peek(TokenType.COMMA):
                self.eat(TokenType.COMMA)
                params.append(self.current_token.value)
                self.eat(TokenType.ID)
        
        self.eat(TokenType.RPAREN)
        body = self.parse_block()
        return FunctionDeclaration(func_name, params, body)
    
    def parse_return_statement(self) -> ReturnStatement:
        """return_stmt → "return" expr ";" """
        self.eat(TokenType.RETURN)
        value = self.parse_expression()
        self.eat(TokenType.SEMI)
        return ReturnStatement(value)
    
    def parse_block(self) -> Block:
        """block → "{" statement* "}" """
        if not self.peek(TokenType.LBRACE):
            self.error("Expected '{' to start block")
            return Block([])

        self.eat(TokenType.LBRACE)
        statements = []
        
        while not self.peek(TokenType.RBRACE) and not self.peek(TokenType.EOF):
            statements.append(self.parse_statement())
        
        self.eat(TokenType.RBRACE)
        return Block(statements)
    
    def parse_expression_statement(self) -> ExpressionStatement:
        """expr_stmt → expr ";" """
        expr = self.parse_expression()
        self.eat(TokenType.SEMI)
        return ExpressionStatement(expr)
    
# parser.py (continued)

    def parse_statement(self) -> Statement:
        """statement → var_decl | assignment | if_stmt | while_stmt 
                     | func_decl | return_stmt | expr_stmt """
        
        if self.peek(TokenType.VAR):
            return self.parse_var_declaration()
        
        elif self.peek(TokenType.IF):
            return self.parse_if_statement()
        
        elif self.peek(TokenType.WHILE):
            return self.parse_while_statement()
        
        elif self.peek(TokenType.DEF):
            return self.parse_function_declaration()
        
        elif self.peek(TokenType.RETURN):
            return self.parse_return_statement()
        
        elif self.peek(TokenType.ID):
            if self.peek_ahead().type == TokenType.ASSIGN:
                return self.parse_assignment()
            else:
                return self.parse_expression_statement()
            
        elif self.peek(TokenType.ELSE):
            self.error("Unexpected 'else' without matching 'if'")
            self.eat(TokenType.ELSE)
            return ExpressionStatement(IntegerLiteral(0))
        
        else:
            return self.parse_expression_statement()
    
    def parse_program(self) -> Program:
        """program → statement* """
        statements = []
        
        while self.current_token and self.current_token.type != TokenType.EOF:
            statements.append(self.parse_statement())
        
        return Program(statements)
    
    def parse(self) -> Program:
        """Main entry point: parse tokens into AST"""
        ast = self.parse_program()
        
        if self.had_error:
            print("\n⚠️  Parsing completed with errors")
        else:
            print("✅ Parsing successful")
        
        return ast
    
