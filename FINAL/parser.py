
import ply.yacc as yacc
from lexer import tokens
import sys
from symbol_table import Symbol_Table
from semantic_routine import Semantic_Routine
from semantic_routine import IR_To_Tiny

infile = sys.argv[1]
with open(infile, 'r') as myfile:
    data = myfile.read()
accepted = True
table = Symbol_Table()
routine = Semantic_Routine()

#Following functions are the grammar for the LITTLE language
def p_program(p):
    'program : PROGRAM id BEGIN pgm_body END'

def p_id(p):
    'id : IDENTIFIER'
    p[0] = p[1]

def p_pgm_body(p):
    'pgm_body : decl func_declarations'

def p_decl(p):
    '''decl : string_decl decl
    | var_decl decl
    | empty'''

def p_string_decl(p):
    'string_decl : STRING id EQ_EQ str SEMI'
    table.add_str(p[2], p[4])

def p_str(p):
    'str : STRINGLITERAL'
    p[0] = p[1]
def p_var_decl(p):
    'var_decl : var_type id_list SEMI'
    table.add_var(p[1], p[2])

def p_var_type(p):
    '''var_type : FLOAT
    | INT'''
    p[0] = p[1]

def p_any_type(p):
    '''any_type : var_type
    | VOID'''

def p_id_list(p):
    'id_list : id id_tail'
    p[0] = [p[1]] + p[2]


def p_id_tail(p):
    '''id_tail : COMM id id_tail
    | empty'''
    if len(p) != 2:
        p[0] = [p[2]] + p[3]
    else:
        p[0] = []

def p_param_decl_list(p):
    '''param_decl_list : param_decl param_decl_tail
    | empty'''

def p_param_decl(p):
    'param_decl : var_type id'
    table.add_var(p[1], [p[2]])

def p_param_decl_tail(p):
    '''param_decl_tail : COMM param_decl param_decl_tail
    | empty'''

def p_func_declarations(p):
    '''func_declarations : func_decl func_declarations
    | empty'''

def p_func_decl(p):
    'func_decl : s_func L_PAR param_decl_list R_PAR BEGIN func_body END'
    table.func_end()

#The following function was added so we could know where functions started
def p_s_func(p):
    's_func : FUNCTION any_type id'
    table.func_start(p[3])

def p_func_body(p):
    'func_body : decl stmt_list'
    if p[2] != None:
        p[0] = p[2]
        IR_To_Tiny(p[0])


def p_stmt_list(p):
    '''stmt_list : stmt stmt_list
    | empty'''

    if len(p) > 2:
        if p[2] != None and p[1] != None:
            p[0] = p[1] + p[2]
        else:
            p[0] = p[1]

    else:
        p[0] = []

def p_stmt(p):
    '''stmt : base_stmt
    | if_stmt
    | while_stmt'''
    p[0] = p[1]

def p_base_stmt(p):
    '''base_stmt : assign_stmt
    | read_stmt
    | write_stmt
    | return_stmt'''
    p[0] = p[1]

def p_assign_stmt(p):
    'assign_stmt : assign_expr SEMI'
    p[0] = p[1]
def p_assign_expr(p):
    'assign_expr : id EQ_EQ expr'
    d_type = table.search(p[1])
    p[0] = routine.add_assign_expr(p[3], p[1])
    p[0] = routine.change_type(p[0], d_type)



def p_read_stmt(p):
    'read_stmt : READ L_PAR id_list R_PAR SEMI'
    p[0] = routine.read_list(p[3])

def p_write_stmt(p):
    'write_stmt : WRITE L_PAR id_list R_PAR SEMI'
    p[0] = routine.write_list(p[3])
def p_return_stmt(p):
    'return_stmt : RETURN expr SEMI'

def p_expr(p):
    'expr : expr_prefix factor'
    if p[2] != None and p[1] != None:
        p[0] = routine.add_mul_op(p[1], p[2])

    elif p[1] == None:
        p[0] = p[2]

def p_expr_prefix(p):
    '''expr_prefix : expr_prefix factor addop
    | empty'''
    if len(p) > 2:
        if p[1] != None:
            p[0] = p[1] + p[2] + [p[3]]
            p[0] = routine.add_mul_op(p[1], p[2]) + [p[3]]
        else:
            p[0] = p[2] + [p[3]]

def p_factor(p):
    'factor : factor_prefix postfix_expr'
    if p[1] != None and p[2] != None:
        p[0] = routine.add_mul_op(p[1], p[2])
    elif p[1] == None:
        p[0] = p[2]

def p_factor_prefix(p):
    '''factor_prefix : factor_prefix postfix_expr mulop
    | empty'''
    if len(p) > 2:
        if p[1] != None:
            p[0] = routine.add_mul_op(p[1], p[2]) + [p[3]]
        else:
            p[0] = p[2] + [p[3]]


def p_postfix_expr(p):
    '''postfix_expr : primary
    | call_expr'''
    p[0] = p[1]

def p_call_expr(p):
    'call_expr : id L_PAR expr_list R_PAR'

def p_expr_list(p):
    '''expr_list : expr expr_list_tail
    | empty'''

def p_expr_list_tail(p):
    '''expr_list_tail : COMM expr expr_list_tail
    | empty'''

def p_primary(p):
    '''primary : L_PAR expr R_PAR
    | id
    | INTLITERAL
    | FLOATLITERAL'''
    if len(p) < 3:
        p[0] = routine.add_primary(p[1])
    else:
        p[0] = p[2]

def p_addop(p):
    '''addop : PLUS
    | MINUS'''
    p[0] = p[1]

def p_mulop(p):
    ''' mulop : MULT
    | DIV'''
    p[0] = p[1]

def p_if_stmt(p):
    'if_stmt : s_if L_PAR cond R_PAR decl stmt_list else_part ENDIF'

    if p[7] == None:
        p[0] = p[3] + p[6] + [["LABEL ", p[3][-1][-1]]]
    else:
        p[0] = p[3] + p[6] + [p[7][0]] +  [["LABEL ", p[3][-1][-1]]] + p[7][1] + [p[7][2]]

    table.block_end()

#The following function was added so we could know where if statements started
def p_s_if(p):
    's_if : IF'
    table.block_start()

def p_else_part(p):
    '''else_part : s_else decl stmt_list
    | empty'''
    if len(p) > 2:
        reg = routine.add_else()
        p[0] = [reg[0]] + [p[3]] + [["LABEL ", reg[0][1]]]
        table.block_end()

#The following function was added so we could know where else statements started
def p_s_else(p):
    's_else : ELSE'
    table.block_start()

def p_cond(p):
    'cond : expr compop expr'
    print p[1][-1][-1]
    d_type = table.search(p[1][-1][-1])
    p[0] = routine.add_cond(p[1], p[2], p[3], d_type)

def p_compop(p):
    ''' compop : LESS
    | MORE
    | EQ
    | N_EQ
    | L_EQ
    | R_EQ'''
    p[0] = p[1]

def p_while_stmt(p):
    'while_stmt : s_while L_PAR cond R_PAR decl stmt_list ENDWHILE'
    label = routine.get_label()
    #print p[6]
    if p[6] != None:
        p[0] = label + p[3] + p[6] + [['JUMP ', label[0][-1]]] + [["LABEL ", p[3][-1][-1]]]
    else:
        p[0] = label + p[3] + [['JUMP ', label[0][-1]]] + [["LABEL ", p[3][-1][-1]]]

    table.block_end()

def p_s_while(p):
    's_while : WHILE'
    table.block_start()

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
         global accepted
         accepted = False
         parser.errok()

parser = yacc.yacc()
result = ''
while True:
    try:
        s = data

    except EOFError:
        break
    if not s: continue

    parser.parse(s, tracking = True)

    """if (accepted == False):
        print ('Not accepted')
    else:
        print ('Accepted')
        """


    break

#table.print_output()
