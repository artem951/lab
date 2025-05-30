#ifndef ARRAY_OPERATIONS_H
#define ARRAY_OPERATIONS_H

// Функция для заполнения массива случайными числами
void fill_array(int *arr, int size);

// Функция для вывода массива на экран
void print_array(int *arr, int size);

// Функция для поиска максимального элемента
int find_max(int *arr, int size);

// Функция для поиска минимального элемента
int find_min(int *arr, int size);

// Функция для сортировки пузырьком
void bubble_sort(int *arr, int size);

// Функция для быстрой сортировки
void quick_sort(int *arr, int low, int high);

#endif
