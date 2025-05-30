#include <stdio.h>
#include <stdlib.h>
#include <time.h>


void FillInc(int A[], int n) {

    for (int i = 0; i<n; i++){

        A[i]=i+1;

    }

}

void FillDec(int A[], int n) {

    for (int i = 0; i<n; i++){

        A[i]=n-i;

    }

}


void FillRand(int A[], int n){

    for (int i=0; i<n; i++){

        A[i]=rand()%100;
    }

}


int CheckSum(int A[], int n){
    int sum = 0;
    for (int i=0; i<n;i++){
        sum+=A[i];
    }
    return sum;
}


int  RunNumber(int A[], int n){
    int count = 1;
    for (int i=1; i<n;i++){
        if (n==0) return 0;
        if (A[i]<A[i-1]){
            count++;
        }
    }

    return count;
}

void PrintMas(int A[], int n){
    int count=1;
    for (int i=0; i<n; i++){

        printf("%d ", A[i]);

    }
    printf("\n");


}


int main(){
    int n = 10;
    int A[n];
    FillInc(A,n);
    printf("Возрастающий массив:");
    PrintMas(A,n);
    printf("Контрольная сумма:%d\n", CheckSum(A,n));
    printf("Количество серий %d\n\n", RunNumber(A,n));

    FillDec(A,n);
    printf("Убывающий массив:");
    PrintMas(A,n);
    printf("Контрольная сумма:%d\n", CheckSum(A,n));
    printf("Количество серий %d\n\n", RunNumber(A,n));
    srand(time(NULL));


    FillRand(A,n);
    printf("Случайный массив:");
    PrintMas(A,n);
    printf("Количество серий %d\n", RunNumber(A,n));
    printf("Контрольная сумма:%d", CheckSum(A,n));

    return 0;
    


}
