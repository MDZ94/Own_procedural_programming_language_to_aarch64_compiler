from ast import type_ignore
import ply.lex as lex
import ply.yacc as yacc
import sys

class MyLexer():

    # CONSTRUCTOR
    def __init__(self):
        print('Lexer constructor called.')
        self.lexer = lex.lex(module=self)
 
    # DESTRUCTOR
    def __del__(self):
        print('Lexer destructor called.')

    tokens = [
        'INT',
        'NAME',
        'PLUS',
        'MINUS',
        'DIVIDE',
        'MULTIPLY',
        'EQUALS',
        'WHILE',
        'LEFT_BRACKET',
        'RIGHT_BRACKET',
        'LEFT_CURLY_BRACKET',
        'RIGHT_CURLY_BRACKET',
        'MORE',
        'LESS',
        'MORE_OR_EQUAL',
        'LESS_OR_EQUAL',
        'IS_EQUAL',
        'SEMICOLON',
        'IF',
        'IF_ELSE',
        'ELSE',
        'MAIN',
        # 'NEW_LINE',
        'RETURN',
        'COMA',
        'VOID',
        'INT_FUN',
        'PRINT',
        'STRING',
        'APOSTROF'
        # 'STRING_NAME'
    ]

    t_PLUS = r'\+'
    t_MINUS = r'\-'
    t_MULTIPLY = r'\*'
    t_DIVIDE = r'\/'
    t_EQUALS = r'\='
    t_LEFT_BRACKET = r'\('
    t_RIGHT_BRACKET = r'\)'
    t_LEFT_CURLY_BRACKET = r'\{'
    t_RIGHT_CURLY_BRACKET = r'\}'
    t_MORE = r'>'
    t_LESS = r'<'
    t_APOSTROF = r'\"'
    t_SEMICOLON = r'\;'
    t_COMA = r'\,'
    t_ignore =r' '

    reserved = {
        'if' : 'IF',
        'main' : 'MAIN',
        'else' : 'ELSE',
        'while' : 'WHILE',
        'ifelse' : 'IF_ELSE',
        'return' : 'RETURN',
        'void' : 'VOID',
        'int' : 'INT_FUN',
        'return' : 'RETURN',
        'print' : 'PRINT',
        'string' : 'STRING'
    }

    def t_NEW_LINE(self,t):
        r'(\n)'
        # t.lexer.skip(1)

    def t_INT(self,t):
        r'-*\d+'
        t.value = int(t.value)
        return t

    def t_ID(self,t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        if t.value in self.reserved:
            t.type = self.reserved.get(t.value,'ID')    # Check for reserved words
            return t
        else:
            t.type = 'NAME'
            return t


    def t_MORE_OR_EQUAL(self,t):
        r'\>='
        t.type = 'MORE_OR_EQUAL'
        return t

    def t_LESS_OR_EQUAL(self,t):
        r'\<='
        t.type = 'LESS_OR_EQUAL'
        return t
        
    def t_IS_EQUAL(self,t):
        r'\=='
        t.type = 'IS_EQUAL'
        return t

    def t_NAME(self,t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = 'NAME'
        return t
    
        

    def t_error(self,t):
        print("Illegal input")
        t.lexer.skip(1)