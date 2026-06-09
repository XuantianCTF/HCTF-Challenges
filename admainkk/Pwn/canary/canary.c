#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void win()
{
    system("ls");
}

void gadget()
{
    __asm__("pop %rdi; ret");
}

int main()
{
    char buf[20];
    unsigned long canary;

    setbuf(stdin, NULL);
    setbuf(stdout, NULL);

    // Leak stack canary
    canary = *(unsigned long *)((char *)__builtin_frame_address(0) - 8);
    puts("no /bin/sh");
    printf("canary = 0x%lx\n", canary);

    read(0, buf, 0x40);
    puts("oioioioioioioioioioioioi!");
    return 0;
}
