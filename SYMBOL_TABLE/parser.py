
import ply.yacc as yacc
from lexer import tokens
import lexer
import sys

class SymbolTable():
    def __init__(self):
        self._stack = []
        glob = {}
        self._stack.append(glob)
        self._type = 'none'
        self._val_list = []
        self._glob = True
        self._val_hold = []
    def add_string(self, name, val):
        self._val_hold.append((name, 'STRING', val))
        #self._stack[-1][name] = ('String', val)

    def add_type(self, d_type):
        self._type = d_type

    def add_val(self, val):
        self._val_list.append(val)

    def add_decl(self):
        for val in reversed(self._val_list):
            if val != None:
                self.add_to_cur_scope(val, self._type)
        
        self._type = 'none'
        self._val_list = []
        
    def add_to_cur_scope(self, name, d_type):
        in_scope = False
        for scope in self._stack:
            if name in scope.keys():
                in_scope = True
                print("Variable already declared" + name)
        if in_scope == False:
            #self._stack[-1][name] = (d_type)
            self._val_hold.append((name, d_type))
            #print ("name " + name +  ' type ' + d_type)

    def add_scope(self, name):
        self._stack.append({})
        print ('\n' + name)
        print (self._val_hold)
        self._val_hold = []
        #print ("Symbol table " + name)

    def add_glob(self, name):
        print ('\n' + name)
        print (self._val_hold)
        
        self._val_hold = []
        
    def first_funct(self):
        if self._glob == True:
            self._glob = False
            self.add_glob('Global')
    


    

infile = 'Step3/inputs/test20.micro'
with open(infile, 'r') as myfile:
    data = myfile.read()

accepted = True
table = SymbolTable()
#print ('Symbol table Global')
#Following functions are the grammar for the LITTLE language
def p_program(p):
    'program : PROGRAM IDENTIFIER BEGIN pgm_body END'
        
"""def p_id(p):
    'id : IDENTIFIER'
    table.add_var(p[1])
    #print 'id     ' + p[1]
    print lexer.t_ID(p[1])"""

def p_pgm_body(p):
    'pgm_body : decl func_declarations'

def p_decl(p):
    '''decl : string_decl decl 
    | var_decl decl 
    | empty'''

def p_string_decl(p):
    'string_decl : STRING IDENTIFIER EQ_EQ STRINGLITERAL SEMI'
 
    table.add_string(p[2], p[4])

def p_var_decl(p):
    'var_decl : var_type id_list SEMI'
    table.add_decl()
 
    
def p_var_type(p):
    '''var_type : FLOAT 
    | INT'''
    table.add_type(p[1])

def p_any_type(p):
    '''any_type : var_type 
    | VOID'''

def p_id_list(p):
    'id_list : IDENTIFIER id_tail'
    table.add_val(p[1])
    
def p_id_tail(p):
    '''id_tail : COMM IDENTIFIER id_tail 
    | empty'''
    if len(p) >= 3:
            table.add_val(p[2])
def p_param_decl_list(p):
    '''param_decl_list : param_decl param_decl_tail 
    | empty'''
    table.first_funct()
def p_param_decl(p):
    'param_decl : var_type IDENTIFIER'
    
def p_param_decl_tail(p):
    '''param_decl_tail : COMM param_decl param_decl_tail 
    | empty'''

def p_func_declarations(p):
    '''func_declarations : func_decl func_declarations 
    | empty'''

def p_func_decl(p):
    'func_decl : FUNCTION any_type IDENTIFIER L_PAR param_decl_list R_PAR BEGIN func_body END'
    table.add_scope(p[3])
    
def p_func_body(p):
    'func_body : decl stmt_list'

def p_stmt_list(p):
    '''stmt_list : stmt stmt_list 
    | empty'''

def p_stmt(p):
    '''stmt : base_stmt
    | if_stmt
    | while_stmt'''

def p_base_stmt(p):
    '''base_stmt : assign_stmt 
    | read_stmt 
    | write_stmt 
    | return_stmt'''

def p_assign_stmt(p):
    'assign_stmt : assign_expr SEMI'

def p_assign_expr(p):
    'assign_expr : IDENTIFIER EQ_EQ expr'

def p_read_stmt(p):
    'read_stmt : READ L_PAR id_list R_PAR SEMI'

def p_write_stmt(p):
    'write_stmt : WRITE L_PAR id_list R_PAR SEMI'

def p_return_stmt(p):
    'return_stmt : RETURN expr SEMI'

def p_expr(p):
    'expr : expr_prefix factor'

def p_expr_prefix(p):
    '''expr_prefix : expr_prefix factor addop 
    | empty'''

def p_factor(p):
    'factor : factor_prefix postfix_expr'

def p_factor_prefix(p):
    '''factor_prefix : factor_prefix postfix_expr mulop 
    | empty'''

def p_postfix_expr(p):
    '''postfix_expr : primary 
    | call_expr'''

def p_call_expr(p):
    'call_expr : IDENTIFIER L_PAR expr_list R_PAR'

def p_expr_list(p):
    '''expr_list : expr expr_list_tail 
    | empty'''

def p_expr_list_tail(p):
    '''expr_list_tail : COMM expr expr_list_tail 
    | empty'''

def p_primary(p):
    '''primary : L_PAR expr R_PAR 
    | IDENTIFIER
    | INTLITERAL 
    | FLOATLITERAL'''

def p_addop(p):
    '''addop : PLUS
    | MINUS'''

def p_mulop(p):
    ''' mulop : MULT
    | DIV'''

def p_if_stmt(p):
    'if_stmt : IF L_PAR cond R_PAR decl stmt_list else_part ENDIF'

def p_else_part(p):
    '''else_part : ELSE decl stmt_list 
    | empty''' 

def p_cond(p):
    'cond : expr compop expr'

def p_compop(p):
    ''' compop : LESS
    | MORE 
    | EQ 
    | N_EQ 
    | L_EQ 
    | R_EQ'''

def p_while_stmt(p):
    'while_stmt : WHILE L_PAR cond R_PAR decl stmt_list ENDWHILE'

def p_empty(p):
    'empty :'
    pass


def p_error(p):
    if p:
            global accepted
            accepted = False
            parser.errok()


    
parser = yacc.yacc()
print ("Symbol table Global")
        
result = ''
while True:
        try:
                s = data

        except EOFError:
                break
        if not s: continue
        parser.parse(s, tracking = True)
 
   # if (accepted == False):
   #    print ('Not accepted')
    #else:
    #   print ('Accepted')

        break

#print (table.print_table())




    
