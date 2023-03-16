program ::= statement*
statement ::= if_statement | while_loop | expression_statement | jump_statement
if_statement ::= "if" expression block ("else" block)?
while_loop ::= "while" expression block
expression_statement ::= expression ";"
jump_statement ::= "jump" | "break"
expression ::= term (("+" | "-") term)*
term ::= factor (("*" | "//") factor)*
factor ::= number | identifier | "(" expression ")"
block ::= "{" statement* "}"

class Parser:
    def __init__(self, lex):
        self.lex = lex
        self.current_token = self.lex.get_next_token()

    def parse(self):
        while self.current_token is not None:
            self.statement()

    def match(self, family):
        if self.current_token is not None and self.current_token.family == family:
            token = self.current_token
            self.current_token = self.lex.get_next_token()
            return token
        else:
            raise SyntaxError(f"Expected {family} but found {self.current_token.family}")

    def statement(self):
        if self.current_token.family == "Keyword":
            if self.current_token.recognized_string == "if":
                self.if_statement()
            elif self.current_token.recognized_string == "while":
                self.while_loop()
            else:
                raise SyntaxError(f"Unexpected keyword {self.current_token.recognized_string}")
        elif self.current_token.family == "Numbers" or self.current_token.family == "ID" or self.current_token.recognized_string == "(":
            self.expression_statement()
        elif self.current_token.family == "Jump":
            self.jump_statement()
        else:
            raise SyntaxError(f"Unexpected token {self.current_token.recognized_string}")

    def if_statement(self):
        self.match("Keyword")
        self.expression()
        self.block()
        if self.current_token is not None and self.current_token.recognized_string == "else":
            self.match("Keyword")
            self.block()

    def while_loop(self):
        self.match("Keyword")
        self.expression()
        self.block()

    def expression_statement(self):
        self.expression()
        self.match("Delimiter")

    def jump_statement(self):
        self.match("Jump")

    def expression(self):
        self.term()
        while self.current_token is not None and self.current_token.recognized_string in ["+", "-"]:
            self.match("AddOperators")
            self.term()

    def term(self):
        self.factor()
        while self.current_token is not None and self.current_token.recognized_string in ["*", "//"]:
            self.match("MulOperators")
            self.factor()

    def factor(tokens):
        if tokens and tokens[0].family == "GroupSymbols" and tokens[0].recognized_string == "(":
            tokens.pop(0)
            expr(tokens)
            if tokens and tokens[0].family == "GroupSymbols" and tokens[0].recognized_string == ")":
                tokens.pop(0)
        elif tokens and tokens[0].family == "Numbers":
            tokens.pop(0)
        else:
            raise SyntaxError("Invalid factor")

    def main():
        lex = Lex("test.txt")
        tokens = []
        token = lex.get_next_token()
        while token is not None:
            tokens.append(token)
            token = lex.get_next_token()
        expr(tokens)
        print("Syntax analysis successful")