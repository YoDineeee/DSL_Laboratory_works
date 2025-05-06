import re
from Token import Token

class Lexer:
    def __init__(self):
        self.tokens = []
        self.token_patterns = {
            'KEYWORD': r'(PROCESS|TITLE|YIELD|TIME|COMPONENT|STEP|TEMP)',
            'STRING': r'"[^"]*"',
            'NUMBER': r'[0-9]+(\.[0-9]+)?',
            'UNIT': r'(g|ml|tsp|tbsp|cup|vehicles)',
            'TIME_UNIT': r'(min|hr|day|days)',
            'TEMP_UNIT': r'(C|F)',
            'ID': r'[a-zA-Z][a-zA-Z0-9_]*',
            'COLON': r':',
            'SEMICOLON': r';',
            'COMMA': r',',
            'LBRACE': r'\{',
            'RBRACE': r'\}',
            'WHITESPACE': r'[ \t]+',
            'NEWLINE': r'\n'
        }

    def tokenize(self, text):
        self.tokens = []
        position = 0
        line = 1
        column = 1
        length = len(text)
        
        while position < length:
            match_found = False
            
            for token_type, pattern in self.token_patterns.items():
                regex = re.compile(f'^{pattern}')
                segment = text[position:]
                match = regex.match(segment)
                
                if match:
                    value = match.group(0)
                    
                    if token_type == 'NEWLINE':
                        line += 1
                        column = 1
                    elif token_type == 'WHITESPACE':
                        column += len(value)
                    else:
                        self.tokens.append(Token(token_type, value, line, column))
                        column += len(value)
                    
                    position += len(value)
                    match_found = True
                    break
                    
            if not match_found:
                snippet = text[position:min(position + 20, length)]
                raise ValueError(f"Unrecognized token at position {position}, line {line}, column {column}: '{snippet}'")
                
        self.tokens.append(Token('EOF', '', line, column))
        return self.tokens
