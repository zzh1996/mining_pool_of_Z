#include <stdio.h>
#include <stdlib.h>
#include "sha2.h"

int main(){
    unsigned char hash[32];
    for(long i=0;;i++){
        if(i%1000000==0)
            printf("%.2f M\n",1.0*i/1000000);
        sha256(&i, 8, hash);
    }
    return 0;
}
