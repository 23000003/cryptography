#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include "transvernamaes.h"

unsigned char key[MAX_VALUE];

int hashContent(const unsigned char *input){
    int sum = 0;
	for (int i = 0; input[i] != '\0'; ++i)
        sum += (int)input[i];
    int len = strlen(input);
    return (sum % 1000) + (len * 7);
}

void determineOrder(int *order, const unsigned char *key, int operation){
    int totalSum = 0;

    for(int i = 0; i < strlen(key); i++){
        totalSum += key[i];
    }

    for(int i = 0; i < TOTAL_PROCESS; i++){
        order[i] = totalSum % TOTAL_PROCESS;
        totalSum++;
    }

    if(operation == 2) { // decrypt
        int temp[TOTAL_PROCESS];
        int end = TOTAL_PROCESS - 1;
        for(int i = 0; i < TOTAL_PROCESS; i++) {
            temp[i] = order[end];
            end--;
        }
        memcpy(order, temp, TOTAL_PROCESS * sizeof(int));
    }
}

void startProgram(const unsigned char *input, unsigned char *output, size_t fileContentLen) {
	
    int encDecOrder[3];
    int operation;

    printf("Enter a key to encrypt/decrypt: ");
    fgets(key, MAX_VALUE, stdin);
    key[strcspn(key, "\n")] = '\0';

    while(1){
        printf("Would you like to encrypt/decrypt\n");
        printf("Enter: 1 - Encrypt | 2 - Decrypt: ");
        scanf("%d", &operation);

        if(operation == 1 || operation == 2){
            break;
        } else {
            printf("Wrong operation!");
        }
    }
    
    determineOrder(encDecOrder, key, operation);
    encryptAndDecrypt(input, output, encDecOrder, operation, fileContentLen);
}

void encryptAndDecrypt(const unsigned char *input, unsigned char *output, int *order, int operation, size_t fileContentLen) {

    size_t currentLength = fileContentLen;
    unsigned char storeOutputState[MAX_LEN];
    unsigned char storeCipherState[MAX_LEN];

    memcpy(storeCipherState, input, fileContentLen);

    if(operation == 1) {
        printf("\n===================================================");
        printf("\nHash value: %d\n", hashContent(input));
        printf("===================================================\n");
    } else {
        // Call AES
    }

    for(int i = 0; i < TOTAL_PROCESS; i++){
        switch(order[i]) {
            case 0:
                printf("\n\nTRANSPOSITIONAL %s\n\n", storeCipherState);
                map_encryption_key();
                if(operation == 1){
                    encryptTranspositional(storeCipherState, storeOutputState, currentLength);
                    printf("Cipher Output: %s\n", storeOutputState);
                } else {
                    decryptTranspositional(storeCipherState, storeOutputState, currentLength);
                }
                currentLength = strlen(storeOutputState);
                memcpy(storeCipherState, storeOutputState, currentLength);
                // call your transpositional encrypt/decrypt with fileContentLen, not MAX_LEN
                break;
            case 1:
                printf("\n\nVERNAM %s\n\n", storeCipherState);
                // if(operation == 1){
                //     vernamEncrypt(storeCipherState, storeOutputState, fileContentLen);
                // } else {
                //     vernamDecrypt(storeCipherState, storeOutputState, fileContentLen);
                // }
                // Copy only fileContentLen bytes
                // memcpy(storeCipherState, storeOutputState, fileContentLen);

                printf("\n");

                break;
            case 2:
                printf("\n\nRSA\n\n");
                // Add RSA encrypt/decrypt with length
                break;
        }
    }

    if(operation == 1) {
        // Call AES
    }

    // Finally copy only fileContentLen bytes to output buffer
    printf("\nFinal output length: %zu bytes\n", currentLength);
    printf("Cipher: %s\n", storeCipherState);
    memcpy(output, storeCipherState, currentLength);
    printf("Output: %s\n", output);

    if(operation == 2) {
        printf("\n===================================================");
        printf("\nHash value: %d\n", hashContent(output));
        printf("===================================================\n");
    }
}
