#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node *next;
    struct Node *extra;
};

// создание узла
struct Node* createNode(int data) {
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->data = data;
    newNode->next = NULL;
    newNode->extra = NULL;
    return newNode;
}

// добавление узла в конец списка
void appendNode(struct Node** head, int data) {
    struct Node* newNode = createNode(data);
    if (*head == NULL) {
        *head = newNode;
        return;
    }
    struct Node* temp = *head;
    while (temp->next != NULL) {
        temp = temp->next;
    }
    temp->next = newNode;
}

// вывод списка
void printList(struct Node* head) {
    struct Node* temp = head;
    while (temp != NULL) {
        printf("%d -> ", temp->data);
        temp = temp->next;
    }
    printf("NULL\n");
}

// связывание двух списков
void linkLists(struct Node* upper, struct Node* lower) {
    while (upper != NULL && lower != NULL) {
        upper->extra = lower;
        upper = upper->next;
        lower = lower->next;
    }
}

// перемещение
void navigateList(struct Node* start) {
    struct Node* current = start;
    char command;
    printf("Управление: D(6) - вправо, A(4) - влево, W(8) - вверх, S(2) - вниз, Q - выход\n");
    while (1) {
        printf("Текущий узел: %d\n", current->data);
        printf("Введите команду: ");
        scanf(" %c", &command);

        if (command == 'D' || command == '6') {
            if (current->next) current = current->next;
            else printf("Достигнут конец списка!\n");
        } else if (command == 'A' || command == '4') {
            printf("Движение влево невозможно в односвязном списке!\n");
        } else if (command == 'W' || command == '8') {
            if (current->extra) current = current->extra;
            else printf("Движение вверх невозможно!\n");
        } else if (command == 'S' || command == '2') {
            if (current->extra) current = current->extra;
            else printf("Движение вниз невозможно!\n");
        } else if (command == 'Q') {
            printf("Выход из программы.\n");
            break;
        } else {
            printf("Неверная команда!\n");
        }
    }
}

int main() {
    struct Node* list1 = NULL;
    struct Node* list2 = NULL;
    int value;
    
    printf("Введите элементы верхнего списка (завершите ввод 0): \n");
    while (1) {
        scanf("%d", &value);
        if (value == 0) break;
        appendNode(&list1, value);
    }

    printf("Создан верхний список:\n");
    printList(list1);

    printf("Введите элементы нижнего списка (завершите ввод 0): \n");
    while (1) {
        scanf("%d", &value);
        if (value == 0) break;
        appendNode(&list2, value);
    }

    // Добавляем узел a0 в нижний список
    appendNode(&list2, 0);

    printf("Создан нижний список:\n");
    printList(list2);

    // связывание списков
    linkLists(list1, list2);

    // указатель на начало
    struct Node* S = list1;

    // навигация
    navigateList(S);
    
    return 0;
}
