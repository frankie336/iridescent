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
const int mod=998244353,MAX=1005,INF=1<<28;
int N;
vector<int> G[MAX],pre[MAX];
int par[MAX];
void init(){
    cin>>N;
    for(int i=1;i<=N;i++){
        G[i].clear();
        par[i]=-1;
    }
}
pair<int,int> ask(vector<int> S){
    cout<<"? ";
    cout<<si(S);
    for(int a:S) cout<<" "<<a;
    cout<<endl;
    int a,b;cin>>a>>b;
    return mp(a,b);
}
pair<int,int> askrem(vector<int> rem){
    vector<int> S;
    for(int i=1;i<=N;i++){
        if(rem[i]) S.push_back(i);
    }
    return ask(S);
}
int C=-1;
int target=-1;
bool centroid[MAX];
int subtree_size[MAX];
int centpar[MAX];
void centinit(){
    for(int i=1;i<=N;i++){
        centroid[i]=0;
        subtree_size[i]=0;
        centpar[i]=0;
    }
    C=-1;
}
int compute_subtree_size(int u,int p){
    int c=1;
    for(auto a:G[u]){
        if(a==p||centroid[a]) continue;
        c+=compute_subtree_size(a,u);
    }
    return subtree_size[u]=c;
}
pair<int,int> search_centroid(int u,int p,int t){
    pair<int,int> res={INF,-1};
    int s=1,m=0;
    for(auto a:G[u]){
        if(a==p||centroid[a]) continue;
                res=min(res,search_centroid(a,u,t));
                m=max(m,subtree_size[a]);
        s+=subtree_size[a];
    }
    m=max(m,t-s);
    res=min(res,{m,u});
    return res;
}
void solve_subproblem(int u,int p){
    compute_subtree_size(u,-1);
    int s=search_centroid(u,-1,subtree_size[u]).second;
        if(si(G[s])==1){
        s=G[s][0];
    }
    centroid[s]=1;
    if(C==-1) C=s;
    centpar[s]=p;
        int sum=0;
    vector<int> Z;
    for(int a:G[s]){
        //if(centroid[a]) continue;
        Z.push_back(a);
        sum+=a;
    }
    Z.push_back(s);
    sum+=s;
        Z.push_back(target);
    sum+=target;
        /*
    if(si(Z)==4){
        int a=Z[0],b=Z[1];
        if(si(G[a])==1&&si(G[b])==1){
            G[s].push_back(target);
            G[target].push_back(s);
            return;
        }
    }
    */
    auto res=ask(Z);
        int diff=sum-res.se;
        if(diff==s){
        G[s].push_back(target);
        G[target].push_back(s);
        return;
    }else{
        int x=diff-s;
        //if(si(G[x])==1) x=G[x][0];
        solve_subproblem(x,s);
        centroid[s]=0;
    }
        /*
    for(auto a:G[s]){
        if(centroid[a]){
            continue;
        }
        solve_subproblem(a,s);
    }
        centroid[s]=0;
     */
}
int main(){
        std::ifstream in("text.txt");
    std::cin.rdbuf(in.rdbuf());
    cin.tie(0);
    ios::sync_with_stdio(false);
        int QQ;cin>>QQ;
    while(QQ--){
        init();
        vector<int> rem(N+1,1);
        int lasum=-1,la=-1;
        vector<int> st;
        for(int q=0;q<N;q++){
            if(q==N-1){
                int t=-1;
                for(int i=1;i<=N;i++) if(rem[i]) t=i;
                par[la]=t;
                G[t].push_back(la);
                G[la].push_back(t);
                la=t;
                break;
            }
            auto res=askrem(rem);
            if(res.se==lasum){
                st.push_back(la);
            }else if(q){
                int t=res.se-lasum;
                G[t].push_back(la);
                G[la].push_back(t);
                par[la]=t;
            }
            rem[res.fi]=0;
            lasum=res.se-res.fi;
            la=res.fi;
        }
                //for(int i=1;i<=N;i++) cout<<par[i]<<" ";
        //cout<<endl;
                int ro=la;
                reverse(all(st));
                //cout<<ro<<endl;
                for(int x:st){
            centinit();
            target=x;
            solve_subproblem(ro,-1);
        }
                cout<<"!"<<endl;
        for(int i=1;i<=N;i++){
            for(int to:G[i]){
                if(i<to) cout<<i<<" "<<to<<endl;
            }
        }
        int x;cin>>x;
            }
}