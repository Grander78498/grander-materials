#include <stdio.h>
#include <malloc.h>
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
    int** b = (int**)realloc(a, n * sizeof(int*));
    if (b == NULL) {
        for (int j = 0; j < n; j++) {
            free(a[j]);
        }
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
        scanf("%d", &a[0][j]);
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