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

        while self.currTok.type is not TokenType.EOF:
            if self.parseStatement(out):
                return out
            else:
                return None

    def parseStatement(self, out):
        """"""
        if not self.parseIP():
            return False
        if not self.parseHyphenSep():
            return False
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
        if not self.currTokenIs(TokenType.INT):
            return False
        for _ in range(3):
            res = self.eatIP()
            if not res:
                return False

        return True

    def parseHyphenSep(self):
        """"""
        if not self.expectPeek(TokenType.SPACE):
            return False
        self.readToken()

        if not self.expectPeek(TokenType.HYPHEN):
            return False
        self.readToken()

        if not self.expectPeek(TokenType.SPACE):
            return False
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

        # skipping over http header for now
        while self.currTok.type is not TokenType.QUOTE:
            self.readToken()

        return True

    def parseStatus(self, out):
        """"""
        allowed_statuses = [200, 301, 400, 401, 403, 404, 405, 500]
        if not self.expectPeek(TokenType.INT):
            return False
        self.readToken()
        if int(self.currTok.literal) not in allowed_statuses:
            return False

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

    def eatIP(self):
        """Parse an IP address."""
        if not self.expectPeek(TokenType.PERIOD):
            return False
        self.readToken()

        if not self.expectPeek(TokenType.INT):
            return False
        self.readToken()

        return True

    def expectPeek(self, tt: TokenType):
        """"""
        if self.nextTokenIs(tt):
            return True
        return False

    def nextTokenIs(self, tt: TokenType):
        """"""
        return self.nextTok.type is tt

    def currTokenIs(self, tt: TokenType):
        """"""
        return self.currTok.type is tt
