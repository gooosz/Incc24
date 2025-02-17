from .code_generation import gen
from ..lexer.datatypes import tokens

used_procedures_and_classes = {
    'SelfEvaluatingExpression',
    'ListExpression',
    'ArrayExpression',
    'ArrayAccessExpression'
}

precedence = [[]]

def p_expression_single_value(p):
    '''expression : NUMBER
                  | FLOAT
                  | CHAR'''
    p[0] = gen().SelfEvaluatingExpression(p[1])

def p_expression_string_value(p):
    '''expression : STRING'''
    p[0] = gen().StringExpression(p[1])


def p_expression_list_non_empty(p):
    'expression : LIST LPAREN expression_list RPAREN'
    p[0] = gen().ListExpression(p[3])

def p_expression_list_empty(p):
    'expression : LIST LPAREN RPAREN'
    p[0] = gen().ListExpression(None)

def p_expression_array_non_empty(p):
    '''expression : LBRACKET expression_list RBRACKET
                  | ARRAY LPAREN expression_list RPAREN'''
    p[0] = gen().ArrayExpression(p[2]) if len(p) == 4 else gen().ArrayExpression(p[3])

def p_expression_array_empty(p):
    '''expression : LBRACKET RBRACKET
                  | ARRAY LPAREN RPAREN'''
    p[0] = gen().ArrayExpression([])

def p_expression_array_access(p):
    'expression : IDENTIFIER LBRACKET expression RBRACKET'
    p[0] = gen().ArrayAccessExpression(p[1], p[3])

def p_size_expression(p):
    'expression : SIZE LPAREN IDENTIFIER RPAREN'
    # conveniently arr := [1,2,3]; arr returns the size
    p[0] = gen().VariableExpression(p[3])

def p_libc_call_expression(p):
    'expression : PRINTF LPAREN expression_list RPAREN'
    p[0] = gen().LibCCallExpression(p[1], p[3])

#def p_array_index_assign(p):
#    'expression : IDENTIFIER LBRACKET expression RBRACKET ASSIGN expression'
#    p[0] = gen().AssignmentExpression(gen().ArrayAccessExpression([1], [3]), p[6])

def p_error(p):
    print(f'Syntax error at {p.value}')
