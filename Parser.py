from Scanner import TokenType as tt


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def print(self):
        for token in self.tokens:
            print(token)

    def advance(self):
        temp = self.tokens[self.current]
        self.current += 1

        return temp

    def isAtEnd(self):
        if self.current >= len(self.tokens):
            return True

        return False

    def peek(self):
        return self.tokens[self.current]

    def expect(self, probe):
        if self.peek().type == probe:
            return True
        return False

    def parser(self):
        obj = {}
        try:
            if self.peek().type == tt.LEFT_BRACE:
                obj = self.obj()
            else:
                raise Exception("Not a valid Json file")
        except Exception as e:
            print(e)

        return obj

    def obj(self):
        self.advance()

        if self.expect(tt.RIGTH_BRACE):
            return {}

        if not self.expect(tt.STRING):
            raise Exception("Expected a String")

        string = self.advance().literal
        obj = {}
        while not self.isAtEnd() and self.peek().type != tt.RIGTH_BRACE:

            if not self.expect(tt.COLON):
                raise Exception("COLON expected")
            self.advance()
            obj[string] = self.value()

            if self.expect(tt.RIGTH_BRACE):
                continue

            if not self.expect(tt.COMMA):
                raise Exception("COMMA expected")

            self.advance()

            if not self.expect(tt.STRING) and self.expect(tt.RIGTH_BRACE):
                raise Exception("Expected a String")

            string = self.advance().literal

        self.advance()
        return obj

    def array(self):

        self.advance()
        array = []
        array.append(self.value())
        while not self.isAtEnd() and self.peek().type != tt.RIGTH_BRACKET:
            if self.expect(tt.COMMA):
                self.advance()
            else:
                raise Exception("COMMA expected")
            array.append(self.value())

        if self.peek().type != tt.RIGTH_BRACKET:
            raise Exception("file is not formatted as expected")

        self.advance()

        return array

    def value(self):

        match self.peek().type:
            case tt.NUMBER:
                return int(self.advance().literal)
            case tt.STRING:
                return self.advance().literal
            case tt.TRUE:
                self.advance()
                return True
            case tt.FALSE:
                self.advance()
                return False
            case tt.NULL:
                self.advance()
                return ""
            case tt.LEFT_BRACKET:
                return self.array()
            case tt.LEFT_BRACE:
                return self.obj()
            case _:
                raise Exception("File is not formatted as expected")
