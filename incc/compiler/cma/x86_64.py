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
                #code += f'push  qword {str(q)}\n'
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
            case ['store']:
                code += ';;; === store ===\n'
                code += 'pop    rcx\n'
                code += 'neg    rcx         ; get the address rbx-rcx of global variable without modifying rbx by doing (-rcx+rbx)\n'
                code += 'add    rcx, rbx    ; rcx now contains the address of the global variable\n'
                code += 'pop    rax         ; pop the relative address of global variable from stack\n'
                code += 'mov    [rcx], rax\n'
                code += 'push   rax         ; push the rvalue of assignment onto stack\n'
            case ['load']:
                code += ';;; === load, put value of global variable on stack ===\n'
                code += 'pop    rcx\n'
                #code += f'mov    rcx, qword {addr}\n'
                code += 'neg    rcx         ; get the address rbx-rcx of global variable without modifying rbx by doing (-rcx+rbx)\n'
                code += 'add    rcx, rbx    ; rcx now contains the address of the global variable\n'
                code += 'push   qword [rcx]       ; push value of global variable onto stack\n'
            case ['jump', label]:
                code += f'jmp  {label}\n'
            case ['jumpz', label]:
                code += 'pop    rax        ; delete result of compare operation\n'
                code += f'cmp   rax, 0\n'
                code += f'je {label}\n'
            case ['dup']:
                code += ';;; === duplicate value on stack ===\n'
                code += 'pop    rcx\n'
                code += 'push   rcx\n'
                code += 'push   rcx\n'
            case ['swap']:
                code += ';;; === swap 2 top values on stack ===\n'
                code += 'pop    rax\n'
                code += 'pop    rcx\n'
                code += 'push   rax\n'
                code += 'push   rcx\n'
            case ['dec']:
                code += ';;; === decrement top value on stack ===\n'
                code += 'pop    rax\n'
                code += 'dec    rax\n'
                code += 'push   rax\n'
            case ['mark']:
                # legt frame pointer auf stack (sichert nur)
                code += ';;; === mark ===\n'
                code += 'push   rbp\n'
            case ['call']:
                #  pushes rsp (Rücksprungadresse) onto stack (where call proc stands)
                code += ';;; === call ===\n'
                code += 'pop    rax\n'  # auf stack liegt adresse von proc
                code += 'call   rax\n'
            case ['alloc', size]:
                """
                    allocate size * 8 bytes of stack memory for local variables
                    x86:
                    sub rsp, qword {size}
                """
                code += f';;; === alloc {size} ===\n'
                code += f'sub   rsp, qword {size}\n'
            case ['loadrc', offset]:
                """
                    mov rax, rbp
                    add rax, qword {offset}
                    push rax
                """
                # offset+rbp addr
                # push value of local variable onto stack, addr is relative to rbx-rsp
                code += f';;; === loadrc {offset} ===\n'
                code += 'mov    rax, rbp\n'
                code += f'add    rax, qword {offset}\n'
                code += 'push   rax\n'
            case ['enter']:
                # enter/call procedure which is stored at the address on top of stack, address is the offset from rsp to the position on stack where proc is stored
                # setzt frame pointer auf rbx-rsp, rbp = rbx-rsp, also neuer frame pointer wird gesetzt
                code += ';;; enter\n'
                code += 'mov    rbp, rbx\n'
                code += 'sub    rbp, rsp\n'
            case ['slide', q, m]:
                # slide(q,m) removes q Bytes below m Bytes from top of stack,
                # so m Bytes from top of stack are preserved
                code += f';;; === slide {q} {m} ===\n'
                code += 'pop    rax\n'    # m (often m=8) bytes from stack
                code += f'add    rsp, qword {q}\n'
                code += 'push   rax\n'
            case ['return']:
                # nimmt rücksprungaddresse vom Stack und springt zurück
                """
                    restore previous frame pointer and go to previous frame
                    rsp = rbx - rbp
                    rbp = [rbx - rbp + 8]
                    ret
                """
                code += ';;; === return ===\n'
                code += 'mov    rsp, rbx\n'
                code += 'sub    rsp, rbp\n'
                #code += 'pop    rbp\n'
                code += 'mov    rax, rbx\n' # rbp = [rbx - rbp + 8]
                code += 'sub    rax, rbp\n'
                code += 'mov    rbp, [rax+8]\n'
                code += 'ret\n'
            case [*unknown]:
                label, *unknown = unknown
                label_match = re.search(r'\w+(?=:)', label)
                if label_match is not None :
                    code += f'{label_match.group(0)}:\n'  # create label
                else:
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
    program += "SECTION .data               ; Data section, initialized variables\n"
    program += 'i64_fmt:  db  "%lld", 10, 0 ; printf format for printing an int64\n'
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
    print(f"global: {global_env(env)}")
    print(f"global size: {total_size(global_env(env))}")

    return program

def x86_final(env):
    program  = "  pop   rax\n"
    program += "  mov   rsi, rax\n"
    program += "  mov   rdi,i64_fmt         ; arguments in rdi, rsi\n"
    program += "  mov   rax,0               ; no xmm registers used\n"
    program += "  push  rbp                 ; set up stack frame, must be alligned\n"
    program += "  call  printf              ; Call C function\n"
    program += "  pop   rbp                 ; restore stack\n"
    program += "\n;;; Rueckkehr zum aufrufenden Kontext\n"
    global_env_size = total_size(global_env(env))   # total size of all global variables
    program +=f"  add rsp, {global_env_size}        ; delete/invalidate the stack-space for global variables\n"
    program += "  pop   rbp                 ; original rbp is last thing on the stack\n"
    program += "  mov   rax,0               ; return 0\n"
    program += "  ret\n"
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

