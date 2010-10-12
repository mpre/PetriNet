#! /usr/bin/python
# -*- coding: utf-8 -*-
import ply.lex as lex
import PetriNet

#lista delle parole riservate
reserved = {
    "PetriNet" : "PETRINET", 
    "Place" : "PLACE", 
    "Transition" : "TRANSITION",
    #            "to_dot" : "TO_DOT", 
    #            "is_occurrency" : "IS_OCCURRENCY", 
    #            "to_matrix" : "TO_MATRIX", 
    #            "createCaseGraph" : "GRAPH", 
    #            "CGtoDot" : "GRAPHDOT", 
    #            "WorkOn" : "WORKON", 
    "show_nets" : "SHOW_NETS",
    "show_places" : "SHOW_PLACES",
    "show_transitions" : "SHOW_TRANSITIONS",
    "show_links" : "SHOW_LINKS",
    "string" : "STRING",
    #"add" : "ADD",
    #"for" : "FOR", 
    #"to" :  "TO", 
    #"in": "IN", 
    "on":"ON", 
    #"union":"UNION", 
    "as" : "AS",
    "id_in_id" : "ID_IN_ID"
    #            "M0" : "M0"
            }
            
literals = ['=', ',', '.', '>', '|','#']
#tokens
tokens = [ 
          "ID", 
          "ARRAY_ID",
          "NUMBER", 
          "LPAREN", 
          "RPAREN", 
          "LBRACE", 
          "RBRACE", 
          "LSQBRACE", 
          "RSQBRACE", 
          "LINK" ,       
          "SEMI",
          "COMMENT",
          "DDOT",
          "OR",
    "IDDOT"
          #"FUNCTION_ID"
           ] + list(reserved.values())
          

#regole per i token
t_LINK = r'->'
t_SEMI = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LSQBRACE= r'\[' 
t_RSQBRACE = r'\]'
t_DDOT = r'::'
t_OR = r'\|'
#caratteri ignorati, spazi e tab
t_ignore = ' \t'

def t_ID_IN_ID(t):
    r'[a-zA-Z][_a-zA-Z0-9]*[\[[0-9][0-9]*\]]*.[a-zA-Z][_a-zA-Z0-9]*'
    return t

# Identificatore di array
def t_ARRAY_ID(t):
    r'[a-zA-Z][_a-zA-Z0-9]*\[[0-9][0-9]*\]'
    t.type = reserved.get(t.value, 'ARRAY_ID')
    i1 = t.value.index('[')
    i2 = t.value.index(']')
    t.value = [t.value[:i1],int(t.value[i1 + 1:i2])]
    return t

#definizione di un identificatore può essere il nome di una rete, posto o transizione o marcatura
def t_ID(t): 
    r'[a-zA-Z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,  'ID')
    #print "lexer:",  t
    return t

#regola per i numeri
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t
    
#a capo
def t_newline(t):
    r'\n+' 
    t.lexer.lineno += t.value.count('\n') 

def t_error(t): 
    print "petriNet: Illegal character '%s'" % t.value[0] 
    t.lexer.skip(1) 

# I commenti sono in c-style.
def t_COMMENT(t):
    r'(//.*)|(/\*(.|\n)*?\*/)'
    pass

# Stringhe
def t_STRING(t):
    r'\".*\"'
    return t

#costruzione del lexer
lexer=lex.lex() 
#data = '''//ciao
#Transition t //ciao
#//ciao
#Place /*nest-comment*/ x/*multi
#line
#comment*/
#Place z'''
#data = '//ciao'
#lexer.input(data)
#dati da dare in input al lexer
#data = ''' PetriNet g;
#Place posto;
#Transition trans;
#posto -> posto;
#
#'''
#lexer.input(data)
#
# Tokenize
#while True:
#    lexer.input(raw_input())
#    tok = lexer.token()
#    if not tok: 
#        break
#    print tok,' linea:', tok.lexer.lineno
# No more input
