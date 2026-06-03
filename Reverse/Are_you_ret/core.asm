default rel

section .data
    encrypted_flag db 0x71, 0x7b, 0x67, 0x61, 0x41, 0x43, 0x0d, 0x5f
                   db 0x4f, 0x4f, 0x1e, 0x5d, 0x44, 0x71, 0x3c, 0x7c
    flag_len equ 16
    key1 db "dret_obfu_2026", 0
    key2 db "secret_key_2026", 0

section .bss
    decrypted resb 64

section .text
    global check_flag
    global xor_flag

strlen:
    xor eax, eax
.loop:
    cmp byte [rdi + rax], 0
    je .done
    inc rax
    jmp .loop
.done:
    ret

check_flag:
    push rbp
    mov rbp, rsp
    sub rsp, 8
    push rbx
    push r12
    push r13

    mov r12, rdi

    call strlen
    cmp rax, flag_len
    jne .fail

    lea rdi, [key2]
    call strlen
    mov r13, rax

    xor ebx, ebx
.loop_check:
    cmp ebx, flag_len
    jge .success

    mov eax, ebx
    xor edx, edx
    div r13d
    movzx ecx, byte [key2 + rdx]
    movzx eax, byte [r12 + rbx]
    xor al, cl
    cmp al, byte [encrypted_flag + rbx]
    jne .fail

    inc ebx
    jmp .loop_check

.success:
    mov eax, 1
    jmp .done

.fail:
    xor eax, eax

.done:
    pop r13
    pop r12
    pop rbx
    leave
    ret

xor_flag:
    push rbp
    mov rbp, rsp
    push rbx
    push r12
    push r13

    mov r12, rdi

    call strlen
    mov r13, rax

    lea rdi, [key1]
    call strlen
    mov rbx, rax

    xor ecx, ecx
.loop_xor:
    cmp ecx, r13d
    jge .done_xor

    mov eax, ecx
    xor edx, edx
    div ebx
    movzx eax, byte [key1 + rdx]
    movzx edx, byte [r12 + rcx]
    xor al, dl
    mov byte [decrypted + rcx], al

    inc ecx
    jmp .loop_xor

.done_xor:
    mov byte [decrypted + r13], 0

    pop r13
    pop r12
    pop rbx
    leave
    lea rdi, [decrypted]
    push check_flag
    ret
