; 编译命令: nasm -f elf64 logic.asm -o logic.o
section .text
    global secure_check        ; 导出函数给 C 调用
    extern check_flag          ; 导入 C 语言定义的逻辑

secure_check:
    push rbp
    mov rbp, rsp

    mov rax, check_flag
    pop rbp
    push rax
    ret

    mov rax, 0x114514
    leave
    ret
    
