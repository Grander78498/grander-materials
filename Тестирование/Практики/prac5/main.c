#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <malloc.h>
#include <string.h>
#include <stdlib.h>

int read_number(int* n) {
    char buffer[100];
    char *endptr;

    if (fgets(buffer, sizeof(buffer), stdin) != NULL) {
        char *newline = strchr(buffer, '\n');
        if (newline) {
            *newline = '\0';
        }

        *n = strtol(buffer, &endptr, 10);

        if (*endptr != '\0') {
            printf("Ошибка: введенная строка содержит нечисловые символы\n");
            return -1;
        }
        return 0;
    } else {
        printf("Ошибка ввода\n");
        return -1;
    }
}

int main()
{
    int n, m;
    n = 0;
    m = 0;
    while (n < 1) {
        printf("Введите высоту матрицы: ");
        if (read_number(&n) != 0) {
            return 1;
        };
    }
    while (m < 1) {
        printf("Введите ширину матрицы: ");
        if (read_number(&m) != 0) {
            return 1;
        };
    }
    int** a = (int**)malloc(n * sizeof(int*));
    if (a == NULL) {
        return -1;
    }
    for (int i = 0; i < n; i++) {
        a[i] = (int*)malloc(m * sizeof(int));
        if (a[i] == NULL) {
            for (int j = 0; j < i; j++) {
                free(a[j]);
            }
            free(a);
            return -1;
        }
    }
    for (int i = 0; i < n; i++) {
        printf("Введите строку\n");
        for (int j = 0; j < m; j++) {
            if (read_number(&a[i][j]) != 0) {
                for (int k = 0; k < i; k++) {
                    free(a[k]);
                }
                free(a);
                return 1;
            };
        }
    }
    printf("Результат ввода\n");
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            if (j == m - 1) {
                printf("%d\n", a[i][j]);
            }
            else {
                printf("%d ", a[i][j]);
            }
        }
    }
    n += 1;
    int** b = (int**)realloc(a, n * sizeof(int*));
    if (b == NULL) {
        free(a);
        return -1;
    }
    a = b;
    a[n - 1] = (int*)calloc(1, m * sizeof(int));
    if (a[n - 1] == NULL) {
        for (int j = 0; j < n; j++) {
            free(a[j]);
        }
        free(a);
        return -1;
    }
    for (int i = n - 1; i > 0; i--) {
        for (int j = 0; j < m; j++) {
            a[i][j] = a[i - 1][j];
        }
    }
    printf("Введите строку для вставки\n");
    for (int j = 0; j < m; j++) {
        if (read_number(&a[0][j]) != 0) {
            for (int i = 0; i < n; j++) {
                free(a[i]);
            }
            free(a);
            return 1;
        };
    }
    printf("Результат выполнения\n");
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            printf("%d ", a[i][j]);
        }
        printf("\n");
    }
    for (int i = 0; i < n; i++) {
        free(a[i]);
    }
    free(a);
    return 0;
}