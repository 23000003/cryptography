#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include "transvernamaes.h"

int letterToNumber(char c) {
    return tolower(c) - 'a' + 1;
}

char numberToLetter(int n, int isUpper) {
    char base = isUpper ? 'A' : 'a';
    return base + (n - 1);
}

void convertBinary(int num, int bin[8]) {
    int j;
	for (j = 0; j < 8; ++j) {
        bin[7 - j] = (num >> j) & 1;
    }
}

int convertDecimal(int bin[8]) {
    int num = 0, i;
    for (i = 0; i < 8; ++i) {
        num = (num << 1) | bin[i];
    }
    return num;
}

void printBinary(int bin[8]) {
    int i;
	for (i = 0; i < 8; ++i)
        printf("%d", bin[i]);
}

int simpleHash(const char* str) {
    int sum = 0, i;
    for (i = 0; str[i] != '\0'; ++i)
        sum += (int)str[i];
    int len = strlen(str);
    return (sum % 1000) + (len * 7);
}

void vernamEncrypt(const char* input, const char* key, char* output, int* xorDecimal) {
    int len = strlen(input), i, j;
    int key_len = strlen(key);
    int bin1[8], bin2[8], result[8];

    printf("\nENCRYPTION PROCESS:\n");
    for (i = 0; i < len; ++i) {
        char ch = input[i];
        char kch = key[i % key_len];

        if (isalpha(ch) && isalpha(kch)) {
            int isUpper = isupper(ch);
            int num1 = letterToNumber(ch);
            int num2 = letterToNumber(kch);

            convertBinary(num1, bin1);
            convertBinary(num2, bin2);

            for (j = 0; j < 8; ++j) {
                result[j] = bin1[j] ^ bin2[j];
            }

            int value = convertDecimal(result);
            xorDecimal[i] = value;

            if (value >= 1 && value <= 26)
                output[i] = numberToLetter(value, isUpper);
            else
                output[i] = '?';

            printf("Plain[%c] (%2d): ", ch, num1); printBinary(bin1);
            printf(" | Key[%c] (%2d): ", kch, num2); printBinary(bin2);
            printf(" | XOR: "); printBinary(result);
            printf(" => Dec: %3d Hex: 0x%02X => Encrypted: %c\n", value, value, output[i]);

        } else {
            output[i] = ch;
            xorDecimal[i] = -1;
            printf("Non-letter or unmatched input/key at position %d: '%c' preserved as is.\n", i, ch);
        }
    }
    output[len] = '\0';
}

void vernamDecrypt(const int* xorDecimal, const char* key, const char* original, char* output) {
    int len = strlen(original);
    int key_len = strlen(key);
    int bin1[8], bin2[8], result[8];

    printf("\nDECRYPTION PROCESS:\n");
    int i, j;
	for (i = 0; i < len; ++i) {
        char kch = key[i % key_len];

        if (xorDecimal[i] != -1 && isalpha(kch)) {
            int isUpper = isupper(original[i]);
            int num2 = letterToNumber(kch);
            convertBinary(xorDecimal[i], bin1);
            convertBinary(num2, bin2);

            for (j = 0; j < 8; ++j) {
                result[j] = bin1[j] ^ bin2[j];
            }

            int value = convertDecimal(result);

            if (value >= 1 && value <= 26)
                output[i] = numberToLetter(value, isUpper);
            else
                output[i] = '?';

            printf("XOR Dec: %3d Hex: 0x%02X: ", xorDecimal[i], xorDecimal[i]); printBinary(bin1);
            printf(" ^ Key[%c] (%2d): ", kch, num2); printBinary(bin2);
            printf(" => Orig: "); printBinary(result);
            printf(" => Dec: %2d => Decrypted: %c\n", value, output[i]);

        } else {
            output[i] = original[i];
            printf("Non-letter or preserved character at position %d: '%c'\n", i, original[i]);
        }
    }
    output[len] = '\0';
}

// int main() {
//     char text[MAX_LEN], key[MAX_LEN];
//     char encrypted[MAX_LEN], decrypted[MAX_LEN];
//     int xorDecimal[MAX_LEN];

//     printf("Enter text: ");
//     fgets(text, sizeof(text), stdin);
//     text[strcspn(text, "\n")] = 0;

//     printf("Enter key (can be shorter, will repeat if needed): ");
//     fgets(key, sizeof(key), stdin);
//     key[strcspn(key, "\n")] = 0;

//     if (strlen(key) == 0) {
//         printf("Error: Key cannot be empty.\n");
//         return 1;
//     }

//     int originalHash = simpleHash(text);
//     vernamEncrypt(text, key, encrypted, xorDecimal);
//     printf("\nEncrypted Output: %s\n", encrypted);

//     vernamDecrypt(xorDecimal, key, text, decrypted);
//     printf("\nDecrypted Output: %s\n", decrypted);

//     int decryptedHash = simpleHash(decrypted);

//     printf("\nOriginal Hash:  %d\n", originalHash);
//     printf("Decrypted Hash: %d\n", decryptedHash);

//     if (originalHash == decryptedHash)
//         printf("Hash Match: ?\n");
//     else
//         printf("Hash Mismatch ?\n");

//     return 0;
// }
