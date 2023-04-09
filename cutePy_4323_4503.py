# Varsos Vasileios | AM: 4323
# Raphael Tzortzis | AM: 4503

import string
import sys
import pdb

tokens = {
    "Keywords": ["while", "if", "else", "do", "or", "and", "not","#declare","input","print","return","def"],
    "AddOperators": ["+", "-"],
    "MulOperators": ["*", "//"],
    "RelOperators": ["==", ">=", "<",">","<=", "<>", "!="],
    "Assignment": ["="],
    "Delimiters": [",", ".", ";"],
    "GroupSymbols": ["(", ")", "[", "]", "#{", "#}"],
    "Comments": ["#$"],
    "Underscore" : ["_"],
}


class Token:
    def __init__(self, recognized_string, family, line_number):
        self.recognized_string = recognized_string
        self.family = family
        self.line_number = line_number

class Lex:
    def __init__(self, file_name):
        self.file_name = file_name
        self.current_line = 1
        self.current_char = None
        self.file_pointer = None
        self.current_position = None

        self.open_file()

    def open_file(self):
        self.file_pointer = open(self.file_name, 'r')
        self.current_char = self.file_pointer.read(1)

    def close_file(self):
        self.file_pointer.close()

    def get_next_char(self):
        position_old = self.current_position
        self.current_char = self.file_pointer.read(1)
        position_new = self.file_pointer.tell()
        if self.current_char == '\n':
            self.current_line += 1
        if position_old == position_new:
            return Token("", "EOF", self.current_line)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.get_next_char()
                continue

            if self.current_char in tokens["GroupSymbols"]:
                recognized_string = self.current_char
                family = "GroupSymbols"
                line_number = self.current_line
                self.get_next_char()
                return Token(recognized_string, family, line_number)

            if self.current_char in tokens["AddOperators"]:
                recognized_string = self.current_char
                family = "AddOperators"
                line_number = self.current_line
                self.get_next_char()
                return Token(recognized_string, family, line_number)

            if self.current_char in ["*", "/"]:
                char2 = self.file_pointer.read(1)
                if char2 == "/":
                    recognized_string = self.current_char + char2
                    family = "MulOperators"
                    line_number = self.current_line
                    self.get_next_char()
                    self.get_next_char()
                    return Token(recognized_string, family, line_number)
                else:
                    recognized_string = self.current_char
                    family = "MulOperators"
                    line_number = self.current_line
                    self.get_next_char()
                    return Token(recognized_string, family, line_number)

            if self.current_char in tokens["Delimiters"]:
                recognized_string = self.current_char
                family = "Delimiters"
                line_number = self.current_line
                self.get_next_char()
                return Token(recognized_string, family, line_number)

            if (self.current_char == "="):
                recognized_string = self.current_char
                char2 = self.file_pointer.read(1)
                if (char2 == "="):
                    recognized_string += char2
                    family = "RelOperators"
                    line_number = self.current_line
                    self.get_next_char()
                    self.get_next_char()
                    return Token(recognized_string, family, line_number)
                else:
                    recognized_string = self.current_char
                    family = "Assignment"
                    line_number = self.current_line
                    self.get_next_char()
                    return Token(recognized_string, family, line_number)

            if (self.current_char == ">"):
                recognized_string = self.current_char
                char2 = self.file_pointer.read(1)
                if (char2 == "="):
                    recognized_string += char2
                    self.get_next_char()
                family = "RelOperators"
                line_number = self.current_line
                self.get_next_char()
                return Token(recognized_string, family, line_number)

            if (self.current_char == "<"):
                recognized_string = self.current_char
                char2 = self.file_pointer.read(1)
                if (char2 == "=" or ">"):
                    recognized_string += char2
                    self.get_next_char()
                family = "RelOperators"
                line_number = self.current_line
                self.get_next_char()
                return Token(recognized_string, family, line_number)

            if (self.current_char == "!"):
                recognized_string = self.current_char
                char2 = self.file_pointer.read(1)
                if (char2 == "="):
                    recognized_string += char2
                    self.get_next_char()
                    family = "RelOperators"
                    line_number = self.current_line
                    self.get_next_char()
                    return Token(recognized_string, family, line_number)
                else:
                    raise SyntaxError(f"Expected '=', found something else")

            if self.current_char.isdigit():
                recognized_string = self.current_char
                while self.current_char is not None and not self.current_char.isspace():
                    char2 = self.file_pointer.read(1)
                    if (char2.isdigit()):
                        recognized_string += char2
                    else:
                        raise SyntaxError(f"Expected integer, found something else. If you're trying to set an ID, it must begin with a letter")
                    self.get_next_char()
                family = "Integer"
                line_number = self.current_line
                return Token(recognized_string, family, line_number)

            if self.current_char.isalpha():
                recognized_string = self.current_char
                while self.current_char is not None and (self.current_char.isalpha() or self.current_char.isdigit() or self.current_char == "_"):
                    recognized_string += self.current_char
                    self.current_char = self.get_next_char()

                if recognized_string in tokens["Keywords"]:
                    family = "Keyword"
                else:
                    family = "ID"

                line_number = self.current_line
                return Token(recognized_string, family, line_number)

            if self.current_char.isalpha():
                recognized_string = self.current_char
                while self.get_next_char() is not None and (self.current_char.isalpha() or self.current_char.isdigit() or self.current_char == "_"):
                    recognized_string += self.current_char
                    self.current_char = self.get_next_char()

                family = "ID"
                if recognized_string in tokens["Keywords"]:
                    family = "Keyword"

                line_number = self.current_line
                return Token(recognized_string, family, line_number)

            if (self.current_char == "_"):
                recognized_string = self.current_char
                str1 = self.file_pointer.read(7)
                if (str1 == "__main__"):
                    recognized_string = self.get_next_char() + str1
                    family = "Main"
                    line_number = self.current_line
                    self.get_next_char()
                    self.get_next_char()
                    self.get_next_char()
                    self.get_next_char()
                    self.get_next_char()
                    self.get_next_char()
                    self.get_next_char()
                    return Token(recognized_string, family, line_number)
                elif (str1 == "__name__"):
                    recognized_string = self.get_next_char() + str1
                    family = "Name"
                    line_number = self.current_line
                    self.get_next_char()
                    self.get_next_char()
                    self.get_next_char()
                    self.get_next_char()
                    self.get_next_char()
                    self.get_next_char()
                    self.get_next_char()
                    return Token(recognized_string, family, line_number)
                else:
                    pass

            if (self.current_char == "#"):
                recognized_string = self.current_char
                char2 = self.file_pointer.read(1)
                if (char2 == "{"):
                    recognized_string += char2
                    while self.get_next_char():
                        newchar = self.file_pointer.read(1)
                        recognized_string += newchar
                    self.get_next_char()
                    if (newchar == "#"):
                        char3 = self.file_pointer.read(1)
                        if (char3 == "}"):
                            family = "Declaration"
                            line_number = self.current_line
                            return Token(recognized_string, family, line_number)
                    if not newchar:
                        raise SyntaxError(f"Unfinished declaration in line {self.current_token.line_number}")
                elif (char2 != "{"):
                    str1 = self.file_pointer.read(7)
                    if (str1 == "declare"):
                        recognized_string = self.get_next_char() + str1
                        family = "Declaration"
                        line_number = self.current_line
                        self.get_next_char()
                        self.get_next_char()
                        self.get_next_char()
                        self.get_next_char()
                        self.get_next_char()
                        self.get_next_char()
                        self.get_next_char()
                        return Token(recognized_string, family, line_number)
                elif (char2 == "$"):
                    recognized_string = self.get_next_char() + char2
                    while self.get_next_char():
                        newchar = self.file_pointer.read(1)
                        recognized_string += newchar
                    self.get_next_char()
                    if (newchar == "#"):
                        char3 = self.file_pointer.read(1)
                        if (char3 == "$"):
                            family = "Comment"
                            line_number = self.current_line
                            return Token(recognized_string, family, line_number)
                    if not newchar:
                        raise SyntaxError(f"Unfinished Comment in line {self.current_token.line_number}")
                elif (char2 != "{" | "$"):
                    if not newchar:
                        raise SyntaxError(f"Unfinished comment or declaration in line {self.current_token.line_number}")
                else:
                    raise SyntaxError(f"Unexpected use of # in line {self.current_token.line_number}")


class Parser:
    def __init__(self, filename):
        self.filename = filename
        self.lex = Lex(filename)
        self.current_token = None
        self.get_next_token()

    def parse(self):
        self.start_rule()
        print(self.current_token.recognized_string)
        while self.current_token is not None:
            raise SyntaxError(f"Unexpected token {self.current_token.recognized_string}")

    def get_next_token(self):
       self.current_token = self.lex.get_next_token()

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
        self.match("Keywords")
        self.match("ID") 
        self.match("GroupSymbols")
        self.match("GroupSymbols")
        self.match("Delimiters")
        self.match("GroupSymbols")
        self.declarations()
        while self.current_token is not None and self.current_token.recognized_string == "def":
            self.def_function()
        self.statements()
        self.match("GroupSymbols")

    def def_function(self):
        self.match("Keywords")
        self.match("ID")
        self.match("GroupSymbols")
        self.id_list()
        self.match("GroupSymbols")
        self.match("Delimiters")
        self.match("GroupSymbols")
        self.declarations()
        while self.current_token is not None and self.current_token.recognized_string == "def":
            self.def_function()
        self.statements()
        self.match("GroupSymbols")

    def declarations(self):
        while self.current_token is not None and self.current_token.family == "Declaration":
            self.declaration_line()

    def declaration_line(self):
        self.match("Declaration")
        self.id_list()

    def statements(self):
        self.statement()
        while self.current_token is not None and self.current_token.family == "Keyword":
            self.statement()
    
    def statement(self):
        if self.current_token.recognized_string in ["print", "return"] or self.current_token.family == "ID":
            self.simple_statement()
        elif self.current_token.recognized_string in ["while", "if"]:
            self.structured_statement()
        else:
            raise SyntaxError("Unknown Keyword or Statement")

    def simple_statement(self):
        if self.current_token.family == "ID":
            self.assignment_stat()
        elif self.current_token.recognized_string == "print":
            self.print_stat()
        elif self.current_token.recognized_string == "return":
            self.return_stat()

    def structured_statement(self):
        if self.current_token.recognized_string == "while":
            self.while_stat()
        elif self.current_token.recognized_string == "if":
            self.if_stat()

    def assignment_stat(self):
        self.match("ID")
        self.match("Assignment")
        self.match("GroupSymbols")
        if self.current_token.family == "Keywords":
            raise SyntaxError(f"Cannot assign a keyword as a value '{self.current_token.recognized_string}'")
        else:
            if self.current_token.family == "Integer":
                self.match("Integer")
                self.match("GroupSymbols")
                if self.current_token.recognized_string == "input":
                    self.match("Keywords")
                    self.match("GroupSymbols")
                    self.match("GroupSymbols")
                    self.match("GroupSymbols")
                    self.match("Delimeters")
                else: 
                    raise SyntaxError(f"Expected input'")
            else:
                self.expression()
                self.match("Delimeters")

    def return_stat(self):
        self.match("Keywords")
        self.match("GroupSymbols")
        self.expression()
        self.match("GroupSymbols")

    def print_stat(self):
        self.match("Keywords")
        self.match("GroupSymbols")
        self.expression()
        self.match("GroupSymbols")

    def if_stat(self):
        if self.current_token.recognized_string == "if":
            self.match("Keywords")
            if not self.match('GroupSymbols'):
                raise SyntaxError("Expected '(' after 'if'.")
            self.condition()
            if not self.match("GroupSymbols"):
                raise SyntaxError("Expected ')' after condition.")
            if not self.match("Delimeters"):
                raise SyntaxError("Expected ':' after condition.")
            if self.current_token.recognized_string == "#{":
                self.match("GroupSymbols")
                self.statements()
                if not self.match("GroupSymbols"):
                    raise SyntaxError("Expected '#}' after conditions.")
            else:
                self.statement()
        if self.current_token.recognized_string == "else":
                    self.match("Keywords")
                    if not self.match("Delimeters"):
                        raise SyntaxError("Expected ':' after 'else'.")
                    if self.current_token.recognized_string == "#{":
                        self.match("GroupSymbols")
                        self.statements()
                        if not self.match("GroupSymbols"):
                            raise SyntaxError("Expected '#}' after conditions.")
                    else:
                        self.statement()

    def call_main_part(self):
        if self.current_token.recognized_string == "if":
            self.match("Keyword")
            if self.current_token.recognized_string == "__name__":
                self.match("Name")
                if self.current_token.recognized_string == "==":
                    self.match("RelOperators")
                    if self.current_token.family == "Main":
                        self.match("Main")
                        if self.current_token.recognized_string == ":":
                            self.match("Delimeters")
                            while self.current_token.family == "ID":
                                self.main_function_call()
                        else:
                            raise SyntaxError("Expected ':' but found something else.")

    def main_function_call(self):
        self.match("ID")
        self.match("GroupSymbols")
        self.match("GroupSymbols")
        self.match("Delimeters")

    def while_stat(self):
        self.match('Keywords')
        if not self.match("GroupSymbols"):
            raise SyntaxError("Expected '(' after 'while'.")
        self.condition()
        if not self.match("GroupSymbols"):
            raise SyntaxError("Expected ')' after condition.")
        if not self.match("Delimeters"):
            raise SyntaxError("Expected ':' after condition.")
        self.statement()

    def id_list(self):
        self.match("ID")
        while self.current_token is not None and self.current_token.recognized_string == ",":
            self.match("Delimeters")
            self.match("ID")

    def expression(self):
        if self.current_token.family == "AddOperators":
            self.optional_sign()
        self.term()
        while self.current_token is not None and self.current_token.family == "AddOperators":
            self.match("AddOperators")
            self.term()

    def term(self):
        self.factor()
        while self.current_token is not None and self.current_token.family == "MulOperators":
            self.match('MulOperators')
            self.factor()
    
    def factor(self):
        if self.current_token.family == "Integer":
            self.match("Integer")
        elif self.current_token.recognized_string == "(":
            self.match("GroupSymbols")
            result = self.expression()
            self.match("GroupSymbols")
            return result
        elif self.current_token.family == "ID":
            id_token = self.match("ID")
            self.idtail(id_token)
        else:
            raise SyntaxError(f"Expected integer or '(', found {self.current_token.recognized_string}")

    def idtail(self):
        if self.current_token.recognized_string == "(":
            self.match("GroupSymbols")
            self.actual_par_list()
            self.match("GroupSymbols")
        else:
            pass

    def actual_par_list(self):
        self.expression()
        if self.current_token.recognized_string == "(":
            self.expression()
            while self.current_token.recognized_string == ",":
                self.match("Delimeters")
                self.expression()
        else:
            pass

    def optional_sign(self):
        if self.current_token.family == "AddOperators":
            self.match("AddOperators")
        else:
            pass

    def condition(self):
        self.bool_term()
        while self.current_token.recognized_string == "or":
            self.match("Keywords")
            self.bool_term()

    def bool_term(self):
        self.bool_factor()
        while self.current_token.recognized_string == "and":
            self.match("Keywords")
            self.bool_factor()

    def bool_factor(self):
        if self.current_token.recognized_string == "not":
            self.match("Keywords")
            self.match("GroupSymbols")
            self.condition()
            self.match("GroupSymbols")
        elif self.current_token.recognized_string == "[":
            self.match("GroupSymbols")
            self.condition()
            self.match("GroupSymbols")
        else:
            self.expression()
            self.match("RelOperators")
            self.expression()



def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <filename>")
        return

    filename = sys.argv[1]

    parser = Parser(filename)
    result = parser.parse()

    if result:
        print("Compilation successful!")
    else:
        print("Compilation failed.")

if __name__ == '__main__':
    main()

