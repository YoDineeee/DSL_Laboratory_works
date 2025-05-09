import re
from tokens import Token, TokenType

class Lexer:
    def __init__(self):
        self.token_patterns = [
            (TokenType.PROCESS, r'PROCESS'),
            (TokenType.TITLE, r'TITLE'),
            (TokenType.YIELD, r'YIELD'),
            (TokenType.TIME, r'TIME'),
            (TokenType.COMPONENT, r'COMPONENT'),
            (TokenType.STEP, r'STEP'),
            (TokenType.TEMP, r'TEMP'),
            (TokenType.STRING, r'"[^"]*"'),
            (TokenType.NUMBER, r'\d+(\.\d+)?'),
            (TokenType.UNIT, r'(g|ml|tsp|tbsp|cup|vehicles)'),
            (TokenType.TIME_UNIT, r'(min|hr|day|days)'),
            (TokenType.TEMP_UNIT, r'(C|F)'),
            (TokenType.COLON, r':'),
            (TokenType.SEMICOLON, r';'),
            (TokenType.COMMA, r','),
            (TokenType.LBRACE, r'\{'),
            (TokenType.RBRACE, r'\}'),
            ('WHITESPACE', r'[ \t]+'),
            ('NEWLINE', r'\n')
        ]
        
    def tokenize(self, text):
        tokens = []
        position = 0
        line, column = 1, 1
        
        while position < len(text):
            match_found = False
            
            for token_type, pattern in self.token_patterns:
                regex = re.compile(f'^{pattern}')
                match = regex.match(text[position:])
                
                if match:
                    value = match.group(0)
                    
                    if token_type == 'NEWLINE':
                        line += 1
                        column = 1
                    elif token_type != 'WHITESPACE':
                        if isinstance(token_type, str):
                            # Skip internal token types like WHITESPACE
                            pass
                        else:
                            tokens.append(Token(token_type, value, line, column))
                        column += len(value)
                    else:
                        column += len(value)
                        
                    position += len(value)
                    match_found = True
                    break
                    
            if not match_found:
                raise ValueError(f"Unexpected character '{text[position]}' at line {line}, column {column}")
                
        # Add EOF token
        tokens.append(Token(TokenType.EOF, '', line, column))
        return tokens
