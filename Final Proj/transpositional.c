#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdlib.h>
#include "transvernamaes.h"

void map_encryption_key(){
    // init map key for encrpytion and decryption
    int keyLen = strlen(key);
    mappedKey = malloc(sizeof(int) * keyLen);
    
    int i, j;
    
    for (i = 0; i < keyLen; i++) mappedKey[i] = i;

    // sort based on key characters (asc order)
    for (i = 0; i < keyLen - 1; i++) {
        for (j = i + 1; j < keyLen; j++) {
            if (key[mappedKey[i]] > key[mappedKey[j]]) {
                int temp = mappedKey[i];
                mappedKey[i] = mappedKey[j];
                mappedKey[j] = temp;
            }
        }
    }
}

void encrypt(const char* plainText, char* encrypted) {
    int plainTxtLen = strlen(plainText);
    int keyLen = strlen(key);
    int rows = (plainTxtLen + keyLen - 1) / keyLen;

    // init matrix
    char matrix[rows][keyLen];
    int idx = 0, i, j, k;
    for (i = 0; i < rows; i++) {
        for (j = 0; j < keyLen; j++) {
            if (idx < plainTxtLen) {
                matrix[i][j] = plainText[idx++];
            } else {
                matrix[i][j] = ' ';
            }
        }
    }

    // encrypt
    idx = 0;
    for (k = 0; k < keyLen; k++) {
        int col = mappedKey[k];
        for (i = 0; i < rows; i++) {
            encrypted[idx++] = matrix[i][col];
        }
    }

    encrypted[idx] = '\0';
}


void decrypt(const char* encrypted, char* decrypted) {
    int encryptedLen = strlen(encrypted);
    int keyLen = strlen(key);
    int rows = (encryptedLen + keyLen - 1) / keyLen;

    // init matrix
    char matrix[rows][keyLen];
    int idx = 0, k, i, j;

    for (k = 0; k < keyLen; k++) {
        int col = mappedKey[k];
        for (i = 0; i < rows; i++) {
            if (idx < encryptedLen) {
                matrix[i][col] = encrypted[idx++];
            } else {
                matrix[i][col] = ' ';
            }
        }
    }

    // decrypt
    idx = 0;
    for (i = 0; i < rows; i++) {
        for (j = 0; j < keyLen; j++) {
            decrypted[idx++] = matrix[i][j];
        }
    }

    decrypted[encryptedLen] = '\0';
}
