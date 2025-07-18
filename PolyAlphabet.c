#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

// ************************************************************** //
// ********************** WHAT I DID *************************** //
// I used the formula that was given, take its base to identify //
// if the plain text is capital or small to also convert my key //
// and to shift from its ascii value to 0 - 25 ******************//
// *************************************************************//

#define MAX_VALUE 100
#define TOTAL_IN_ALPHABET 26
#define CAPITAL_ALPHA_ASCII 65
#define SMALL_ALPHA_ASCII 97

char key[MAX_VALUE];

void encrypt(const char* value, char* encrypted);
void decrypt(const char* encrypted, char* decrypted);

int main() {
    char value[MAX_VALUE];
    char encrypted[MAX_VALUE];
    char decrypted[MAX_VALUE];

    while (1) {
        printf("========== PolyAlphabet Cipher ==========\n");
        printf("Enter a value to encrypt (or 'exit' to quit): ");
        fgets(value, MAX_VALUE, stdin);
        value[strcspn(value, "\n")] = '\0';
        
        if (strcmp(value, "exit") == 0) return 0;
        
        printf("Enter a key to be used to encrypt/decrypt: ");
        fgets(key, MAX_VALUE, stdin);
        key[strcspn(key, "\n")] = '\0';
        
        encrypt(value, encrypted);
        printf("\nEncrypted: %s\n", encrypted);

        decrypt(encrypted, decrypted);
        printf("Decrypted: %s\n", decrypted);

        printf("=========================================\n\n");
    }

    return 0;
}

void encrypt(const char* value, char* encrypted) {
    int valLen = strlen(value);
    int keyLen = strlen(key);

    for (int i = 0; i < valLen; i++) {
        char P = value[i];
        char K = key[i % keyLen];

        if (isalpha(P)) {
            char base = isupper(P) ? CAPITAL_ALPHA_ASCII : SMALL_ALPHA_ASCII;
            K = isupper(P) ? toupper(K) : tolower(K);
            P -= base;
            K -= base;

            encrypted[i] = ((P + K) % TOTAL_IN_ALPHABET) + base;
        } else {
            encrypted[i] = P;
        }
    }
    encrypted[valLen] = '\0';
}

void decrypt(const char* encrypted, char* decrypted) {
    int encLen = strlen(encrypted);
    int keyLen = strlen(key);

    for (int i = 0; i < encLen; i++) {
        char C = encrypted[i];
        char K = key[i % keyLen];

        if (isalpha(C)) {
            char base = isupper(C) ? CAPITAL_ALPHA_ASCII : SMALL_ALPHA_ASCII;
            K = isupper(C) ? toupper(K) : tolower(K);
            C -= base;
            K -= base;

            decrypted[i] = ((C - K + TOTAL_IN_ALPHABET) % TOTAL_IN_ALPHABET) + base;
        } else {
            decrypted[i] = C;
        }
    }
    decrypted[encLen] = '\0';
}
