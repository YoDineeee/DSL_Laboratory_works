from enum import Enum, auto

# Define Token class
class Token:
    def __init__(self, token_type, value, line=0, column=0):
        self.token_type = token_type
        self.value = value
        self.line = line
        self.column = column
        
    def __repr__(self):
        return f"Token({self.token_type}, '{self.value}', line={self.line}, col={self.column})"

# Define token types as enum
class TokenType(Enum):
    # Keywords
    PROCESS = auto()
    TITLE = auto()
    COMPONENT = auto()
    STEP = auto()
    YIELD = auto()
    TIME = auto()
    TEMP = auto()
    # Literals
    STRING = auto()
    NUMBER = auto()
    # Units
    UNIT = auto()
    TIME_UNIT = auto()
    TEMP_UNIT = auto()
    # Symbols
    COLON = auto()
    SEMICOLON = auto()
    COMMA = auto()
    LBRACE = auto()
    RBRACE = auto()
    # Special
    EOF = auto()
