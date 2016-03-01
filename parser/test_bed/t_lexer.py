import  ply.lex as lex
import ply.yacc as yacc
import filecmp
import sys
#infile = sys.argv[1]


# List of token names.   This is always required
keywords = {'PROGRAM' : 'PROGRAM',
			'BEGIN' : 'BEGIN',
			'END' : 'END',
			'WHILE' : 'WHILE',
			'FUNCTION' : 'FUNCTION',
			'READ' : 'READ',
			'WRITE' : 'WRITE',
			'IF' : 'IF',
			'ELSE' : 'ELSE',
			'ENDIF' : 'ENDIF',
			'ENDWHILE' : 'ENDWHILE',
			'CONTINUE' : 'CONTINUE',
			'BREAK' : 'BREAK',
			'RETURN' : 'RETURN',
			'INT' : 'INT',
			'VOID' : 'VOID',
			'STRING' : 'STRING',
			'FLOAT' : 'FLOAT'}

operators = ('EQ_EQ',
			'PLUS',
			'MINUS',
			'MULT',
			'DIV',
			'EQ',
			'N_EQ',
			'LESS',
			'MORE',
			'L_PAR',
			'R_PAR',
			'SEMI',
			'COMM',
			'L_EQ',
			'R_EQ')


tokens = tuple(keywords.values()) + operators +('IDENTIFIER',
          'INTLITERAL',
          'FLOATLITERAL',
          'STRINGLITERAL',
          'COMMENT',     
          'empty')
print (tokens)

          
#t_KEYWORD= (r"PROGRAM|BEGIN|END(?!WHILE|IF)|FUNCTION|READ|WRITE|IF|ELSE|ENDIF|WHILE|ENDWHILE|CONTINUE|BREAK|RETURN|INT|VOID|STRING|FLOAT")


"""
T_PROGRAM = (r"PROGRAM")
T_BEGIN = (r"BEGIN")
T_END = (r"END(?!WHILE|IF)")
T_WHILE = (r"WHILE")
T_FUNCTION = (r"FUNCTION")
T_READ = (r"READ")
T_WRITE = (r"WRITE")
T_IF = (r"IF")
T_ELSE = (r"ELSE")
T_ENDIF = (r"ENDIF")
T_ENDWHILE = (r"ENDWHILE")
T_CONTINUE = (r"CONTINUE")
T_BREAK = (r"BREAKs")
T_RETURN = (r"RETURN")
T_INT = (r"INT")
T_VOID = (r"VOID")
T_STRING = (r"STRING")
T_FLOAT = (r"FLOAT")
"""

t_EQ_EQ = (r":=")
t_PLUS = (r"\+")
t_MINUS = (r"-(?!-)")
t_MULT = (r"\*")
t_DIV = (r"/")
t_EQ = (r"=")
t_N_EQ = (r"!=")
t_LESS = (r"<(?!=)")
t_MORE = (r">(?!=)")
t_L_PAR = (r"\(")
t_R_PAR = (r"\)")
t_SEMI = (r";")
t_COMM = (r",")
t_L_EQ = (r"<=")
t_R_EQ = (r">=")

T_empty = (r"")

#t_IDENTIFIER =(r"[a-zA-Z]+[a-zA-Z0-9]*")
t_INTLITERAL = (r"[0-9]+")
t_FLOATLITERAL = (r"[0-9]*\.[0-9]+|\.[0-9]+")
t_STRINGLITERAL = (r"\"[^\"]*\"")
#t_OPERATOR = (r":=|\+|-(?!-)|\*|/|=|!=|<(?!=)|>(?!=)|\(|\)|;|,|<=|>=")
t_ignore_COMMENT = (r"--.*\n")
t_ignore  = (" \t | \n | ")

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in keywords:
        t.type = keywords[ t.value ]
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
