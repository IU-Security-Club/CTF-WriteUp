#include <openssl/evp.h>
#include <stdio.h>
#include <stdlib.h>

void handleErrors(const char *errMsg) {
    fprintf(stderr, "%s\n", errMsg);
    exit(EXIT_FAILURE);
}

int main() {
    FILE *stream, *s;
    /*
    unsigned char v11[32] = {0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF, 
                             0x10, 0x32, 0x54, 0x76, 0x98, 0xBA, 0xDC, 0xFE,
                             0xF0, 0xE1, 0xD2, 0xC3, 0xB4, 0xA5, 0x96, 0x87,
                             0x78, 0x69, 0x5A, 0x4B, 0x3C, 0x2D, 0x1E, 0x0F}; 
    unsigned char v10[16] = {0x00, 0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 
                             0x08, 0x90, 0xA0, 0xB0, 0xC0, 0xD0, 0xE0, 0xF0}; 
    */
                             
	unsigned char v11[32] =
	{
	  0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF, 0x10, 0x32, 
	  0x54, 0x76, 0x98, 0xBA, 0xDC, 0xFE, 0xF0, 0xE1, 0xD2, 0xC3,  // Decryption key
	  0xB4, 0xA5, 0x96, 0x87, 0x78, 0x69, 0x5A, 0x4B, 0x3C, 0x2D, 
	  0x1E, 0x0F
	};
	unsigned char v10[16] =
	{
	  0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09,  // IV
	  0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F
	};

    EVP_CIPHER_CTX *v9;
    const EVP_CIPHER *v3;
    unsigned char v12[1024], ptr[1024];
    int v5, v6;

    // Open files for decryption
    stream = fopen("flag.txt.enc", "rb");
    s = fopen("flag_decrypted.txt", "wb");
    if (!stream || !s) handleErrors("Error opening file");

    // Initialize the decryption context
    v9 = EVP_CIPHER_CTX_new();
    v3 = EVP_aes_256_cfb128();
    EVP_DecryptInit_ex(v9, v3, 0LL, v11, v10);

    // Decrypt the file in chunks
    while (1) {
        v6 = fread(v12, 1uLL, 0x400uLL, stream);
        if ((int)v6 <= 0) break;
        EVP_DecryptUpdate(v9, ptr, &v5, v12, v6);
        fwrite(ptr, 1uLL, v5, s);
    }

    // Finalize decryption
    EVP_DecryptFinal_ex(v9, ptr, &v5);
    fwrite(ptr, 1uLL, v5, s);

    // Clean up
    EVP_CIPHER_CTX_free(v9);
    fclose(stream);
    fclose(s);

    return 0;
}
