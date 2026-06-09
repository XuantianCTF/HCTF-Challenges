#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h> // 修复：引入 read() 需要的头文件
#include <seccomp.h>

void sandbox()
{
    scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_ALLOW);

    // 禁止 execve 和 execveat，防止 system("/bin/sh") / getshell
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(execve), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(execveat), 0);

    seccomp_load(ctx);
}
// 修复：提前声明函数，防止 main 函数找不到它们
int vuln();
int shell();
int IO();

int main()
{
    // 关掉缓冲区，这是 Pwn 题的标准起手式，防止 printf/puts 吞掉输出
    IO();
    shell();
    vuln();
    return 0;
}

int vuln()
{
    char pad[0x1d];
    char buf[11];

    memset(buf, 0, 0x28);
    // IDE 会在这里疯狂警告溢出，请无视它，我们要的就是溢出
    printf("Go!\n");
    read(0, buf, 0x34);
    printf("%s", buf);
    read(0, buf, 0x34);
    return printf("%s", buf);
}

int shell()
{
    // 后门函数
    return system("ls");
}

int IO()
{
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);
    return 0;
}