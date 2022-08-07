from ast import type_ignore
import ply.lex as lex
import ply.yacc as yacc
import sys

from myLexer import *
from myParser import *
from myParser import MyParser

myLex = MyLexer()
lexer = myLex.lexer

myPars = MyParser()
parser = myPars.parser



new = ''

input_file = open(sys.argv[1], "r")
new = input_file.read()
myPars.file_prepare(sys.argv[2])

parsed_code = parser.parse(new)
print(parsed_code)
myPars.file_closing()

input_file.close()

