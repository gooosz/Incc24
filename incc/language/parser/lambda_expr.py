from .code_generation import gen
from .local_expr import *
from ..lexer.lambda_expr import tokens

used_procedures_and_classes |= {
    'LambdaExpression',
    'CallExpression'
}

precedence = [
    ['left', 'COMMA'],
    ['left', 'ARROW']
] + precedence

def p_expression_list(p):
    '''expression_list : expression
                       | expression COMMA expression_list'''
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

def p_expression_n_lambda(p):
    '''expression : LAMBDA LPAREN RPAREN ARROW expression
                  | LAMBDA identifier_list ARROW expression
                  | LAMBDA LPAREN identifier_list RPAREN ARROW expression'''
    if (len(p) == 6):
        # no params
        p[0] = gen().LambdaExpression([], p[5])
    elif (len(p) == 5):
        p[0] = gen().LambdaExpression(p[2], p[4])
    else: # len(p) == 7
        p[0] = gen().LambdaExpression(p[3], p[6])

def p_expression_0_lambda(p):
    'expression : LAMBDA ARROW expression'
    p[0] = gen().LambdaExpression([], p[3])

def p_expression_call_n_args(p):
    'expression : expression LPAREN expression_list RPAREN'
    p[0] = gen().CallExpression(p[1], p[3])

def p_expression_call_0_args(p):
    'expression : expression LPAREN RPAREN'
    p[0] = gen().CallExpression(p[1], [])
