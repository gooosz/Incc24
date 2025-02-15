        extern  printf  
        extern  malloc  
        SECTION .data                   ; Data section, initialized variables
basic_type_fmt: db      "%lld", 10,     0       ; printf format for printing an int64
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
                                        ;;; === alloc 5 ===
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
                                        ;;; === mkvec 5 ===
                                        ;;; malloc 2
        push    rdx     
        mov     rdi,    16      
        call    malloc  
        pop     rdx     
                                        ;;; alloc_tuple
        mov     rdx,    rax     
        mov     qword [rdx],'V'     
                                        ;;; malloc 6
        push    rdx     
        mov     rdi,    48      
        call    malloc  
        pop     rdx     
        mov     qword [rdx+8],rax     
        mov     qword [rax],5       
        mov     qword [rax+40],0       
        mov     qword [rax+40],0       
        mov     qword [rax+40],0       
        mov     qword [rax+40],0       
        mov     qword [rax+40],0       
        pop     qword [rax+8]
        pop     qword [rax+16]
        pop     qword [rax+24]
        pop     qword [rax+32]
        pop     qword [rax+40]
        push    rdx     
                                        ;;; === setgv ===
        pop     r12     
                                        ;;; === pushglobalvec ===
        push    r12     
                                        ;;; === pushaddr 1 ===
        pop     rax     
        mov     qword rdx,[rax+8] 
        push    qword [rdx+16]
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
                                        ;;; === mkfunval lambda_0 ===
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
        mov     qword [rax],lambda_0
        pop     qword [rax+8]
        push    rdx     
                                        ;;; === jump  end_lambda_0 ===
        jmp     end_lambda_0
lambda_0:         
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
end_lambda_0:         
                                        ;;; === rewrite ===
        pop     rax     
        pop     rdx     
        mov     qword rcx,[rax]   
        mov     qword [rdx],rcx     
        mov     qword rcx,[rax+8] 
        mov     qword [rdx+8],rcx     
        push    rdx     
                                        ;;; === pop 1 ===
        pop     rax     
                                        ;;; === pushglobalvec ===
        push    r12     
                                        ;;; === pushaddr 3 ===
        pop     rax     
        mov     qword rdx,[rax+8] 
        push    qword [rdx+32]
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
                                        ;;; === mkfunval lambda_1 ===
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
        mov     qword [rax],lambda_1
        pop     qword [rax+8]
        push    rdx     
                                        ;;; === jump  end_lambda_1 ===
        jmp     end_lambda_1
lambda_1:         
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
                                        ;;; === loadc 2 ===
        mov     rcx,    qword 2 
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
                                        ;;; === popenv ===
        pop     rax     
        pop     rcx     
        pop     rbp     
        pop     r14     
        pop     r12     
        push    rax     
        jmp     rcx     
end_lambda_1:         
                                        ;;; === rewrite ===
        pop     rax     
        pop     rdx     
        mov     qword rcx,[rax]   
        mov     qword [rdx],rcx     
        mov     qword rcx,[rax+8] 
        mov     qword [rdx+8],rcx     
        push    rdx     
                                        ;;; === pop 1 ===
        pop     rax     
                                        ;;; === pushglobalvec ===
        push    r12     
                                        ;;; === pushaddr 0 ===
        pop     rax     
        mov     qword rdx,[rax+8] 
        push    qword [rdx+8]
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
                                        ;;; === mkfunval lambda_2 ===
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
        mov     qword [rax],lambda_2
        pop     qword [rax+8]
        push    rdx     
                                        ;;; === jump  end_lambda_2 ===
        jmp     end_lambda_2
lambda_2:         
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
                                        ;;; === loadc 3 ===
        mov     rcx,    qword 3 
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
                                        ;;; === popenv ===
        pop     rax     
        pop     rcx     
        pop     rbp     
        pop     r14     
        pop     r12     
        push    rax     
        jmp     rcx     
end_lambda_2:         
                                        ;;; === rewrite ===
        pop     rax     
        pop     rdx     
        mov     qword rcx,[rax]   
        mov     qword [rdx],rcx     
        mov     qword rcx,[rax+8] 
        mov     qword [rdx+8],rcx     
        push    rdx     
                                        ;;; === pop 1 ===
        pop     rax     
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
                                        ;;; === rewriteloc 1 ===
        mov     qword rdx,[rsp+8] 
        pop     rax     
        mov     qword rcx,[rax]   
        mov     qword [rdx],rcx     
        mov     qword rcx,[rax+8] 
        mov     qword [rdx+8],rcx     
        push    rdx     
                                        ;;; === pop 1 ===
        pop     rax     
                                        ;;; === pushglobalvec ===
        push    r12     
                                        ;;; === pushaddr 2 ===
        pop     rax     
        mov     qword rdx,[rax+8] 
        push    qword [rdx+24]
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
                                        ;;; === rewrite ===
        pop     rax     
        pop     rdx     
        mov     qword rcx,[rax]   
        mov     qword [rdx],rcx     
        mov     qword rcx,[rax+8] 
        mov     qword [rdx+8],rcx     
        push    rdx     
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
while_0:         
                                        ;;; === pushlocal 1 ===
        push    qword [rsp + 8]
                                        ;;; === getbasic ===
        pop     rax     
        mov     rcx,    [rax+8] 
        push    qword [rcx]
                                        ;;; === loadc 3 ===
        mov     rcx,    qword 3 
        push    rcx     
        pop     rcx     
        pop     rax     
        cmp     rax,    rcx     
        setl    al      
        movzx   rax,    al              ; store result of compare in rax
        push    rax     
                                        ;;; === jumpz  endwhile_0 ===
        pop     rax                     ; delete result of compare operation
        cmp     rax,    0       
        je      endwhile_0
do_0:           
                                        ;;; === pop 1 ===
        pop     rax     
                                        ;;; === pushglobalvec ===
        push    r12     
                                        ;;; === pushaddr 2 ===
        pop     rax     
        mov     qword rdx,[rax+8] 
        push    qword [rdx+24]
                                        ;;; === pushglobalvec ===
        push    r12     
                                        ;;; === pushaddr 2 ===
        pop     rax     
        mov     qword rdx,[rax+8] 
        push    qword [rdx+24]
                                        ;;; === getbasic ===
        pop     rax     
        mov     rcx,    [rax+8] 
        push    qword [rcx]
ite_0:          
                                        ;;; === pushlocal 2 ===
        push    qword [rsp + 16]
                                        ;;; === getbasic ===
        pop     rax     
        mov     rcx,    [rax+8] 
        push    qword [rcx]
                                        ;;; === loadc 0 ===
        mov     rcx,    qword 0 
        push    rcx     
        pop     rcx     
        pop     rax     
        cmp     rax,    rcx     
        sete    al      
        movzx   rax,    al              ; store result of compare in rax
        push    rax     
                                        ;;; === jumpz  else_0 ===
        pop     rax                     ; delete result of compare operation
        cmp     rax,    0       
        je      else_0  
then_0:         
                                        ;;; === loadc 1 ===
        mov     rcx,    qword 1 
        push    rcx     
                                        ;;; === jump  endite_0 ===
        jmp     endite_0
else_0:         
ite_1:          
                                        ;;; === pushlocal 2 ===
        push    qword [rsp + 16]
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
        sete    al      
        movzx   rax,    al              ; store result of compare in rax
        push    rax     
                                        ;;; === jumpz  else_1 ===
        pop     rax                     ; delete result of compare operation
        cmp     rax,    0       
        je      else_1  
then_1:         
                                        ;;; === loadc 3 ===
        mov     rcx,    qword 3 
        push    rcx     
                                        ;;; === jump  endite_1 ===
        jmp     endite_1
else_1:         
                                        ;;; === loadc 5 ===
        mov     rcx,    qword 5 
        push    rcx     
endite_1:         
endite_0:         
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
                                        ;;; === rewrite ===
        pop     rax     
        pop     rdx     
        mov     qword rcx,[rax]   
        mov     qword [rdx],rcx     
        mov     qword rcx,[rax+8] 
        mov     qword [rdx+8],rcx     
        push    rdx     
                                        ;;; === pop 1 ===
        pop     rax     
                                        ;;; === pushlocal 0 ===
        push    qword [rsp + 0]
                                        ;;; === pushlocal 1 ===
        push    qword [rsp + 8]
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
                                        ;;; === rewrite ===
        pop     rax     
        pop     rdx     
        mov     qword rcx,[rax]   
        mov     qword [rdx],rcx     
        mov     qword rcx,[rax+8] 
        mov     qword [rdx+8],rcx     
        push    rdx     
                                        ;;; === jump  while_0 ===
        jmp     while_0 
endwhile_0:         
                                        ;;; === slide 1 ===
        pop     rax     
        add     rsp,    8       
        push    rax     
                                        ;;; === pop 1 ===
        pop     rax     
                                        ;;; === pushglobalvec ===
        push    r12     
                                        ;;; === pushaddr 2 ===
        pop     rax     
        mov     qword rdx,[rax+8] 
        push    qword [rdx+24]
                                        ;;; === getbasic ===
        pop     rax     
        mov     rcx,    [rax+8] 
        push    qword [rcx]
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
