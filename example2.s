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
                                        ;;; === alloc 6 ===
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
                                        ;;; === mkvec 6 ===
                                        ;;; malloc 2
        push    rdx     
        mov     rdi,    16      
        call    malloc  
        pop     rdx     
                                        ;;; alloc_tuple
        mov     rdx,    rax     
        mov     qword [rdx],'V'     
                                        ;;; malloc 7
        push    rdx     
        mov     rdi,    56      
        call    malloc  
        pop     rdx     
        mov     qword [rdx+8],rax     
        mov     qword [rax],6       
        mov     qword [rax+48],0       
        mov     qword [rax+48],0       
        mov     qword [rax+48],0       
        mov     qword [rax+48],0       
        mov     qword [rax+48],0       
        mov     qword [rax+48],0       
        pop     qword [rax+8]
        pop     qword [rax+16]
        pop     qword [rax+24]
        pop     qword [rax+32]
        pop     qword [rax+40]
        pop     qword [rax+48]
        push    rdx     
                                        ;;; === setgv ===
        pop     r12     
                                        ;;; === pushglobalvec ===
        push    r12     
                                        ;;; === pushaddr 1 ===
        pop     rax     
        mov     qword rdx,[rax+8] 
        push    qword [rdx+16]
                                        ;;; === pushglobalvec ===
        push    r12     
                                        ;;; === pushaddr 0 ===
        pop     rax     
        mov     qword rdx,[rax+8] 
        push    qword [rdx+8]
                                        ;;; === mkvec 2 ===
                                        ;;; malloc 2
        push    rdx     
        mov     rdi,    16      
        call    malloc  
        pop     rdx     
                                        ;;; alloc_tuple
        mov     rdx,    rax     
        mov     qword [rdx],'V'     
                                        ;;; malloc 3
        push    rdx     
        mov     rdi,    24      
        call    malloc  
        pop     rdx     
        mov     qword [rdx+8],rax     
        mov     qword [rax],2       
        mov     qword [rax+16],0       
        mov     qword [rax+16],0       
        pop     qword [rax+8]
        pop     qword [rax+16]
        push    rdx     
                                        ;;; === mkfunval lambda_3 ===
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
        mov     qword [rax],lambda_3
        pop     qword [rax+8]
        push    rdx     
                                        ;;; === jump  end_lambda_3 ===
        jmp     end_lambda_3
lambda_3:         
                                        ;;; === pushparamvec ===
        push    r14     
                                        ;;; === pushaddr 0 ===
        pop     rax     
        mov     qword rdx,[rax+8] 
        push    qword [rdx+8]
                                        ;;; === pushparamvec ===
        push    r14     
                                        ;;; === pushaddr 1 ===
        pop     rax     
        mov     qword rdx,[rax+8] 
        push    qword [rdx+16]
                                        ;;; === getbasic ===
        pop     rax     
        mov     rcx,    [rax+8] 
        push    qword [rcx]
                                        ;;; === pushaddr ===
        pop     rcx     
        pop     rax     
        mov     qword rdx,[rax+8] 
        push    rdx     
        mov     rax,    8       
        mul     rcx     
        add     rax,    8       
        pop     rdx     
        add     rdx,    rax     
        push    qword [rdx]
                                        ;;; === pushparamvec ===
        push    r14     
                                        ;;; === rewriteinvec 1 ===
        pop     rax     
        mov     qword rdx,[rax+8] 
        pop     rcx     
        mov     qword rax,[rdx + 16]
        mov     qword rdx,[rcx]   
        mov     qword [rax],rdx     
        mov     qword rdx,[rcx+8] 
        mov     qword [rax+8],rdx     
        push    rax     
                                        ;;; === pop 1 ===
        pop     rax     
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
                                        ;;; === pushglobalvec ===
        push    r12     
                                        ;;; === rewriteinvec 1 ===
        pop     rax     
        mov     qword rdx,[rax+8] 
        pop     rcx     
        mov     qword rax,[rdx + 16]
        mov     qword rdx,[rcx]   
        mov     qword [rax],rdx     
        mov     qword rdx,[rcx+8] 
        mov     qword [rax+8],rdx     
        push    rax     
                                        ;;; === pop 1 ===
        pop     rax     
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
while_1:         
                                        ;;; === pushglobalvec ===
        push    r12     
                                        ;;; === pushaddr 0 ===
        pop     rax     
        mov     qword rdx,[rax+8] 
        push    qword [rdx+8]
                                        ;;; === getbasic ===
        pop     rax     
        mov     rcx,    [rax+8] 
        push    qword [rcx]
                                        ;;; === pushparamvec ===
        push    r14     
                                        ;;; === pushaddr 1 ===
        pop     rax     
        mov     qword rdx,[rax+8] 
        push    qword [rdx+16]
                                        ;;; === getbasic ===
        pop     rax     
        mov     rcx,    [rax+8] 
        push    qword [rcx]
        pop     rcx     
        pop     rax     
        cmp     rax,    rcx     
        setl    al      
        movzx   rax,    al              ; store result of compare in rax
        push    rax     
                                        ;;; === jumpz  endwhile_1 ===
        pop     rax                     ; delete result of compare operation
        cmp     rax,    0       
        je      endwhile_1
do_1:           
                                        ;;; === pop 1 ===
        pop     rax     
                                        ;;; === pushglobalvec ===
        push    r12     
                                        ;;; === pushaddr 1 ===
        pop     rax     
        mov     qword rdx,[rax+8] 
        push    qword [rdx+16]
                                        ;;; === getbasic ===
        pop     rax     
        mov     rcx,    [rax+8] 
        push    qword [rcx]
                                        ;;; === pushparamvec ===
        push    r14     
                                        ;;; === pushaddr 1 ===
        pop     rax     
        mov     qword rdx,[rax+8] 
        push    qword [rdx+16]
                                        ;;; === pushglobalvec ===
        push    r12     
                                        ;;; === pushaddr 0 ===
        pop     rax     
        mov     qword rdx,[rax+8] 
        push    qword [rdx+8]
                                        ;;; === getbasic ===
        pop     rax     
        mov     rcx,    [rax+8] 
        push    qword [rcx]
                                        ;;; === pushaddr ===
        pop     rcx     
        pop     rax     
        mov     qword rdx,[rax+8] 
        push    rdx     
        mov     rax,    8       
        mul     rcx     
        add     rax,    8       
        pop     rdx     
        add     rdx,    rax     
        push    qword [rdx]
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
                                        ;;; === pushglobalvec ===
        push    r12     
                                        ;;; === rewriteinvec 1 ===
        pop     rax     
        mov     qword rdx,[rax+8] 
        pop     rcx     
        mov     qword rax,[rdx + 16]
        mov     qword rdx,[rcx]   
        mov     qword [rax],rdx     
        mov     qword rdx,[rcx+8] 
        mov     qword [rax+8],rdx     
        push    rax     
                                        ;;; === pop 1 ===
        pop     rax     
                                        ;;; === pushglobalvec ===
        push    r12     
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
                                        ;;; === jump  while_1 ===
        jmp     while_1 
endwhile_1:         
                                        ;;; === pop 1 ===
        pop     rax     
                                        ;;; === pushglobalvec ===
        push    r12     
                                        ;;; === pushaddr 1 ===
        pop     rax     
        mov     qword rdx,[rax+8] 
        push    qword [rdx+16]
                                        ;;; === popenv ===
        pop     rax     
        pop     rcx     
        pop     rbp     
        pop     r14     
        pop     r12     
        push    rax     
        jmp     rcx     
end_lambda_3:         
                                        ;;; === pushglobalvec ===
        push    r12     
                                        ;;; === rewriteinvec 3 ===
        pop     rax     
        mov     qword rdx,[rax+8] 
        pop     rcx     
        mov     qword rax,[rdx + 32]
        mov     qword rdx,[rcx]   
        mov     qword [rax],rdx     
        mov     qword rdx,[rcx+8] 
        mov     qword [rax+8],rdx     
        push    rax     
                                        ;;; === pop 1 ===
        pop     rax     
                                        ;;; === loadc 5 ===
        mov     rcx,    qword 5 
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
                                        ;;; === loadc 4 ===
        mov     rcx,    qword 4 
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
                                        ;;; === mkvec 2 ===
                                        ;;; malloc 2
        push    rdx     
        mov     rdi,    16      
        call    malloc  
        pop     rdx     
                                        ;;; alloc_tuple
        mov     rdx,    rax     
        mov     qword [rdx],'V'     
                                        ;;; malloc 3
        push    rdx     
        mov     rdi,    24      
        call    malloc  
        pop     rdx     
        mov     qword [rdx+8],rax     
        mov     qword [rax],2       
        mov     qword [rax+16],0       
        mov     qword [rax+16],0       
        pop     qword [rax+8]
        pop     qword [rax+16]
        push    rdx     
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
                                        ;;; === mkvec 2 ===
                                        ;;; malloc 2
        push    rdx     
        mov     rdi,    16      
        call    malloc  
        pop     rdx     
                                        ;;; alloc_tuple
        mov     rdx,    rax     
        mov     qword [rdx],'V'     
                                        ;;; malloc 3
        push    rdx     
        mov     rdi,    24      
        call    malloc  
        pop     rdx     
        mov     qword [rdx+8],rax     
        mov     qword [rax],2       
        mov     qword [rax+16],0       
        mov     qword [rax+16],0       
        pop     qword [rax+8]
        pop     qword [rax+16]
        push    rdx     
                                        ;;; === mkvec 2 ===
                                        ;;; malloc 2
        push    rdx     
        mov     rdi,    16      
        call    malloc  
        pop     rdx     
                                        ;;; alloc_tuple
        mov     rdx,    rax     
        mov     qword [rdx],'V'     
                                        ;;; malloc 3
        push    rdx     
        mov     rdi,    24      
        call    malloc  
        pop     rdx     
        mov     qword [rdx+8],rax     
        mov     qword [rax],2       
        mov     qword [rax+16],0       
        mov     qword [rax+16],0       
        pop     qword [rax+8]
        pop     qword [rax+16]
        push    rdx     
                                        ;;; === pushglobalvec ===
        push    r12     
                                        ;;; === rewriteinvec 2 ===
        pop     rax     
        mov     qword rdx,[rax+8] 
        pop     rcx     
        mov     qword rax,[rdx + 24]
        mov     qword rdx,[rcx]   
        mov     qword [rax],rdx     
        mov     qword rdx,[rcx+8] 
        mov     qword [rax+8],rdx     
        push    rax     
                                        ;;; === pop 1 ===
        pop     rax     
                                        ;;; === mark back_from_call_4 ===
        push    r12     
        push    r14     
        push    rbp     
        push    back_from_call_4
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
                                        ;;; === pushglobalvec ===
        push    r12     
                                        ;;; === pushaddr 2 ===
        pop     rax     
        mov     qword rdx,[rax+8] 
        push    qword [rdx+24]
                                        ;;; === mkvec 2 ===
                                        ;;; malloc 2
        push    rdx     
        mov     rdi,    16      
        call    malloc  
        pop     rdx     
                                        ;;; alloc_tuple
        mov     rdx,    rax     
        mov     qword [rdx],'V'     
                                        ;;; malloc 3
        push    rdx     
        mov     rdi,    24      
        call    malloc  
        pop     rdx     
        mov     qword [rdx+8],rax     
        mov     qword [rax],2       
        mov     qword [rax+16],0       
        mov     qword [rax+16],0       
        pop     qword [rax+8]
        pop     qword [rax+16]
        push    rdx     
                                        ;;; === setpv ===
        pop     r14     
                                        ;;; === pushglobalvec ===
        push    r12     
                                        ;;; === pushaddr 3 ===
        pop     rax     
        mov     qword rdx,[rax+8] 
        push    qword [rdx+32]
                                        ;;; === apply ===
        pop     rdx     
        mov     qword rcx,[rdx+8] 
        mov     qword r12,[rcx+8] 
        mov     qword rax,[rcx]   
        jmp     rax     
back_from_call_4:         
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
