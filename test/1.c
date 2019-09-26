#include <stdio.h>

const int holes[10] = {1, 0, 0, 0, 1, 0, 1, 0, 2, 1};

int main() {
    int n, ans = 0;
    scanf("%d", &n);
    for( ; n>0; n /= 10 ) ans += holes[n%10];
    printf("%d\n", ans);
    return 0;
}