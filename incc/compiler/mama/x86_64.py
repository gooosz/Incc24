import re

# return an env containing all variables from env that have scope 'global'
def global_env(env):
    return {k: v for k,v in env.items() if v['scope'] == 'global'}

# return a sum of sums in env
def total_size(env):
    return sum([v['size'] for k,v in env.items()])

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
    code = f'mov    rdi, {8*int(n)}\n'
    code += 'call   malloc\n'
    # rax now contains return value of malloc
    #code += 'mov    rdi, rax\n' # move malloc result into rdi to check if malloc failed
    #code += 'call   check_malloc_res\n'
    # hopefully malloc didn't fail, so fill in the values in newly allocated memory in heap
    return code

def to_x86_64(cma_code, env) :
    code = ""
    for line in cma_code.splitlines() :
        instruction = re.split("[,\s]+",line)
        # possible label at front
        label, *rest = instruction
        match instruction:
            case ['pop'] :
                code += ';;; === pop ===\n'
                code +=  'pop   rax\n'
            case ['loadc', q] :
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
            case ['le' | 'gr' | 'leq' | 'geq' | 'eq' | 'neq'] :
                code += 'pop    rcx\n'
                code += 'pop    rax\n'
                code += 'cmp    rax, rcx\n'
                code += f'{set_flags_op[instruction[0]]}   al\n'
                code += 'movzx  rax, al     ; store result of compare in rax\n'
                code += 'push   rax\n'
            case ['jump', label]:
                code += f'jmp  {label}\n'
            case ['jumpz', label]:
                code += 'pop    rax        ; delete result of compare operation\n'
                code += f'cmp   rax, 0\n'
                code += f'je {label}\n'
            ### MaMa to x86 ###
            case ['mkbasic']:
                # Wert liegt im Stack
                # mkbasic nimmt den Wert und erstellt Tupel ['B', Wert] im Heap
                # und pushed Adresse zu Tupel auf Stack
                code += ';;; === mkbasic ===\n'
                code += malloc(2)  # 16 bytes for basic tuple on heap ['B', value] both cells are 8 byte
                code += 'mov    rdx, rax\n'
                code += "mov    qword [rdx], 'B'\n"
                code += 'pop    rax\n'  # value to store
                code += 'mov    [rdx+8], rax\n'
                code += 'push   rdx\n'  # address to tuple on heap
            case ['getbasic']:
                # Adresse zu Tupel liegt auf Stack
                # getbasic nimmt Adresse vom Stack
                # pushed Wert vom Tupel an der Adresse auf Stack
                code += ';;; === getbasic ===\n'
                code += 'pop    rax\n'
                code += ''  # check if basic type
                code += 'mov    rcx, [rax+8]\n'   # get value from heap
                code += 'push   rcx\n'
            case ['pushloc', N]:
                # legt Adresse zu Variable mit relativer Adresse N auf Stack
                code += f";;; === pushloc {N} ===\n"
                code += 'mov    rdx, rsp\n'
                code +=f'add    rdx, {8*int(N)}\n'
                code += 'mov    rax, [rdx]\n'
                code += 'push   rax\n'
                #code += f'push  qword [rsp + 8*{int(N)}]\n'
            case ['pushglob', N]:
                # legt Adresse zu globaler Variable
                # rbx holds address of global vector
                # push address at gp[N] onto stack
                code += f";;; === pushglob {N} ===\n"
                code += f'push   qword [16 + rbx + 8*{int(N)}]\n'   # 16 offset because first two 8 Byte of vector are 'V', n
            case ['slide', q]:
                # slide(n) removes n*8 Bytes below 8 Bytes from top of stack,
                # so 8 Bytes from top of stack are preserved
                code += f';;; === slide {q} ===\n'
                code += 'pop    rax\n'    # save 8 bytes from stack
                code +=f'add    rsp, {8*int(q)}\n'
                code += 'push   rax\n'
            case ['alloc', n]:
                code += f';;; === alloc {n} ===\n'
                # heap object anlegen ('F',0,0,0) jede Zelle ist 8 Byte
                for i in range(int(n)):
                    code += malloc(4)
                    code += "mov    qword [rax], 'F'\n" # type
                    code += 'mov    qword [rax+8], 0\n'       # addr
                    code += 'mov    qword [rax+16], 0\n'      # args
                    code += 'mov    qword [rax+24], 0\n'      # gp
                    code += 'push   rax\n'  # put address on stack
            case ['rewrite', j]:
                code += f';;; === rewrite {j} ===\n'
                code += f'mov   qword rdx, [rsp+{8*int(j)}]\n'   # rdx holds address to prototype in heap
                code += 'pop    rcx\n'  # rcx holds address to temporary values that will replace values in rdx
                # type
                code += 'mov    qword rax, [rcx]\n'   # indirect because intel can't handle double dereference: mov [],[]
                code += 'mov    qword [rdx], rax\n'
                # addr
                code += 'mov    qword rax, [rcx+8]\n'   # indirect because intel can't handle double dereference: mov [],[]
                code += 'mov    qword [rdx+8], rax\n'
                # args
                code += 'mov    qword rax, [rcx+16]\n'   # indirect because intel can't handle double dereference: mov [],[]
                code += 'mov    qword [rdx+16], rax\n'
                # gp
                code += 'mov    qword rax, [rcx+24]\n'   # indirect because intel can't handle double dereference: mov [],[]
                code += 'mov    qword [rdx+24], rax\n'
            case ['mark', A]:
                code += f';;; === mark {A} ===\n'
                code += 'push   rbx\n'
                code += 'push   rbp\n'
                code += f'push   {A}\n'
                code += 'mov    rbp, rsp\n'
            case ['apply']:
                code += ';;; === apply ===\n'
                code += 'pop    rcx\n'
                code += 'mov    rbx, [rcx+24]\n'  # new global vector is in funktion object at index 3 (3*8)
                code += 'mov    rax, [rcx+8]\n' # address to function is at index 1
                code += 'jmp    rax\n'  # go into function
            case ['popenv']:
                code += ';;; === popenv ===\n'
                code += 'mov    rbx, [rbp+16]\n' # restore global vector
                code += 'pop    qword [rbp+16]\n'    # put result of function where old frame pointer was
                #code += 'mov    rcx, rbp\n' # rsp = rbp + 16
                #code += 'add    rcx, 16\n'
                #code += 'mov    rsp, rcx\n' # restore old stack pointer
                code += 'lea    rsp, [rbp+16]\n'
                code += 'mov    rax, [rbp]\n'
                code += 'mov    rbp, [rbp+8]\n' # restore old frame pointer
                code += 'jmp    rax\n'  # jump to Rücksprungadresse
            case ['mkvec', n]:
                # create vector object with n elements on Heap
                # n ptr to objects are on stack already to fill the vector with
                # stack => vector needs to be filled from back to front
                code += f';;; === mkvec {n} ===\n'
                code += malloc(2+int(n)) # 'V' + n + n elements
                code += "mov    qword [rax], 'V'\n"
                code += f"mov   qword [rax+8], {n}\n"
                for i in range(int(n)):
                    code += 'pop    rdx\n'  # element to write to index n-i in vector
                    code += f'mov    [rax+{16+(int(n)-i-1)*8}], rdx\n'
                code += 'push   rax\n'  # push reference to vector object onto stack
            case ['mkfunval', addr]:
                code += f';;; === mkfunval {addr} ===\n'
                # create a function object ['F', addr, &['V',0], gp]
                # gp is on stack
                # create empty vector first
                #code += 'mov    rdi, 16\n'  # 8+8 Byte for empty vector ['V',0], empty vec because we don't allow currying
                #code += 'call   malloc\n'
                #code += "mov    qword [rax], 'V'\n"
                #code += 'mov    qword [rax+8], 0\n'
                #code += 'mov    r12, rax\n'  # preserve address of empty vector against new malloc
                # create function object
                code += malloc(4)
                code += "mov    qword [rax], 'F'\n"         # 'F'
                code += f'mov    qword [rax+8], {addr}\n'   # addr
                code += 'mov    qword [rax+16], 0\n'        # &['V',0]
                code += 'pop    qword [rax+24]\n'           # gp
                code += 'push   rax\n'
            case [*unknown]:
                label, *unknown = unknown
                label_match = re.search(r'\w+(?=:)', label)
                if label_match is not None :
                    code += f'{label_match.group(0)}:\n'  # create label
                else:
                    raise NotImplementedError(f"statement {instruction}")
                    code += f'Error: unknown CMa statement {unknown}\n'
    return format_code(code)



def x86_program(x86_code, env) :
    program  = x86_prefix(env)
    program += x86_start(env)
    program += "\n;;; Start des eigentlichen Programms\n"
    program += x86_code
    program += ";;; Ende des eigentlichen Programms\n\n"
    program += x86_final(env)
    return format_code(program)

def x86_prefix(env):
    program  = "extern  printf\n"
    program += "extern  malloc\n"
    program += "SECTION .data               ; Data section, initialized variables\n"
    program += 'i64_fmt:  db  "%lld", 10, 0 ; printf format for printing an int64\n'
    program += 'malloc_errormsg:  db "Error: malloc failed, 10, 0"\n'
    return program

def x86_start(env):
    program  = "\n"
    program += "SECTION  .text\nglobal main\n"
    program += "main:\n"
    program += "  push  rbp                 ; unnötig, weil es den Wert 1 enthält, trotzem notwendig, weil sonst segfault\n"              
    program += "  mov   rax,rsp             ; rsp zeigt auf den geretteten rbp  \n"          
    program += "  sub   rax,qword 8         ; neuer rbp sollte ein wort darüber liegen\n"      
    program += "  mov   rbp,rax             ; set frame pointer to current (empty) stack pointer\n"          
    # reserve space at start of stack for global variables
    global_env_size = total_size(global_env(env)) # total size of all global variables
    program +=f"  sub   rsp, {global_env_size}      ; reserve size in stack for global variables\n"
    #print(f"global: {global_env(env)}")
    #print(f"global size: {total_size(global_env(env))}")

    return program

def x86_final(env):
    program  = "  pop   rax\n"
    program += "  mov   rsi, rax\n"
    program += "  mov   rdi,i64_fmt         ; arguments in rdi, rsi\n"
    program += "  mov   rax,0               ; no xmm registers used\n"
    program += "  push  rbp                 ; set up stack frame, must be aligned\n"
    program += "  call  printf              ; Call C function\n"
    program += "  pop   rbp                 ; restore stack\n"
    program += "\n;;; Rueckkehr zum aufrufenden Kontext\n"
    global_env_size = total_size(global_env(env))   # total size of all global variables
    program +=f"  add rsp, {global_env_size}        ; delete/invalidate the stack-space for global variables\n"
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

