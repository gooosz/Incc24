        extern  printf  
        extern  malloc  
        SECTION .data                   ; Data section, initialized variables
i64_fmt: db      "%lld", 10,     0       ; printf format for printing an int64
malloc_errormsg: db      "Error: malloc failed,10,     0"      
                                        ; macros
                
                
        SECTION .text   
        global  main    
main:           
        push    rbp                     ; unnötig, weil es den Wert 1 enthält, trotzem notwendig, weil sonst segfault
        mov     rax,    rsp             ; rsp zeigt auf den geretteten rbp
        sub     rax,    qword 8         ; neuer rbp sollte ein wort darüber liegen
        mov     rbp,    rax             ; set frame pointer to current (empty) stack pointer
                
        ;;; Start des eigentlichen Programms
program_start:         
                                        ;;; === alloc 1 ===
                                        ;;; malloc 2
        push    rdx     
        mov     rdi,    16      
        call    malloc  
        pop     rdx     
                                        ;;; alloc_tuple
        mov     rdx,    rax     
        mov     qword [rdx],'D'     
        mov     qword [rdx+8],0       
        push    rdx     
                                        ;;; === mkvec 1 ===
                                        ;;; malloc 2
        push    rdx     
        mov     rdi,    16      
        call    malloc  
        pop     rdx     
                                        ;;; alloc_tuple
        mov     rdx,    rax     
        mov     qword [rdx],'V'     
                                        ;;; malloc 2
        push    rdx     
        mov     rdi,    16      
        call    malloc  
        pop     rdx     
        mov     qword [rdx+8],rax     
        mov     qword [rax],1       
        mov     qword [rax+8],0       
        pop     qword [rax+8]
        push    rdx     
                                        ;;; === setgv ===
        pop     r12     
                                        ;;; === alloc 1 ===
                                        ;;; malloc 2
        push    rdx     
        mov     rdi,    16      
        call    malloc  
        pop     rdx     
                                        ;;; alloc_tuple
        mov     rdx,    rax     
        mov     qword [rdx],'D'     
        mov     qword [rdx+8],0       
        push    rdx     
                                        ;;; === mkvec 1 ===
                                        ;;; malloc 2
        push    rdx     
        mov     rdi,    16      
        call    malloc  
        pop     rdx     
                                        ;;; alloc_tuple
        mov     rdx,    rax     
        mov     qword [rdx],'V'     
                                        ;;; malloc 2
        push    rdx     
        mov     rdi,    16      
        call    malloc  
        pop     rdx     
        mov     qword [rdx+8],rax     
        mov     qword [rax],1       
        mov     qword [rax+8],0       
        pop     qword [rax+8]
        push    rdx     
                                        ;;; === setpv ===
        pop     r14     
                                        ;;; === alloc 1 ===
                                        ;;; malloc 2
        push    rdx     
        mov     rdi,    16      
        call    malloc  
        pop     rdx     
                                        ;;; alloc_tuple
        mov     rdx,    rax     
        mov     qword [rdx],'D'     
        mov     qword [rdx+8],0       
        push    rdx     
                                        ;;; === loadc 1 ===
        mov     rcx,    qword 1 
        push    rcx     
                                        ;;; === mkbasic ===
                                        ;;; malloc 2
        push    rdx     
        mov     rdi,    16      
        call    malloc  
        pop     rdx     
                                        ;;; alloc_tuple
        mov     rdx,    rax     
        mov     qword [rdx],'B'     
                                        ;;; malloc 1
        push    rdx     
        mov     rdi,    8       
        call    malloc  
        pop     rdx     
        mov     qword [rdx+8],rax     
        pop     qword [rax]
        push    rdx     
                                        ;;; === rewriteloc 1 ===
        mov     qword rdx,[rsp+8] 
        pop     rax     
        mov     qword rcx,[rax]   
        mov     qword [rdx],rcx     
        mov     qword rcx,[rax+8] 
        mov     qword [rdx+8],rcx     
                                        ;;; === alloc 1 ===
                                        ;;; malloc 2
        push    rdx     
        mov     rdi,    16      
        call    malloc  
        pop     rdx     
                                        ;;; alloc_tuple
        mov     rdx,    rax     
        mov     qword [rdx],'D'     
        mov     qword [rdx+8],0       
        push    rdx     
                                        ;;; === pushlocal 0 ===
        push    qword [rsp + 0]
                                        ;;; === mkvec 1 ===
                                        ;;; malloc 2
        push    rdx     
        mov     rdi,    16      
        call    malloc  
        pop     rdx     
                                        ;;; alloc_tuple
        mov     rdx,    rax     
        mov     qword [rdx],'V'     
                                        ;;; malloc 2
        push    rdx     
        mov     rdi,    16      
        call    malloc  
        pop     rdx     
        mov     qword [rdx+8],rax     
        mov     qword [rax],1       
        mov     qword [rax+8],0       
        pop     qword [rax+8]
        push    rdx     
                                        ;;; === mkfunval lambda_18 ===
                                        ;;; malloc 2
        push    rdx     
        mov     rdi,    16      
        call    malloc  
        pop     rdx     
                                        ;;; alloc_tuple
        mov     rdx,    rax     
        mov     qword [rdx],'F'     
                                        ;;; malloc 2
        push    rdx     
        mov     rdi,    16      
        call    malloc  
        pop     rdx     
        mov     qword [rdx+8],rax     
        mov     qword [rax],0       
        mov     qword [rax+8],0       
        mov     qword [rax],lambda_18
        pop     qword [rax+8]
        push    rdx     
                                        ;;; === jump  end_lambda_18 ===
        jmp     end_lambda_18
lambda_18:         
ite_5:          
                                        ;;; === pushparamvec ===
        push    r14     
                                        ;;; === pushaddr 0 ===
        pop     rax     
        mov     qword rdx,[rax+8] 
        push    qword [rdx+8]
                                        ;;; === getbasic ===
        pop     rax     
        mov     rcx,    [rax+8] 
        push    qword [rcx]
                                        ;;; === loadc 1 ===
        mov     rcx,    qword 1 
        push    rcx     
        pop     rcx     
        pop     rax     
        cmp     rax,    rcx     
        setl    al      
        movzx   rax,    al              ; store result of compare in rax
        push    rax     
                                        ;;; === jumpz  else_5 ===
        pop     rax                     ; delete result of compare operation
        cmp     rax,    0       
        je      else_5  
then_5:         
                                        ;;; === loadc 0 ===
        mov     rcx,    qword 0 
        push    rcx     
                                        ;;; === mkbasic ===
                                        ;;; malloc 2
        push    rdx     
        mov     rdi,    16      
        call    malloc  
        pop     rdx     
                                        ;;; alloc_tuple
        mov     rdx,    rax     
        mov     qword [rdx],'B'     
                                        ;;; malloc 1
        push    rdx     
        mov     rdi,    8       
        call    malloc  
        pop     rdx     
        mov     qword [rdx+8],rax     
        pop     qword [rax]
        push    rdx     
                                        ;;; === jump  endite_5 ===
        jmp     endite_5
else_5:         
                                        ;;; === pushparamvec ===
        push    r14     
                                        ;;; === pushaddr 0 ===
        pop     rax     
        mov     qword rdx,[rax+8] 
        push    qword [rdx+8]
                                        ;;; === getbasic ===
        pop     rax     
        mov     rcx,    [rax+8] 
        push    qword [rcx]
                                        ;;; === mark back_from_call_23 ===
        push    r12     
        push    rbp     
        push    back_from_call_23
        mov     rbp,    rsp     
                                        ;;; === pushparamvec ===
        push    r14     
                                        ;;; === pushaddr 0 ===
        pop     rax     
        mov     qword rdx,[rax+8] 
        push    qword [rdx+8]
                                        ;;; === getbasic ===
        pop     rax     
        mov     rcx,    [rax+8] 
        push    qword [rcx]
                                        ;;; === loadc 1 ===
        mov     rcx,    qword 1 
        push    rcx     
        pop     rcx     
        pop     rax     
        sub     rax,    rcx     
        push    rax     
                                        ;;; === mkbasic ===
                                        ;;; malloc 2
        push    rdx     
        mov     rdi,    16      
        call    malloc  
        pop     rdx     
                                        ;;; alloc_tuple
        mov     rdx,    rax     
        mov     qword [rdx],'B'     
                                        ;;; malloc 1
        push    rdx     
        mov     rdi,    8       
        call    malloc  
        pop     rdx     
        mov     qword [rdx+8],rax     
        pop     qword [rax]
        push    rdx     
                                        ;;; === pushparamvec ===
        push    r14     
                                        ;;; === storeaddr 0 ===
        pop     rax     
        mov     qword rdx,[rax+8] 
        pop     qword [rdx+8]
        push    qword [rdx+8]
                                        ;;; === pop 1 ===
        pop     rax     
                                        ;;; === pushglobalvec ===
        push    r12     
                                        ;;; === pushaddr 0 ===
        pop     rax     
        mov     qword rdx,[rax+8] 
        push    qword [rdx+8]
                                        ;;; === apply ===
        pop     rdx     
        mov     qword rcx,[rdx+8] 
        mov     qword r12,[rcx+8] 
        mov     qword rax,[rcx]   
        jmp     rax     
back_from_call_23:         
                                        ;;; === getbasic ===
        pop     rax     
        mov     rcx,    [rax+8] 
        push    qword [rcx]
        pop     rcx     
        pop     rax     
        add     rax,    rcx     
        push    rax     
                                        ;;; === mkbasic ===
                                        ;;; malloc 2
        push    rdx     
        mov     rdi,    16      
        call    malloc  
        pop     rdx     
                                        ;;; alloc_tuple
        mov     rdx,    rax     
        mov     qword [rdx],'B'     
                                        ;;; malloc 1
        push    rdx     
        mov     rdi,    8       
        call    malloc  
        pop     rdx     
        mov     qword [rdx+8],rax     
        pop     qword [rax]
        push    rdx     
endite_5:         
                                        ;;; === popenv ===
        pop     rax     
        pop     rcx     
        pop     rbp     
        pop     r12     
        push    rax     
        jmp     rcx     
end_lambda_18:         
                                        ;;; === rewriteloc 1 ===
        mov     qword rdx,[rsp+8] 
        pop     rax     
        mov     qword rcx,[rax]   
        mov     qword [rdx],rcx     
        mov     qword rcx,[rax+8] 
        mov     qword [rdx+8],rcx     
                                        ;;; === mark back_from_call_24 ===
        push    r12     
        push    rbp     
        push    back_from_call_24
        mov     rbp,    rsp     
                                        ;;; === loadc 2 ===
        mov     rcx,    qword 2 
        push    rcx     
                                        ;;; === mkbasic ===
                                        ;;; malloc 2
        push    rdx     
        mov     rdi,    16      
        call    malloc  
        pop     rdx     
                                        ;;; alloc_tuple
        mov     rdx,    rax     
        mov     qword [rdx],'B'     
                                        ;;; malloc 1
        push    rdx     
        mov     rdi,    8       
        call    malloc  
        pop     rdx     
        mov     qword [rdx+8],rax     
        pop     qword [rax]
        push    rdx     
                                        ;;; === pushparamvec ===
        push    r14     
                                        ;;; === storeaddr 0 ===
        pop     rax     
        mov     qword rdx,[rax+8] 
        pop     qword [rdx+8]
        push    qword [rdx+8]
                                        ;;; === pop 1 ===
        pop     rax     
                                        ;;; === pushlocal 3 ===
        push    qword [rsp + 24]
                                        ;;; === apply ===
        pop     rdx     
        mov     qword rcx,[rdx+8] 
        mov     qword r12,[rcx+8] 
        mov     qword rax,[rcx]   
        jmp     rax     
back_from_call_24:         
                                        ;;; === slide 1 ===
        pop     rax     
        add     rsp,    8       
        push    rax     
                                        ;;; === getbasic ===
        pop     rax     
        mov     rcx,    [rax+8] 
        push    qword [rcx]
                                        ;;; === pushlocal 1 ===
        push    qword [rsp + 8]
                                        ;;; === getbasic ===
        pop     rax     
        mov     rcx,    [rax+8] 
        push    qword [rcx]
        pop     rcx     
        pop     rax     
        add     rax,    rcx     
        push    rax     
                                        ;;; === mkbasic ===
                                        ;;; malloc 2
        push    rdx     
        mov     rdi,    16      
        call    malloc  
        pop     rdx     
                                        ;;; alloc_tuple
        mov     rdx,    rax     
        mov     qword [rdx],'B'     
                                        ;;; malloc 1
        push    rdx     
        mov     rdi,    8       
        call    malloc  
        pop     rdx     
        mov     qword [rdx+8],rax     
        pop     qword [rax]
        push    rdx     
                                        ;;; === slide 1 ===
        pop     rax     
        add     rsp,    8       
        push    rax     
                                        ;;; === getbasic ===
        pop     rax     
        mov     rcx,    [rax+8] 
        push    qword [rcx]
        ;;; Ende des eigentlichen Programms
                
program_end:         
        pop     rax     
        mov     rsi,    rax     
        mov     rdi,    i64_fmt         ; arguments in rdi, rsi
        mov     rax,    0               ; no xmm registers used
printf_call:         
        push    rbp                     ; set up stack frame, must be aligned
        call    printf                  ; Call C function
        pop     rbp                     ; restore stack
                
        ;;; Rueckkehr zum aufrufenden Kontext
        pop     rbp                     ; original rbp is last thing on the stack
        mov     rax,    0               ; return 0
        ret     
