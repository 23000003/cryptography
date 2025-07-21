#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include "aesheaders.h"

void startAES() {
    uint8_t plainText[BLOCK_SIZE];
    uint8_t encrypted[BLOCK_SIZE];
    uint8_t decrypted[BLOCK_SIZE];

    get_key(key);
    get_plain_text(plainText);

    printf("Plain Text: ");
    print_block(plainText);

    encrypt(plainText, encrypted);
    printf("Encrypted: ");
    print_block(encrypted);

    decrypt(encrypted, decrypted);
    printf("Decrypted: ");
    print_block(decrypted);
}