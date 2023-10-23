"""
Input format:
<IP Address> - [<date>] "GET /projects/260 HTTP/1.1" <status code> <file size>

(if the format is not this one, the line must be skipped)
"""

from logParser.lexer import Lexer
from logParser.token import Token, TokenType


def newParser(ll: Lexer):
    """Define and initialize a new parser."""
    pp = Parser(ll)
    pp.readToken()
    pp.readToken()

    return pp


class Parser:
    """"""

    def __init__(self, lexer: Lexer):
        self.ll = lexer
        self.currTok = Token()
        self.nextTok = Token()

    def readToken(self):
        """Advance internal state of the parser."""
        self.currTok = self.nextTok
        self.nextTok = self.ll.nextToken()

    def parseProgram(self):
        """Central Parsing Unit."""
        out = {}

        while not self.currTokenIs(TokenType.EOF):
            if self.parseStatement(out):
                return out
            else:
                return None

    def parseStatement(self, out):
        """"""
        self.parseIP()

        if not self.parseDateTime():
            return False

        if not self.expectPeek(TokenType.SPACE):
            return False
        self.readToken()

        if not self.parseHeader(out):
            return False

        if not self.expectPeek(TokenType.SPACE):
            return False
        self.readToken()

        if not self.parseStatus(out):
            return False

        if not self.expectPeek(TokenType.SPACE):
            return False
        self.readToken()

        if not self.parseFileSize(out):
            return False
        if not self.expectPeek(TokenType.EOF):
            return False

        return True

    def parseIP(self):
        """"""
        while not self.currTokenIs(TokenType.HYPHEN) and not\
                self.currTokenIs(TokenType.EOF):
            self.readToken()

        if self.expectPeek(TokenType.SPACE):
            self.readToken()

        return True

    def parseDateTime(self):
        """Parse dates in datetime format"""
        if not self.expectPeek(TokenType.LSQUARE):
            return False
        self.readToken()

        if not self.eatDate():
            return False

        if not self.expectPeek(TokenType.SPACE):
            return False
        self.readToken()

        if not self.eatTime():
            return False

        if not self.expectPeek(TokenType.RSQUARE):
            return False
        self.readToken()

        return True

    def parseHeader(self, out):
        """"""
        if not self.expectPeek(TokenType.QUOTE):
            return False
        self.readToken()
        self.readToken()

        lit = ""

        while self.currTok.type is not TokenType.QUOTE:
            lit += self.currTok.literal
            self.readToken()

        return lit == "GET /projects/260 HTTP/1.1"

    def parseStatus(self, out):
        """"""
        allowed_statuses = [200, 301, 400, 401, 403, 404, 405, 500]
        if not self.expectPeek(TokenType.INT):
            self.readToken()
            out["status"] = "nil"
            return True

        self.readToken()
        if int(self.currTok.literal) in allowed_statuses:
            out["status"] = self.currTok.literal

        return True

    def parseFileSize(self, out):
        """"""
        if not self.expectPeek(TokenType.INT):
            return False
        self.readToken()
        out["filesize"] = int(self.currTok.literal)

        return True

    def eatDate(self):
        """Parse date portion of a datetime string."""
        if not self.expectPeek(TokenType.INT):
            return False
        self.readToken()

        if not self.expectPeek(TokenType.HYPHEN):
            return False
        self.readToken()

        if not self.expectPeek(TokenType.INT):
            return False
        self.readToken()

        if not self.expectPeek(TokenType.HYPHEN):
            return False
        self.readToken()

        if not self.expectPeek(TokenType.INT):
            return False
        self.readToken()

        return True

    def eatTime(self):
        """Parse time portion of a datetime string."""
        if not self.expectPeek(TokenType.INT):
            return False
        self.readToken()

        if not self.expectPeek(TokenType.COLON):
            return False
        self.readToken()

        if not self.expectPeek(TokenType.INT):
            return False
        self.readToken()

        if not self.expectPeek(TokenType.COLON):
            return False
        self.readToken()

        if not self.expectPeek(TokenType.INT):
            return False
        self.readToken()

        if not self.expectPeek(TokenType.PERIOD):
            return False
        self.readToken()

        if not self.expectPeek(TokenType.INT):
            return False
        self.readToken()

        return True

    def expectPeek(self, tt: TokenType):
        """Check if next token is a given TokenType
        without advancing the internal state"""
        if self.nextTokenIs(tt):
            return True
        return False

    def nextTokenIs(self, tt: TokenType):
        """Check next TokenType."""
        return self.nextTok.type is tt

    def currTokenIs(self, tt: TokenType):
        """Check current TokenType."""
        return self.currTok.type is tt
