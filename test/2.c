#include <stdio.h>

int main(){
    int t,n,m,c;
    // int count =0;
    scanf("%d", &t);
    for(int i=0;i<t;i++){
        scanf("%d %d %d", &n, &c, &m);
        int ans = n/c; n /= c;
        while( n >= m ) ans += n/m, n = n/m + n%m;
    printf("%d\n", ans);

    }
    return 0;

}