default rel

section .data
    prompt db "请输入 Flag: "
    prompt_len equ $ - prompt
    success db "恭喜！Flag 正确。", 0x0a
    success_len equ $ - success
    fail db "验证失败，请再试一次。", 0x0a
    fail_len equ $ - fail

section .bss
    input resb 64

section .text
    global _start
    extern secure_check

_start:
    mov eax, 1
    mov edi, 1
    lea rsi, [prompt]
    mov edx, prompt_len
    syscall

    xor edi, edi
    lea rsi, [input]
    mov edx, 63
    xor eax, eax
    syscall

    dec rax
    mov byte [input + rax], 0

    lea rdi, [input]
    call secure_check

    test al, al
    jnz .success

    mov eax, 1
    mov edi, 1
    lea rsi, [fail]
    mov edx, fail_len
    syscall
    jmp .exit

.success:
    mov eax, 1
    mov edi, 1
    lea rsi, [success]
    mov edx, success_len
    syscall

.exit:
    mov eax, 60
    xor edi, edi
    syscall
