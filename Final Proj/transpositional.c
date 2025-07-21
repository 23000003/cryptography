#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdlib.h>
#include "transvernamaes.h"

unsigned int *mappedKey;

void map_encryption_key() {
    int keyLen = strlen(key);
    mappedKey = malloc(sizeof(int) * keyLen);

    int i, j;
    for (i = 0; i < keyLen; i++) mappedKey[i] = i;

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

void encryptTranspositional(const unsigned char* plainText, unsigned char* encrypted, size_t fileContentLen) {
    int keyLen = strlen(key);
    int rows = (fileContentLen + keyLen - 1) / keyLen;

    unsigned char matrix[rows][keyLen];
    int idx = 0;

    // Fill matrix, pad with 0 (zero)
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < keyLen; j++) {
            if (idx < fileContentLen) {
                matrix[i][j] = plainText[idx++];
            } else {
                matrix[i][j] = ' ';  // pad with zero byte, safer for binary
            }
        }
    }

    // Read columns in key order
    idx = 0;
    for (int k = 0; k < keyLen; k++) {
        int col = mappedKey[k];
        for (int i = 0; i < rows; i++) {
            encrypted[idx++] = matrix[i][col];
        }
    }
    
    // NO null termination here, encrypted data can contain zero bytes
}



void decryptTranspositional(const unsigned char* encrypted, unsigned char* decrypted, size_t fileContentLen) {
    int keyLen = strlen(key);
    int rows = (fileContentLen + keyLen - 1) / keyLen;

    unsigned char matrix[rows][keyLen];
    int idx = 0;

    // Fill matrix column-wise using mappedKey
    for (int k = 0; k < keyLen; k++) {
        int col = mappedKey[k];
        for (int i = 0; i < rows; i++) {
            if (idx < fileContentLen) {
                matrix[i][col] = encrypted[idx++];
            } else {
                matrix[i][col] = ' ';
            }
        }
    }

    // Read matrix row-wise to get decrypted text
    idx = 0;
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < keyLen; j++) {
            if (idx < fileContentLen) {
                decrypted[idx++] = matrix[i][j];
            }
        }
    }
    // NO null termination here; the caller should handle length explicitly.
}
