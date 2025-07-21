#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdlib.h>

// ****************************************************************  //
// ************************ Transposition Cipher *****************  //
// *************************************************************** //
// *******What i did: Made a double array to identify indexes**** //
// *******base on GFG visualization******************************//
// ***********************************************************  //

// global vars
#define MAX_VALUE 100
unsigned char key[MAX_VALUE];
int *mappedKey;


// function prottype
void encrypt(const unsigned char* plainText, unsigned char* encrypted);
void decrypt(const unsigned char* encrypted, unsigned char* decrypted);
void map_encryption_key();

int main() {
    unsigned char plainText[MAX_VALUE];
    unsigned char encrypted[MAX_VALUE];
    unsigned char decrypted[MAX_VALUE];

    while (1) {
        printf("========== Transpositional Cryptograph ==========\n");
        printf("Enter a value to encrypt (or 'exit' to quit): ");
        fgets(plainText, MAX_VALUE, stdin);
        plainText[strcspn(plainText, "\n")] = '\0';
        
        if (strcmp(plainText, "exit") == 0) return 0;
        
        printf("Enter a key (words) to be used to encrypt/decrypt: ");
        fgets(key, MAX_VALUE, stdin);
        key[strcspn(key, "\n")] = '\0';
        
        map_encryption_key();
        
        encrypt(plainText, encrypted);
        printf("\nEncrypted: %s\n", encrypted);

        decrypt(encrypted, decrypted);
        printf("Decrypted: %s\n", decrypted);

        printf("=========================================\n\n");
    }

    return 0;
}

void map_encryption_key(){
    // init map key for encrpytion and decryption
    int keyLen = strlen(key);
    mappedKey = malloc(sizeof(int) * keyLen);
    
    for (int i = 0; i < keyLen; i++) mappedKey[i] = i;

    // sort based on key unsigned characters (asc order)
    for (int i = 0; i < keyLen - 1; i++) {
        for (int j = i + 1; j < keyLen; j++) {
            if (key[mappedKey[i]] > key[mappedKey[j]]) {
                int temp = mappedKey[i];
                mappedKey[i] = mappedKey[j];
                mappedKey[j] = temp;
            }
        }
    }
}

void encrypt(const unsigned char* plainText, unsigned char* encrypted) {
    int plainTxtLen = strlen(plainText);
    int keyLen = strlen(key);
    int rows = (plainTxtLen + keyLen - 1) / keyLen;

    // init matrix
    unsigned char matrix[rows][keyLen];
    int idx = 0;
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < keyLen; j++) {
            if (idx < plainTxtLen) {
                matrix[i][j] = plainText[idx++];
            } else {
                matrix[i][j] = ' ';
            }
        }
    }

    // encrypt
    idx = 0;
    for (int k = 0; k < keyLen; k++) {
        int col = mappedKey[k];
        for (int i = 0; i < rows; i++) {
            encrypted[idx++] = matrix[i][col];
        }
    }

    encrypted[idx] = '\0';
}


void decrypt(const unsigned char* encrypted, unsigned char* decrypted) {
    int encryptedLen = strlen(encrypted);
    int keyLen = strlen(key);
    int rows = (encryptedLen + keyLen - 1) / keyLen;

    // init matrix
    unsigned char matrix[rows][keyLen];
    int idx = 0;

    for (int k = 0; k < keyLen; k++) {
        int col = mappedKey[k];
        for (int i = 0; i < rows; i++) {
            if (idx < encryptedLen) {
                matrix[i][col] = encrypted[idx++];
            } else {
                matrix[i][col] = ' ';
            }
        }
    }

    // decrypt
    idx = 0;
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < keyLen; j++) {
            decrypted[idx++] = matrix[i][j];
        }
    }

    decrypted[encryptedLen] = '\0';
}
