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

class CompiledExpression:
    def code_b(self, env):
        return self.code_v(env) + "getbasic\n"
        #raise Exception(f"code_b von {self} uninplemented")
    def code_v(self, env):
        return self.code_b(env) + "mkbasic\n"
        #raise Exception(f"code_v von {self} uninplemented")

@dataclass
class ProgramExpression:
    body: CompiledExpression

    def code_b(self, env):
        ret = ""
        # create local variables vector of whole program, IMPORTANT: watch out for nested environments when local expression

        # local/global variable vectors fixed by
        """
        1. LMAO THIS WORKS:
            - why isn't it as simple as getting all local variables of program in a flat list
            - each gets their entry in env
            - at start of local expression:
                - the local vars in that expression in env get assigned scope 'local', save old scope (might be global)
                - save the current local vector on stack to restore it afterwards
            - at end of local expression:
                - to avoid use out of scope, the local variables get assigned scope None
                - restore previous local vector
            - this implies that local variables with the same name will get shadowed which is fine
            - Problem when global and local variables have the same name
                    => this is fine because in environment globals get set after locals, so at start of program global variables are accessed,
                       but when in local expression the scope gets updated to 'local'
        """

        """
        2. new problem:
            x:=1;
            local y:=2, x:=3 in x+y
            - returns 6 instead of 3, when environment has {y: addr=0, x: addr=0} because of global var
            - works when environment has {x: addr=0, y: addr=1}
            - the order in environment is mostly random i guess, because a set is unordered
            => solution: sort the local/global vars by alphabet before assigning in env to always get the same order
        """

        """
        3. solutions for getting a correct keyerror when trying to use variable out of scope:
            1. in ProgramExpression:
                - sammle alle globalen und lokalen Variablen, weise Adressen hinzu, scope is None because values have not been initialized yet
            2. in AssignmentExpression/LocalExpression:
                - setzt die Werte von globaler/lokaler Variable, setzt im Environment scope auf 'global' oder 'local'
        """
        all_local_vars = local_vars(self.body) # (nested) list of all local variables in program
        print(f"all_local_vars: {all_local_vars}")
        all_global_vars = free_vars(self.body)
        print(f"global vars: {all_global_vars}")
        # IMPORTANT: global, local vars with same name must have the same addr or else wrong index is used
        # e.g.  {
        #           a := 1;
        #           x := 2;
        #           z := local y:=3, x:=4 in x*y;
        #           x+z
        #       }
        #   should be 24 but is 18
        #
        #
        # variables with same name that are global, local, must be added to env first to guarantee correct indices
        global_local_same_vars = all_local_vars & all_global_vars
        print(f"global_local_same_vars: {global_local_same_vars}")
        for i,var in enumerate(global_local_same_vars):
            env[var] = {'addr': i, 'scope': None, 'size': 8}
        basic_index = len(global_local_same_vars) # all other vars in environment get addr = basic_index + i

        only_local_vars = all_local_vars - global_local_same_vars
        print(f"only_local_vars: {only_local_vars}")
        for i, var in enumerate(only_local_vars):
            # set scope to None to avoid use out of scope, the scope will get set to 'local' when entering local expression
            env[var] = {'addr': basic_index+i, 'scope': None, 'size': 8}
        # create local vector
        ret += "# setting up local variables of whole program\n"
        ret += f"alloc {len(all_local_vars)}\n"
        ret += f"mkvec {len(all_local_vars)}\n"
        ret += "setlv\n"


        # create global variables vector
        only_global_vars = all_global_vars - global_local_same_vars
        print(f"only_global_vars: {only_global_vars}")
        for i, var in enumerate(only_global_vars):
            env[var] = {'addr': basic_index+i, 'scope': None, 'size': 8}
        # create global vector
        ret += "# setting up global variables\n"
        ret += f"alloc {len(all_global_vars) + len(all_local_vars) + max_num_params(self.body)}\n"
        ret += f"mkvec {len(all_global_vars) + len(all_local_vars) + max_num_params(self.body)}\n" # in lambda the local vars + global vars + old/outer params are written into new global vector, so it must have enough size for both
        ret += "setgv\n"
        print(f"global vector size: {len(all_global_vars) + len(all_local_vars) + max_num_params(self.body)}")



        # create params vector
        ret += "# setting up params vector\n"
        ret += f"alloc {max_num_params(self.body)}\n"
        ret += f"mkvec {max_num_params(self.body)}\n"
        ret += "setpv\n"
        print(f"params vector size: {max_num_params(self.body)}")

        print(f"===env: {env}")
        ret += "# body of program\n"
        ret += self.body.code_b(env)
        return ret

@dataclass
class SelfEvaluatingExpression(CompiledExpression):
    id : CompiledExpression

    def code_b(self, env):
        print(f"code_b: {self}")
        return f'loadc {self.id}\n'

    def code_v(self, env):
        print(f"code_v: {self}")
        # legt neue Zelle im Heap ['B',id] an
        return self.code_b(env) + "mkbasic\n"

@dataclass
class BinaryOperatorExpression(CompiledExpression):
    e1: CompiledExpression
    op: str
    e2: CompiledExpression

    def code_b(self, env):
        print(f"code_b: {self}")
        ret = self.e1.code_b(env)
        ret += self.e2.code_b(env)
        ret += f"{operators[self.op][0]}\n"
        #return f"# {self}\n" + ret
        return ret


# 1. BinaryOperator hat code_b, code_v
# 2. Sequence, Variables, Assignment nur code_v
# 3. ITE (hat code_b+code_v), While, loop nur code_v
# 4. Function, Lambda nur code_v
# wenn nur code_v definiert wird macht code_b: code_v + getbasic

@dataclass
class SequenceExpression(CompiledExpression):
    seq: list[CompiledExpression]

    def code_v(self, env):
        print(f"code_v: {self}")
        n = len(self.seq)
        ret = ""
        # pop after every expression if followed by ; and is not assignment (else leads to bug see comment below)
        for expr in self.seq[:-1]:
            ret += expr.code_v(env)
            # TODO: fix Bug
            #           mkvec 0
            #           mkfunval lambda_0
            #           jump end_lambda_0
            #           lambda_0:
            #           loadc 2
            #           mkbasic
            #           popenv
            #           end_lambda_0:
            #           pushglobalvec
            #           storeaddr 0     <- doesn't leave anything on stack => so the pop1 afterwards will remove random stuff on stack
            #                              (e.g. old rbp) leading to segfault
            #                           => FIX: in sequence expression only do pop if the previous expression was not assignment
            #           pop 1
            #if type(expr) is not AssignmentExpression:
            #    ret += f"pop 1\n"
            # !! Assignment should return it's value/address !!
            ret += "pop 1\n"
        ret += self.seq[-1].code_v(env)
        #return f"# {self}\n" + ret
        return ret

@dataclass
class VariableExpression(CompiledExpression):
    name: str

    def code_v(self, env):
        print(f"code_v: {self} in env {env}")
        # lookup because variable could be defined in parent environment
        return getvec(self.name, env) + f"pushaddr {lookup(env, self.name)['addr']}\n"


@dataclass
class AssignmentExpression(CompiledExpression):
    var: VariableExpression
    value: CompiledExpression

    def code_v(self, env):
        #if self.var.name not in env:
            # variable is not stored yet, so get a new address for it
            # valid scopes: global, local, param
        #    env[self.var.name] = {'addr': new_addr('global'), 'scope': 'global', 'size': 8}
        # set scope to global only if variable hasn't been initialized yet (scope = None)
        # or else f := \(z) -> z:=4; tries to use z as global variable in AssignmentExpression
        #
        if env[self.var.name]['scope'] is None:
            env[self.var.name]['scope'] = 'global' # set scope to 'global' => this means global value got initialized
        addr = env[self.var.name]['addr']
        return self.value.code_v(env) + getvec(self.var.name, env) + f"rewrite {addr}\n" #f'storeaddr {addr}\n'

@dataclass
class ITEExpression(CompiledExpression):
    condition: CompiledExpression # always gets evaluated using code_b
    ifbody: CompiledExpression      # code_b or code_v depending on call of ITEExpression
    elsebody: CompiledExpression    # code_b or code_v depending on call of ITEExpression

    def code_b(self, env):
        print(f"code_b: {self}")
        ite_label, then_label, else_label, end_label = nextlabel(self)

        ret  = f"{ite_label}:\n"
        ret += self.condition.code_b(env)
        ret += f"jumpz {else_label}\n"
        ret += f"{then_label}:\n"
        ret += self.ifbody.code_b(env)
        ret += f"jump {end_label}\n"
        ret += f"{else_label}:\n"
        ret += self.elsebody.code_b(env) if self.elsebody is not None else "loadc 0\n" # elsebody doesn't exist => load default 0
        ret += f"{end_label}:\n"
        return ret

    def code_v(self, env):
        print(f"code_v: {self}")
        ite_label, then_label, else_label, end_label = nextlabel(self)

        ret  = f"{ite_label}:\n"
        ret += self.condition.code_b(env)
        ret += f"jumpz {else_label}\n"
        ret += f"{then_label}:\n"
        ret += self.ifbody.code_v(env)
        ret += f"jump {end_label}\n"
        ret += f"{else_label}:\n"
        ret += self.elsebody.code_v(env) if self.elsebody is not None else "loadc 0\nmkbasic\n" # elsebody doesn't exist => load default 0
        ret += f"{end_label}:\n"
        return ret

@dataclass
class WhileExpression(CompiledExpression):
    condition: CompiledExpression
    body: CompiledExpression

    def code_b(self, env):
        print(f"code_b: {self}")
        while_label, do_label, end_label = nextlabel(self)
        # if condition fails at first check, must return default value 0
        # new iteration discards the old value
        ret  = "loadc 0\n"
        ret += f"{while_label}:\n"
        ret += self.condition.code_b(env)
        ret += f"jumpz {end_label}\n"
        ret += f"{do_label}:\n"
        ret += "pop 1\n" # discard value from last iteration
        ret += self.body.code_b(env)
        ret += f"jump {while_label}\n"
        ret += f"{end_label}:\n"
        return ret

    def code_v(self, env):
        print(f"code_v: {self}")
        while_label, do_label, end_label = nextlabel(self)
        # if condition fails at first check, must return default value 0
        # new iteration discards the old value
        ret  = "loadc 0\n"
        ret += f"{while_label}:\n"
        ret += self.condition.code_b(env)
        ret += f"jumpz {end_label}\n"
        ret += f"{do_label}:\n"
        ret += "pop 1\n" # discard value from last iteration
        ret += self.body.code_v(env)
        ret += f"jump {while_label}\n"
        ret += f"{end_label}:\n"
        return ret


@dataclass
class LoopExpression(CompiledExpression):
    # loop expression do expression
    # runs the loop until the loopvar is 0
    loopvar: CompiledExpression
    body: CompiledExpression

    def code_b(self, env):
        print(f"code_b: {self}")
        loop_label, do_label, end_label = nextlabel(self)

        ret = "loadc 0\n" # default value in case loop body doesnt get executed
        ret += self.loopvar.code_b(env)
        ret += f"{loop_label}:\n"
        ret += "dup\n"    # duplicate the loopvar because the jumpz later on will delete one
        ret += f"jumpz {end_label}\n"
        ret += "swap\n"   # swap 1. and 2. value on stack
        ret += "pop 1\n"  # remove old iteration value
        ret += f"{do_label}:\n"
        ret += self.body.code_b(env)    # push new iteration value
        ret += "swap\n" # swap, so that loopvar is on top of stack
        ret += "dec\n"  # decrement top value (loopvar) of stack
        ret += f"jump {do_label}\n"   # check loopvar if next iteration
        ret += f"{end_label}:\n"
        ret += "pop 1\n"  # final pop because loopvar is on top of stack
        return ret

    def code_v(self, env):
        print(f"code_v: {self}")
        loop_label, do_label, end_label = nextlabel(self)

        ret = "loadc 0\n" # default value in case loop body doesnt get executed
        ret += "mkbasic\n"
        ret += self.loopvar.code_b(env)
        ret += f"{loop_label}:\n"
        ret += "dup\n"    # duplicate the loopvar because the jumpz later on will delete one
        ret += f"jumpz {end_label}\n"
        ret += "swap\n"   # swap 1. and 2. value on stack
        ret += "pop 1\n"  # remove old iteration value
        ret += f"{do_label}:\n"
        ret += self.body.code_v(env)    # push new iteration value
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

    def code_v(self, env):
        # local variables only get created in let block, nowhere else
        print(f"code_v: {self}")
        print(f"in local env: {env}")
        n = len(self.localvars)

        ret = ""

        """
            1. add each local variable to environment (set scope to 'local')
            2. evaluate each local variable expression
        this order is important to allow recursion
        """
        old_scopes = {} # old scopes of local variables, needed at end of local expression so a global variables that got shadowed gets 'global' scope again
        for var, val in self.localvars:
            # set scope to local, this is needed, e.g.
            #   local x in 1; <- after that env['x'] has scope None to avoid use out of scope
            #   local x in 2  <- needs to access a new x
            #
            #
            print(f"localvar: {var} = {val}")
            old_scopes[var] = env[var]['scope'] # save old scope of var
            # store those that have an old scope 'local' on stack, so they are not overwritten in inside local expression
            # and put them back into local vector after local expression
            # so the old value is preserved/restored after local expression
            if old_scopes[var] == 'local':
                ret += "# save old local values\n"
                ret += "pushlocalvec\n"
                ret += f"pushaddr {env[var]['addr']}\n"
            env[var]['scope'] = 'local' # set scope to 'local' => this means local value got initialized
        print(f"old_scopes: {old_scopes}")

        # No need to store the old local vector on stack, because local vector holds space for all local vars in whole program
        # + the one who are accessible are set to 'local' scope
        #ret += "pushlocalvec\n" # save old local vector on stack,
        # TODO: create a copy with new allocated objects of local var
        # so shadowing x inside 2 local expression works correctly
        # the code:
        #           local x:=2 in {
        #               local x:=3 in {
	#			x
	#		} + x
	#           }
        #   prints 6 instead of 5, because the value in local vector got overwritten
        #


        for var, value in self.localvars:
            # evaluate each local expression
            ret += f"{value.code_v(env)}"
            # writes the address at top of stack into local vector at index i => local var gets it's value assigned
            ret += "pushlocalvec\n"
            """
                Problem:
                    use rewrite: allows recursion, breaks restoring value after local got shadowed
                    use storeaddr: doesn't allow recursion, allows restoring value after local got shadowed

            """
            ret += f"# scope of {var}: {env[var]['scope']}\n"
            ret += f"rewrite {env[var]['addr']}\n" # must be rewrite so recursion works (uses dummy value in local/function global vector)
            #ret += f"storeaddr {env[var]['addr']}\n"
            ret += "pop 1\n" # only store value into locals vector, return value of storeaddr is not used/needed
            """
            Idea:
                - instead of storeaddr, do a rewrite at that addr
                - mkvec creates a vector with n values and fills it with dummy values ['D', 0]
                - assignment and here will rewrite instead of store, so recursion and changing global vars works
                - rewrite i needs stack to look like:   |  vector   |
                                                        | new value |
                  rewrite goes to index i in vector and changes the value from ['D', 0] to the 2 values of new value
            """
        # evaluate body
        ret += "# local body\n"
        ret += f"{self.body.code_v(env)}"
        # no need for slide because local vars are stored in r13 locals vector not on stack
        #ret += "swap\n" # swap return value with old local vector, so old local vector is on top of stack and can be restored next
        #ret += f"restorelocalvec\n" # resets to old local vector

        # set all scopes of used local variables to old scope
        # and store the original values (saved on stack) back into local vector, must do it in reverse to preserve order
        for var, val in reversed(self.localvars):
            # only reset scope if old scope is not None
            # so the program
            #       f := \() -> x:=5;
            #       f();
            #       x
            # defines the global variable x as valid/'global' correctly
            print(f"{var}: current scope {env[var]['scope']}, old scope {old_scopes[var]}")
            env[var]['scope'] = old_scopes[var]
            # stack after local expression looks like:
            #   | return value |
            #   |  old local 3 |
            #   |  old local 2 |
            #   |  old local 1 |
            if old_scopes[var] == 'local':
                ret += "# restore old local values\n"
                ret += "swap\n"
                ret += "pushlocalvec\n"
                ret += f"storeaddr {env[var]['addr']}\n"
                ret += "pop 1\n"
            #ret += "swap\n"
        return f"# Start of {self}\n" + ret + f"# End of {self}\n"


@dataclass
class CallExpression(CompiledExpression):
    # Caller
    # used for calling a function
    # so when e.g. f(1,2) is written
    # knows the name of caller, given parameters
    procname: CompiledExpression
    params: list[CompiledExpression]

    def code_v(self, env):
        print(f"code_v: {self}")
        call_return_label = nextlabel(self)

        n = len(self.params)
        ret = ""
        ret += f"mark {call_return_label}\n"
        # run code_v of each param, fill param vector
        for i in range(n):
            ret += f"{self.params[i].code_v(env)}"
            ret += "pushparamvec\n"
            ret += f"storeaddr {i}\n" # must be storeaddr instead of rewrite, so changing parameter value changes the value globally
            ret += "pop 1\n" # only store value into param vector so return value of storeaddr is not needed
        ret += f"{self.procname.code_v(env)}"
        ret += "apply\n"
        ret += f"{call_return_label}:\n"
        return ret


@dataclass
class LambdaExpression(CompiledExpression):
    # has a list of formal parameters, body
    params: list()      # may be empty
    body: CompiledExpression

    """
        Stack frame on entry:
        |   return value    |
        | Rücksprungadresse |
        |     old rbp       |
        | old global vector |

        Registers:
        r12: global vector
        r13: local vector
        r14: param vector
    """
    def code_v(self, env):
        print(f"code_v: {self}")
        lambda_label, end_lambda = nextlabel(self)

        # free variables = global variables | current params
        # get put into a new global vector, that is given to lambda

        freevars = sorted(free_vars(self)) # get free variables of lambda expression, sort them to avoid index issues
        print(f"> free_vars {freevars} in {self}")
        n = len(freevars)
        ret = ""
        outside_vars = [x for x in freevars if env[x]['scope'] is not None] # only variables that are already defined outside lambda
        print(f"> outside_vars {outside_vars}")
        # so outside_vars = free_vars - (global vars that are defined in lambda and not outside)

        """
            TODO: KeyError when a new global variable is defined inside lambda, that has not been named outside lambda before
                        f := \() -> {
                            x:=5
                        };
                        f()
                because x is considered a free variable inside lambda, but scope is None because not defined outside
        """

        """
            in LambdaExpression a rewrite must happen when global variables get new assigned
            something like:

        """


        # filling new global vector with all free vars must happen inside lambda because else the global vector outside lambda gets overwritten and
        # and code like
        #   y:=2
        #   f := \(x) -> x;
        #   1+y;
        #   f(56)
        # wouldn't work because lambda isn't immediately called after definition
        # => set new global vector only if jumped inside lambda
        #

        """
            Solution:
                - rewrite instead of storeaddr
                    => global variables can be modified inside lambda
                    => recursive lambdas work
                - rewrite pushes the address of changed object back to stack
        """

        # put all free vars in new gp for lambda in reverse, so order in vector is preserved
        # fill new global vector with values of all free variables and create new environment
        # add those to new environment
        env2 = {}
        for i,v in reversed(sorted(enumerate(freevars))):
            #push address of free variables into vector in reverse, so adding it to a vector is easier
            ret += f"### fill {i}, {v}\n"
            ret += f"{getvec(v, env)}"
            ret += f"pushaddr {env[v]['addr']}\n"
            #ret += f"pushaddr {lookup(env, v)['addr']}\n" # put address to value onto stack
            env2[v] = {'addr': i, 'scope': 'global', 'size': 8} # all free vars (global variables/params) become global now
        ret += f"mkvec {n}\n" # fills a new vector with n values on stack

        # add params to new environment
        for i,v in enumerate(self.params):
            env2[v] = {'addr': i, 'scope': 'param', 'size': 8}
        print(f"lambda env: {env2}")

        ret += f"mkfunval {lambda_label}\n" # creates function object ['F', ptr] -> [addr, newly filled global vector]
        ret += f"jump {end_lambda}\n"
        ret += f"{lambda_label}:\n"
        ret += f"{self.body.code_v(env2)}"
        ret += "popenv\n"
        ret += f"{end_lambda}:\n"
        #return f"# {self}\n# env: {env2}\n" + ret
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
# push address of variable onto stack
# TODO: change this to pushlocalvec, pushglobalvec, pushparamvec + push j
#def getvar(var, env):
#    match lookup(env, var):
#        case {'scope': 'local', 'addr': j, 'size': _}: return f"pushlocalvar {j}\n"     # j is index in local vector
#        case {'scope': 'global', 'addr': j, 'size': _}: return f"pushglobalvar {j}\n"   # j is index in global vector
#        case _: raise Exception(f"Variable {var} not defined in {env}")
# push address of vector where variable is in or will be in
def getvec(var, env):
    match lookup(env, var):
        case {'scope': 'local', 'addr': j, 'size': _}:  return f"pushlocalvec\n"
        case {'scope': 'global', 'addr': j, 'size': _}: return f"pushglobalvec\n"
        case {'scope': 'param', 'addr': j, 'size': _}:  return f"pushparamvec\n"
        case _: raise Exception(f"Variable {var} not defined in {env}") # scope None means variable is out of scope / hasn't been initialized yet => cannot use it

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
        case _:                                     raise Exception(f"free_vars({expr}) wrong")

# returns set of variables (local + global) that are defined in expr
# used because free_vars(expr) reports x in code
#   f := \() -> {
#       x:=5
#   };
#   f()
# as free variable even though it is bound to,defined in lambda
# so TODO: in lambda freevars = free_vars(body) - var_assigns(body)
# to correctly get only the variable defined outside lambda as free variables
def var_assigns(expr):
    match expr:
        case SelfEvaluatingExpression(x):           return set()
        case VariableExpression(x):                 return {x} # WARNING
        case BinaryOperatorExpression(e1, op, e2):  return var_assigns(e1) | var_assigns(e2)
        case SequenceExpression(seq):               return {x for el in seq for x in var_assigns(el)}
        case AssignmentExpression(var, val):        return var_assigns(var) | var_assigns(val)
        case ITEExpression(condition, ifbody, None): return var_assigns(condition) | var_assigns(ifbody)
        case ITEExpression(condition, ifbody, elsebody): return var_assigns(condition) | var_assigns(ifbody) | var_assigns(elsebody)
        case WhileExpression(condition, body):      return var_assigns(condition) | var_assigns(body)
        case LoopExpression(loopvar, body):         return var_assigns(loopvar) | var_assigns(body)
        case LocalExpression(localvars, body):      return var_assigns(body) + {x for x,e in localvars}  # WARNING
        case LambdaExpression(params, body):        return var_assigns(body) + {x for x in params}     # WARNING
        case CallExpression(name, params):          return var_assigns(name).union(*(var_assigns(p) for p in params))
        case _:                                     raise Exception(f"var_assigns({expr}) wrong")

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
        case _:                                     raise Exception(f"max_num_params({expr}) wrong")











