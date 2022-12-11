#include <stdio.h>
#include <memory.h>
#include <algorithm>
using namespace std;
int tt,qq,ll,rr,xx,lg,n,len,i,x,y;
long long u,v,step[13];
int t[13],k[13],ne[13];
long long a[500010];
void rec(int v,int c,long long w) {
  if (!v) {
    if (!c) a[++n] = w;
    return;
  }
  int j,p,u,pr;
  for (pr=11,j=ne[11];j!=10;pr=j,j=ne[j]) {
    if (k[j]) {
      if (v == 1 && j == 0) continue;
      p = j+j+c;
      if (p > 9) p -= 10, u = 1;
      else u = 0;
      if (t[p]) {
        k[j]--; t[p]--;
        if (!k[j]) ne[pr] = ne[j];
        rec(v-1,u,w+step[v]*j);
        if (!k[j]) ne[pr] = j;
        k[j]++; t[p]++;
      }
    }
  }
}
void recc(int v,int c,long long w) {
  for (int pr=11,i=0;i<=9;i++)
    if (!k[i]) ne[pr] = ne[i];
    else pr = i;
  rec(v,c,w);
  for (int i=0;i<=10;i++) ne[i] = i+1;
  ne[11] = 0;
}
int main() {
#ifndef ONLINE_JUDGE
  freopen("in","r",stdin);
  freopen("out","w",stdout);
#endif
  for (i=0;i<=10;i++) ne[i] = i+1;
  ne[11] = 0;
  n = 0;
  for (len=6;len<=10;len++) {
    step[len] = 1;
    for (i=len-1;i>=1;i--) step[i] = step[i+1]*10;
    for (i=0;i<=9;i++) k[i] = !!(i % 3);
    for (x=0;x+x<=len-6;x++)
      for (y=0;y<=len-6-x-x;y++) {
        k[3] += x; k[6] += x;
        k[0] += y; k[9] += len-6-x-x-y;
        for (i=0;i<=9;i++) t[i] = k[i];
        recc(len,0,0);
        k[3] -= x; k[6] -= x;
        k[0] -= y; k[9] -= len-6-x-x-y;
      }
    if (len == 10) {
      memset(k,0,sizeof(k));
      k[1] = 2; k[2] = 3; k[4] = 1;
      k[5] = 2; k[6] = 1; k[8] = 1;
      for (i=0;i<=9;i++) t[i] = k[i];
      recc(len,0,0);
      memset(k,0,sizeof(k));
      k[1] = 1; k[3] = 1; k[4] = 2;
      k[5] = 1; k[7] = 3; k[8] = 2;
      for (i=0;i<=9;i++) t[i] = k[i];
      recc(len,0,0);
    }
  }
  sort(a+1,a+n+1);
  scanf("%d",&tt);
  while (tt--) {
    scanf("%I64lld %I64lld",&u,&v);
    ll = 1; rr = n+1;
    while (ll < rr) {
      xx = (ll+rr) >> 1;
      if (a[xx] < u) ll = xx+1;
      else rr = xx;
    }
    lg = ll;
    ll = 0; rr = n;
    while (ll < rr) {
      xx = (ll+rr+1) >> 1;
      if (a[xx] <= v) ll = xx;
      else rr = xx-1;
    }
    printf("%d\n",ll-lg+1);
  }
  return 0;
}