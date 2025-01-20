from enum import Enum


class TokenType(Enum):
    LEFT_BRACE = 1
    RIGTH_BRACE = 2
    LEFT_BRACKET = 3
    RIGTH_BRACKET = 4

    WHITESPACE = 5
    COLON = 6
    COMMA = 7

    STRING = 8
    NUMBER = 9
    OBJECT = 10
    ARRAY = 11
    TRUE = 12
    FALSE = 13
    NULL = 14

    EOF = 18


class Token:

    def __init__(self, type, lexeme, literal, line):

        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self):
        return f"[{self.type} {self.lexeme} {self.literal}]"


class Scanner:

    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.reservedTokens = {"true": TokenType.TRUE,
                               "false": TokenType.FALSE,
                               "null": TokenType.NULL}

    def scanTokens(self):

        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()

        self.tokens.append(Token(TokenType.EOF, "", "", self.line))
        return self.tokens

    def isAtEnd(self):
        return self.current >= len(self.source)

    def scanToken(self):
        c = self.advance()

        match c:
            case '{':
                self.addToken(TokenType.LEFT_BRACE)
            case '}':
                self.addToken(TokenType.RIGTH_BRACE)
            case ',':
                self.addToken(TokenType.COMMA)
            case ':':
                self.addToken(TokenType.COLON)
            case '[':
                self.addToken(TokenType.LEFT_BRACKET)
            case ']':
                self.addToken(TokenType.RIGTH_BRACKET)
            case '"':
                self.string()
            case _:
                if c.isdigit():
                    self.number()
                elif c.isalpha():
                    self.identifier()
                else:
                    return

    def advance(self):
        temp = self.source[self.current]
        self.current += 1
        return temp

    def next_match(self, expected):
        if self.isAtEnd():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self):
        if self.isAtEnd():
            return '\0'
        return self.source[self.current]

    def string(self):

        while (self.peek() != '"' and not self.isAtEnd()):
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.isAtEnd():
            print("Untermined string")
            return

        self.advance()

        value = self.source[self.start+1:self.current - 1]
        self.__addToken(TokenType.STRING, value)

    def number(self):

        while self.peek().isdigit():
            self.advance()

        is_float = False
        if self.peek() == '.' and self.peekNext().isdigit():
            is_float = True
            self.advance()
            while self.peek().isdigit():
                self.advance()

        value = self.source[self.start:self.current]
        if is_float:
            value = float(value)
        else:
            value = int(value)

        self.__addToken(TokenType.NUMBER, value)

    def identifier(self):

        while self.peek().isalpha():
            self.advance()

        value = self.source[self.start:self.current]
        if value in self.reservedTokens.keys():
            self.addToken(self.reservedTokens[value])

    def peekNext(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def addToken(self, type):
        self.__addToken(type, "")

    def __addToken(self, type, literal):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))
