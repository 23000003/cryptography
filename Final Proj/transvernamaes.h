#ifndef TRANSVERNAMAES_H
#define TRANSVERNAMAES_H

#define MAX_LEN 500

// global vars Trans
#define MAX_VALUE 100
char key[MAX_VALUE];
int *mappedKey;

// Vernam
int letterToNumber(char c);
char numberToLetter(int n, int isUpper);
void convertBinary(int num, int bin[8]);
int convertDecimal(int bin[8]);
void printBinary(int bin[8]);
int simpleHash(const char* str);
void vernamEncrypt(const char* input, const char* key, char* output, int* xorDecimal);
void vernamDecrypt(const int* xorDecimal, const char* key, const char* original, char* output);

// Trans
void encrypt(const char* plainText, char* encrypted);
void decrypt(const char* encrypted, char* decrypted);
void map_encryption_key();

// AES

#endif
