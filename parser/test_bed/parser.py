
import ply.yacc as yacc
from t_lexer import tokens
print (tokens)

def p_program(p):
    'program : PROGRAM id BEGIN END RETURN'
   
def p_id(p):
	'id : IDENTIFIER'

#def p_error(p):
 #   print("Syntax error in input!")


	
parser = yacc.yacc()

while True:
   try:
       s = "PROGRAM hello BEGIN END RETURN"
       print (s)
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)
   break
