#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
template<class T>bool chmax(T &a, const T &b) { if (a<b) { a=b; return true; } return false; }
template<class T>bool chmin(T &a, const T &b) { if (b<a) { a=b; return true; } return false; }
#define all(x) (x).begin(),(x).end()
#define fi first
#define se second
#define mp make_pair
#define si(x) int(x.size())
const int mod=998244353,MAX=200005,INF=1<<30;
int ask(int a){
    cout<<a+1<<endl;
    int res;cin>>res;
}
vector<int> preG[MAX],G[MAX],ch[MAX];
void make(int u,int p){
    for(int to:preG[u]){
        if(to==p) continue;
        G[u].push_back(to);
        make(to,u);
    }
}
void pre(int u,int ro){
    if(u!=ro) ch[ro].push_back(u);
    for(int to:G[u]){
        pre(to,ro);
    }
}
int now=0;
void solve(int u){
    if(si(G[u])==0) return;
        int A=now,B=-1;
    for(int c:ch[u]){
        B=ask(c);
    }
    if(A<B){
        for(int c:ch[u]){
            B=ask(c);
        }
    }
        for(int to:G[u]){
        solve(to);
    }
}
int main(){
        int Q;cin>>Q;
    while(Q--){
        int N;cin>>N;
        for(int i=0;i<N;i++){
            preG[i].clear();
            G[i].clear();
        }
        for(int i=0;i<N-1;i++){
            int a,b;cin>>a>>b;a--;b--;
            preG[a].push_back(b);
            preG[b].push_back(a);
        }
        now=ask(0);
        make(0,-1);
        for(int i=0;i<N;i++){
            pre(i,-1);
        }
        solve(0);
                cout<<0<<endl;
        int c;cin>>c;
    }
}