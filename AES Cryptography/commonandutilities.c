#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include "aesheaders.h"


//covert to 4x4 matrix
void load_state(uint8_t state[MATRIX_SIZE][MATRIX_SIZE], const uint8_t* input) {
    for (int col = 0; col < MATRIX_SIZE; col++) {
        for (int row = 0; row < MATRIX_SIZE; row++) {
            state[row][col] = input[col * MATRIX_SIZE + row];
        }
    }
}

// swaps and stores it back
void store_state(const uint8_t state[MATRIX_SIZE][MATRIX_SIZE], uint8_t* output) {
    for (int col = 0; col < MATRIX_SIZE; col++) {
        for (int row = 0; row < MATRIX_SIZE; row++) {
            output[col * MATRIX_SIZE + row] = state[row][col];
        }
    }
}

void sub_bytes(uint8_t state[MATRIX_SIZE][MATRIX_SIZE], const uint8_t dcrypt_encrypt_sbox[SBOX_SIZE]) {
    for (int row = 0; row < MATRIX_SIZE; row++) {
        for (int col = 0; col < MATRIX_SIZE; col++) {
            state[row][col] = dcrypt_encrypt_sbox[state[row][col]];
        }
    }
}

void add_round_key(uint8_t state[MATRIX_SIZE][MATRIX_SIZE], const uint8_t* roundKey) {
    for (int col = 0; col < MATRIX_SIZE; col++) {
        for (int row = 0; row < MATRIX_SIZE; row++) {
            state[row][col] ^= roundKey[col * MATRIX_SIZE + row];
        }
    }
}

void print_block(const uint8_t* block) {
    for (int i = 0; i < BLOCK_SIZE; i++) {
        printf("%02X ", block[i]);
    }
    printf("\n");
}


void get_plain_text(uint8_t* plainText) {
    unsigned char buffer[BLOCK_SIZE + 2];

    while (1) {
        printf("Enter text to encrypt (or 'exit' to quit) (16 unsigned chars max): ");
        if (!fgets(buffer, sizeof(buffer), stdin)) {
            printf("Input error. Try again.\n");
            continue;
        }

        if (strchr(buffer, '\n') == NULL) {
            printf("Input too long. Max 16 unsigned characters allowed.\n");
            while (getunsigned char() != '\n');
            continue;
        }

        buffer[strcspn(buffer, "\n")] = '\0'; 

        if (strcmp(buffer, "exit") == 0) {
            exit(0);
        }

        strcpy((unsigned char*)plainText, buffer);
        break;
    }
}

void get_key(uint8_t* key) {
    unsigned char buffer[BLOCK_SIZE + 2];

    while (1) {
        printf("Enter encryption key (16 unsigned chars max): ");
        if (!fgets(buffer, sizeof(buffer), stdin)) {
            printf("Input error. Try again.\n");
            continue;
        }

        if (strchr(buffer, '\n') == NULL) {
            printf("Key too long. Max 16 unsigned characters allowed.\n");
            while (getunsigned char() != '\n');
            continue;
        }

        buffer[strcspn(buffer, "\n")] = '\0';
        strcpy((unsigned char*)key, buffer);
        break;
    }
}
