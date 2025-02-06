from ply.lex import lex

token_set = {'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN'}

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore  = ' \t'
t_ignore_COMMENT = r'\#.*'


def t_error(t):
    raise Exception("Illegal character '%s'" % t.value[0])

tokens = list(token_set)
arith_expr_lex=lex()

