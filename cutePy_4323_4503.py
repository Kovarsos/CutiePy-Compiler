# Varsos Vasileios | AM: 4323
# Raphael Tzortzis | AM: 4503

import string
import sys
import logging as l
from typing import List


tokens = {
    "Keywords": ["while", "if", "else", "do", "or", "and", "not","#declare","input","print","return","def"],
    "AddOperators": ["+", "-"],
    "MulOperators": ["*", "//"],
    "RelOperators": ["==", ">=", "<",">","<=", "<>", "!="],
    "Assignment": ["="],
    "Delimiters": [",", ".", ";", ":"],
    "GroupSymbols": ["(", ")", "[", "]", "#{", "#}"],
    "Comments": ["#$"],
    "Underscore" : ["_"],
}

quadnum = 1
temp_counter = 1
quadList = []

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
        self.current_position = 0
        self.recognized_string = ""

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
        if self.current_char == '':
            return Token("", "EOF", self.current_line)
        return self.current_char

    def get_next_token(self):
        
        while self.current_char is not None:

            if self.current_char in tokens["AddOperators"]:
                l.debug("Found a AddOperator in: "+ self.current_char)
                recognized_string = self.current_char
                family = "AddOperators"
                line_number = self.current_line
                self.get_next_char()
                
                return Token(recognized_string, family, line_number)

            if self.current_char in tokens["GroupSymbols"]:
                l.debug("Found a GroupSymbol in: "+ self.current_char)
                recognized_string = self.current_char
                family = "GroupSymbols"
                line_number = self.current_line
                self.get_next_char()
                return Token(recognized_string, family, line_number)


            if self.current_char in ["*", "/"]:
                l.debug("Found a * or / in: "+ self.current_char)
                
                char2 = self.file_pointer.read(1)
                if (self.current_char == "/" and char2 == "/"):
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
                l.debug("Found a Delimiter in: "+ self.current_char)
                
                recognized_string = self.current_char
                family = "Delimiters"
                line_number = self.current_line
                self.get_next_char()
                return Token(recognized_string, family, line_number)

            if (self.current_char == "="):
                l.debug("Found a = in: "+ self.current_char)
                
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
                l.debug("Found a RelOperator: "+ self.current_char)
                
                recognized_string = self.current_char
                self.get_next_char()
                if (self.current_char == "="):
                    recognized_string += self.current_char
                family = "RelOperators"
                line_number = self.current_line
                self.get_next_char()
                return Token(recognized_string, family, line_number)

            if (self.current_char == "<"):
                l.debug("Found a RelOperator: "+ self.current_char)
                
                recognized_string = self.current_char
                self.get_next_char()
                if (self.current_char == "=" or self.current_char == ">"):
                    recognized_string += self.current_char
                family = "RelOperators"
                line_number = self.current_line
                self.get_next_char()
                return Token(recognized_string, family, line_number)

            if (self.current_char == "!"):
                l.debug("Found a Delimiter in: "+ self.current_char)
                
                recognized_string = self.current_char
                self.get_next_char
                if (self.current_char == "="):
                    recognized_string += self.current_char
                    family = "RelOperators"
                    line_number = self.current_line
                    self.get_next_char()
                    return Token(recognized_string, family, line_number)
                else:
                    raise SyntaxError(f"Expected '=', found something else")

            if self.current_char.isdigit():
                l.debug("Found an Integer in: ."+ self.current_char + ".")
                
                recognized_string = self.current_char
                self.get_next_char()
                while self.current_char is not None and not self.current_char.isspace():
                    if self.current_char == ";":
                        break
                    self.get_next_char()
                    if (self.current_char.isdigit()):
                        recognized_string += self.current_char
                    else:
                        raise SyntaxError(f"Expected integer, found something else. If you're trying to set an ID, it must begin with a letter")
                    self.get_next_char()
                family = "Integer"
                line_number = self.current_line
                return Token(recognized_string, family, line_number)

            if self.current_char.isalpha():
                self.recognized_string = self.current_char
                self.get_next_char()

                while not self.current_char.isspace():
                    if (self.current_char.isalpha() or self.current_char.isdigit() or self.current_char == "_"):
                      
                        self.recognized_string += self.current_char
                        self.current_char = self.get_next_char()
                    else:
                        break

                if self.recognized_string in tokens["Keywords"]:
                    
                    l.debug("...Found Family Keywords in ." + self.recognized_string + ".")
                    family = "Keywords"

                else:
                    
                    l.debug("...Found Family ID in ." + self.recognized_string + ".")
                    family = "ID"

                line_number = self.current_line
                return Token(self.recognized_string, family, line_number)

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
                l.debug("...Found #")
                recognized_string = self.current_char
                self.get_next_char()
                if (self.current_char == "{" or self.current_char == "}"):
                    recognized_string += self.current_char
                    l.debug("...Found a GroupSymbol in: "+ recognized_string)
                    family = "GroupSymbols"
                    line_number = self.current_line
                    self.get_next_char()
                    return Token(recognized_string, family, line_number)

                elif (self.current_char == "$"):
                    l.debug("...Found start of comment")
                    comment = ""
                    while self.current_char is not None:
                        self.get_next_char()
                        comment += self.current_char
                        if self.current_char == "#":
                            self.get_next_char()
                            if self.current_char == "$":
                                l.debug("...Found end of comment, the comment was: " + comment)
                                self.get_next_char()
                                break
                            else:
                                continue

                elif (self.current_char.isalpha()):
                    recognized_string = self.current_char
                    for i in range(6):
                        self.get_next_char()
                        recognized_string += self.current_char
                    if (recognized_string == "declare"):
                        l.debug("...Found declaration with current string ." + recognized_string + ".")
                        family = "Declaration"
                        line_number = self.current_line
                        self.get_next_char()
                        return Token(recognized_string, family, line_number)
                    else: 
                        raise SyntaxError("Unfinished declaration")


            if self.current_char.isspace():
                l.debug("\n")
                self.get_next_char()
                self.recognized_string = " "
                continue

class Parser:
    def __init__(self, filename):
        self.filename = filename
        self.lex = Lex(filename)
        self.current_token = None
        self.quad = Quad(quadnum, "_","_","_","_")
        self.get_next_token()

    def parse(self):
        self.start_rule()
        
    def get_next_token(self):
       self.current_token = self.lex.get_next_token()

    def start_rule(self):
        l.debug("...Went in on Start Rule with current token " + self.current_token.recognized_string)
        self.def_main_part()
        self.call_main_part()
        
    def def_main_part(self):
        l.debug("...Went in on def_main_part with current token " + self.current_token.recognized_string)
        while self.current_token.recognized_string == "def":
            self.def_main_function()

    def def_main_function(self):
        l.debug("...Went in on def_main_function with current token " + self.current_token.recognized_string)
        if (self.current_token.recognized_string == "def"):
            self.get_next_token()
            l.debug("...Matching ID with current token " + self.current_token.recognized_string)

            if (self.current_token.family == "ID"):
                id_token = self.current_token.recognized_string
                self.quad.genquad("begin_block", id_token, "_", "_")
                self.get_next_token()

                l.debug("...Matching GroupSymbols with current token " + self.current_token.recognized_string)
                if (self.current_token.recognized_string == "("):
                    self.get_next_token()

                    l.debug("...Matching GroupSymbols with current token " + self.current_token.recognized_string)
                    if (self.current_token.recognized_string == ")"):
                        self.get_next_token()

                        l.debug("...Matching Delimiters with current token " + self.current_token.recognized_string)
                        if (self.current_token.recognized_string == ":"):
                            self.get_next_token()

                            l.debug("...Found start of block with current token " + self.current_token.recognized_string)
                            if (self.current_token.recognized_string == "#{"):
                                self.get_next_token()
                                self.declarations()
                                while self.current_token is not None and self.current_token.recognized_string == "def":
                                    l.debug("...Found new function with current token  " + self.current_token.recognized_string)
                                    self.def_function()
                                self.statements()
                                l.debug("...Found end of block with current token " + self.current_token.recognized_string)
                                if (self.current_token.recognized_string == "#}"):
                                    self.quad.genquad("end_block",id_token,"_","_")
                                    self.get_next_token()
                                else:
                                    raise SyntaxError(f"Expected end of declaration but found " + self.current_token.family + "in line " + self.current_token.current_line)
                            else:
                                raise SyntaxError(f"Expected start of declaration but found " + self.current_token.family + "in line " + self.current_token.current_line)
                        else:
                            raise SyntaxError(f"Expected : but found " + self.current_token.family + "in line " + self.current_token.current_line)
                    else:
                        raise SyntaxError(f"Expected ) but found " + self.current_token.family + "in line " + self.current_token.current_line)     
                else:
                    raise SyntaxError(f"Expected ( but found " + self.current_token.family + "in line " + self.current_token.current_line)   
            else:
                raise SyntaxError(f"Expected ID but found " + self.current_token.family + "in line " + self.current_token.current_line)  
        else:
            raise SyntaxError(f"Expected def but found " + self.current_token.family + "in line " + self.current_token.current_line)


    def def_function(self):
        l.debug("...Matching Keywords")
        if (self.current_token.recognized_string == "def"):
            self.get_next_token()

            l.debug("...Matching ID")
            if (self.current_token.family == "ID"):
                id_token = self.current_token.recognized_string
                self.quad.genquad("begin_block",id_token,"_","_")
                self.get_next_token()

                l.debug("...Matching GroupSymbols")
                if (self.current_token.recognized_string == "("):
                    self.get_next_token()

                    self.id_list()

                    l.debug("...Matching GroupSymbols")
                    if (self.current_token.recognized_string == ")"):
                        self.get_next_token()

                        l.debug("...Matching Delimiters")
                        if (self.current_token.recognized_string == ":"):
                            self.get_next_token()

                            l.debug("...Matching GroupSymbols")
                            if (self.current_token.recognized_string == "#{"):
                                self.current_token = self.get_next_token()
                                self.declarations()
                                while self.current_token is not None and self.current_token.recognized_string == "def":
                                    self.def_function()
                                self.statements()
                                if (self.current_token.recognized_string == "#}"):
                                    self.quad.genquad("end_block",id_token,"_","_")
                                    self.get_next_token()

                                else:
                                    raise SyntaxError(f"Expected" + "#} but found " +self.current_token.family + "in line" + self.current_token.current_line)
                            else:
                                raise SyntaxError(f"Expected" + "#{ but found " +self.current_token.family+ "in line" + self.current_token.current_line)
                        else:
                            raise SyntaxError(f"Expected :, but found " +self.current_token.family+ "in line" + self.current_token.current_line)
                    else:
                        raise SyntaxError(f"Expected ), but found " +self.current_token.family+ "in line" + self.current_token.current_line)     
                else:
                    raise SyntaxError(f"Expected ( but found " +self.current_token.family+ "in line" + self.current_token.current_line)   
            else:
                raise SyntaxError(f"Expected ID, but found " + self.current_token.family+ "in line" + self.current_token.current_line)   
        else:
            raise SyntaxError(f"Expected def statement, but found " +self.current_token.family+ "in line" + self.current_token.current_line)       

    def declarations(self):
        l.debug("...Went in on declarations")
        while self.current_token is not None and self.current_token.family == "Declaration":
            self.declaration_line()

    def declaration_line(self):
        l.debug("...Parsing through the declaration line")
        if (self.current_token.family == "Declaration"):
            self.get_next_token()
            self.id_list()
        else: 
            raise SyntaxError(f"Expected Declaration, but found " +self.current_token.family)

    def statements(self):
        l.debug("...Went in on statements")
        self.statement()
        while self.current_token is not None and (self.current_token.family == "ID" or self.current_token.family == "Keywords"):
            self.statement()
    
    def statement(self):
        l.debug("...Trying to understand if its a simple or structured statement")
        if self.current_token.recognized_string in ["print", "return"] or self.current_token.family == "ID":
            self.simple_statement()
        elif self.current_token.recognized_string in ["while", "if"]:
            self.structured_statement()
        else:
            raise SyntaxError("Unknown keyword or improper statement in line "+ self.current_line)

    def simple_statement(self):
        l.debug("...Simple Statement found")
        if self.current_token.family == "ID":
            l.debug("...Found ID with current token " + self.current_token.recognized_string)
            self.assignment_stat()
        elif self.current_token.recognized_string == "print":
            l.debug("...Found print function with current token " + self.current_token.recognized_string)
            self.print_stat()
        elif self.current_token.recognized_string == "return":
            l.debug("...Found return function with current token " + self.current_token.recognized_string)
            self.return_stat()

    def structured_statement(self):
        l.debug("...Structured Statement found")
        if self.current_token.recognized_string == "while":
            l.debug("...Found while function with current token " + self.current_token.recognized_string)
            self.while_stat()
        elif self.current_token.recognized_string == "if":
            l.debug("...Found if function with current token " + self.current_token.recognized_string)
            self.if_stat()

    def assignment_stat(self):
        l.debug("...Assiginment function detected, matching ID with current token "+self.current_token.recognized_string)
        if self.current_token.family == "ID":
            self.get_next_token()
        
            l.debug("...Matching Assignment with current token "+self.current_token.recognized_string)
            if self.current_token.family == "Assignment":
                self.get_next_token()
            
                if self.current_token.family == "Keywords":
                    raise SyntaxError("Cannot assign a keyword as a value")
                else:
                    if self.current_token.recognized_string == "int":
                        self.get_next_token()
                        if self.current_token.recognized_string == "(":
                            self.get_next_token()
                            if self.current_token.recognized_string == "input":
                                self.get_next_token()
                                if self.current_token.recognized_string == "(":
                                    self.get_next_token()
                                    if self.current_token.recognized_string == ")":
                                        self.get_next_token()
                                        if self.current_token.recognized_string == ")":
                                            self.get_next_token()
                                            if self.current_token.recognized_string == ";":
                                                self.quad.genquad("in","input","_","_");
                                                self.get_next_token()
                                            else:
                                                raise SyntaxError(f"Missing ; in line {self.current_token.current_line}")
                                        else:
                                            raise SyntaxError(f"Expected ) but found {self.current_token.family} in line {self.current_token.current_line}")
                                    else:
                                        raise SyntaxError(f"Expected ) but found {self.current_token.family} in line {self.current_token.current_line}")
                                else:
                                    raise SyntaxError(f"Expected ( but found {self.current_token.family} in line {self.current_token.current_line}")
                            else:
                                raise SyntaxError(f"Expected input but found {self.current_token.family} in line {self.current_token.current_line}")
                        else:
                            raise SyntaxError(f"Expected ( but found {self.current_token.family} in line {self.current_token.current_line}")
                    else:
                        self.get_next_token()
                        if self.current_token.recognized_string == ";":
                            self.get_next_token()
                        else:
                            self.expression()
                        




    def return_stat(self):
        if self.current_token.recognized_string == "return":
            self.get_next_token()
            if self.current_token.recognized_string == "(":
                self.get_next_token()
                self.expression()
                if self.current_token.recognized_string == ")":
                    self.get_next_token()
                    if self.current_token.recognized_string == ";":
                        self.get_next_token()
                    else:
                        raise SyntaxError(f"Missing ; in line" + self.current_token.current_line)
                else:
                    raise SyntaxError(f"Expected ) but found " + self.current_token.family + "in line" + self.current_token.current_line)
            else:
                raise SyntaxError(f"Expected ( but found " + self.current_token.family + "in line" + self.current_token.current_line)
        else:
            raise SyntaxError(f"Expected return statement but found " + self.current_token.family + "in line" + self.current_token.current_line)

    def print_stat(self):
        if self.current_token.recognized_string == "print":
            self.get_next_token()
            if self.current_token.recognized_string == "(":
                self.get_next_token()
                self.expression()
                if self.current_token.recognized_string == ")":
                    self.get_next_token()
                    if self.current_token.recognized_string == ";":
                        self.quad.genquad("out","_","_","_")
                        self.get_next_token()
                    else:
                        raise SyntaxError(f"Missing ; in line" + self.current_token.current_line)
                else:
                    raise SyntaxError(f"Expected ) but found " + self.current_token.family + "in line" + self.current_token.current_line)
            else:
                raise SyntaxError(f"Expected ( but found " + self.current_token.family + "in line" + self.current_token.current_line)
        else:
            raise SyntaxError(f"Expected print statement but found " + self.current_token.family + "in line" + self.current_token.current_line)

    def if_stat(self):
        B = []
        statements_bool = False
        if (self.current_token.recognized_string == "if"):
            self.get_next_token()
            if (self.current_token.recognized_string == "("):
                self.get_next_token()
                B = self.condition()
                if (self.current_token.recognized_string == ")"):
                    BTrue = B[0]
                    BFalse = B[1]
                    self.quad.backpatch(BTrue,self.quad.nextquad())
                    self.get_next_token()
                    if (self.current_token.recognized_string == ":"):
                        self.get_next_token()
                        if (self.current_token.recognized_string == "#{"):
                            statements_bool = True
                            self.get_next_token()
                            self.statements()
                            ifList = self.quad.makeList(self.quad.nextQuad())
                            self.quad.genQuad('jump','_','_','_')
                            self.quad.backpatch(BFalse,self.quad.nextquad())
                            if (self.current_token.recognized_string == "#}"):
                                if (statements_bool == True):
                                    statements_bool = False
                                    self.get_next_token()
                                else:
                                    raise SyntaxError(f"Incomplete statement block" + "in line" + self.current_token.current_line)
                            else:
                                raise SyntaxError(f"Expected" + "#} but found " +self.current_token.family + "in line" + self.current_token.current_line)
                        else:
                            self.statement()
                    else:
                        raise SyntaxError(f"Expected :, but found " +self.current_token.family+ "in line" + self.current_token.current_line)
                else:
                    raise SyntaxError(f"Expected ), but found " +self.current_token.family+ "in line" + self.current_token.current_line)     
            else:
                raise SyntaxError(f"Expected ( but found " +self.current_token.family+ "in line" + self.current_token.current_line)   

        if (self.current_token.recognized_string == "else"):
            self.quad.backpatch(BFalse,self.quad.nextquad())
            self.quad.backpatch(ifList,self.quad.nextquad())
            self.get_next_token()
            if (self.current_token.recognized_string == ":"):
                self.get_next_token()
                if (self.current_token.recognized_string == "#{"):
                    statements_bool = True
                    self.get_next_token()
                    self.statements()
                    if (self.current_token.recognized_string == "#}"):
                        if (statements_bool == True):
                            statements_bool = False
                            self.get_next_token()
                        else:
                            raise SyntaxError(f"Incomplete statement block" + "in line" + self.current_token.current_line)
                    else:
                        raise SyntaxError(f"Expected" + "#} but found " +self.current_token.family + "in line" + self.current_token.current_line)
                else:
                    self.statement()
            else:
                raise SyntaxError(f"Expected :, but found " +self.current_token.family+ "in line" + self.current_token.current_line)

    def call_main_part(self):
        
        if self.current_token.recognized_string == "if":
            self.get_next_token()
            if self.current_token.recognized_string == "__name__":
                self.get_next_token()
                if self.current_token.recognized_string == "==":
                    self.get_next_token()
                    if self.current_token.family == "Main":
                        self.get_next_token()
                        if self.current_token.recognized_string == ":":
                            self.get_next_token()
                            while self.current_token.family == "ID":
                                self.main_function_call()
                        else:
                            raise SyntaxError("Expected ':' but found something else.")

    def main_function_call(self):
        l.debug("...Matching ID")
        if (self.current_token.family == "ID"):
            self.get_next_token()
            l.debug("...Matching GroupSymbols")
            if (self.current_token.recognized_string == "("):
                self.get_next_token()
                l.debug("...Matching GroupSymbols")
                if (self.current_token.recognized_string == ")"):
                    self.get_next_token()

                    l.debug("...Matching Delimiters")
                    if (self.current_token.recognized_string == ":"):
                        self.get_next_token()
                    else:
                       raise SyntaxError(f"Expected :, but found " +self.current_token.family+ "in line" + self.current_token.current_line)
                else:
                    raise SyntaxError(f"Expected ), but found " +self.current_token.family+ "in line" + self.current_token.current_line)     
            else:
                raise SyntaxError(f"Expected ( but found " +self.current_token.family+ "in line" + self.current_token.current_line)   
        else:
            raise SyntaxError(f"Expected ID, but found " + self.current_token.family+ "in line" + self.current_token.current_line) 

    def while_stat(self):
        l.debug("...Went in on while_stat with current token " + self.current_token.recognized_string)
        statements_bool = False
        if (self.current_token.recognized_string == "while"):
            condQuad = self.quad.nextQuad()
            self.get_next_token()
            if (self.current_token.recognized_string == "("):
                self.get_next_token()
                B = self.condition()
                BTrue = B[0]
                BFalse = B[1]
                self.get_next_token()
                if (self.current_token.recognized_string == ")"):
                    self.quad.backpatch(BTrue,self.quad.nextQuad())
                    self.get_next_token()
                    if (self.current_token.recognized_string == ":"):
                        self.get_next_token()
                        if (self.current_token.recognized_string == "#{"):
                            statements_bool = True
                            self.get_next_token()
                            self.statements()
                            self.quad.genquad('jump','_','_',condQuad)
                            backpatch(condition.false,nextQuad())
                            if (self.current_token.recognized_string == "#}"):
                                if (statements_bool == True):
                                    statements_bool = False
                                    self.get_next_token()
                                else:
                                    raise SyntaxError(f"Incomplete statement block" + "in line" + self.current_token.current_line)
                            else:
                                raise SyntaxError(f"Expected" + "#} but found " +self.current_token.family + "in line" + self.current_token.current_line)
                        else:
                            self.statements()
                    else:
                        raise SyntaxError(f"Expected :, but found " +self.current_token.family+ "in line" + self.current_token.current_line)
                else:
                    raise SyntaxError(f"Expected ), but found " +self.current_token.family+ "in line" + self.current_token.current_line)     
            else:
                raise SyntaxError(f"Expected ( but found " +self.current_token.family+ "in line" + self.current_token.current_line)   

    def id_list(self):
        l.debug("...Went in on id_list")
        id_list = []
        l.debug("...Matching ID")
        if(self.current_token.family == "ID"):
            id_list.append(self.current_token.recognized_string)
            self.get_next_token()
            while self.current_token is not None and self.current_token.recognized_string == ",":
                self.get_next_token()
                if (self.current_token.family == "ID"):
                    self.get_next_token()
                else:
                    raise SyntaxError("Expected ID after comma.")


    def expression(self):
        l.debug("...Went in on expression with current token " + self.current_token.recognized_string)
        self.optional_sign()
        t1place = self.term()
        l.debug("...Found term " + t1place)
        while self.current_token is not None and self.current_token.family == "AddOperators":
            l.debug("...Found AddOp " + self.current_token.recognized_string)
            w = self.quad.newTemp()
            op = self.current_token.recognized_string
            self.get_next_token()
            t2place = self.current_token.recognized_string
            l.debug("...Found term " + t2place)
            self.quad.genquad(op,t1place,t2place,w)
            t1place = w
            self.term()
            eplace = t1place
        l.debug("...Returning expression " + t1place)
        return t1place

    def term(self):
        l.debug("...Went in on term with current token " + self.current_token.recognized_string)
        self.factor()
        t1place = self.current_token.recognized_string
        while self.current_token is not None and self.current_token.family == "MulOperators":
            w = self.quad.newTemp()
            op = self.current_token.recognized_string
            self.get_next_token()
            t2place = self.current_token.recognized_string
            self.quad.genquad(op,t1place,t2place,w)
            t1place = w
            self.factor()
            self.get_next_token()
        l.debug("...Returning term " + t1place)
        return t1place
    
    def factor(self):
        l.debug("...Went in on factor with current token " + self.current_token.recognized_string)
        if self.current_token.family == "Integer":
            self.get_next_token()

        elif self.current_token.recognized_string == "(":
            self.get_next_token()
            self.expression()
            if self.current_token.recognized_string == ")":
                self.get_next_token()
                if self.current_token.recognized_string == ";":
                    self.get_next_token()
                else:
                    raise SyntaxError(f"Expected ';', found " + self.current_token.recognized_string)
            else:
                raise SyntaxError("Expected ')' but found something else.")
        elif self.current_token.family == "ID":
            self.idtail()

    def idtail(self):
        l.debug("...Went in on idtail with current token " + self.current_token.recognized_string)
        if self.current_token.recognized_string == "(":
            self.get_next_token()
            self.actual_par_list()
            if self.current_token.recognized_string == ")":
                self.get_next_token()
            else:
                raise SyntaxError("Expected ')' but found something else.")
        else:
            pass

    def actual_par_list(self):
        l.debug("...Went in on actual_par_list with current token " + self.current_token.recognized_string)
        self.expression()
        if self.current_token.recognized_string == "(":
            self.expression()
            while self.current_token.recognized_string == ",":
                self.get_next_token()
                self.expression()
        else:
            pass

    def optional_sign(self):
        l.debug("...Went in on optional_sign with current token " + self.current_token.recognized_string)
        if self.current_token.family == "AddOperators":
            l.debug("...Found this AddOperator: " + self.current_token.recognized_string)
            self.get_next_token()
        else:
            l.debug("...No sign found, returning")
            pass

   
    def condition(self):
        B = []
        l.debug("...Went in on condition with current token " + self.current_token.recognized_string)
        B = self.bool_term()
        while self.current_token.recognized_string == "or":
            Btrue = B[0]
            Bfalse = B[1]
            self.quad.backpatch(Bfalse,self.quad.nextQuad())
            self.get_next_token()
            l.debug("...Found another contidion, calling bool_term again with current token " + self.current_token.recognized_string)
            B = self.bool_term()
            Q2True = B[0]
            Q2False = B[1]
            Bfalse = self.quad.mergeList(Bfalse,Q2false)
            Btrue = Q2true

            B = []
            B.append(BTrue)
            B.append(BFalse)

        return B

    def bool_term(self):
        B = []
        l.debug("...Went in on bool_term with current token " + self.current_token.recognized_string)
        B = self.bool_factor()
        while self.current_token.recognized_string == "and":
            Btrue = B[0]
            Bfalse = B[1]
            self.quad.backpatch(Btrue,self.quad.nextQuad())
            self.get_next_token()
            l.debug("...Found another bool term, calling bool_factor again with current token " + self.current_token.recognized_string)
            B = self.bool_factor()
            Q2True = B[0]
            Q2False = B[1]
            Bfalse = self.quad.mergeList(Bfalse,Q2false)
            Btrue = Q2true

            B = []
            B.append(BTrue)
            B.append(BFalse)

        return B

    def bool_factor(self):

        B = []
        l.debug("...Went in on bool_factor with current token " + self.current_token.recognized_string)
        if self.current_token.recognized_string == "not":
            self.get_next_token()
            if self.current_token.recognized_string == "(":
                self.get_next_token()
                B = self.condition()
                if self.current_token.recognized_string == ")":
                    Btrue = B[1]
                    Bfalse = B[0]
                    self.get_next_token()

                    B = []
                    B.append(BTrue)
                    B.append(BFalse)
                    return B
                else:
                    raise SyntaxError("Expected ')' but found something else.")
            else:
                raise SyntaxError("Expected '(' but found something else.")
        elif self.current_token.recognized_string == "[":
            self.get_next_token()
            B = self.condition()
            if self.current_token.recognized_string == "]":
                Btrue = B[0]
                Bfalse = B[1]
                self.get_next_token()
                B = []
                B.append(BTrue)
                B.append(BFalse)
                return B
            else:
                raise SyntaxError("Expected ']' but found something else.")
        
        else:
            E1place = self.expression()
            self.get_next_token()
            if self.current_token.family == "RelOperators":
                B = []
                rel_op = self.current_token.recognized_string
                l.debug("...Found a RelOperator: " + self.current_token.recognized_string + " , getting next token and finding next expression")
                self.get_next_token()
                E2place = self.expression()
                BTrue = self.quad.makeList(self.quad.nextQuad())
                self.quad.genquad(rel_op,E1place,E2place,"_")
                BFalse = self.quad.makeList(self.quad.nextQuad())
                self.quad.genquad("jump","_","_","_")
                B.append(BTrue)
                B.append(BFalse)
                return B
                


class Quad:
    def __init__(self, operator, operand1, operand2, operand3, quad_num):
        self.operator = operator
        self.operand1 = operand1
        self.operand2 = operand2
        self.operand3 = operand3
        self.quad_num = quad_num


    def nextQuad(self):
        global quadnum
        quadnum += 1
        l.debug("...nextQuad called. The next generated quad will have no. " + str(quadnum))
        return quadnum - 1

    def genquad(self,operator, operand1, operand2, operand3):
        qnum = self.nextQuad()
        l.debug("Generating quad " + str(qnum) + ": " + operator + ", " + operand1 + ", " + operand2 + ", " + operand3)
        q = Quad(quadnum, operator, operand1, operand2, operand3)
        quadList.append(q)

    def newTemp(self):
        global temp_counter
        temp = "%" + str(temp_counter)
        temp_counter += 1
        l.debug("...Creating new temp " + temp)
        return temp

    def emptyList(self):
        l = list()
        return l

    def makeList(self,label):
        l = list(str(label))
        return l

    def mergeList(list1, list2):
        if list1 is None: 
            return list2
        if list2 is None:
            return list1
        merged_list = list1 + list2
        return merged_list

    def backpatch(self,list,label):
        for q in list:
            if q.op[3] == "_":
                q.op[3] = str(label)

class Variable: 
    def __init__(self, name, datatype, offset):
        self.name = name
        self.datatype = datatype
        self.offset = offset

class Parameter: 
    def __init__(self, name, datatype, mode, offset):
        self.name = name
        self.datatype = datatype
        self.mode = mode
        self.offset = offset

class FormalParameter: 
    def __init__(self, datatype, mode):
        self.datatype = datatype
        self.mode = mode

class Procedure:
        def __init__(self, name, startingQuad, framelength, formalParameters):
            self.name = name
            self.startingQuad = startingQuad
            self.framelength = framelength
            self.formalParameters = formalParameters

class Function:
        def __init__(self, name, datatype, startingQuad, framelength, formalParameters):
            self.name = name
            self.datatype = datatype
            self.startingQuad = startingQuad
            self.framelength = framelength
            self.formalParameters = formalParameters

class TemporaryVariable: 
    def __init__(self, name, datatype, offset):
        self.name = name
        self.datatype = datatype
        self.offset = offset

class SymbolicConstant: 
    def __init__(self, name, offset):
        self.name = name
        self.offset = offset

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <filename>")
        return
    
    l.basicConfig(level=l.DEBUG)
    filename = sys.argv[1]

    parser = Parser(filename)
    
    
    result = parser.parse()
    
    if result:
        print("Compilation successful!")
    else:
        print("Compilation failed.")

if __name__ == '__main__':
    main()
