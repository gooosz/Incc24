from .code_generation import gen
from .lock_expr import *
from ..lexer.local_expr import tokens

used_procedures_and_classes |= {
    'LocalExpression'
}

def p_assign_list(p):
    '''assign_list : IDENTIFIER ASSIGN expression
                 | assign_list COMMA IDENTIFIER ASSIGN expression'''
    if (len(p) == 4):
        p[0] = [(p[1], p[3])]   # tuples x:=value
    else:
        # chained assign_list
        p[0] = p[1] + [(p[3], p[5])]

def p_expression_local(p):
    'expression : LOCAL assign_list IN expression'
    #'expression : LOCAL IDENTIFIER ASSIGN expression IN expression'
    p[0] = gen().LocalExpression(p[2], p[4])

def p_expression_localrec(p):
    'expression : LOCALREC assign_list IN expression'
    p[0] = gen().LocalExpression(p[2], p[4])
