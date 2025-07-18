#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include "aesheaders.h"


// *************************************************************//
// ****************AES Cryptograph******************** //
// ********************** WHAT I DID *************************** //
// ********I just followed GFG steps and nesoacad YT vid ******* //
// *************************************************************//

uint8_t key[BLOCK_SIZE];

int main() {
    uint8_t* plainText = (uint8_t*)calloc(BLOCK_SIZE + 1, sizeof(uint8_t));
    uint8_t* encrypted  = (uint8_t*)calloc(BLOCK_SIZE + 1, sizeof(uint8_t));
    uint8_t* decrypted  = (uint8_t*)calloc(BLOCK_SIZE + 1, sizeof(uint8_t));

    while (1) {
        printf("========== Kenny's AES Cipher Algorithm ==========\n");

        get_plain_text(plainText);
        get_key(key);

        printf("\nPlain Text: %s\n", plainText);
        printf("Plain Text (Block): ");
        print_block(plainText);

        encrypt(plainText, encrypted);
        printf("\nEncrypted: %s\n", encrypted);
        printf("Encrypted (Block): ");
        print_block(encrypted);

        decrypt(encrypted, decrypted);
        printf("\nDecrypted: %s\n", decrypted);
        printf("Decrypted (Block): ");
        print_block(decrypted);

        printf("======================================\n\n");
    }

    free(plainText);
    free(encrypted);
    free(decrypted);
    return 0;
}
