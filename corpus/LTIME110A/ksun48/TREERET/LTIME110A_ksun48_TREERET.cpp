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
namespace ecnerwala {
using std::swap;
struct level_ancestor {
    int N;
    std::vector<int> preorder;
    std::vector<int> idx;
    std::vector<std::pair<int, int>> heavyPar; // heavy parent, distance
    level_ancestor() : N(0) {}
    level_ancestor(const std::vector<int>& par) : N(int(par.size())), preorder(N), idx(N), heavyPar(N) {
        std::vector<std::vector<int>> ch(N);
        for (int i = 0; i < N; i++) {
            if (par[i] != -1) ch[par[i]].push_back(i);
        }
        std::vector<int> sz(N);
        int nxt_idx = 0;
        for (int i = 0; i < N; i++) {
            if (par[i] == -1) {
                std::y_combinator([&](auto self, int cur) -> void {
                    sz[cur] = 1;
                    for (int nxt : ch[cur]) {
                        self(nxt);
                        sz[cur] += sz[nxt];
                    }
                    if (!ch[cur].empty()) {
                        auto mit = max_element(ch[cur].begin(), ch[cur].end(), [&](int a, int b) { return sz[a] < sz[b]; });
                        swap(*ch[cur].begin(), *mit);
                    }
                })(i);
                std::y_combinator([&](auto self, int cur, int isRoot = true) -> void {
                    preorder[idx[cur] = nxt_idx++] = cur;
                    if (isRoot) {
                        heavyPar[idx[cur]] = {par[cur] == -1 ? -1 : idx[par[cur]], 1};
                    } else {
                        assert(idx[par[cur]] == idx[cur]-1);
                        heavyPar[idx[cur]] = heavyPar[idx[cur]-1];
                        heavyPar[idx[cur]].second++;
                    }
                    bool chRoot = false;
                    for (int nxt : ch[cur]) {
                        self(nxt, chRoot);
                        chRoot = true;
                    }
                })(i);
            }
        }
    }
    int get_ancestor(int a, int k) const {
        assert(k >= 0);
        a = idx[a];
        while (a != -1 && k) {
            if (k >= heavyPar[a].second) {
                k -= heavyPar[a].second;
                assert(heavyPar[a].first <= a - heavyPar[a].second);
                a = heavyPar[a].first;
            } else {
                a -= k;
                k = 0;
            }
        }
        if (a == -1) return -1;
        else return preorder[a];
    }
    int lca(int a, int b) const {
        a = idx[a], b = idx[b];
        while (true) {
            if (a > b) swap(a, b);
            assert(a <= b);
            if (a > b - heavyPar[b].second) {
                return preorder[a];
            }
            b = heavyPar[b].first;
            if (b == -1) return -1;
        }
    }
    int dist(int a, int b) const {
        a = idx[a], b = idx[b];
        int res = 0;
        while (true) {
            if (a > b) swap(a, b);
            assert(a <= b);
            if (a > b - heavyPar[b].second) {
                res += b - a;
                break;
            }
            res += heavyPar[b].second;
            b = heavyPar[b].first;
            if (b == -1) return -1;
        }
        return res;
    }
};
} // namespace ecnerwala
int TEST = 0;
mt19937 mt(time(0));
void solve(){
    vector<int> ans_par;
    int n;
    if(TEST){
        n = 2 + (mt() % 30);
        ans_par.assign(n, -1);
        vector<int> ord(n);
        for(int i = 0; i < n; i++) ord[i] = i;
        shuffle(ord.begin(), ord.begin(), mt);
        for(int i = 1; i < n; i++){
            ans_par[ord[i]] = ord[mt() % i];
        }
        cerr << "n: " << n << '\n';
    } else {
        cin >> n;
    }
    ecnerwala::level_ancestor la(ans_par);
    auto ask = [&](vector<int> r) -> pair<int, int> {
        if((int)r.size() <= 2){
            return {r[0], accumulate(r.begin(), r.end(), 0)};
        }
        if(TEST){
            cerr << "asking " << '\n';
            for(int& x : r) x--;
            int found = 0;
            int sum = 0;
            for(int x : r){
                bool works = true;
                for(int y : r){
                    for(int z : r){
                        if(y == x || z == x) continue;
                        if(la.dist(x, z) + la.dist(x, y) == la.dist(y, z)) works = false;
                    }
                }
                if(works){
                    found = x + 1;
                    sum += x + 1;
                }
            }
            return {found, sum};
        }
        cout << "? " << r.size();
        for(int x : r){
            cout << ' ' << x;
        }
        cout << '\n';
        cout << flush;
        int v, sum;
        cin >> v >> sum;
        return {v, sum};
    };
    vector<int> active(n+1, 1);
    active[0] = 0;
    vector<int> ord;
    vector<int> par(n+1, 0);
    int pv = 0;
    int psum;
    for(int i = 0; i < n; i++){
        vector<int> z;
        for(int j = 1; j <= n; j++){
            if(active[j]) z.push_back(j);
        }
        auto [v, sum] = ask(z);
        ord.push_back(v);
        active[v] = 0;
        if(pv && sum != psum - pv){
            assert(sum > psum - pv);
            par[pv] = sum - (psum - pv);
        }
        psum = sum;
        pv = v;
    }
    reverse(ord.begin(), ord.end());
    par[ord[1]] = ord[0];
    for(int idx = 1; idx < n; idx++){
        int v = ord[idx];
        if(par[v]) continue;
        vector<int> alive(n+1, 0);
        vector<int> tree_alive(ord.begin(), ord.begin() + idx);
        for(int x : tree_alive) alive[x] = 1;
        while(tree_alive.size() > 1){
            // cerr << "tree ";
            // for(int x : tree_alive) cerr << x << ' ';
            // cerr << '\n';
            vector<vector<int> > ch(n+1), e(n+1);
            int root;
            for(int x : tree_alive){
                if(par[x] && alive[par[x]]){
                    ch[par[x]].push_back(x);
                    e[par[x]].push_back(x);
                    e[x].push_back(par[x]);
                } else {
                    root = x;
                }
            }
            int centroid = 0;
            y_combinator(
                [&](auto self, int u) -> int {
                    int ss = 1;
                    for(int w : ch[u]){
                        ss += self(w);
                    }
                    if(ss * 2 >= (int)tree_alive.size()){
                        if(!centroid) centroid = u;
                    }
                    return ss;
                }
            )(root);
            vector<int> neighbors = e[centroid];
            int nsum = 0;
            for(int x : neighbors) nsum += x;
            neighbors.push_back(centroid);
            if(neighbors.size() == 2){
                nsum += centroid;
                assert(tree_alive.size() == 2);
            }
            neighbors.push_back(v);
            // cerr << "nsum " << nsum << '\n';
            int res = ask(neighbors).second;
            if(res == nsum + v){
                tree_alive = {centroid};
            } else {
                int diff = nsum - (res - v);
                assert(alive[diff]);
                vector<int> ntree;
                if(diff == centroid){
                    assert(neighbors.size() == 3);
                    int other = e[centroid][0];
                    assert(alive[other]);
                    alive[other] = 0;
                } else {
                    alive[centroid] = 0;
                }
                y_combinator(
                    [&](auto self, int u, int p) -> void {
                        ntree.push_back(u);
                        for(int w : e[u]){
                            if(w == p) continue;
                            if(!alive[w]) continue;
                            self(w, u);
                        }
                    }
                )(diff, 0);
                tree_alive = ntree;
            }
            alive = vector<int>(n+1, 0);
            for(int x : tree_alive) alive[x] = 1;
        }
        par[v] = tree_alive[0];
    }
    cout << "!" << '\n';
    vector<pair<int,int> > edges;
    for(int i = 1; i <= n; i++){
        if(par[i]){
            edges.push_back({i, par[i]});
        }
    }
    assert(edges.size() == n-1);
    for(auto [x, y] : edges){
        cout << x << ' ' << y << '\n';
    }
    cout << flush;
    if(TEST){
        cerr << "done " << '\n';
        for(auto [x, y] : edges){
            assert(ans_par[x-1] == y-1 || ans_par[y-1] == x-1);
        }
    } else {
        int res;
        cin >> res;
        assert(res == 1);
    }
}
int main(){
    ios_base::sync_with_stdio(false), cin.tie(nullptr);
    if(TEST){
        while(true) solve();
    } else {
        int T;
        cin >> T;
        while(T--) solve();
    }
}