from .lock_expr import *

reserved_set |= {
    'LOCAL', 'LOCALREC'
}

# Combine Tokens
tokens = list(token_set | reserved_set)
