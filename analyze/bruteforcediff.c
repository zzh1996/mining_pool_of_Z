#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <stdlib.h>
#include <signal.h>

#define N 2*1024*1024
#define threshold 102
#define THREADS 4

char data[N][16];

__attribute__((always_inline))
int diff(int i,int j){
    return 128-
    __builtin_popcountll(*(unsigned long long*)&data[i][0]^*(unsigned long long*)&data[j][0])-
    __builtin_popcountll(*(unsigned long long*)&data[i][8]^*(unsigned long long*)&data[j][8]);
}

int main(){
    FILE *f=fopen("md5.bin","rb");
    fread(data,16,N,f);
    fclose(f);

    pid_t childs[THREADS];

    for(int p=0;p<THREADS;p++){
        pid_t pid=fork();
        if(pid==0){
            fprintf(stderr,"Process %d started!\n",p);

            long long cnt=0;
            long long lastcnt=0;
            for(int i=N/THREADS*p;i<N/THREADS*(p+1);i++){
                if(cnt>lastcnt+1000000000){
                    fprintf(stderr,"%d: %.1f G\n",p,1.0*cnt/1000000000);
                    lastcnt=cnt;
                }
                for(int j=0;j<i;j++){
                    if(diff(i,j)>=threshold){
                        printf("%d %d %d\n",i,j,diff(i,j));
                        exit(0);
                    }
                    cnt++;
                }
            }
            exit(1);
        }else{
            childs[p]=pid;
        }
    }
    wait(NULL);
    for(int p=0;p<THREADS;p++){
        kill(childs[p],SIGTERM);
    }
    return 0;
}
