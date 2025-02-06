from ply.yacc import yacc
from ..lexer.arith_expr import tokens as expression_lexer_tokens
from incc.language.parser.code_generation import gen

# these items are expected to be implemented in module cg.gen()erate (see below)
used_procedures_and_classes={'ProgramExpression','BinaryOperatorExpression',
                             'UnaryOperatorExpression','SelfEvaluatingExpression'}

# the actual parser

precedence = [['left', 'PLUS', 'MINUS'],
              ['left', 'TIMES', 'DIVIDE'],
              ['right', 'UMINUS']]

def p_program(p):
    'program : expression'
    p[0] = gen().ProgramExpression(p[1])


def p_expr_plus(p):
    'expression : expression PLUS expression'
    p[0] = gen().BinaryOperatorExpression(p[1], '+', p[3])


def p_expr_minus(p):
    'expression : expression MINUS expression'
    p[0] = gen().BinaryOperatorExpression(p[1], '-', p[3])


def p_expr_times(p):
    'expression : expression TIMES expression'
    p[0] = gen().BinaryOperatorExpression(p[1], '*', p[3])


def p_expr_div(p):
    'expression : expression DIVIDE expression'
    p[0] = gen().BinaryOperatorExpression(p[1], '/', p[3])


def p_expr_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = gen().UnaryOperatorExpression('-', p[2])


def p_expr_num(p):
    'expression : NUMBER'
    p[0] = gen().SelfEvaluatingExpression(p[1])


def p_paren_expr(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_error(p):
    raise Exception("Parser: Syntax error in input!")

tokens = expression_lexer_tokens
arith_expr_yacc = yacc(start='program')

def check_gen():
    print(gen())
