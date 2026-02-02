# lexer.py

class TokenType:
    # Keywords
    VAR = 'VAR'
    DEF = 'DEF'
    IF = 'IF'
    ELSE = 'ELSE'
    WHILE = 'WHILE'
    RETURN = 'RETURN'
    
    # Identifiers and literals
    ID = 'ID'
    INT = 'INT'
    FLOAT = 'FLOAT'
    STRING = 'STRING'
    
    # Operators
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MULTIPLY = 'MULTIPLY'
    DIVIDE = 'DIVIDE'
    ASSIGN = 'ASSIGN'
    EQ = 'EQ'           # ==
    NEQ = 'NEQ'         # !=
    LT = 'LT'           # <
    GT = 'GT'           # >
    
    # Delimiters
    LPAREN = 'LPAREN'   # (
    RPAREN = 'RPAREN'   # )
    LBRACE = 'LBRACE'   # {
    RBRACE = 'RBRACE'   # }
    SEMI = 'SEMI'       # ;
    COMMA = 'COMMA'     # ,

    AND = 'AND'           # &&
    OR = 'OR'             # ||
    LTE = 'LTE'           # <=
    GTE = 'GTE'   
    # Special
    EOF = 'EOF'

    # lexer.py (continued)

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type}, '{self.value}', line={self.line}, col={self.column})"
    
# lexer.py (continued)

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = self.text[0] if self.text else None
    
    def error(self, message):
        raise Exception(f"Lexer error at line {self.line}, column {self.column}: {message}")
    
    def advance(self):
        """Move to next character"""
        if self.current_char == '\n':
            self.line += 1
            self.column = 0
        
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
            self.column += 1
        else:
            self.current_char = None
    
    def peek(self):
        """Look ahead one character"""
        peek_pos = self.pos + 1
        if peek_pos < len(self.text):
            return self.text[peek_pos]
        return None
    
    def skip_whitespace(self):
        """Skip spaces, tabs, newlines"""
        while self.current_char and self.current_char in ' \t\r\n':
            self.advance()
    
    def skip_comment(self):
        """Skip single-line comments (# ...)"""
        while self.current_char and self.current_char != '\n':
            self.advance()
        self.advance()  # Skip the newline
    
    def number(self):
        """Read a number (int or float)"""
        result = ''
        start_col = self.column
        
        while self.current_char and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        
        if self.current_char == '.':
            result += self.current_char
            self.advance()
            while self.current_char and self.current_char.isdigit():
                result += self.current_char
                self.advance()
            return Token(TokenType.FLOAT, float(result), self.line, start_col)
        
        return Token(TokenType.INT, int(result), self.line, start_col)
    
    def string(self):
        """Read a string literal"""
        start_col = self.column
        self.advance()  # Skip opening quote
        result = ''
        
        while self.current_char and self.current_char != '"':
            result += self.current_char
            self.advance()
        
        if not self.current_char:
            self.error("Unterminated string")
        
        self.advance()  # Skip closing quote
        return Token(TokenType.STRING, result, self.line, start_col)
    
    def identifier(self):
        """Read an identifier or keyword"""
        result = ''
        start_col = self.column
        
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        # Check if it's a keyword
        keywords = {
            'var': TokenType.VAR,
            'def': TokenType.DEF,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE,
            'return': TokenType.RETURN
        }
        
        token_type = keywords.get(result, TokenType.ID)
        return Token(token_type, result, self.line, start_col)
    
    def get_next_token(self):
        """Main method to get next token"""
        while self.current_char:
            # Skip whitespace
            if self.current_char in ' \t\r\n':
                self.skip_whitespace()
                continue
            
            # Skip comments
            if self.current_char == '#':
                self.skip_comment()
                continue
            
            # Numbers
            if self.current_char.isdigit():
                return self.number()
            
            # Strings
            if self.current_char == '"':
                return self.string()
            
            # Identifiers and keywords
            if self.current_char.isalpha() or self.current_char == '_':
                return self.identifier()
            
            # Operators and delimiters
            start_col = self.column
            char = self.current_char
            
            # Multi-character operators
            if char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.EQ, '==', self.line, start_col)
                return Token(TokenType.ASSIGN, '=', self.line, start_col)
            
            if char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.NEQ, '!=', self.line, start_col)
                self.error(f"Unexpected character: {char}")
            
# In get_next_token() method, find the '<' and '>' handling:

            if char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.LTE, '<=', self.line, start_col)
                return Token(TokenType.LT, '<', self.line, start_col)

            if char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.GTE, '>=', self.line, start_col)
                return Token(TokenType.GT, '>', self.line, start_col)
            
            # In get_next_token() method:
            if char == '&':
                self.advance()
                if self.current_char == '&':
                    self.advance()
                    return Token(TokenType.AND, '&&', self.line, start_col)
                self.error(f"Unexpected character: {char}")

            if char == '|':
                self.advance()
                if self.current_char == '|':
                    self.advance()
                    return Token(TokenType.OR, '||', self.line, start_col)
                self.error(f"Unexpected character: {char}")

            if char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.LTE, '<=', self.line, start_col)
                return Token(TokenType.LT, '<', self.line, start_col)

            if char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.GTE, '>=', self.line, start_col)
                return Token(TokenType.GT, '>', self.line, start_col)
            
            # Single character tokens
            single_tokens = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.MULTIPLY,
                '/': TokenType.DIVIDE,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                ';': TokenType.SEMI,
                ',': TokenType.COMMA
            }
            
            if char in single_tokens:
                self.advance()
                return Token(single_tokens[char], char, self.line, start_col)
            
            # Unknown character
            self.error(f"Unexpected character: {char}")
        
        return Token(TokenType.EOF, None, self.line, self.column)
    
    def tokenize(self):
        """Return all tokens as a list"""
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens