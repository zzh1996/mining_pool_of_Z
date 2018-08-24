#include <openssl/sha.h>
#include <stdio.h>
#include <stdlib.h>

void sha256(void *input, void *output){
    SHA256_CTX sha256;
    SHA256_Init(&sha256);
    SHA256_Update(&sha256, input, 8);
    SHA256_Final(output, &sha256);
}

__attribute__((always_inline))
int diff(unsigned char *x, unsigned char *y){
    return 256-
    __builtin_popcountll(*(unsigned long long*)&x[0]^*(unsigned long long*)&y[0])-
    __builtin_popcountll(*(unsigned long long*)&x[8]^*(unsigned long long*)&y[8])-
    __builtin_popcountll(*(unsigned long long*)&x[16]^*(unsigned long long*)&y[16])-
    __builtin_popcountll(*(unsigned long long*)&x[24]^*(unsigned long long*)&y[24]);
}

int main(){
    unsigned int *table;
    table=malloc(4LL*(1LL<<32)/4);
    unsigned char hash[SHA256_DIGEST_LENGTH];
    unsigned char hash2[SHA256_DIGEST_LENGTH];
    puts("Generating table");
    for(long i=0;i<(1LL<<24);i++){
        if(i%1000000==0)
            printf("%.2f M\n",1.0*i/1000000);
        sha256(&i, hash);
        if(*(unsigned int *)hash<(1<<30))
        table[*(unsigned int *)hash]=i;
    }
    puts("Hashing");
    for(long i=(1LL<<32);;i++){
        sha256(&i,hash);
        long seed=0;
        //if(*(unsigned int *)hash<(1<<30))
        //seed=table[*(unsigned int *)hash];
        sha256(&seed,hash2);
        if(diff(hash,hash2)>=200){
            printf("%ld %ld\n",seed,i);
        }
        if(i%1000000==0){
            printf("%.2f M\n",1.0*i/1000000);
        }
    }
    return 0;
}
