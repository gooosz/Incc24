from .code_generation import gen
from .struct_expr import *
from ..lexer.proc_expr import tokens


used_procedures_and_classes |= {
    'ProgramExpression'
}

def p_program(p):
    'program : expression'
    p[0] = gen().ProgramExpression(p[1])
