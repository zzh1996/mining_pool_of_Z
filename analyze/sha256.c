#include <openssl/sha.h>
#include <stdio.h>
#include <stdlib.h>

void sha256(void *input, void *output){
    SHA256_CTX sha256;
    SHA256_Init(&sha256);
    SHA256_Update(&sha256, input, 8);
    SHA256_Final(output, &sha256);
}

int main(){
    unsigned char hash[SHA256_DIGEST_LENGTH];
    for(long i=0;;i++){
        if(i%1000000==0)
            printf("%.2f M\n",1.0*i/1000000);
        sha256(&i, hash);
    }
    return 0;
}
