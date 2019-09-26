#include<stdio.h>

char s[210][210];
int vis[210][210];
int h, w, ans;

void dfs( int i, int j ) {
    vis[i][j] = 1;
    if( i < h && vis[i+1][j] == 0 && s[i+1][j] == s[i][j] )
        dfs( i+1, j );
    if( i > 0 && vis[i-1][j] == 0 && s[i-1][j] == s[i][j] )
        dfs( i-1, j );
    if( j > 0 && vis[i][j-1] == 0 && s[i][j-1] == s[i][j] )
        dfs( i, j-1 );
    if( j < w && vis[i][j+1] == 0 && s[i][j+1] == s[i][j] )
        dfs( i, j+1 );

    if( j < w && i < h && vis[i+1][j+1] == 0 && s[i+1][j+1] == s[i][j] )
        dfs( i+1, j+1 );
    if( j < w && i > 0 && vis[i-1][j+1] == 0 && s[i-1][j+1] == s[i][j] )
        dfs( i-1, j+1 );
    if( i < h && j > 0 && vis[i+1][j-1] == 0 && s[i+1][j-1] == s[i][j] )
        dfs( i+1, j-1 );
    if( i > 0 && j < w && vis[i-1][j-1] == 0 && s[i-1][j-1] == s[i][j] )
        dfs( i-1, j-1 );
}

int main() {
    scanf("%d", &h );
    for( int i=0; i<h; ++i ) {
        scanf("%s", &(s[i][0]) );
    }
    for( w=0; s[0][w] != '\0'; ++w );
    for( int i=0; i<h; ++i ) 
        for( int j=0; j<w; ++j ) 
            if( vis[i][j] == 0 )
                dfs(i,j), ++ans;
    printf("%d\n", ans);
}