#include <stdio.h>
#include <math.h>

long double abso( long double a ) {
    if( a > 0 )
        return a;
    return -a;
}

const long double PI = 3.14159265359L;
long double area[100005];

int main() {
    int n, M;
    scanf("%d", &n);
    for( long long int i=0, r; i<n; ++i ) {
        scanf("%lld\n", &r);
        area[i] = PI*(r*r);
    }
    scanf("%d", &M);
    long double l = 0, m, r=0;
    for( int i=0; i<n; ++i ) 
        if( r < area[i] ) r = area[i];
    while( abso(l-r) >= 0.000001L ) {
        m = (l+r)/2;
        int c = 0;
        for( int i=0; i<n; ++i )
            c += floor(area[i]/m);
        if( c < M )
            r = m - 0.000001L;
        else
            l = m;
    }
    printf("%Lf", l);
}