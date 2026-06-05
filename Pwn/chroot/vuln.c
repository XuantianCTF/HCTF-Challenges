#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    printf("sandbox is starting...\n");

    // 漏洞点：执行了 chroot，但没有执行 chdir("/")
    if (chroot("/tmp/sandbox") != 0) {
        perror("fail");
        return 1;
    }

    printf("success, work dir is /tmp/sandbox\n");
    printf("Here is a shell\n");

    system("/bin/sh");

    return 0;
}
