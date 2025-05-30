#include <stdio.h>
#include "array_operations.h"

#define SIZE 10

int main() {
    int arr[SIZE];
    
    // Заполняем массив случайными числами
    fill_array(arr, SIZE);
    
    printf("Исходный массив:\n");
    print_array(arr, SIZE);
    
    printf("Максимальный элемент: %d\n", find_max(arr, SIZE));
    printf("Минимальный элемент: %d\n", find_min(arr, SIZE));
    
    // Сортировка пузырьком
    bubble_sort(arr, SIZE);
    printf("После сортировки пузырьком:\n");
    print_array(arr, SIZE);
    
    // Заполняем снова для быстрой сортировки
    fill_array(arr, SIZE);
    printf("Новый массив для быстрой сортировки:\n");
    print_array(arr, SIZE);
    
    // Быстрая сортировка
    quick_sort(arr, 0, SIZE - 1);
    printf("После быстрой сортировки:\n");
    print_array(arr, SIZE);
    
    return 0;
}
