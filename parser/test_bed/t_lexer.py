import  ply.lex as lex
import ply.yacc as yacc
import filecmp
import sys
#infile = sys.argv[1]



# List of token names.   This is always required
keywords = ('PROGRAM',
			'BEGIN',
			'END',
			'WHILE',
			'FUNCTION',
			'READ',
			'WRITE',
			'IF',
			'ELSE',
			'ENDIF',
			'ENDWHILE',
			'CONTINUE',
			'BREAK',
			'RETURN',
			'INT',
			'VOID',
			'STRING',
			'FLOAT')

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

tokens = keywords + operators +('IDENTIFIER',
          'INTLITERAL',
          'FLOATLITERAL',
          'STRINGLITERAL',
          'COMMENT',     
          'OPERATOR',
          'empty')

          
#t_KEYWORD= (r"PROGRAM|BEGIN|END(?!WHILE|IF)|FUNCTION|READ|WRITE|IF|ELSE|ENDIF|WHILE|ENDWHILE|CONTINUE|BREAK|RETURN|INT|VOID|STRING|FLOAT")



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

T_EQ_EQ = (r":=")
T_PLUS = (r"\+")
T_MINUS = (r"-(?!-)")
T_MULT = (r"\*")
T_DIV = (r"/")
T_EQ = (r"=")
T_N_EQ = (r"!=")
T_LESS = (r"<(?!=)")
T_MORE = (r">(?!=)")
T_L_PAR = (r"\(")
T_R_PAR = (r"\)")
T_SEMI = (r";")
T_COMM = (r",")
T_L_EQ = (r"<=")
T_R_EQ = (r">=")

T_empty = (r"")

t_IDENTIFIER =(r"[a-zA-Z]+[a-zA-Z0-9]*")
t_INTLITERAL = (r"[0-9]+")
t_FLOATLITERAL = (r"[0-9]*\.[0-9]+|\.[0-9]+")
t_STRINGLITERAL = (r"\"[^\"]*\"")
#t_OPERATOR = (r":=|\+|-(?!-)|\*|/|=|!=|<(?!=)|>(?!=)|\(|\)|;|,|<=|>=")
t_ignore_COMMENT = (r"--.*\n")
t_ignore  = (" \t | \n | ")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()