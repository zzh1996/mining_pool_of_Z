#include <stdio.h>

#define N 530259

char data[N][32];

__attribute__((always_inline))
int diff(int i,int j){
    return 256-
    __builtin_popcountll(*(unsigned long long*)&data[i][0]^*(unsigned long long*)&data[j][0])-
    __builtin_popcountll(*(unsigned long long*)&data[i][8]^*(unsigned long long*)&data[j][8])-
    __builtin_popcountll(*(unsigned long long*)&data[i][16]^*(unsigned long long*)&data[j][16])-
    __builtin_popcountll(*(unsigned long long*)&data[i][24]^*(unsigned long long*)&data[j][24]);
}

int main(){
    FILE *f=fopen("hashes.bin","rb");
    fread(data,32,N,f);
    fclose(f);
    for(int i=0;i<N;i++){
        //if(i%10000==0)
        //    printf("%d / %d\n",i,N);
        for(int j=0;j<i;j++){
            if(diff(i,j)>=199){
                printf("%d %d %d\n",diff(i,j),i,j);
            }
        }
    }
    return 0;
}
