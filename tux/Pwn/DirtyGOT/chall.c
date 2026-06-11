#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main() {
    char buf[0x100];
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    while (1) {
        ssize_t n = read(0, buf, sizeof(buf) - 1);
        if (n <= 0) break;
        buf[n] = '\0';
        printf(buf);
    }

    return 0;
}
