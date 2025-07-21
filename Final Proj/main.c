#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include "transvernamaes.h"

#define TOTAL_PROCESS 3


int hashContent(const char *input){
    int sum = 0;
    
	int i;
	for (i = 0; input[i] != '\0'; ++i)
        sum += (int)input[i];
    int len = strlen(input);
    return (sum % 1000) + (len * 7);
}

void determineOrder(int *order, const char *key, int operation){
    int totalSum = 0, i;

    for(i = 0; i < strlen(key); i++){
        totalSum += key[i];
    }

    for(i = 0; i < TOTAL_PROCESS; i++){
        order[i] = totalSum % TOTAL_PROCESS;
        totalSum++;
    }

    if(operation == 2) { // decrypt
        int temp[TOTAL_PROCESS];
        int end = TOTAL_PROCESS - 1;
        for(i = 0; i < TOTAL_PROCESS; i++) {
            temp[i] = order[end];
            end--;
        }
        memcpy(order, temp, TOTAL_PROCESS * sizeof(int));
    }
}

void modifyContent(const char *input, char *output) {
	
    int encDecOrder[3];
    int operation;
    
    printf("Enter a key to encrypt/decrypt");
    fgets(key, MAX_VALUE, stdin);
    key[strcspn(key, "\n")] = '\0';

    while(1){
        printf("Would you like to encrypt/decrypt\n");
        printf("Enter: 1 - Encrypt | 2 - Decrypt");
        scanf("%d", &operation);

        if(operation != 1 || operation != 2){
            printf("Wrong operation!");
        } else {
            break;
        }
    }
    
    determineOrder(encDecOrder, key, operation);
    
    int i;
    for(i = 0; i < TOTAL_PROCESS; i++){
        switch(encDecOrder[i]) {
            case 0:
                map_encryption_key();
                // transpo
                if(operation == 1){
                    //encrypt
                    encryptTranspositional(input, output);
                } else {
                    // decrypt
                    decryptTranspositional(input, output);
                }
                break;
            case 1:
                // vernam
                printf("VERNAM");
                if(operation == 1){
                    //encrypt
                    // vernamEncrypt(input, output)
                } else {
                    // decrypt
                }
                break;
            case 2:
                //RSA
                printf("RSA");
                if(operation == 1){
                    //encrypt
                } else {
                    // decrypt
                }
                break;
        }
    }

    // CALL AES by 
}

int main() {
    
    char filename[MAX_VALUE];
    char newFilename[MAX_VALUE];
    char buffer[MAX_VALUE];
    char modified[MAX_VALUE];

    printf("Enter a file name to encrypt/decrypt: ");
    fgets(filename, sizeof(filename), stdin);
    filename[strcspn(filename, "\n")] = 0;  // remove trailing newline

    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        perror("Error opening file");
        return 1;
    }

    // Read file content
    size_t bytesRead = fread(buffer, 1, MAX_VALUE - 1, file);
    buffer[bytesRead] = '\0';
    fclose(file);


    // ============ encryption decryption ====================
    // Modify the content (e.g., encrypt or decrypt)
    modifyContent(buffer, modified);

    // Ask for new file name or generate one
    snprintf(newFilename, sizeof(newFilename), "%s.modified.txt", filename);

    FILE *newFile = fopen(newFilename, "w");
    if (newFile == NULL) {
        perror("Error creating new file");
        return 1;
    }

    fwrite(modified, 1, strlen(modified), newFile);
    fclose(newFile);

    printf("Modified content written to: %s\n", newFilename);

    return 0;
}


