#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>
#include<malloc.h>
int main()
{
    int n, m;
    n = 0;
    m = 0;
    while (n < 1) {
        printf("Введите высоту матрицы: ");
        scanf("%d", &n);
    }
    while (m < 1) {
        printf("Введите ширину матрицы: ");
        scanf("%d", &m);
    }
    int** a = (int**)malloc(n * sizeof(int*));
    for (int i = 0; i < n; i++) {
        a[i] = (int*)malloc(m * sizeof(int));
    }
    for (int i = 0; i < n; i++) {
        printf("Введите %d строку\n", (i + 1));
        for (int j = 0; j < m; j++) {
            scanf("%d", &a[i][j]);
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
    getchar();
    n += 1;
    a = (int**)realloc(a, n * sizeof(int*));
    a[n - 1] = (int*)calloc(1, m * sizeof(int));
    for (int i = n - 1; i > 0; i--) {
        for (int j = 0; j < m; j++) {
            a[i][j] = a[i - 1][j];
        }
    }
    printf("Введите строку дл€ вставки\n");
    for (int j = 0; j < m; j++) {
        scanf("%d", &a[0][j]);
    }
    printf("Результат выполнени€\n");
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            printf("%d ", a[i][j]);
        }
        printf("\n");
    }
    return 0;
}