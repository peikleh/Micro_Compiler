import  lex
import filecmp
import sys
infile = sys.argv[1]



# List of token names.   This is always required
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
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()



with open(infile, 'r') as myfile:
    data = myfile.read()
#file = open('fibonacci.txt' , 'a')


lexer.input(data)
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    #file.write('Token Type: ' + tok.type + '\n')
    #file.write('Value: ' + tok.value + '\n')
    print ('Token Type: ' + tok.type)
    print ('Value: ' + tok.value)
  
#file.close()

#print (filecmp.cmp('fibonacci.txt', 'loop2.txt'))
#file.close()





