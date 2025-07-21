#ifndef TRANSVERNAMAES_H
#define TRANSVERNAMAES_H

#define MAX_LEN 500
#define MAX_VALUE 100
#define TOTAL_PROCESS 3

// global vars Trans
extern unsigned char key[MAX_VALUE];
extern unsigned int *mappedKey;

// Vernam
void vernamEncrypt(const unsigned char *input, unsigned char *output, size_t len);
void vernamDecrypt(const unsigned char *input, unsigned char *output, size_t len);

// Trans
void encryptTranspositional(const unsigned char* plainText, unsigned char* encrypted, size_t fileContentLen);
void decryptTranspositional(const unsigned char* encrypted, unsigned char* decrypted, size_t fileContentLen);
void map_encryption_key();

// AES


// submain
int hashContent(const unsigned char *input);
void startProgram(const unsigned char *input, unsigned char *output, size_t fileContentLen);
void determineOrder(int *order, const unsigned char *key, int operation);
void encryptAndDecrypt(const unsigned char *input, unsigned char *output, int *order, int operation, size_t fileContentLen);

#endif
