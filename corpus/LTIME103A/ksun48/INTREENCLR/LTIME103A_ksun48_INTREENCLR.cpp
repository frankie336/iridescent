#include <bits/stdc++.h>
using namespace std;
namespace std {
template<class Fun>
class y_combinator_result {
    Fun fun_;
public:
    template<class T>
    explicit y_combinator_result(T &&fun): fun_(std::forward<T>(fun)) {}
    template<class ...Args>
    decltype(auto) operator()(Args &&...args) {
        return fun_(std::ref(*this), std::forward<Args>(args)...);
    }
};
template<class Fun>
decltype(auto) y_combinator(Fun &&fun) {
    return y_combinator_result<std::decay_t<Fun>>(std::forward<Fun>(fun));
}
} // namespace std
void solve(){
    int n;
    cin >> n;
    int Q;
    cin >> Q;
    vector<vector<int> > edges(n);
    for(int i = 0; i < n-1; i++){
        int u, v;
        cin >> u >> v;
        u--; v--;
        edges[u].push_back(v);
        edges[v].push_back(u);
    }
    int last_query;
    cout << 1 << '\n';
    cout << flush;
    cin >> last_query;
    vector<int> up_diff(n, 0);
    y_combinator(
        [&](auto self, int v, int p) -> void {
            for(int w : edges[v]){
                if(w == p) continue;
                self(w, v);
            }
            if(v > 0){
                cout << (v+1) << '\n';
                cout << flush;
                int q;
                cin >> q;
                int y = q - last_query;
                for(int w : edges[v]){
                    if(w == p) continue;
                    y -= up_diff[w];
                    y += !up_diff[w];
                }
                assert(y == 1 || y == -1);
                last_query = q;
                if(y == 1){
                    up_diff[v] = 0;
                } else {
                    up_diff[v] = 1;
                }
            }
        }
    )(0, -1);
    vector<int> color(n, 0);
    y_combinator(
        [&](auto self, int v, int p) -> void {
            for(int w : edges[v]){
                if(w == p) continue;
                color[w] = color[v] ^ up_diff[w];
                self(w, v);
            }
        }
    )(0, -1);
    color[0] ^= 1;
    vector<int> freq = {0, 0};
    for(int x : color) freq[x]++;
    int d = (freq[0] < freq[1]) ? 0 : 1;
    for(int i = 0; i < n; i++){
        if(color[i] == d){
            cout << (i+1) << '\n';
            cout << flush;
            int y;
            cin >> y;
        }
    }
    cout << 0 << '\n';
    cout << flush;
    int y;
    cin >> y;
}
int main(){
    ios_base::sync_with_stdio(false), cin.tie(nullptr);
    int T;
    cin >> T;
    while(T--) solve();
}