#include <stdio.h>
#include <string.h>
#include <stdbool.h>

// 声明汇编中的外部函数
extern bool secure_check(const char* input);

unsigned char encrypted_flag[] = {
    0x15, 0x09, 0x02, 0x15, 0x1e, 0x2c, 0x6f, 0x39,
    0x3a, 0x10, 0x2c, 0x6d, 0x76, 0x47, 0x58, 0x0e
};
const char* key = "secret_key_2026";

// 这个函数会被汇编代码在“假栈”上调用
bool check_flag(const char* input) {
    // __asm__ __volatile__ (
    // ".intel_syntax noprefix;" // 切换到 Intel 语法
    // "sub rsp, 8;"             // 调整栈指针
    // ".att_syntax prefix;"     // 切换回 AT&T 语法（编译器默认）
    // :                         // 无输出
    // :                         // 无输入
    // : "rsp"                   // 告诉编译器 rsp 被修改了（Clobber list）
    // );
    int flag_len = sizeof(encrypted_flag);
    int key_len = strlen(key);

    if (strlen(input) != flag_len) return false;

    for (int i = 0; i < flag_len; i++) {
        if ((unsigned char)(input[i] ^ key[i % key_len]) != encrypted_flag[i]) {
            return false;
        }
    }
    return true;
}

int main() {
    char input[64];
    printf("请输入 Flag: ");
    if (scanf("%63s", input) != 1) return 1;

    // 调用汇编入口，而非直接调用 check_flag
    if (secure_check(input)) {
        printf("恭喜！Flag 正确。\n");
    } else {
        printf("验证失败，请再试一次。\n");
    }
    return 0;
}
