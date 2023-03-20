import string

tokens = {
    "Keywords": ["while", "if", "else", "do", "jump", "break", "declare","input","print","return","def"],
    "AddOperators": ["+", "-"],
    "MulOperators": ["*", "//"],
    "RelOperators": ["==", ">=", "<", "<>", "!="],
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

        self.open_file()

    def open_file(self):
        self.file_pointer = open(self.file_name, 'r')
        self.current_char = self.file_pointer.read(1)

    def close_file(self):
        self.file_pointer.close()

    def get_next_char(self):
        self.current_char = self.file_pointer.read(1)
        if self.current_char == '\n':
            self.current_line += 1

    def get_next_token(self):
        while self.current_char:
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
                if (self.current_char == "/"):
                    if (char2 == "/"):
                        recognized_string = self.current_char + char2
                        family = "MulOperators"
                        line_number = self.current_line
                        self.get_next_char()
                        self.get_next_char()
                        return Token(recognized_string, family, line_number)
                        
                    else:
                        raise SyntaxError(f"Expected '/', found {self.current_token.recognized_string}")
                else:
                    recognized_string = self.current_char
                    family = "MulOperators"
                    line_number = self.current_line
                    self.get_next_char()
                    return Token(recognized_string, family, line_number)

            if self.current_char in tokens["Delimiters"]:
                recognized_string = self.current_char
                family = "Delimiter"
                line_number = self.current_line
                self.get_next_char()
                return Token(recognized_string, family, line_number)

            if (self.current_char == "="):
                char2 = self.file_pointer.read(1)
                if (char2 == "="):
                    recognized_string = self.current_char + char2
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
                char2 = self.file_pointer.read(1)
                if (char2 == "="):
                    recognized_string = self.current_char + char2
                    family = "RelOperators"
                    line_number = self.current_line
                    self.get_next_char()
                    self.get_next_char()
                    return Token(recognized_string, family, line_number)

            if self.current_char.isdigit():
                recognized_string = self.current_char 
                while not self.current_char.isspace():
                    char2 = self.file_pointer.read(1)
                    if (char2.isdigit()):
                        recognized_string += char2
                    if (char2 == "."):
                        raise SyntaxError(f"Expected integer, found floating point")
                    self.get_next_char()
                family = "Integer"
                line_number = self.current_line
                return Token(recognized_string, family, line_number)

            if self.current_char.isalpha():
                recognized_string = "" 
                while self.current_char.isalnum() or self.current_char == "_":
                    recognized_string += self.current_char
                    self.get_next_char()

                family = "ID"
                if recognized_string in tokens["Keywords"]:
                    family = "Keyword"

                line_number = self.current_line
                return Token(recognized_string, family, line_number)
            

            if (self.current_char == "_"):
                recognized_string = self.current_char 
                str1 = self.file_pointer.read(7)
                if (str1 == "__main__"):
                    recognized_string = self.current_char + str1
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
              
            if(self.current_char.isspace):
                self.get_next_char()


def main():
    lex = Lex("test.txt")
    token = lex.get_next_token()
    while token is not None:
        print(token.recognized_string,token.family,token.line_number)
        token = lex.get_next_token()


if __name__ == "__main__":
    main()      