#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

//  1. Создание потока 
void* thread_func_1(void* arg) {
    for (int i = 0; i < 5; i++) {
        printf("Дочерний поток 1: строка %d\n", i+1);
    }
    return NULL;
}

void task1() {
    printf("\nЗадание 1: Создание потока \n");
    pthread_t thread;
    if (pthread_create(&thread, NULL, thread_func_1, NULL) != 0) {
        perror("Ошибка создания потока");
        return;
    }
    
    for (int i = 0; i < 5; i++) {
        printf("Родительский поток 1: строка %d\n", i+1);
    }
    
    if (pthread_join(thread, NULL) != 0) {
        perror("Ошибка ожидания потока");
    }
}

//  2. Ожидание потока 
void* thread_func_2(void* arg) {
    for (int i = 0; i < 5; i++) {
        printf("Дочерний поток 2: строка %d\n", i+1);
    }
    return NULL;
}

void task2() {
    printf("\nЗадание 2: Ожидание потока \n");
    pthread_t thread;
    if (pthread_create(&thread, NULL, thread_func_2, NULL) != 0) {
        perror("Ошибка создания потока");
        return;
    }
    
    if (pthread_join(thread, NULL) != 0) {
        perror("Ошибка ожидания потока");
    }
    
    for (int i = 0; i < 5; i++) {
        printf("Родительский поток 2: строка %d\n", i+1);
    }
}

//  3. Параметры потока 
typedef struct {
    char messages[5][100];
    int count;
} ThreadData;

void* thread_func_3(void* arg) {
    ThreadData* data = (ThreadData*)arg;
    for (int i = 0; i < data->count; i++) {
        printf("Поток %lu: %s\n", (unsigned long)pthread_self(), data->messages[i]);
    }
    return NULL;
}

void task3() {
    printf("\n=== Задание 3: Параметры потока ===\n");
    pthread_t threads[4];
    ThreadData data[4] = {
        {{"Сообщение 1", "Сообщение 2", "Сообщение 3", "Сообщение 4", "Сообщение 5"}, 5},
        {{"Другое 1", "Другое 2", "Другое 3", "Другое 4", "Другое 5"}, 5},
        {{"Текст 1", "Текст 2", "Текст 3", "Текст 4", "Текст 5"}, 5},
        {{"Строка 1", "Строка 2", "Строка 3", "Строка 4", "Строка 5"}, 5}
    };
    
    for (int i = 0; i < 4; i++) {
        if (pthread_create(&threads[i], NULL, thread_func_3, &data[i]) != 0) {
            perror("Ошибка создания потока");
            continue;
        }
    }
    
    for (int i = 0; i < 4; i++) {
        if (pthread_join(threads[i], NULL) != 0) {
            perror("Ошибка ожидания потока");
        }
    }
}

//  4. Завершение потока без ожидания 
void* thread_func_4(void* arg) {
    pthread_setcancelstate(PTHREAD_CANCEL_ENABLE, NULL);
    pthread_setcanceltype(PTHREAD_CANCEL_DEFERRED, NULL);
    
    for (int i = 0; i < 5; i++) {
        printf("Поток 4.%lu: строка %d\n", (unsigned long)pthread_self(), i+1);
        sleep(1);
        
        // Точка отмены
        pthread_testcancel();
    }
    return NULL;
}

void task4() {
    printf("\nЗадание 4: Завершение потока без ожидания \n");
    pthread_t threads[4];
    
    for (int i = 0; i < 4; i++) {
        if (pthread_create(&threads[i], NULL, thread_func_4, NULL) != 0) {
            perror("Ошибка создания потока");
            continue;
        }
    }
    
    sleep(2);
    
    for (int i = 0; i < 4; i++) {
        if (pthread_cancel(threads[i]) != 0) {
            perror("Ошибка отмены потока");
        }
    }
    
    printf("Основной поток завершил работу\n");
}

// 5. Обработка завершения потока 
void cleanup_handler(void* arg) {
    printf("Поток 5.%lu: выполняется очистка перед завершением\n", (unsigned long)pthread_self());
}
void* thread_func_5(void* arg) {
    pthread_cleanup_push(cleanup_handler, NULL);
    
    pthread_setcancelstate(PTHREAD_CANCEL_ENABLE, NULL);
    pthread_setcanceltype(PTHREAD_CANCEL_DEFERRED, NULL);
    
    for (int i = 0; i < 5; i++) {
        printf("Поток 5.%lu: строка %d\n", (unsigned long)pthread_self(), i+1);
        sleep(1);
        
        // Точка отмены
        pthread_testcancel();
    }
    
    pthread_cleanup_pop(1); // Выполнить cleanup даже если не было отмены
    return NULL;
}

void task5() {
    printf("\nЗадание 5: Обработка завершения потока \n");
    pthread_t thread;
    
    if (pthread_create(&thread, NULL, thread_func_5, NULL) != 0) {
        perror("Ошибка создания потока");
        return;
    }
    
    sleep(2);
    if (pthread_cancel(thread) != 0) {
        perror("Ошибка отмены потока");
    }
    
    if (pthread_join(thread, NULL) != 0) {
        perror("Ошибка ожидания потока");
    }
    printf("Основной поток завершил работу\n");
}

// 6. Sleepsort 
void* sleep_sort(void* arg) {
    int value = *(int*)arg;
    usleep(value * 1000); // Используем микросекунды (1 мс = 1000 мкс)
    printf("%d ", value);
    return NULL;
}

void task6() {
    printf("\nЗадание 6: Sleepsort \n");
    int arr[] = {34, 23, 122, 9, 87, 45};
    int n = sizeof(arr)/sizeof(arr[0]);
    
    printf("Исходный массив: ");
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\n");
    
    printf("Отсортированный массив: ");
    pthread_t threads[n];
    
    for (int i = 0; i < n; i++) {
        if (pthread_create(&threads[i], NULL, sleep_sort, &arr[i]) != 0) {
            perror("Ошибка создания потока");
            continue;
        }
    }
    
    for (int i = 0; i < n; i++) {
        if (pthread_join(threads[i], NULL) != 0) {
            perror("Ошибка ожидания потока");
        }
    }
    printf("\n");
}

// Главная функция 
int main() {
    task1();
    task2();
    task3();
    task4();
    task5();
    task6();
    return 0;
}
