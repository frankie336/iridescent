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
const int mod=998244353,MAX=300005,INF=1<<30;
void solve(){
    int N;cin>>N;
    string S,T;cin>>S>>T;
    if(S==T){
        cout<<"YES\n";
        return;
    }
        bool one=false;
    for(char c:S) if(c=='1') one=true;
    if(!one){
        cout<<"NO\n";
        return;
    }
    string ng;
    for(int i=0;i<N;i++){
        if(i&1) ng+='1';
        else ng+='0';
    }
    if(T==ng){
        cout<<"NO\n";
        return;
    }
        for(int i=0;i<N;i++){
        if(ng[i]=='1') ng[i]='0';
        else ng[i]='1';
    }
        if(T==ng){
        cout<<"NO\n";
        return;
    }
        cout<<"YES\n";
}
int main(){
        std::ifstream in("text.txt");
    std::cin.rdbuf(in.rdbuf());
    cin.tie(0);
    ios::sync_with_stdio(false);
        int Q;cin>>Q;
    while(Q--){
        solve();
    }
}