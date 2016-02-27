import yacc
import filecmp
import sys
#infile = sys.argv[1]
infile = "output.txt"

tokens = ('IDENTIFIER',
		  'INTLITERAL',
		  'FLOATLITERAL',
		  'STRINGLITERAL',
		  'COMMENT',     
		  'KEYWORD',
		  'OPERATOR')	  

t_KEYWORD= (r"PROGRAM|BEGIN|END(?!WHILE|IF)|FUNCTION|READ|WRITE|IF|ELSE|ENDIF|WHILE|ENDWHILE|CONTINUE|BREAK|RETURN|INT|VOID|STRING|FLOAT")
t_IDENTIFIER =(r"[a-zA-Z]+[a-zA-Z0-9]*")
t_INTLITERAL = (r"[0-9]+")
t_FLOATLITERAL = (r"[0-9]*\.[0-9]+|\.[0-9]+")
t_STRINGLITERAL = (r"\"[^\"]*\"")
t_OPERATOR = (r":=|\+|-(?!-)|\*|/|=|!=|<(?!=)|>(?!=)|\(|\)|;|,|<=|>=")
t_ignore_COMMENT = (r"--.*\n")
t_ignore  = (" \t\n")

__var_names = {}

def p_assign_statement(t) :
    'assign_statement : IDENTIFIER OPERATOR statement'
    __var_names[t[1]] = t[3]

"""def p_statement_plus(t) :
    'statement : statement ADDOP term'
    t[0] = t[1] + t[3]

def p_statement_minus(t) :
    'statement : statement SUBOP term'
    t[0] = t[1] - t[3]

def p_statement_term(t) :
    'statement : term'
    t[0] = t[1]

def p_term_times(t) :
    'term : term MULOP factor'
    t[0] = t[1] * t[3]

def p_term_div(t) :
    'term : term DIVOP factor'
    t[0] = t[1] / t[3]

def p_term_factor(t) :
    'term : factor'
    t[0] = t[1]

def p_factor_num(t) :
    'factor : NUM'
    t[0] = t[1]

def p_factor_var(t) :
    'factor : INLITERAL'
    if __var_names.has_key(t[1]) :
        t[0] = __var_names[t[1]]
    else :
        print "Undefined Variable", t[1], "in line no.", t.lineno(1)

def p_factor_expr(t):
    'factor : LPAREN statement RPAREN'
    t[0] = t[2]

# Error rule for syntax errors
def p_error(t):
    print "Syntax error in input!"
"""

parser = yacc.yacc()


with open(infile, 'r') as myfile:
	data = myfile.read()
	
	
parser.parse(data)

