from enum import Enum


class Token:
    """The token class"""

    def __init__(self, lit=''):
        self.literal: str = lit
        self.type: TokenType = TokenType.EOF


class TokenType(Enum):
    ILLEGAL = 1
    EOF = 2

    INT = 3
    IDENT = 4

    LSQUARE = 5
    RSQUARE = 6
    FSLASH = 7
    PERIOD = 8
    QUOTE = 9
    COLON = 10
    HYPHEN = 11
    SPACE = 12
