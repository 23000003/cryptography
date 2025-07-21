#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <ctype.h>
#include "transvernamaes.h"

// --- Greatest Common Divisor ---
long long int gcd(long long int a, long long int b) {
    while (b != 0) {
        long long int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

// --- Modular Inverse using Extended Euclidean Algorithm ---
long long int modInverse(long long int e, long long int tot) {
    long long int t = 0, newT = 1;
    long long int r = tot, newR = e;

    while (newR != 0) {
        long long int quotient = r / newR;
        long long int tempT = newT;
        newT = t - quotient * newT;
        t = tempT;

        long long int tempR = newR;
        newR = r - quotient * newR;
        r = tempR;
    }

    if (r > 1) return -1; // No inverse
    if (t < 0) t += tot;
    return t;
}

// --- Modular Exponentiation ---
long long int modPow(long long int base, long long int exp, long long int mod) {
    long long int result = 1;
    base %= mod;

    while (exp > 0) {
        if (exp % 2 == 1)
            result = (result * base) % mod;
        exp /= 2;
        base = (base * base) % mod;
    }
    return result;
}

// --- Key Generation ---
RSAKey generateRSAKey(long long int p, long long int q) {
    RSAKey key;
    key.N = p * q;
    long long int tot = (p - 1) * (q - 1);

    key.e = 3;
    while (gcd(key.e, tot) != 1)
        key.e += 2;

    key.d = modInverse(key.e, tot);
    return key;
}

// --- Encrypt Function ---
void encrypt(const char* input, long long int* encrypted, RSAKey rsaKey) {
    int i;
    for (i = 0; input[i] != '\0'; ++i) {
        int m = (unsigned char)input[i];  // full byte range
        encrypted[i] = modPow(m, rsaKey.e, rsaKey.N);
    }
    encrypted[i] = -1; // end marker
}

void decrypt(const long long int* encrypted, char* output, RSAKey rsaKey) {
    int i;
    for (i = 0; encrypted[i] != -1; ++i) {
        long long int c = encrypted[i];
        long long int m = modPow(c, rsaKey.d, rsaKey.N);
        output[i] = (char)m;
    }
    output[i] = '\0';
}

// // --- Main Program for Testing ---
// int main() {
//     char plain[500], decrypted[500];
//     long long int encrypted[500];
//     long long int p = 47, q = 53;

//     printf("Enter message to encrypt: ");
//     fgets(plain, sizeof(plain), stdin);
//     plain[strcspn(plain, "\n")] = '\0';

//     RSAKey key = generateRSAKey(p, q);
//     printf("\nGenerated Key:\n");
//     printf("Public (e, N): (%lld, %lld)\n", key.e, key.N);
//     printf("Private (d, N): (%lld, %lld)\n", key.d, key.N);

//     encrypt(plain, encrypted, key);
//     printf("\nEncrypted: ");
//     for (int i = 0; encrypted[i] != -1; ++i)
//         printf("%lld ", encrypted[i]);

//     decrypt(encrypted, decrypted, key);
//     printf("\nDecrypted: %s\n", decrypted);

//     return 0;
// }