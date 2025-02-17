        extern  printf  
        extern  malloc  
        SECTION .data                   ; Data section, initialized variables
basic_type_fmt: db      10,     "%lld", 10,     0       ; printf format for printing an int64
string_type_fmt: db      "%s",   10,     0       ; printf format for printing a string
malloc_errormsg: db      "Error: malloc failed,10,     0"      
                                        ; macros
                
                
        SECTION .text   
        global  main    
                
getbasic:         
        push    rbp     
        mov     rbp,    rsp     
        mov     rax,    rdi     
        mov     qword rdx,[rax]   
        cmp     rdx,    'B'     
        je      getbasic_basic
        cmp     rdx,    'S'     
        je      getbasic_string
getbasic_basic:         
        mov     rdx,    [rax+8] 
        mov     qword rax,[rdx]   
        jmp     finished_getbasic
getbasic_string:         
        mov     rdx,    [rax+8]         ; rdx holds ptr to C-string
        mov     rax,    rdx     
        jmp     finished_getbasic
finished_getbasic:         
        mov     rsp,    rbp     
        pop     rbp     
        ret     
                
fill_libc_params:         
        push    rbp     
        mov     rbp,    rsp     
        mov     qword r10,[rsp+16]
        cmp     r10,    0       
        je      filled_params
        mov     qword rdi,[rsp+24]
        cmp     r10,    1       
        je      filled_params
        mov     qword rsi,[rsp+32]
        cmp     r10,    2       
        je      filled_params
        mov     qword rdx,[rsp+40]
        cmp     r10,    3       
        je      filled_params
        mov     qword rcx,[rsp+48]
        cmp     r10,    4       
        je      filled_params
        mov     qword r8,[rsp+56]
        cmp     r10,    5       
        je      filled_params
        mov     qword r9,[rsp+64]
        jmp     filled_params
filled_params:         
        mov     rsp,    rbp     
        pop     rbp     
        ret     
                
main:           
        push    rbp                     ; unnötig, weil es den Wert 1 enthält, trotzem notwendig, weil sonst segfault
        mov     rax,    rsp             ; rsp zeigt auf den geretteten rbp
        sub     rax,    qword 8         ; neuer rbp sollte ein wort darüber liegen
        mov     rbp,    rax             ; set frame pointer to current (empty) stack pointer
                
        ;;; Start des eigentlichen Programms
program_start:         
                                        ;;; === alloc 0 ===
                                        ;;; === mkvec 0 ===
                                        ;;; malloc 2
        push    rdx     
        mov     rdi,    16      
        call    malloc  
        pop     rdx     
                                        ;;; alloc_tuple
        mov     rdx,    rax     
        mov     qword [rdx],'V'     
                                        ;;; malloc 1
        push    rdx     
        mov     rdi,    8       
        call    malloc  
        pop     rdx     
        mov     qword [rdx+8],rax     
        mov     qword [rax],0       
        push    rdx     
                                        ;;; === setgv ===
        pop     r12     
                                        ;;; === mkstr Test\n ===
                                        ;;; malloc 2
        push    rdx     
        mov     rdi,    16      
        call    malloc  
        pop     rdx     
                                        ;;; alloc_tuple
        mov     rdx,    rax     
        mov     qword [rdx],'S'     
        push    rdx     
        mov     rdi,    7       
        call    malloc  
        pop     rdx     
        mov     qword [rdx+8],rax     
        mov     byte [rax+0],'T'     
        mov     byte [rax+1],'e'     
        mov     byte [rax+2],'s'     
        mov     byte [rax+3],'t'     
        mov     word [rax+4],'\n'    
        mov     byte [rax+6],0       
        push    rdx     
                                        ;;; === getstr ===
        pop     rax     
        push    qword [rax+8]
                                        ;;; === loadc 1 ===
        mov     rcx,    qword 1 
        push    rcx     
                                        ;;; === filllibcparams ===
        call    fill_libc_params
        add     rsp,    8       
                                        ;;; === call printf ===
        mov     rax,    0               ; no xmm registers used
        push    rbp                     ; set up stack frame, must be aligned
        call    printf                  ; Call LibC function
        pop     rbp                     ; restore stack
        push    rax     
                                        ;;; === slide 1 ===
        pop     rax     
        add     rsp,    8       
        push    rax     
        ;;; Ende des eigentlichen Programms
                
program_end:         
        pop     rax     
        mov     rsi,    rax     
        mov     rdi,    basic_type_fmt  ; arguments in rdi, rsi
        mov     rax,    0               ; no xmm registers used
printf_call:         
        push    rbp                     ; set up stack frame, must be aligned
        call    printf                  ; Call C function
        pop     rbp                     ; restore stack
                
        ;;; Rueckkehr zum aufrufenden Kontext
        pop     rbp                     ; original rbp is last thing on the stack
        mov     rax,    0               ; return 0
        ret     
