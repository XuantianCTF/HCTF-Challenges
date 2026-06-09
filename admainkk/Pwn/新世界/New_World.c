#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/prctl.h>
#include <seccomp.h>

int init();
int inquire();
static void install_seccomp(void);
int IO();
int New_World();
void *p = NULL;

int main()
{

    IO();
    void *addr = (void *)0x1337000;

    p = mmap(
        addr,
        0x1000,
        PROT_READ | PROT_WRITE | PROT_EXEC,
        MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED,
        -1,
        0);

    if (p == MAP_FAILED)
    {
        perror("mmap");
        return 1;
    }
    New_World();
    return 0;
}

int init()
{
    char a[0x18];
    char key[0x18];

    printf("Stop your footsteps, stop...Stop..........\n");
    read(0, key, 0x60);

    return 0;
}

int inquire()
{
    printf("Welcome to the New World!\n");
    read(0, p, 4);

    ((char *)p)[4] = '\0';
    ((char *)p)[5] = '\0';
    ((char *)p)[6] = '\0';
    ((char *)p)[7] = '\0';
    ((char *)p)[8] = '\0';
    ((char *)p)[9] = '\0';
    ((char *)p)[10] = '\0';

    printf("Yes, there is %s\n", (char *)p);

    return 0;
}

static void install_seccomp(void)
{
    if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0))
    {
        perror("prctl");
        exit(1);
    }

    scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_ALLOW);
    if (!ctx)
    {
        perror("seccomp_init");
        exit(1);
    }

    seccomp_rule_add(ctx, SCMP_ACT_KILL_PROCESS, SCMP_SYS(execve), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL_PROCESS, SCMP_SYS(execveat), 0);

    if (seccomp_load(ctx) < 0)
    {
        perror("seccomp_load");
        exit(1);
    }

    seccomp_release(ctx);
}

int IO()
{
    install_seccomp();
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);
    return 0;
}

int New_World()
{
    char b[3];
    ssize_t n;

    inquire();
    printf("Do you want to stay in the new world? (y/no)\n");

    n = read(0, b, 1);
    b[1] = '\0';

    if (strcmp(b, "y") == 0)
    {
        init();
    }
    else
        printf("You have entered the new world.\n");

    return 0;
}
