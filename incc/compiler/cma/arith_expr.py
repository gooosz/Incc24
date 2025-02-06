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
    def code(self, env):
        return self.code_r(env) + 'pop' + '\n'
    def code_l(self, env):
        raise Exception("code_l uninplemented")
    def code_r(self, env):
        raise Exception("code_r uninplemented")

@dataclass
class ProgramExpression(CompiledExpression) :
    e: CompiledExpression

    def code_r(self, env):
        return self.e.code_r(env)

@dataclass
class SelfEvaluatingExpression(CompiledExpression):
    id : CompiledExpression
    
    def code_r(self,env):
        return f'loadc {self.id}' + '\n'

@dataclass
class BinaryOperatorExpression(CompiledExpression):
    e1: CompiledExpression
    op: str
    e2: CompiledExpression

    def code_r(self,env):
        return self.e1.code_r(env) + self.e2.code_r(env) + operators[self.op]+ '\n'

@dataclass
class VariableExpression(CompiledExpression):
    name: str
    def code_l(self, env):
        # read from dict env[name] the value from ['addr']
        # env is dict of dicts and contains all global variables
        # loads the address of the variable onto stack
        var_scope = lookup(env, self.name)['scope'] # check in environmen if variable is global or local
        if var_scope == 'global':
            return f"loadc {lookup(env, self.name)['addr']}" + '\n'
        else:
            # local variable
            return f"loadrc {lookup(env, self.name)['addr']}" + '\n'
    
    def code_r(self, env):
        # pushes the value of the variable onto stack
        return self.code_l(env) + f"load\n"

@dataclass
class AssignmentExpression(CompiledExpression):
    # var = val
    var: CompiledExpression
    val: CompiledExpression

    # hat kein code weil es nur ein assignment ist, z.B. x := 3+4
    # hat kein code_l weil man einem assignment nichts zuweisen kann

    def code_r(self, env):
        if self.var.name not in env:
            # variable is not stored yet, so get a new address for it
            env[self.var.name] = {'addr': new_addr(size=8), 'scope': 'global', 'size': 8}
        # evaluate stack, get address of variable name, do store
        # so Stack will look like this:
        #   ------------------
        #    variable address
        #   ------------------
        #         value
        #   ------------------
        # C-Maschine looks like:
        #   loadc address
        #   loadc value
        #   store

        # x:=3 => VariableExpression(x), SelfEvaluatingExpression(3)
        #print(f"Assignment: var = {self.var}, val = {self.val}")
        return self.val.code_r(env) + self.var.code_l(env) + 'store\n'
        
            

@dataclass
class SequenceExpression(CompiledExpression):
    s: list()   # of CompiledExpressions

    def code_r(self, env):
        ret = ""
        # every CompiledExpression except the last one will call code to evaluate because the return value is discarded by ;
        # last expression keeps return value on stack
        for l in self.s[:-1] :
            ret += l.code(env)
        ret += self.s[-1].code_r(env)
        return ret

ite_count = 0 # used to differentiate labels in asm
@dataclass
class ITEExpression(CompiledExpression):
    # if then else
    # if without else has None as else body
    condition: CompiledExpression
    ifbody: CompiledExpression
    elsebody: CompiledExpression
    """
        condition
        jumpz else
        if:
            ifbody
        jump endif
        else:
            elsebody
        endif: 
    """
    def code_r(self, env):
        global ite_count
        # must do it like this or else nested ifs would use the same labels
        current_ite_count = ite_count
        ite_count += 1
        ret = f"ite_{current_ite_count}:\n"
        ret += self.condition.code_r(env)
        ret += f"jumpz else_{current_ite_count}\n"
        # -- if body --
        ret += f"then_{current_ite_count}:\n"
        ret += self.ifbody.code_r(env)
        ret += f"jump endif_{current_ite_count}\n"
        # Achtung: wenn elsebody is None muss trotzdem default 0 zurückgegeben werden, weil Wert erwartet wird
        ret += f"else_{current_ite_count}:\n"
        if self.elsebody is None:
            ret += "loadc 0\n"
        else:
            ret += self.elsebody.code_r(env)
        ret += f"endif_{current_ite_count}:\n"
        
        return ret 

@dataclass
class WhileExpression(CompiledExpression):
    # while (condition) { body }
    condition: CompiledExpression
    body: CompiledExpression

    def code_r(self, env):
        global ite_count
        """     while (condition) { body }
         * is same as
         *      if (condition) { body; jump if }
        """
        ret = "loadc 0\n"    # default value in case the while loop doesnt get executed => a value has to be returned
        ret += f"ite_{ite_count}:\n"
        ret += self.condition.code_r(env)
        ret += f"jumpz endif_{ite_count}\n"
        # -- if body --
        ret += "pop\n"  # new iteration, so old iteration return value is irrelevant
        ret += f"then_{ite_count}:\n"
        ret += self.body.code_r(env)
        ret += f"jump ite_{ite_count}\n"
        ret += f"endif_{ite_count}:\n"

        ite_count += 1  # used to differentiate if labels when debugging
        return ret

@dataclass
class LoopExpression(CompiledExpression):
    # loop expression do expression
    # runs the loop until the loopvar is 0
    loopvar: CompiledExpression
    body: CompiledExpression

    def code_r(self, env):
        global ite_count
        ret = "loadc 0\n" # default value in case loop body doesnt get executed
        ret += self.loopvar.code_r(env)
        ret += f"loop_{ite_count}:\n"
        ret += "dup\n"    # duplicate the loopvar because the jumpz later on will delete one
        ret += f"jumpz end_loop_{ite_count}\n"
        ret += "swap\n"   # swap 1. and 2. value on stack
        ret += "pop\n"  # remove old iteration value
        ret += f"do_{ite_count}:\n"
        ret += self.body.code_r(env)    # push new iteration value
        ret += "swap\n" # swap, so that loopvar is on top of stack
        ret += "dec\n"  # decrement top value (loopvar) of stack
        ret += f"jump loop_{ite_count}\n"   # check loopvar if next iteration
        ret += f"end_loop_{ite_count}:\n"
        ret += "pop\n"  # final pop because loopvar is on top of stack

        ite_count += 1
        return ret


@dataclass
class CallExpression(CompiledExpression):
    # Caller
    # used for calling a procedure
    # so when e.g. f(1,2) is written
    # knows the name of caller, given parameters
    procname: CompiledExpression
    params: list()

    def code_r(self, env):
        """
        Step into procedure:
            Caller:
            1.  push all formal parameters reversed (last to first) onto stack
            2.  push Rücksprungadresse rbp
            3.  push address von procedure (loadc)
            4.  load address of procedure (load)     -> address of procedure is stored in stack at position rbx-rbp
            5.  call procedure

        Return from procedure:
            Caller:
            11. pop Rücksprungadresse from stack
            12. remove the parameters from stack via slide(n,8)
        => result of procedure is on top of stack and back to old stack frame
        """
        ret = ""
        # ====== 1. ======
        if not self.params:
            # no params given, add default 0 for return value
            self.params.append(0)
        for param in reversed(self.params):
            ret += param.code_r(env)    # params are expressions
        # ====== 2. ======
        ret += "mark\n"
        # ====== 3,4. ======
        ret += self.procname.code_r(env)
        # ====== 5. ======
        ret += "call\n"

        # ====== 11. ======
        ret += "pop\n"
        # ====== 12. ======
        ret += f"slide {(len(self.params)-1) * 8} 8\n" # preserve the first parameter and delete all other params
        return ret

proc_count = 0
@dataclass
class ProcExpression(CompiledExpression):
    # has a list of formal parameters, a list of local variables, body
    params: list()      # may be empty, Achtung: address of first parameter will contain the result afterwards, so if empty list, add default 0 to list
    localvars: list()   # may be empty
    body: CompiledExpression

    def code_r(self, env):
        global proc_count
        # must be incremented before any code generation
        # because else nested procedures would use the same proc_count value
        # and the value would get incremented by nested procedure
        # so that the endproc label has a wrong number
        current_proc_count = proc_count
        proc_count += 1

        """
        Step into procedure:
            Callee:
            6.  enter procedure, setzt rbp = rbx-rsp also offset von aktueller Stack Position (rsp) zu Stack Beginn (rbx)
            7.  reserve/alloc space on stack for local variables     -> relative to rbx-rbp, so relative address is at position 8*(1+i) = S[FP+j] = rbx-(rbp+j)
            8.  call code_r of procedure body

        Return from procedure:
            Callee:
            9.  put result into first parameter value, so loadrc 8*2 (2 cells down from rbx-rbp) + store, then pop result from stack
            10. ret, so remove local variables, rbx-rbp from stack
        => result of procedure is on top of stack and back to old stack frame
        """
        # Callee

        # ====== 6. ======
        ret = f"jump endproc_{current_proc_count}\n" # jump over procedure (as it is not used directly)
        ret += f"proc_{current_proc_count}:\n"
        ret += "enter\n"
        # ====== 7. ======
        env_proc = {}
        offset = -16    # rücksprungaddresse, gesicherter frame pointer liegt drunter deshalb -16
        for param in self.params:
            env_proc[param] = {'addr': offset, 'scope': 'local', 'size': 8}
            offset -= 8
        offset = 8
        for local in self.localvars:
            env_proc[local] = {'addr': offset, 'scope': 'local', 'size': 8}
            offset += 8
        env_proc['parent_env'] = env
        ret += f"alloc {len(self.localvars)*8}\n"
        # ====== 8. ======
        ret += self.body.code_r(env_proc)

        # ====== 9. ======
        ret += "loadrc -16\n"  # -16, so 2 cells below rbx-rbp is first parameter
        ret += "store\n"
        ret += "pop\n"  # pop result because now stored in first parameter
        # ====== 10. ======
        ret += "return\n"  # removes local variables, Rücksprungadresse by decrementing rsp by rsp-(rbx-rbp)+1
        ret += f"endproc_{current_proc_count}:\n"
        ret += f"loadc proc_{current_proc_count}\n" #load address of this procedure (line nr at proc label) onto stack

        return ret

# returns relative address of a new global variable 
global_addr = 0
def new_addr(size=8):
    global global_addr
    address = global_addr
    global_addr += size
    return address

# returns entry of variable in env or local env if exists
def lookup(env, name):
    if name in env:
        return env[name]
    if 'parent_env' in env:
        # parent_env should be root env because else nested procedures might access each others variables
        root_env = env['parent_env']
        while 'parent_env' in root_env:
            root_env = root_env['parent_env']
        return lookup(root_env, name)  # parent might have parent aswell
    # this case should not happen
    raise KeyError(f"No known variable named {name} in env {env}")






