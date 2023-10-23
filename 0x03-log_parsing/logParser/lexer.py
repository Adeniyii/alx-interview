from logParser.token import Token, TokenType


class Lexer:
    """The lexer class."""

    def __init__(self, input: str):
        self.input = input
        self.pos = 0
        self.nextPos = 0
        self.ch = ''

    def readChar(self):
        """Initializes and advances position and character attributes."""
        if self.nextPos >= len(self.input):
            self.ch = None
            return

        self.ch = self.input[self.nextPos]
        self.pos = self.nextPos
        self.nextPos += 1

    def readIdent(self):
        """Reads a consecutive set of alphabets."""
        start = self.pos
        while str(self.ch).isalpha():
            self.readChar()

        return self.input[start: self.pos]

    def readDigit(self):
        """Reads a consecutive set of numbers."""
        start = self.pos
        while str(self.ch).isnumeric():
            self.readChar()

        return self.input[start: self.pos]

    def nextToken(self):
        """Reads the current char, and constructs a corresponding token."""
        tok = Token()
        ch = self.ch

        # why the f*** does python not have switch statements?
        if ch is None or ch == '\n':
            tok.literal = ""
            tok.type = TokenType.EOF
        elif ch == '[':
            tok.literal = str(self.ch)  # python doesn't do type narrowing :|
            tok.type = TokenType.LSQUARE
        elif ch == ']':
            tok.literal = str(self.ch)
            tok.type = TokenType.RSQUARE
        elif ch == '/':
            tok.literal = str(self.ch)
            tok.type = TokenType.FSLASH
        elif ch == '.':
            tok.literal = str(self.ch)
            tok.type = TokenType.PERIOD
        elif ch == '-':
            tok.literal = str(self.ch)
            tok.type = TokenType.HYPHEN
        elif ch == ':':
            tok.literal = str(self.ch)
            tok.type = TokenType.COLON
        elif ch == '"':
            tok.literal = str(self.ch)
            tok.type = TokenType.QUOTE
        elif ch == ' ':
            tok.literal = str(self.ch)
            tok.type = TokenType.SPACE
        else:
            if str(self.ch).isalpha():
                tok.literal = self.readIdent()
                tok.type = TokenType.IDENT
                return tok
            elif str(self.ch).isnumeric():
                tok.literal = self.readDigit()
                tok.type = TokenType.INT
                return tok
            else:
                tok.literal = str(self.ch)
                tok.type = TokenType.ILLEGAL

        self.readChar()
        return tok


def newLexer(input: str):
    """Initializes a lexer object and it's internal state."""
    ll = Lexer(input)
    ll.readChar()
    return ll
