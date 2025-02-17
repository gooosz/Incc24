import re

# return an env containing all variables from env that have scope 'global'
def global_env(env):
    return {k: v for k,v in env.items() if v['scope'] == 'global'}

# return a sum of sums in env
def total_size(env):
    return sum([v['size'] for k,v in env.items()])

# return amount of global variables
def num_of_globalvars(env):
    assert 'parent' not in env  # env must be root environment
    return len(env.items()) # amount of variables

# set operation of different boolean comparisons
set_flags_op = {
        'le': 'setl',
        'gr': 'setg',
        'leq': 'setle',
        'geq': 'setge',
        'eq': 'sete',
        'neq': 'setne'
        }

# returns x86 asm instructions to allocate n Byte using malloc
# after calling, address to allocated memory is in rax
def malloc(n):
    code = f';;; malloc {n}\n'
    code += 'push    rdx\n'  # preserve rdx across malloc call because it will hold address of tuple after alloc_tuple() call
    code += f'mov    rdi, {8*int(n)}\n'
    code += 'call   malloc\n'
    code += 'pop    rdx\n'
    # rax now contains return value of malloc
    #code += 'mov    rdi, rax\n' # move malloc result into rdi to check if malloc failed
    #code += 'call   check_malloc_res\n'
    # hopefully malloc didn't fail, so fill in the values in newly allocated memory in heap
    return code


# returns x86 code to create a tuple of typ
# n is elements in vector
# after call rdx holds address of tuple, rax holds address to values, the values in [rax] needs to be filled!
def alloc_tuple(typ, n=0):
    ret = malloc(2) # for tuple
    ret += ';;; alloc_tuple\n'
    ret += 'mov    rdx, rax\n'
    #ret += 'push    rdx\n ; preserve rdx across malloc call\n'
    print(f"===== alloc_tuple({typ}, {n})" if typ == 'V' else f"===== alloc_tuple({typ})")
    match typ:
        case 'B':
            ret += "mov    qword [rdx], 'B'\n"
            ret += malloc(1)
            ret += 'mov    qword [rdx+8], rax\n'
        case 'F':
            ret += "mov    qword [rdx], 'F'\n"
            ret += malloc(2)
            ret += 'mov    qword [rdx+8], rax\n'
            ret += 'mov    qword [rax], 0\n'      # addr
            ret += 'mov    qword [rax+8], 0\n'    # gp
        case 'V':
            ret += "mov    qword [rdx], 'V'\n"
            ret += malloc(n+1)
            ret += 'mov    qword [rdx+8], rax\n'
            ret += f'mov    qword [rax], {n}\n'      # size of vector
            for i in range(n):
                # create dummy object
                ret += f'mov    qword [rax+{8*n}], 0\n'    # elements of vector
        case 'D':
            # Dummy object
            ret += "mov     qword [rdx], 'D'\n"
            ret += "mov     qword [rdx+8], 0\n"
        case 'S':
            # String object, n is size of string (without '\0' at end)
            # each cell of C-string only has size 1 Byte
            ret += "mov    qword [rdx], 'S'\n"
            #ret += malloc(n+1) # length of string + '\0'
            ret += 'push    rdx\n'  # preserve rdx across malloc call because it should hold address of tuple after call
            ret += f'mov    rdi, {int(n+1)}\n'
            ret += 'call   malloc\n'
            ret += 'pop    rdx\n'
            ret += 'mov    qword [rdx+8], rax\n'
        case _: raise NotImplementedError(f"No such type {typ} exists")
    return ret



def to_x86_64(cma_code, env) :
    code = ""
    for line in cma_code.splitlines() :
        instruction = re.split("[,\s]+",line)
        # possible label at front
        label, *rest = instruction
        # ignore comments starting with '#'
        if label.startswith("#"):
            continue
        match instruction:
            case ['pop', n] :
                code += f';;; === pop {n} ===\n'
                code += '\n'.join('pop  rax' for i in range(int(n))) + '\n'
            case ['loadc', q]:
                # push qword cannot whatsoever push 64bit values (large numbers) onto stack
                # however mov can put 64bit values into registers, use that as a workaround
                code += f';;; === loadc {q} ===\n'
                code += f'mov   rcx, qword {str(q)}\n'
                code += 'push   rcx\n'
            case ['add'] :
                code += 'pop    rcx\n'
                code += 'pop    rax\n'
                code += 'add    rax, rcx\n'
                code += 'push   rax\n'
            case ['sub'] :
                code += 'pop    rcx\n'
                code += 'pop    rax\n'
                code += 'sub    rax, rcx\n'
                code += 'push   rax\n'
            case ['mul'] :
                code += 'pop    rcx\n'
                code += 'pop    rax\n'
                code += 'mul    rcx\n'
                code += 'push   rax\n'
            case ['div'] :
                code += 'pop    rcx\n'
                code += 'pop    rax\n'
                code += 'xor    rdx, rdx    ; dividend is in rdx:rax, so zero out rdx before division (or else floating point exception might occur)\n'
                code += 'div    rcx\n'
                code += 'push   rax\n'
            case ['neg']:
                code += 'pop    rax\n'
                code += 'neg    rax\n'
                code += 'push   rax\n'
            case ['le' | 'gr' | 'leq' | 'geq' | 'eq' | 'neq'] :
                code += 'pop    rcx\n'
                code += 'pop    rax\n'
                code += 'cmp    rax, rcx\n'
                code += f'{set_flags_op[instruction[0]]}   al\n'
                code += 'movzx  rax, al     ; store result of compare in rax\n'
                code += 'push   rax\n'
            case ['jump', label]:
                code += f';;; === jump  {label} ===\n'
                code += f'jmp  {label}\n'
            case ['jumpz', label]:
                code += f';;; === jumpz  {label} ===\n'
                code += 'pop    rax        ; delete result of compare operation\n'
                code += f'cmp   rax, 0\n'
                code += f'je {label}\n'
            case ['mkbasic']:
                # Wert liegt im Stack
                # mkbasic nimmt den Wert und erstellt Tupel ['B', ptr] und ptr->[value] im Heap
                # und pushed Adresse zu Tupel auf Stack
                code += ';;; === mkbasic ===\n'
                code += alloc_tuple('B')  # basic tuple on heap ['B', ptr] both cells are 8 byte
                code += 'pop    qword [rax]\n' # value to store
                code += 'push   rdx\n'  # address to tuple ['B', ptr] on heap
            case ['getbasic']:
                # Adresse zu Tupel liegt auf Stack
                # getbasic nimmt Adresse vom Stack
                # pushed Wert vom Tupel an der Adresse auf Stack
                code += ';;; === getbasic ===\n'
                #code += 'pop    rax\n'
                #code += ''  # check if basic type
                #code += 'mov    rcx, [rax+8]\n'   # get value from heap
                #code += 'lea    rax, [rip]\n' # save Rücksprungadresse (without label) on stack
                #code += 'push   rax\n'
                code += "pop    rdi\n" # address to object
                code += "call   getbasic\n" # returns getbasic value in rax
                code += "push   rax\n"
                #code += 'push   qword [rcx]\n'
            case ['dup']:
                # duplicate the value on top of stack
                code += ';;; === dup ===\n'
                code += 'pop    rax\n'
                code += 'push   rax\n'
                code += 'push   rax\n'
            case ['swap']:
                # swap first to values on top of stack
                code += ';;; === swap ===\n'
                code += 'pop    rax\n'
                code += 'pop    rdx\n'
                code += 'push   rax\n'
                code += 'push   rdx\n'
            case ['dec']:
                # decrement value on top of stack
                code += ';;; === dec ===\n'
                code += 'pop    rax\n'
                code += 'dec    rax\n'
                code += 'push   rax\n'
            case ['mkvec', n]:
                # create a vector with n elements that are stored on stack
                # stack got pushed like this:
                #   |    free var 1     |
                #   |    free var 2     |
                #   |    free var 3     |
                code += f';;; === mkvec {n} ===\n'
                code += alloc_tuple('V', int(n)) # rdx holds address of vector, rax holds address to values in vector
                for i in range(int(n)):
                    code += f'pop   qword [rax+{8+8*i}]\n'
                    #code += f'mov    qword [rax+{8+8*i}], 0\n'
                    #code += alloc_tuple('D') # rdx now holds address of new tuple
                    #code += f'mov   qword [rax+{8+8*i}], rdx\n'
                code += 'push   rdx\n'
            case ['setgv']:
                # set address on top of stack as new global vector (r12)
                code += ';;; === setgv ===\n'
                code += 'pop    r12\n'
            case ['setlv']:
                # set address on top of stack as new local vector (r13)
                code += ';;; === setlv ===\n'
                code += 'pop    r13\n'
            case ['setpv']:
                # set address on top of stack as new param vector (r14)
                code += ';;; === setpv ===\n'
                code += 'pop    r14\n'
            case ['pushglobalvec']:
                # pushes address of global vector (r12) onto stack
                code += ';;; === pushglobalvec ===\n'
                code += 'push   r12\n'
            case ['pushlocalvec']:
                # pushes address of local vector (r13) onto stack
                code += ';;; === pushlocalvec ===\n'
                code += 'push   r13\n'
            case ['pushparamvec']:
                # pushes address of param vector (r14) onto stack
                code += ';;; === pushparamvec ===\n'
                code += 'push   r14\n'
            case ['restorelocalvec']:
                # restores address of local vector from top of stack into r13
                code += ';;; === restorelocalvec ===\n'
                code += 'pop   r13\n'
            case ['pushlocal', j]:
                code += f';;; === pushlocal {j} ===\n'
                code += f'push    qword [rsp + {8*int(j)}]\n'
            case ['pushaddr', j]:
                # on stack is address of vector, push address at index j in that vector onto stack
                #   | address of vector |
                # vector is:
                # ['V', ptr] -> [n, 0, 1, ...]
                code += f';;; === pushaddr {j} ===\n'
                code += 'pop    rax\n'
                code += 'mov    qword rdx, [rax+8]\n'
                code += f'push   qword [rdx+{8+8*int(j)}]\n' # 8 offset in vec because first element is size of vec
            case ['pushaddr']:
                # on stack is address of vector, index j
                # push address at index j in that vector onto stack
                #   |       j           |
                #   | address of vector |
                # vector is:
                # ['V', ptr] -> [n, 0, 1, ...]
                code += f';;; === pushaddr ===\n'
                code += 'pop    rcx\n' # index
                code += 'pop    rax\n'
                code += 'mov    qword rdx, [rax+8]\n'
                code += 'push   rdx\n' # mul will overwrite rdx value, so save it to restore after
                code += 'mov    rax, 8\n' # multiply index by 8 because 64bit values
                code += 'mul    rcx\n'    # rax = 8 * index
                code += 'add    rax, 8\n' # add 8 offset because first element is size of vec
                code += 'pop    rdx\n' # restore previous rdx value
                code += 'add    rdx, rax\n' # rdx holds memory address to access the vector at index
                code += f'push   qword [rdx]\n'
            case ['storeaddr', j]:
                # on stack is:
                #   | address of vector       |
                #   | address to new variable |
                # store address of variable at index j in that vector and put address of variable onto stack again
                # should storeaddr put the address back on stack? => Yes because simple assignment returns the value back
                code += f';;; === storeaddr {j} ===\n'
                code += 'pop    rax\n' # rax holds address to vector
                code += 'mov    qword rdx, [rax+8]\n'
                code += f'pop   qword [rdx+{8+8*int(j)}]\n' # put address of variable at index j in vector
                code += f'push  qword [rdx+{8+8*int(j)}]\n' # put address of variable back onto stack
            case ['alloc', n]:
                # creates n dummy tuple values and stores them on stack
                code += f';;; === alloc {n} ===\n'
                for i in range(int(n)):
                    code += alloc_tuple('D') # rdx holds address of object
                    code += 'push   rdx\n'
            case ['rewriteloc', j]:
                # rewrites the local value with addr j with the values from object on top of stack
                #   | new value |
                #   |   ...     | ↓j
                #   | old value |
                code += f';;; === rewriteloc {j} ===\n'
                code += f'mov    qword rdx, [rsp+{8*int(j)}]\n' # holds old dummy values
                code += 'pop    rax\n' # holds new values
                # type
                code += "mov    qword rcx, [rax]\n" # indirection, because nasm can't do double dereference mov [rdx], [rax]
                code += "mov    qword [rdx], rcx\n"
                # ptr to object values
                code += "mov    qword rcx, [rax+8]\n" # indirection, because nasm can't do double dereference mov [rdx+8], [rax+8]
                code += "mov    qword [rdx+8], rcx\n"
                code += "push   rdx\n" # push changed object onto stack again
            case ['rewriteinvec', j]:
                # overwrites the values in i-th object in vector with new values
                # stack looks like:
                #   |  vector   |
                #   | new value |
                code += f';;; === rewriteinvec {j} ===\n'
                code += 'pop    rax\n'
                code += 'mov    qword rdx, [rax+8]\n' # values of vector are at rdx
                code += 'pop    rcx\n' # new values [' ', ptr]
                code += f'mov    qword rax, [rdx + {8+8*int(j)}]\n' # rax holds old values [' ', ptr]
                # type of object
                code += "mov    qword rdx, [rcx]\n" # indirection, because nasm can't do double dereference mov [rax], [rcx]
                code += "mov    qword [rax], rdx\n"
                # ptr to object values
                code += "mov    qword rdx, [rcx+8]\n" # indirection, because nasm can't do double dereference mov [rax], [rcx]
                code += "mov    qword [rax+8], rdx\n"
                code += "push   rax\n" # push address of changed object back to stack
            case ['rewrite']:
                # overwrites the values old object in with new values
                # stack looks like:
                #   | new value |
                #   | old value |
                code += f';;; === rewrite ===\n'
                code += 'pop    rax\n' # new values
                code += 'pop    rdx\n' # old values [type, ptr]
                # type of object
                code += "mov    qword rcx, [rax]\n" # indirection, because nasm can't do double dereference mov [rdx], [rax]
                code += "mov    qword [rdx], rcx\n"
                # ptr to object values
                code += "mov    qword rcx, [rax+8]\n" # indirection, because nasm can't do double dereference mov [rdx+8], [rax+8]
                code += "mov    qword [rdx+8], rcx\n"
                code += "push   rdx\n" # push address of changed object back to stack
            case ['slide', j]:
                # remove j values under the top value of stack
                code += f';;; === slide {j} ===\n'
                code += 'pop    rax\n' # keep the top value
                code += f'add    rsp, {8*int(j)}\n'
                code += 'push   rax\n'
            case ['mkfunval', addr]:
                # create a function object ['F', addr, gp]
                # global pointer is on stack
                code += f';;; === mkfunval {addr} ===\n'
                code += alloc_tuple('F') # rdx holds address to function object ['F', ptr], rax holds address to [addr, gp]
                code += f'mov    qword [rax], {addr}\n'
                code += 'pop    qword [rax+8]\n'
                code += 'push   rdx\n' # put address to funcion object onto stack
            case ['popenv']:
                # restore param, local, global vectors
                # restore old stack pointer
                # go to Rücksprungadresse
                # Stack frame:
                #   |   return value      |
                #   | Rücksprungadresse/A | <- new rbp
                #   |      old rbp        |
                #   | old global vector   |
                code += ';;; === popenv ===\n'
                code += 'pop    rax\n' # return value save for later
                code += 'pop    rcx\n' # Rücksprungadresse
                code += 'pop    rbp\n' # restore old frame pointer
                code += 'pop    r14\n' # restore old param vector
                code += 'pop    r12\n' # restore old global vector
                code += 'push   rax\n' # put return value onto stack again
                code += 'jmp    rcx\n'  # return to Rücksprungadresse
            case ['mark', A]:
                # save rbp, global, param vectors
                # Stack frame:
                #   |   return value      |
                #   | Rücksprungadresse/A | <- new rbp
                #   |      old rbp        |
                #   |  old param vector   |
                #   | old global vector   |
                code += f';;; === mark {A} ===\n'
                code += 'push   r12\n'
                code += 'push   r14\n'
                code += 'push   rbp\n'
                code += f'push   {A}\n'
                code += 'mov    rbp, rsp\n'
            case ['apply']:
                # call the function object [addr, gp] on stack
                code += f';;; === apply ===\n'
                code += 'pop    rdx\n'  # address of function object
                code += 'mov    qword rcx, [rdx+8]\n' # address of function object values
                code += 'mov    qword r12, [rcx+8]\n' # set new global vector
                code += 'mov    qword rax, [rcx]\n' # addr of function body
                code += 'jmp    rax\n'  # go into function
            case ['mkstr', *q]:
                # string, but q is a list because whitespaces got split by regex
                s = ' '.join(str(x) for x in q) # create a correct whitespace str, so undo the regex haha
                #s = q[1:-1] # ignore leading, trailing "
                n = len(s)
                code += f';;; === mkstr {s} ===\n'
                code += alloc_tuple('S', n) # rdx holds address of tuple, rax holds address of values
                # add characters of string to each cell of string object
                #count_escaped = 0 # count escaped because this decreases n
                for i in range(n):
                #for i,c in enumerate(s):
                    #if c.isdigit():
                    #    # must add '0' to char value so the correct ascii value is placed in string
                    #    code += f'mov   rcx, {c}\n'
                    #    code += "add    rcx, '0'\n"
                    #    code += f'mov    qword [rax+{i}], rcx\n'
                    #else:
                        # simply add the char
                        # character needs to be escaped if \n e.g.
                    # skip if value was escaped
                    if i>0 and (s[i-1] == '\\' or s[i-1] == '%'):
                        print(f"s[{i}]={s[i]} got escaped")
                        #count_escaped += 1
                        continue
                    c = s[i]
                    if (s[i] == '\\' or s[i] == '%') and i+1<len(s):
                        c = s[i:i+2] # escaped value, e.g. \n, is 2 bytes big
                        code += f"mov    word [rax+{i}], '{c}'" + '\n'
                    else:
                        #c = s[i] if s[i] != r'\\' else s[i:i+1]
                        code += f"mov    byte [rax+{i}], '{c}'" + '\n'
                    print(f"c = {c}")
                #code += f"mov    qword [rax+{n}], '\\0'\n" # add '\0' to string
                code += fr"mov    byte [rax+{n}], 0" + '\n' # add '\0' to string
                code += 'push   rdx\n'
            case ['getstr']:
                # returns pointer to first cell of string object values
                # on stack is address of object
                code += f';;; === getstr ===\n'
                code += 'pop    rax\n'
                code += 'push   qword [rax+8]\n'
            case ['filllibcparams', n]:
                # fills registers with values from stack according to libc standard
                # stack looks like
                #   |    n    |
                #   | param 1 |
                #   |   ...   |
                #   | param n |
                code += ';;; === filllibcparams ===\n'
                code += 'call fill_libc_params\n'
                code += 'add    rsp, 8\n' # discard n
                # discard the params on stack that are moved to the registers for call (<= 6)
                if int(n)<=6:
                    code += f'add   rsp, {8*int(n)}\n'
                else:
                    code += f'add   rsp, {8*6}\n'
                # TODO: code += f'add    rsp, {8+ 8*(int(n) if int(n)<=6 else 6)}\n' # discard n + params on stack that are moved to the registers for call
            case ['call', func]:
                code += f';;; === call {func} ===\n'
                code += "mov    rax,0               ; no xmm registers used\n"
                code += "push   rbp                 ; set up stack frame, must be aligned\n"
                code += f"call   {func}             ; Call LibC function\n"
                code += "pop    rbp                 ; restore stack\n"
                code += 'push   rax\n' # push return value onto stack
            case [*unknown]:
                label, *unknown = unknown
                label_match = re.search(r'\w+(?=:)', label)
                if label_match is not None :
                    code += f'{label_match.group(0)}:\n'  # create label
                else:
                    raise NotImplementedError(f"statement {instruction}")
                    code += f'Error: unknown IMa statement {unknown}\n'
    return format_code(code)


# getbasic must decide what to output
# basic type: value of first object value cell
# string type: pointer to first object value cell (so returns a C-string)
# @param rdi has address of object
# @returns rax the basic value
def getbasic_function():
    code = 'getbasic:\n'
    code += 'push   rbp\n' # save old rbp
    code += 'mov    rbp, rsp\n' # setup new stack frame

    #code += 'pop    rcx\n' # Rücksprungadresse
    code += 'mov    rax, rdi\n' # address of object
    # check type of object
    code += "mov    qword rdx, [rax]\n"
    code += "cmp    rdx, 'B'\n"
    code += "je     getbasic_basic\n"
    code += "cmp    rdx, 'S'\n"
    code += "je     getbasic_string\n"
    # ========================================
    # if not a type of anything asked, it will default to printing as if object would be basic type
    code += "getbasic_basic:\n"
    code += 'mov    rdx, [rax+8]\n'   # get value from heap
    code += 'mov    qword rax, [rdx]\n'
    code += "jmp    finished_getbasic\n"
    # ========================================
    code += "getbasic_string:\n"
    code += "mov    rdx, [rax+8]      ; rdx holds ptr to C-string\n"
    code += "mov    rax, rdx\n"
    code += "jmp    finished_getbasic\n"
    # ========================================
    code += "finished_getbasic:\n"
    code += "mov    rsp, rbp\n"
    code += "pop    rbp\n" # restore old stack frame
    code += "ret\n"
    return code

def fill_libc_params_function():
    # fills registers with values from stack according to calling convention
    # when fill_libc_params is called, the stack looks like:
    #   | Rücksprungadresse |
    #   |    n    |
    #   | param 1 |
    #   |   ...   |
    #   | param n |

    """
            Params:
                1. rdi
                2. rsi
                3. rdx
                4. rcx
                5. r8
                6. r9
                all others get pushed on stack in reverse order:
                |  7. |
                | ... |
        """
    code = 'fill_libc_params:\n'
    #code += 'mov    qword rcx, [rsp+8]\n'
    code += 'push   rbp\n' # save old rbp
    code += 'mov    rbp, rsp\n' # setup new stack frame
    # Stack now looks like:
    #   |     old rbp       |
    #   | Rücksprungadresse |
    #   |        n          |
    #   |     param 1       |
    #   |       ...         |
    #   |     param n       |
    code += f'mov    qword r10, [rsp+{16+8*0}]\n' # number of parameters given to printf
    # check number of params
    code += 'cmp    r10, 0\n'
    code += 'je     filled_params\n'
    code += f'mov    qword rdi, [rsp+{16+8*1}]\n'
    code += 'cmp    r10, 1\n'
    code += 'je     filled_params\n'
    code += f'mov    qword rsi, [rsp+{16+8*2}]\n'
    code += 'cmp    r10, 2\n'
    code += 'je     filled_params\n'
    code += f'mov    qword rdx, [rsp+{16+8*3}]\n'
    code += 'cmp    r10, 3\n'
    code += 'je     filled_params\n'
    code += f'mov    qword rcx, [rsp+{16+8*4}]\n'
    code += 'cmp    r10, 4\n'
    code += 'je     filled_params\n'
    code += f'mov    qword r8, [rsp+{16+8*5}]\n'
    code += 'cmp    r10, 5\n'
    code += 'je     filled_params\n'
    code += f'mov    qword r9, [rsp+{16+8*6}]\n'
    code += 'jmp    filled_params\n'
    # ========================================
    code += 'filled_params:\n'
    code += "mov    rsp, rbp\n"
    code += "pop    rbp\n" # restore old stack frame
    code += "ret\n"
    return code



def x86_program(x86_code, env) :
    program  = x86_prefix(env)
    program += x86_start(env)
    program += "\n;;; Start des eigentlichen Programms\n"
    program += "program_start:\n"
    program += x86_code
    program += ";;; Ende des eigentlichen Programms\n\n"
    program += "program_end:\n"
    program += x86_final(env)
    return format_code(program)

def x86_prefix(env):
    program  = "extern  printf\n"
    program += "extern  malloc\n"
    program += "SECTION .data               ; Data section, initialized variables\n"
    program += 'basic_type_fmt:  db  10, "%lld", 10, 0 ; printf format for printing an int64\n'
    program += 'string_type_fmt:  db  "%s", 10, 0 ; printf format for printing a string\n'
    program += 'malloc_errormsg:  db "Error: malloc failed, 10, 0"\n'
    program += '''; macros

    '''
    return program

def x86_start(env):
    program  = "\n"
    program += "SECTION  .text\nglobal main\n"
    program += "\n"
    program += getbasic_function()
    program += "\n"
    program += fill_libc_params_function()
    program += "\n"
    program += "main:\n"
    program += "  push  rbp                 ; unnötig, weil es den Wert 1 enthält, trotzem notwendig, weil sonst segfault\n"              
    program += "  mov   rax,rsp             ; rsp zeigt auf den geretteten rbp  \n"          
    program += "  sub   rax,qword 8         ; neuer rbp sollte ein wort darüber liegen\n"      
    program += "  mov   rbp,rax             ; set frame pointer to current (empty) stack pointer\n"          
    return program

def x86_final(env):
    program  = "  pop   rax\n" # rax holds value to print
    # TODO: in main run program.code_v so return value is a pointer
    #       this way we can check here if the object to print is 'B', 'F', 'V'
    #       and print the return value of program in different ways
    program += "  mov    rsi, rax\n"
    program += "  mov    rdi, basic_type_fmt ; arguments in rdi, rsi\n"
    program += "  mov    rax,0               ; no xmm registers used\n"
    program += "printf_call: \n"
    program += "  push  rbp                 ; set up stack frame, must be aligned\n"
    program += "  call  printf              ; Call C function\n"
    program += "  pop   rbp                 ; restore stack\n"
    program += "\n;;; Rueckkehr zum aufrufenden Kontext\n"
    program += "  pop   rbp                 ; original rbp is last thing on the stack\n"
    program += "  mov   rax,0               ; return 0\n"
    program += "  ret\n"
    """
    program += 'check_malloc_res:   ;;; prints error message in case malloc failed\n'
    program += 'cmp     rdi, 0\n'  # check if malloc failed
    program += 'jne     malloc_success\n'
    program += 'mov     rdi, malloc_errormsg\n'
    program += "mov     rax,0               ; no xmm registers used\n"
    program += "push    rbp                 ; set up stack frame, must be aligned\n"
    program += "call    printf              ; Call C function\n"
    program += "pop     rbp                 ; restore stack\n"
    program += 'malloc_success:\n'
    program += 'ret\n'
    """
    return program

def format_line(line) :
    tab_width=8
    l = ""
    if ':' in line :
        x = re.split(":",line,1)
        l +=f'{x[0]+": ":<{tab_width}}'
        line = x[1]
    else :
        l += tab_width*' '

    if line.startswith(";;;") :
        return l+line+'\n'

    comment = None
    if ";" in line :
        x = re.split(";",line.strip(),1)
        comment = x[1]
        line = x[0]
    
    x=re.split("[\s]+", line.strip(),1)
    l+=f'{x[0]:<{tab_width}}'

    if len(x)>1 :
        line = x[1]
        x=re.split(",", line.strip())
        for y in x[:-1]:
            l += f'{y.strip()+",":<{tab_width}}'
        l += f'{x[-1].strip():<{tab_width}}'
    if comment :
        l=f'{l:<40}'+";"+comment

    return l+'\n'

def format_code(c) :
    return "".join([format_line(l) for l in c.splitlines()])

