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
                                        ;;; === alloc 3 ===
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
                                        ;;; === mkvec 3 ===
                                        ;;; malloc 2
        push    rdx     
        mov     rdi,    16      
        call    malloc  
        pop     rdx     
                                        ;;; alloc_tuple
        mov     rdx,    rax     
        mov     qword [rdx],'V'     
                                        ;;; malloc 4
        push    rdx     
        mov     rdi,    32      
        call    malloc  
        pop     rdx     
        mov     qword [rdx+8],rax     
        mov     qword [rax],3       
        mov     qword [rax+24],0       
        mov     qword [rax+24],0       
        mov     qword [rax+24],0       
        pop     qword [rax+8]
        pop     qword [rax+16]
        pop     qword [rax+24]
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
                                        ;;; === pushglobalvec ===
        push    r12     
                                        ;;; === pushaddr 1 ===
        pop     rax     
        mov     qword rdx,[rax+8] 
        push    qword [rdx+16]
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
                                        ;;; === mkfunval lambda_19 ===
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
        mov     qword [rax],lambda_19
        pop     qword [rax+8]
        push    rdx     
                                        ;;; === jump  end_lambda_19 ===
        jmp     end_lambda_19
lambda_19:         
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
                                        ;;; === mkfunval lambda_20 ===
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
        mov     qword [rax],lambda_20
        pop     qword [rax+8]
        push    rdx     
                                        ;;; === jump  end_lambda_20 ===
        jmp     end_lambda_20
lambda_20:         
                                        ;;; === pushparamvec ===
        push    r14     
                                        ;;; === pushaddr 0 ===
        pop     rax     
        mov     qword rdx,[rax+8] 
        push    qword [rdx+8]
                                        ;;; === popenv ===
        pop     rax     
        pop     rcx     
        pop     rbp     
        pop     r14     
        pop     r12     
        push    rax     
        jmp     rcx     
end_lambda_20:         
                                        ;;; === pushglobalvec ===
        push    r12     
                                        ;;; === rewriteinvec 0 ===
        pop     rax     
        mov     qword rdx,[rax+8] 
        pop     rcx     
        mov     qword rax,[rdx + 8]
        mov     qword rdx,[rcx]   
        mov     qword [rax],rdx     
        mov     qword rdx,[rcx+8] 
        mov     qword [rax+8],rdx     
        push    rax     
                                        ;;; === pop 1 ===
        pop     rax     
                                        ;;; === mark back_from_call_25 ===
        push    r12     
        push    r14     
        push    rbp     
        push    back_from_call_25
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
back_from_call_25:         
                                        ;;; === getbasic ===
        pop     rax     
        mov     rcx,    [rax+8] 
        push    qword [rcx]
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
                                        ;;; === popenv ===
        pop     rax     
        pop     rcx     
        pop     rbp     
        pop     r14     
        pop     r12     
        push    rax     
        jmp     rcx     
end_lambda_19:         
                                        ;;; === pushglobalvec ===
        push    r12     
                                        ;;; === rewriteinvec 0 ===
        pop     rax     
        mov     qword rdx,[rax+8] 
        pop     rcx     
        mov     qword rax,[rdx + 8]
        mov     qword rdx,[rcx]   
        mov     qword [rax],rdx     
        mov     qword rdx,[rcx+8] 
        mov     qword [rax+8],rdx     
        push    rax     
                                        ;;; === pop 1 ===
        pop     rax     
                                        ;;; === mark back_from_call_26 ===
        push    r12     
        push    r14     
        push    rbp     
        push    back_from_call_26
        mov     rbp,    rsp     
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
back_from_call_26:         
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
