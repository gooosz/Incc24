from dataclasses import dataclass
import operator

# can call an operator using the string by operators['+'][1](a,b) which will do a+b
operators = {'+': ('add', lambda x,y: x+y),
             '-': ('sub', lambda x,y: x-y),
             '*': ('mul', lambda x,y: x*y),
             '/': ('div', lambda x,y: x/y),
             '<': ('le', lambda x,y: x<y),
             '>': ('gr', lambda x,y: x>y),
             '<=': ('leq', lambda x,y: x<=y),
             '>=': ('geq', lambda x,y: x>=y),
             '==': ('eq', lambda x,y: x==y),
             '!=': ('neq', lambda x,y: x!=y)
             }

# can call an operator using the string by unary_operators['-'][1](a) which will do -a
unary_operators = {
            '-': ('neg', lambda x: -x)
    }

class CompiledExpression:
    def code_b(self, env, kp):
        return self.code_v(env, kp) + "getbasic\n"
        #raise Exception(f"code_b von {self} uninplemented")
    def code_v(self, env, kp):
        return self.code_b(env, kp) + "mkbasic\n"
        #raise Exception(f"code_v von {self} uninplemented")

@dataclass
class ProgramExpression:
    body: CompiledExpression

    def code_b(self, env, kp):
        ret = ""
        # create global variables vector of whole program
        all_global_vars = free_vars(self.body)
        print(f"global vars: {all_global_vars}")
        # create global vector, in lambda the global vars + old/outer params are written into new global vector, so it must have enough size for both
        for i,v in enumerate(all_global_vars):
            env[v] = {'addr': i, 'scope': 'global', 'size': 8}
        ret += "# setting up global variables\n"
        ret += f"alloc {len(all_global_vars) + max_num_params(self.body)}\n"
        ret += f"mkvec {len(all_global_vars) + max_num_params(self.body)}\n"
        ret += "setgv\n"

        # params vector gets created and set in every call expression

        ret += "# body of program\n"
        ret += self.body.code_b(env, kp)
        return ret

@dataclass
class SelfEvaluatingExpression(CompiledExpression):
    id : CompiledExpression

    def code_b(self, env, kp):
        print(f"code_b kp={kp}: {self}")
        return f'loadc {self.id}\n'

    def code_v(self, env, kp):
        print(f"code_v kp={kp}: {self}")
        # legt neue Zelle im Heap ['B',id] an
        return self.code_b(env, kp) + "mkbasic\n"

@dataclass
class BinaryOperatorExpression(CompiledExpression):
    e1: CompiledExpression
    op: str
    e2: CompiledExpression

    def code_b(self, env, kp):
        print(f"code_b kp={kp}: {self}")
        ret = self.e1.code_b(env, kp)
        ret += self.e2.code_b(env, kp+1)
        ret += f"{operators[self.op][0]}\n"
        #return f"# {self}\n" + ret
        return ret

@dataclass
class UnaryOperatorExpression(CompiledExpression):
    op: str
    expr: CompiledExpression

    def code_b(self, env, kp):
        print(f"code_b kp={kp}: {self}")
        ret = self.expr.code_b(env, kp)
        ret += f"{unary_operators[self.op][0]}\n"
        return ret

# 1. BinaryOperator hat code_b, code_v
# 2. Sequence, Variables, Assignment nur code_v
# 3. ITE (hat code_b+code_v), While, loop nur code_v
# 4. Function, Lambda nur code_v
# wenn nur code_v definiert wird macht code_b: code_v + getbasic

@dataclass
class SequenceExpression(CompiledExpression):
    seq: list[CompiledExpression]

    def code_v(self, env, kp):
        print(f"code_v kp={kp}: {self}")
        n = len(self.seq)
        ret = ""
        # pop after every expression if followed by ;
        for expr in self.seq[:-1]:
            ret += expr.code_v(env, kp)
            ret += "pop 1\n" # ; follows so value is disregarded
        ret += self.seq[-1].code_v(env, kp)
        #return f"# {self}\n" + ret
        return ret

@dataclass
class VariableExpression(CompiledExpression):
    name: str

    def code_v(self, env, kp):
        print(f"code_v kp={kp}: {self} in env {env}")
        # lookup because variable could be defined in parent environment or is in global/param vector
        print(f"Zugriff auf var {self.name} at addr {lookup(env, self.name)['addr']}")
        return getvar(self.name, env, kp)


@dataclass
class AssignmentExpression(CompiledExpression):
    var: VariableExpression
    value: CompiledExpression

    def code_v(self, env, kp):
        var_entry = lookup(env, self.var.name)
        addr = var_entry['addr']

        ret = self.value.code_v(env,kp)
        ret += rewrite(env, self.var.name, n=1, j=addr) # n=0 is optional
        return ret


@dataclass
class ArrayExpression(CompiledExpression):
    # syntax: [ expressionlist ] or array(expressionlist)
    values: list[CompiledExpression]

    # code_b of array is the size, because it will simply go to object ['V', ptr] -> [n, ...]
    # and return the size n

    def code_v(self, env, kp):
        # returns address to array object
        # evaluate every expression and push value on stack in reverse
        # (so mkvec can add values in correct order easier)
        n = len(self.values)
        ret = ""
        for i in reversed(range(n)):
            ret += f"{self.values[i].code_v(env, kp+i)}"
        ret += f"mkvec {n}\n"
        return f"# {self}\n" + ret

@dataclass
class ArrayAccessExpression(CompiledExpression):
    # syntax: var[expr]
    var: str
    index: CompiledExpression

    def code_v(self, env, kp):
        ret = getvar(self.var, env, kp)
        ret += self.index.code_b(env, kp+1)
        # address of array/vector is on top of stack => simply pushaddr now
        ret += f"pushaddr\n"
        return f"# {self}\n" + ret

@dataclass
class ITEExpression(CompiledExpression):
    condition: CompiledExpression # always gets evaluated using code_b
    ifbody: CompiledExpression      # code_b or code_v depending on call of ITEExpression
    elsebody: CompiledExpression    # code_b or code_v depending on call of ITEExpression

    def code_b(self, env, kp):
        print(f"code_b kp={kp}: {self}")
        ite_label, then_label, else_label, end_label = nextlabel(self)

        ret  = f"{ite_label}:\n"
        ret += self.condition.code_b(env, kp)
        ret += f"jumpz {else_label}\n"
        ret += f"{then_label}:\n"
        ret += self.ifbody.code_b(env, kp)
        ret += f"jump {end_label}\n"
        ret += f"{else_label}:\n"
        ret += self.elsebody.code_b(env, kp) if self.elsebody is not None else "loadc 0\n" # elsebody doesn't exist => load default 0
        ret += f"{end_label}:\n"
        return ret

    def code_v(self, env, kp):
        print(f"code_v kp={kp}: {self}")
        ite_label, then_label, else_label, end_label = nextlabel(self)

        ret  = f"{ite_label}:\n"
        ret += self.condition.code_b(env, kp)
        ret += f"jumpz {else_label}\n"
        ret += f"{then_label}:\n"
        ret += self.ifbody.code_v(env, kp)
        ret += f"jump {end_label}\n"
        ret += f"{else_label}:\n"
        ret += self.elsebody.code_v(env, kp) if self.elsebody is not None else "loadc 0\nmkbasic\n" # elsebody doesn't exist => load default 0
        ret += f"{end_label}:\n"
        return ret

@dataclass
class WhileExpression(CompiledExpression):
    condition: CompiledExpression
    body: CompiledExpression

    def code_b(self, env, kp):
        print(f"code_b kp={kp}: {self}")
        while_label, do_label, end_label = nextlabel(self)
        # if condition fails at first check, must return default value 0
        # new iteration discards the old value
        ret  = "loadc 0\n"
        ret += f"{while_label}:\n"
        ret += self.condition.code_b(env, kp+1)
        ret += f"jumpz {end_label}\n"
        ret += f"{do_label}:\n"
        ret += "pop 1\n" # discard value from last iteration
        ret += self.body.code_b(env, kp+1)
        ret += f"jump {while_label}\n"
        ret += f"{end_label}:\n"
        return ret

    def code_v(self, env, kp):
        print(f"code_v kp={kp}: {self}")
        while_label, do_label, end_label = nextlabel(self)
        # if condition fails at first check, must return default value 0
        # new iteration discards the old value
        ret  = "loadc 0\nmkbasic\n"
        ret += f"{while_label}:\n"
        ret += self.condition.code_b(env, kp+1)
        ret += f"jumpz {end_label}\n"
        ret += f"{do_label}:\n"
        ret += "pop 1\n" # discard value from last iteration
        ret += self.body.code_v(env, kp+1)
        ret += f"jump {while_label}\n"
        ret += f"{end_label}:\n"
        return ret


@dataclass
class LoopExpression(CompiledExpression):
    # loop expression do expression
    # runs the loop until the loopvar is 0
    loopvar: CompiledExpression
    body: CompiledExpression

    def code_b(self, env, kp):
        print(f"code_b kp={kp}: {self}")
        loop_label, do_label, end_label = nextlabel(self)

        ret = "loadc 0\n" # default value in case loop body doesnt get executed
        ret += self.loopvar.code_b(env, kp+1)
        ret += f"{loop_label}:\n"
        ret += "dup\n"    # duplicate the loopvar because the jumpz later on will delete one
        ret += f"jumpz {end_label}\n"
        ret += "swap\n"   # swap 1. and 2. value on stack
        ret += "pop 1\n"  # remove old iteration value
        ret += f"{do_label}:\n"
        ret += self.body.code_b(env, kp+1)    # push new iteration value
        ret += "swap\n" # swap, so that loopvar is on top of stack
        ret += "dec\n"  # decrement top value (loopvar) of stack
        ret += f"jump {loop_label}\n"   # check loopvar if next iteration
        ret += f"{end_label}:\n"
        ret += "pop 1\n"  # final pop because loopvar is on top of stack
        return ret

    def code_v(self, env, kp):
        print(f"code_v kp={kp}: {self}")
        loop_label, do_label, end_label = nextlabel(self)

        ret = "loadc 0\nmkbasic\n" # default value in case loop body doesnt get executed
        ret += self.loopvar.code_b(env, kp+1)
        ret += f"{loop_label}:\n"
        ret += "dup\n"    # duplicate the loopvar because the jumpz later on will delete one
        ret += f"jumpz {end_label}\n"
        ret += "swap\n"   # swap 1. and 2. value on stack
        ret += "pop 1\n"  # remove old iteration value
        ret += f"{do_label}:\n"
        ret += self.body.code_v(env, kp+1)    # push new iteration value
        ret += "swap\n" # swap, so that loopvar is on top of stack
        ret += "dec\n"  # decrement top value (loopvar) of stack
        ret += f"jump {loop_label}\n"   # check loopvar if next iteration
        ret += f"{end_label}:\n"
        ret += "pop 1\n"  # final pop because loopvar is on top of stack
        return ret

# because of double indirection in pointers, letrec and let can do same functionality, so they are merged into let
# => implement let now like letrec
# let expression variables shadow global variables with same name
@dataclass
class LocalExpression(CompiledExpression):
    # local name1:=expr1, ..., namen:=exprn in body
    localvars: list # list of tupels (variableName, expression)
    body: CompiledExpression

    """
        Stack frame:
        |   return value   |
        | old local vector |

        Registers:
        r12: global vector
        r13: local vector
        r14: param vector
    """

    def code_v(self, env, kp):
        # local variables only get created in let block, nowhere else
        print(f"code_v kp={kp}: {self}")
        n = len(self.localvars)

        ret = f"alloc {n}\n" # empty/dummy objects, get rewritten later on, so recursion works
        env2 = {'parent': env}
        for i, [var, val] in enumerate(self.localvars):
            print(f"localvar {i}, kp={kp}: {var} = {val}")
            env2[var] = {'addr': kp+i+1, 'scope': 'local', 'size': 8}
        for i, [var, val] in enumerate(self.localvars):
            ret += f"{val.code_v(env2, kp+n)}"
            ret += rewrite(env2, var, n, i) # gets the correct statements (must differ between local and global/param because the latter use vectors)
            ret += "pop 1\n" # no need to keep object on stack, because the dummy value from before has been rewritten
        # evaluate body
        ret += "# local body\n"
        ret += f"{self.body.code_v(env2, kp+n)}"
        ret += f"slide {n}\n" # remove the local vars from stack
        return f"# Start of {self}\n" + ret + f"# End of {self}\n"


@dataclass
class CallExpression(CompiledExpression):
    procname: CompiledExpression
    params: list[CompiledExpression]

    def code_v(self, env, kp):
        print(f"code_v kp={kp}: {self}")
        call_return_label = nextlabel(self)

        n = len(self.params)
        ret = ""
        ret += f"mark {call_return_label}\n" # saves old param vector as well to recover later on
        # TODO: save old param vector values on stack to recover later on
        # run code_v of each param, fill param vector
        for i in reversed(range(n)):
            ret += f"{self.params[i].code_v(env, kp+4+i)}" # params get stored in param vector, not on stack
            #ret += "pushparamvec\n"
            #ret += f"storeaddr {i}\n" # must be storeaddr instead of rewrite, so changing parameter value changes the value globally
            #ret += "pop 1\n" # only store value into param vector so return value of storeaddr is not needed
        # create a new param vector, so old params are saved across nested lambdas
        ret += f"mkvec {n}\n"
        ret += "setpv\n"

        ret += f"{self.procname.code_v(env, kp+4)}"
        ret += "apply\n"
        ret += f"{call_return_label}:\n"
        return ret


@dataclass
class LambdaExpression(CompiledExpression):
    params: list()      # may be empty
    body: CompiledExpression

    """
        Stack frame on entry:
        | Rücksprungadresse |
        |     old rbp       |
        | old param vector  |
        | old global vector |

        Stack frame on exit:
        |   return value    |

        Registers:
        r12: global vector
        r13: local vector
        r14: param vector
    """
    def code_v(self, env, kp):
        print(f"code_v kp={kp}: {self}")
        lambda_label, end_lambda = nextlabel(self)

        # free variables = global variables + current locals + current params
        # get put into a new global vector, that is given to lambda

        freevars = free_vars(self) # get free variables of lambda expression
        print(f"> free_vars {freevars} in {self}")
        n = len(freevars)
        ret = ""

        # put all free vars in new gp for lambda in reverse, so easier to add to vector in asm (simply mkvec)
        # add free vars, params of lambda to new environment
        for i,v in reversed(list(enumerate(freevars))):
            ret += getvar(v, env, kp)
        ret += f"mkvec {n}\n" # fills a new vector with n values on stack
        ret += f"mkfunval {lambda_label}\n" # creates function object ['F', ptr] -> [addr, newly filled global vector]
        ret += f"jump {end_lambda}\n"
        ret += f"{lambda_label}:\n"
        env2 = {}
        for i,v in enumerate(freevars):
            env2[v] = {'addr': i, 'scope': 'global', 'size': 8} # all free vars (former global/local/param variables) become global now
        for i,v in enumerate(self.params):
            env2[v] = {'addr': i, 'scope': 'param', 'size': 8} # add current params to new environment
        print(f"lambda env: {env2}")
        ret += f"{self.body.code_v(env2, 0)}"
        ret += "popenv\n"
        ret += f"{end_lambda}:\n"
        return ret


# returns generator for next labels of given expression
count_ite = 0
count_while = 0
count_loop = 0
count_call = 0
count_lambda = 0
def nextlabel(expr: CompiledExpression):#
    global count_ite
    global count_while
    global count_loop
    global count_call
    global count_lambda
    ret = ("empty")
    match expr:
        case ITEExpression(_, _, _):
            ret = (f"ite_{count_ite}", f"then_{count_ite}", f"else_{count_ite}", f"endite_{count_ite}")
            count_ite += 1
        case WhileExpression(_, _):
            ret = (f"while_{count_while}", f"do_{count_while}", f"endwhile_{count_while}")
            count_while += 1
        case LoopExpression(_, _):
            ret = (f"loop_{count_loop}", f"do_{count_loop}", f"endloop_{count_loop}")
            count_loop += 1
        case CallExpression(_, _):
            ret = (f"back_from_call_{count_call}")
            count_call += 1
        case LambdaExpression(_, _):
            ret = (f"lambda_{count_lambda}", f"end_lambda_{count_lambda}")
            count_lambda += 1
    return ret


# push address of vector where variable is in or will be in
def getvec(var, env):
    match lookup(env, var):
        case {'scope': 'local', 'addr': j, 'size': _}:  return f"pushlocalvec\n"
        case {'scope': 'global', 'addr': j, 'size': _}: return f"pushglobalvec\n"
        case {'scope': 'param', 'addr': j, 'size': _}:  return f"pushparamvec\n"
        case _: raise Exception(f"Variable {var} not defined in {env}") # scope None means variable is out of scope / hasn't been initialized yet => cannot use it

# push address of variable onto stack
# checks if var is global/local/param
def getvar(var, env, kp):
    match lookup(env, var):
        case {'scope': 'local', 'addr': j, 'size': _}:  return f"# getvar({var}, {env}, {kp}), addr={j}\npushlocal {kp-j}\n"
        case {'scope': 'global', 'addr': j, 'size': _}: return "pushglobalvec\n" + f"pushaddr {j}\n"
        case {'scope': 'param', 'addr': j, 'size': _}:  return "pushparamvec\n" + f"pushaddr {j}\n"
        case _: raise Exception(f"Variable {var} not defined in {env}")

# on stack is pointer to new object
# function rewrites the object at pos i in stack with the new values on top of stack
def rewrite(env, var, n=1, j=0):
    match lookup(env, var):
        case {'scope': 'local', 'addr': _, 'size': _}:  return f"rewriteloc {n-j}\n"
        case {'scope': 'global', 'addr': _, 'size': _}: return "pushglobalvec\n" + f"rewriteinvec {j}\n"
        case {'scope': 'param', 'addr': _, 'size': _}:  return "pushparamvec\n" + f"rewriteinvec {j}\n"

# returns entry of variable in env or it's parent if exists
def lookup(env, name):
    if name in env:
        return env[name]
    if 'parent' in env:
        return lookup(env['parent'], name)
    # this case should not happen
    raise KeyError(f"No known variable named {name} in env {env}")

# returns index of new address
local_count = 0
global_count = 0
def new_addr(scope):
    global local_count
    global global_count
    match scope:
        case 'local':
            curr_local_count = local_count
            local_count += 1
            return curr_local_count
        case 'global':
            curr_global_count = global_count
            global_count += 1
            return curr_global_count
        case _: raise Exception(f"Wrong scope {scope} when requesting new address\n")

# get free variables of an expression, used for calculating free/global variables when entering lambda expression
def free_vars(expr):
    match expr:
        case SelfEvaluatingExpression(x):           return set()
        case VariableExpression(x):                 return {x}
        case BinaryOperatorExpression(e1, op, e2):  return free_vars(e1) | free_vars(e2)
        case SequenceExpression(seq):               return {x for el in seq for x in free_vars(el)}
        case AssignmentExpression(var, val):        return free_vars(var) | free_vars(val)
        case ITEExpression(condition, ifbody, None): return free_vars(condition) | free_vars(ifbody)
        case ITEExpression(condition, ifbody, elsebody): return free_vars(condition) | free_vars(ifbody) | free_vars(elsebody)
        case WhileExpression(condition, body):      return free_vars(condition) | free_vars(body)
        case LoopExpression(loopvar, body):         return free_vars(loopvar) | free_vars(body)
        case LocalExpression(localvars, body):      return free_vars(body) - {x for x,e in localvars}  # localvars are bound variables
        case LambdaExpression(params, body):        return free_vars(body) - {x for x in params}     # params are bound variables
        case CallExpression(name, params):          return free_vars(name).union(*(free_vars(p) for p in params))
        case ArrayExpression(values):               return {x for el in values for x in free_vars(el)}
        case ArrayAccessExpression(var, index):     return {var} | free_vars(index)
        case UnaryOperatorExpression(op, expr):     return free_vars(expr)
        case _:                                     raise Exception(f"free_vars({expr}) wrong")


# returns set of local variables of whole program
def local_vars(expr):
    match expr:
        case SelfEvaluatingExpression(x):           return set()
        case VariableExpression(x):                 return set()
        case BinaryOperatorExpression(e1, op, e2):  return local_vars(e1).union(local_vars(e2))
        case SequenceExpression(seq):               return {x for el in seq for x in local_vars(el)}
        case AssignmentExpression(var, val):        return local_vars(var).union(local_vars(val))
        case ITEExpression(condition, ifbody, None): return local_vars(condition).union(local_vars(ifbody))
        case ITEExpression(condition, ifbody, elsebody): return local_vars(condition).union(local_vars(ifbody)).union(local_vars(elsebody))
        case WhileExpression(condition, body):      return local_vars(condition).union(local_vars(body))
        case LoopExpression(loopvar, body):         return local_vars(loopvar).union(local_vars(body))
        case LocalExpression(localvars, body):      return {x for x,e in localvars}.union(local_vars(body)) # nested, names of all locally defined variables
        case LambdaExpression(params, body):        return local_vars(body) # params go into param vector
        case CallExpression(name, params):          return local_vars(name).union(*(local_vars(x) for x in params))
        case ProgramExpression(body):               return local_vars(body)
        case _:                                     raise Exception(f"local_vars({expr}) wrong")

# returns biggest number of params of a lambda
# varargs should be possible in the future, so biggest number of params is decided between lambda params and given params in call
def max_num_params(expr):
    match expr:
        case SelfEvaluatingExpression(x):           return 0
        case VariableExpression(x):                 return 0
        case BinaryOperatorExpression(e1, op, e2):  return max(max_num_params(e1), max_num_params(e2))
        case SequenceExpression(seq):               return max([max_num_params(el) for el in seq])
        case AssignmentExpression(var, val):        return max(max_num_params(var), max_num_params(val))
        case ITEExpression(condition, ifbody, None): return max(max_num_params(condition), max_num_params(ifbody))
        case ITEExpression(condition, ifbody, elsebody): return max(max_num_params(condition), max_num_params(ifbody), max_num_params(elsebody))
        case WhileExpression(condition, body):      return max(max_num_params(condition), max_num_params(body))
        case LoopExpression(loopvar, body):         return max(max_num_params(loopvar), max_num_params(body))
        case LocalExpression(localvars, body):
            max_in_seq = max([max_num_params(e) for x,e in localvars])
            return max(max_in_seq, max_num_params(body))
        case LambdaExpression(params, body):        return max(len(params), max_num_params(body))
        case CallExpression(name, params):          return max(max_num_params(name), len(params))
        case ProgramExpression(body):               return max_num_params(body)
        case ArrayExpression(values):               return max([max_num_params(el) for el in values]) if values else 0
        case ArrayAccessExpression(var, index):     return max_num_params(index)
        case UnaryOperatorExpression(op, expr):     return max_num_params(expr)
        case _:                                     raise Exception(f"max_num_params({expr}) wrong")


# formats ir code to be more readable
# e.g. puts all lambdas on top of file
# creates main label where execution starts (TODO: must work with that in x86 assembly, like Tims formatting)
def format_ir(ir_code: str, lambdas: list[str]):
    pass









