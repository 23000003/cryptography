#ifndef AESHEADERS_H
#define AESHEADERS_H

#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>

#define BLOCK_SIZE 16
#define SBOX_SIZE 256
#define NUMBER_OF_ROUNDS 10
#define MATRIX_SIZE 4

extern uint8_t key[BLOCK_SIZE];

// aes core funcs
void encrypt(const uint8_t* plainText, uint8_t* encrypted);
void decrypt(const uint8_t* encrypted, uint8_t* decrypted);

// encryption
void shift_rows(uint8_t state[MATRIX_SIZE][MATRIX_SIZE]);
void mix_columns(uint8_t state[MATRIX_SIZE][MATRIX_SIZE]);

//decryption
void inv_shift_rows(uint8_t state[MATRIX_SIZE][MATRIX_SIZE]);
void inv_mix_columns(uint8_t state[MATRIX_SIZE][MATRIX_SIZE]);
uint8_t gal_mul(uint8_t a, uint8_t b); // helper for IMC

// common aes funcs
void sub_bytes(uint8_t state[MATRIX_SIZE][MATRIX_SIZE], const uint8_t dcrypt_encrypt_sbox[SBOX_SIZE]);
void add_round_key(uint8_t state[MATRIX_SIZE][MATRIX_SIZE], const uint8_t* roundKey);

// utilities
void print_block(const uint8_t* block);
void load_state(uint8_t state[MATRIX_SIZE][MATRIX_SIZE], const uint8_t* input);
void store_state(const uint8_t state[MATRIX_SIZE][MATRIX_SIZE], uint8_t* output);

// main inputs
void get_plain_text(uint8_t* plainText);
void get_key(uint8_t* key);

#endif