#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include "transvernamaes.h"

void vernamEncrypt(const unsigned char *input, unsigned char *output, size_t len) {
    int keyLen = strlen(key);
    for (int i = 0; i < len; ++i) {
        output[i] = input[i] ^ key[i % keyLen];
    }
}

void vernamDecrypt(const unsigned char *input, unsigned char *output, size_t len) {
    int keyLen = strlen(key);
    for (int i = 0; i < len; ++i) {
        output[i] = input[i] ^ key[i % keyLen];
    }
    output[len] = '\0'; // Properly terminate decrypted string
}
