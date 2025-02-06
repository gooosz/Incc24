from dataclasses import dataclass

operators = {'+': 'add',
             '-': 'sub',
             '*': 'mul',
             '/': 'div',
             '<': 'le',
             '>': 'gr',
             '<=': 'leq',
             '>=': 'geq',
             '==': 'eq',
             '!=': 'neq'
             }

class CompiledExpression:
    def code_b(self, rho, kp):
        raise Exception(f"code_b von {self} uninplemented")
    def code_v(self, rho, kp):
        #return self.code_b(rho, kp) + "getbasic\n"
        raise Exception(f"code_v von {self} uninplemented")

@dataclass
class SelfEvaluatingExpression(CompiledExpression):
    id : CompiledExpression
    
    def code_b(self, rho, kp):
        print(f"code_b: {self}")
        return f'loadc {self.id}\n'

    def code_v(self, rho, kp):
        print(f"code_v: {self}")
        # legt neue Zelle im Heap ['B',id] an
        return self.code_b(rho, kp) + "mkbasic\n"

@dataclass
class BinaryOperatorExpression(CompiledExpression):
    e1: CompiledExpression
    op: str
    e2: CompiledExpression

    def code_b(self, rho, kp):
        print(f"code_b: {self}")
        ret = self.e1.code_b(rho, kp)
        ret += self.e2.code_b(rho, kp+1)
        ret += f"{operators[self.op]}\n"
        return ret

    def code_v(self, rho, kp):
        print(f"code_v: {self}")
        return self.code_b(rho, kp) + 'mkbasic\n'


@dataclass
class VariableExpression(CompiledExpression):
    name: str

    def code_b(self, rho, kp):
        print(f"code_b: {self}")
        return self.code_v(rho, kp) + 'getbasic\n'

    def code_v(self, rho, kp):
        print(f"code_v: {self}")
        # legt neue Zelle im Heap ['B',id] an
        #ret = f";; getvar({self.name}, rho, {kp})\n"
        #ret += f";;; VariableExpression {self.name}\n"
        ret = getvar(self.name, rho, kp)
        return ret


# fast nur (ausser temporäres) wird nurnoch code_v aufgerufen

ite_count = 0
@dataclass
class ITEExpression(CompiledExpression):
    # if then else
    # if without else has None as else body
    condition: CompiledExpression
    ifbody: CompiledExpression
    elsebody: CompiledExpression

    # condition immer code_b
    # bodies je nachdem ob code_v oder code_b aufgerufen
    """
        ite:
        condition
        jumpz else
        then:
            ifbody
        jump endif
        else:
            elsebody
        endif: 
    """
    def code_b(self, rho, kp):
        print(f"code_b: {self}")
        global ite_count
        current_ite_count = ite_count
        ite_count += 1
        ret = f"ite_{current_ite_count}:\n"
        ret += self.condition.code_b(rho, kp)
        ret += f"jumpz else_{current_ite_count}\n"
        ret += f"then_{current_ite_count}:\n"
        ret += self.ifbody.code_b(rho, kp)
        ret += f"jump endif_{current_ite_count}\n"
        ret += f"else_{current_ite_count}:\n"
        ret += "loadc 0\n" if self.elsebody is None else self.elsebody.code_b(rho, kp)
        ret += f"endif_{current_ite_count}:\n"
        return ret

    def code_v(self, rho, kp):
        print(f"code_v: {self}")
        global ite_count
        current_ite_count = ite_count
        ite_count += 1
        ret = f"ite_{current_ite_count}:\n"
        ret += self.condition.code_b(rho, kp)
        ret += f"jumpz else_{current_ite_count}\n"
        ret += f"then_{current_ite_count}:\n"
        ret += self.ifbody.code_v(rho, kp)
        ret += f"jump endif_{current_ite_count}\n"
        ret += f"else_{current_ite_count}:\n"
        ret += "loadc 0\n" if self.elsebody is None else self.elsebody.code_v(rho, kp)
        ret += f"endif_{current_ite_count}:\n"
        return ret

@dataclass
class LocalExpression(CompiledExpression):
    # local name1:=expr1, ..., namen:=exprn in body
    localvars: list # list of tupels (variableName, expression)
    body: CompiledExpression

    def code_b(self, rho, kp):
        print(f"code_b: {self}")
        return self.code_v(rho, kp) + 'getbasic\n'

    def code_v(self, rho, kp):
        print(f"code_v: {self}")
        n = len(self.localvars)
        rho2 = {'parent': rho}
        ret = ""
        for i in range(n):
            var, value = self.localvars[i] # assignment von variable aus list nehmen
            rho2[var] = {'scope': 'local', 'addr': kp+i+1, 'size': 8}
            ret += f"{value.code_v(rho2, kp+i)}"
        ret += f"{self.body.code_v(rho2, kp+n)}"
        ret += f"slide {n}\n"
        return ret

@dataclass
class LocalRecExpression(CompiledExpression):
    # localrec name1:=expr1, ..., namen:=exprn in body
    # IMPORTANT: only defined for declaring functions (lambdas) recursively, else the rewrite fails
    localvars: list # list of tupels (funcname, expressions)
    body: CompiledExpression

    def code_b(self, rho, kp):
        print(f"code_b: {self}")
        return self.code_v(rho, kp) + 'getbasic\n'

    def code_v(self, rho, kp):
        print(f"code_v: {self}")
        n = len(self.localvars)
        # Hüllen im Heap anlegen für localvars
        ret = f"alloc {n}\n"

        rho2 = {'parent': rho}
        # loop must be split:
        # 1. put all localvars into environment
        # 2. evaluate expression of each localvar
        # if this is done in only 1 loop for each, then the localvars cannot reference each other in their expression
        # because the other variable and it's address is not known in environment yet
        for i, [var, value] in enumerate(self.localvars):
            rho2[var] = {'scope': 'local', 'addr': kp+i+1, 'size': 8}
        for i, [var, value] in enumerate(self.localvars):
            ret += f"{value.code_v(rho2, kp+n)}"
            ret += f"rewrite {n-i}\n"
        ret += f"{self.body.code_v(rho2, kp+n)}"
        ret += f"slide {n}\n"
        return ret

call_count = 0
@dataclass
class CallExpression(CompiledExpression):
    # Caller
    # used for calling a procedure
    # so when e.g. f(1,2) is written
    # knows the name of caller, given parameters
    procname: CompiledExpression
    params: list[CompiledExpression]

    def code_b(self, rho, kp):
        print(f"code_b: {self}")
        return self.code_v(rho, kp) + "getbasic\n"

    def code_v(self, rho, kp):
        print(f"code_v: {self}")
        global call_count
        current_call_count = call_count
        call_count += 1

        n = len(self.params)
        ret = ""
        ret += f"mark back_from_call_{call_count}\n"
        # run code_v of params from last param to first param
        for i in range(n-1, -1, -1):
            ret += f"{self.params[i].code_v(rho, kp+3+i)}"
        ret += f"{self.procname.code_v(rho, kp+3+n)}"
        ret += "apply\n"
        ret += f"back_from_call_{call_count}:\n"
        return ret

lambda_count = 0
@dataclass
class LambdaExpression(CompiledExpression):
    # has a list of formal parameters, a list of local variables, body
    params: list()      # may be empty
    body: CompiledExpression

    # no code_b because v value of lambda is pointer to ['F', addr, 0, gp]
    # but for code_b what would be the basic value of this tuple?

    def code_v(self, rho, kp):
        print(f"code_v: {self}")
        global lambda_count
        current_lambda_count = lambda_count
        lambda_count += 1

        free_vars = free(self) # get free variables of lambda expression
        n = len(free_vars)
        ret = ""
        for i,v in enumerate(free_vars):
            ret += f"{getvar(v, rho, kp)}"   # push address of free variables onto stack
        ret += f"mkvec {n}\n"
        ret += f"mkfunval lambda_{current_lambda_count}\n"
        ret += f"jump end_lambda_{current_lambda_count}\n"
        ret += f"lambda_{current_lambda_count}:\n"
        rho2 = {}
        for i in range(len(self.params)):
            rho2[self.params[i]] = {'scope': 'local', 'addr': -i, 'size': 8}
        for i,v in enumerate(free_vars):
            rho2[v] = {'scope': 'global', 'addr': i, 'size': 8}
        ret += f"{self.body.code_v(rho2, 0)}"
        ret += "popenv\n"
        ret += f"end_lambda_{current_lambda_count}:\n"

        return ret


# get free variables of an expression
def free(expr):
    match expr:
        case SelfEvaluatingExpression(x):           return set()
        case VariableExpression(x):                 return {x}
        case BinaryOperatorExpression(e1, op, e2):  return free(e1) | free(e2)
        case ITEExpression(condition, ifbody, elsebody): return free(condition) | free(ifbody) | free(elsebody)
        case LocalExpression(localvars, body):      return free(body) - {x for x,e in localvars}  # localvars are bound variables
        case LocalRecExpression(localvars, body):   return free(body) - {x for x,e in localvars}  # localvars are bound variables
        case LambdaExpression(params, body):        return free(body) - {x for x in params}     # params are bound variables
        case CallExpression(name, params):          return free(name).union(*(free(p) for p in params))
        case _:                                     raise Exception(f"free({expr}) wrong")


# push address of variable onto stack
def getvar(var, rho, kp):
    match lookup(rho, var):
        case {'scope': 'local', 'addr': j, 'size': _}: return f"pushloc {kp-j}\n" # kp-j ist offset vom Kellerpegel, Adresse von variable ist relativ zu rsp, also muss in x86 rsp-(kp-j) gemacht werden
        case {'scope': 'global', 'addr': j, 'size': _}: return f"pushglob {j}\n"
        case _: raise Exception(f"Variable {var} not defined in {rho}")

# returns entry of variable in rho or it's parent if exists
def lookup(rho, name):
    if name in rho:
        return rho[name]
    if 'parent' in rho:
        # check if parent environment contains variable
        return lookup(rho['parent'], name)
    # this case should not happen
    raise KeyError(f"No known variable named {name} in env {rho}")

