class Parser:
    def __init__(self, lex):
        self.lex = lex
        self.current_token = self.lex.get_next_token()

    def parse(self):
        self.start_rule()
        while self.current_token is not None:
            raise SyntaxError(f"Unexpected token {self.current_token.recognized_string}")

    def match(self, family):
        if self.current_token is not None and self.current_token.family == family:
            token = self.current_token
            self.current_token = self.lex.get_next_token()
            return token
        else:
            raise SyntaxError(f"Expected {family} but found {self.current_token.family}")

    def start_rule(self):
        self.def_main_part()
        self.call_main_part()

    def def_main_part(self):
        while self.current_token is not None and self.current_token.recognized_string == "def":
            self.def_main_function()

    def def_main_function(self):
        self.match("def")
        self.match("ID")
        self.match("(")
        self.match(")")
        self.match(":")
        self.match("#")
        self.match("{")
        self.declarations()
        while self.current_token is not None and self.current_token.recognized_string == "def":
            self.def_function()
        self.statements()
        self.match("#")
        self.match("}")

    def def_function(self):
        self.match("def")
        self.match("ID")
        self.match("(")
        self.id_list()
        self.match(")")
        self.match(":")
        self.match("#")
        self.match("{")
        self.declarations()
        while self.current_token is not None and self.current_token.recognized_string == "def":
            self.def_function()
        self.statements()
        self.match("#")
        self.match("}")

    def declarations(self):
        while self.current_token is not None and self.current_token.recognized_string == "#declare":
            self.declaration_line()

    def declaration_line(self):
        self.match("#declare")
        self.id_list()

    def statements(self):
        self.statement()
        while self.current_token is not None and self.current_token.family == "Keyword":
            self.statement()

    def statement(self):
        if self.current_token.family == "ID":
            self.assignment_stat()
        elif self.current_token.family == "Keyword":
            if self.current_token.recognized_string == "print":
                self.print_stat()
            elif self.current_token.recognized_string == "return":
                self.return_stat()
            elif self.current_token.recognized_string == "if":
                self.if_stat()
            elif self.current_token.recognized_string == "while":
                self.while_stat()
            else:
                raise SyntaxError(f"Unexpected keyword {self.current_token.recognized_string}")
        else:
            raise SyntaxError(f"Unexpected token {self.current_token.recognized_string}")

    def assignment_stat(self):
        self.match("ID")
        self.match("=")
        self.match("(")
        if self.current_token.family == "Keyword":
            raise SyntaxError(f"Cannot assign a keyword as a value '{self.current_token.recognized_string}'")
        else:
            self.expression()
            self.match(")")

    def print_stat(self):
        self.match("print")
        self.match("(")
        self.expression()
        self.match(")")

    def return_stat(self):
        self.match("return")
        self.match("(")
        self.expression()
        self.match(")")

    def id_list(self):
        self.match("ID")
        while self.current_token is not None and self.current_token.recognized_string == ",":
            self.match(",")
            self.match("ID")

    def expression(self):
        if self.current_token.recognized_string in tokens["AddOperators"]:
            self.optional_sign()
        self.term()
        while self.current_token is not None and self.current_token.recognized_string in tokens["AddOperators"]:
            self.match(self.current_token.family)
            self.term()

    def term(self):
        self.factor()
        while self.current_token is not None and self.current_token.family in token["MulOperators"]:
            self.match(self.current_token.family)
            self.factor()
    
    def factor(self):
        if self.current_token.family == "Integer":
            return self.match("Integer")
        elif self.current_token.recognized_string == "(":
            self.match("(")
            result = self.expression()
            self.match(")")
            return result
        elif self.current_token.family == "ID":
            id_token = self.match("ID")
            return self.idtail(id_token)
        else:
            raise SyntaxError(f"Expected integer or '(', found {self.current_token.recognized_string}")

    def idtail(self):
        if self.current_token.type == "(":
            self.match("(")
            self.actual_par_list()
            self.match(")")
        else:
            pass

    def actual_par_list(self):
        if self.current_token.recognized_string == "(" or self.current_token.family == "Integer" or self.current_token.family == "ID":
            self.expression()
            while self.current_token.recognized_string == ",":
                self.match(",")
                self.expression()
        else:
            pass

    def optional_sign(self):
        if self.current_token.recognized_string in tokens["AddOperators"]:
            self.match("AddOperators")
        else:
            pass

    def condition(self):
        self.bool_term()
        while self.current_token.type == "or":
            self.match("or")
            self.bool_term()

    def bool_term(self):
        self.bool_factor()
        while self.current_token.type == "and":
            self.match("and")
            self.bool_factor()

    def bool_factor(self):
        if self.current_token.type == "not":
            self.match("not")
            self.match("(")
            self.condition()
            self.match(")")
        elif self.current_token.type == "(":
            self.match("(")
            self.condition()
            self.match(")")
        else:
            self.expression()
            self.match("RelOperators")

    def call_main_part(self):
        self.match("if")
        self.match("name")
        self.match("==")
        self.match("Main")
        self.match(":")
        while self.current_token.family == "ID":
            self.main_function_call()

    def main_function_call(self):
        self.match("ID")
        self.match("(")
        self.match(")")
        self.match(";")
