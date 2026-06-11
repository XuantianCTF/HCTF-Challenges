#include <stdio.h>
#include <stdint.h>
#include <string.h>

#define DELTA 0x9E3779B9u
#define FLAG_LEN 24
#define ENC_LEN 24
#define MAX_INPUT 128

static const uint32_t tea_key[4] = {
    11, 45, 14, 91
};

static const unsigned char encrypted_flag[ENC_LEN] = {
    0xA0, 0x2B, 0x3C, 0xEF, 0x87, 0x59, 0x20, 0x86,
    0xA1, 0x36, 0xDD, 0x95, 0x76, 0x0D, 0x9B, 0x9F,
    0x60, 0xB0, 0x32, 0x1A, 0xEC, 0x53, 0x1F, 0x03
};

static uint32_t get_u32(const unsigned char *p) {
    return ((uint32_t)p[0]) |
           ((uint32_t)p[1] << 8) |
           ((uint32_t)p[2] << 16) |
           ((uint32_t)p[3] << 24);
}

static void put_u32(unsigned char *p, uint32_t v) {
    p[0] = (unsigned char)(v);
    p[1] = (unsigned char)(v >> 8);
    p[2] = (unsigned char)(v >> 16);
    p[3] = (unsigned char)(v >> 24);
}

static void tea_encrypt_block(unsigned char *block) {
    uint32_t v0 = get_u32(block);
    uint32_t v1 = get_u32(block + 4);
    uint32_t sum = 0;
    int i;

    for (i = 0; i < 32; i++) {
        sum += DELTA;
        v0 += ((v1 << 4) + tea_key[0]) ^ (v1 + sum) ^ ((v1 >> 5) + tea_key[1]);
        v1 += ((v0 << 4) + tea_key[2]) ^ (v0 + sum) ^ ((v0 >> 5) + tea_key[3]);
    }

    put_u32(block, v0);
    put_u32(block + 4, v1);
}

static void tea_encrypt(unsigned char *data) {
    int i;

    for (i = 0; i < ENC_LEN; i += 8) {
        tea_encrypt_block(data + i);
    }
}

int main(void) {
    char input[MAX_INPUT];
    unsigned char buf[ENC_LEN];
    size_t len;

    printf("Enter flag: ");

    if (scanf("%127s", input) != 1) {
        puts("error, do you know D810?");
        return 0;
    }

    len = strlen(input);

    if (len != FLAG_LEN) {
        puts("error, do you know D810?");
        return 0;
    }

    memcpy(buf, input, FLAG_LEN);
    tea_encrypt(buf);

    if (memcmp(buf, encrypted_flag, ENC_LEN) == 0) {
        puts("correct, D810 is cool!");
    } else {
        puts("error, do you know D810?");
    }

    return 0;
}