from enum import Enum, auto


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
    ID = auto()

    # Special
    EOF = auto()