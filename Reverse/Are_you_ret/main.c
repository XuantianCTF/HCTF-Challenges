#include <stdio.h>
#include <string.h>
#include <stdbool.h>

extern void xor_flag(const char* input);
extern bool secure_check(const char* input);

unsigned char encrypted_flag[] = {
    0x71, 0x7b, 0x67, 0x61, 0x41, 0x43, 0x0d, 0x5f,
    0x4f, 0x4f, 0x1e, 0x5d, 0x44, 0x71, 0x3c, 0x7c
};
const char* key1 = "dret_obfu_2026";
const char* key2 = "secret_key_2026";

bool check_flag(const char* input) {
    __asm__ __volatile__(
    ".intel_syntax noprefix;"
    "sub rsp, 8;"
    ".att_syntax prefix;"
    :
    :
    : "rsp"
    );
    int flag_len = sizeof(encrypted_flag);
    int key_len = strlen(key2);

    if (strlen(input) != flag_len) return false;

    for (int i = 0; i < flag_len; i++) {
        if ((unsigned char)(input[i] ^ key2[i % key_len]) != encrypted_flag[i]) {
            return false;
        }
    }
    return true;
}

void xor_flag(const char* input) {
    static char decrypted[64];
    int len = strlen(input);
    int key1_len = strlen(key1);

    for (int i = 0; i < len; i++) {
        decrypted[i] = input[i] ^ key1[i % key1_len];
    }
    decrypted[len] = '\0';

    __asm__ __volatile__(
        ".intel_syntax noprefix;"
        "leave;"
        "mov rdi, %[buf];"
        "push %[addr];"
        "ret;"
        ".att_syntax prefix;"
        :
        : [buf] "r"(decrypted), [addr] "r"(check_flag)
        : "rdi"
    );
    __builtin_unreachable();
}

int main() {
    char input[64];
    printf("请输入 Flag: ");
    if (scanf("%63s", input) != 1) return 1;

    if (secure_check(input)) {
        printf("恭喜！Flag 正确。\n");
    } else {
        printf("验证失败，请再试一次。\n");
    }
    return 0;
}
