#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include "transvernamaes.h"

size_t openFile(const unsigned char *filename, unsigned char *buffer, size_t bufferSize) {
    FILE *file = fopen(filename, "rb"); // read binary
    if (file == NULL) {
        perror("Error opening file");
        exit(EXIT_FAILURE);
    }
    
    size_t bytesRead = fread(buffer, 1, bufferSize, file);
    fclose(file);
    return bytesRead;  // return actual size read
}

void createFile(const unsigned char *filename, const unsigned char *content, size_t contentSize) {
    FILE *newFile = fopen(filename, "wb");  // write binary
    if (newFile == NULL) {
        perror("Error creating new file");
        return;
    }

    fwrite(content, 1, contentSize, newFile);
    fclose(newFile);

    printf("Modified content written to: %s\n", filename);
}

int main() {
    unsigned char filename[MAX_VALUE];
    unsigned char newFilename[MAX_VALUE];
    unsigned char buffer[MAX_VALUE];
    unsigned char modified[MAX_VALUE];

    printf("Enter a file name to encrypt/decrypt: ");
    fgets(filename, sizeof(filename), stdin);
    filename[strcspn(filename, "\n")] = 0;  // remove trailing newline

    size_t inputLength = openFile(filename, buffer, sizeof(buffer));

    // start program (encrypt/decrypt)
    // You'll need to modify startProgram and encrypt/decrypt functions to accept length info.
    startProgram(buffer, modified, inputLength);

    // create new file name
    snprintf(newFilename, sizeof(newFilename), "new.txt");

    createFile(newFilename, modified, inputLength);

    return 0;
}


