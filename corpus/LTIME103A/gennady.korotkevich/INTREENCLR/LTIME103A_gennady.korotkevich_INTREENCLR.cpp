/**
 *    author:  tourist
 *    created: 25.12.2021 18:57:32       
**/
#include <bits/stdc++.h>
using namespace std;
template <typename A, typename B>
string to_string(pair<A, B> p);
template <typename A, typename B, typename C>
string to_string(tuple<A, B, C> p);
template <typename A, typename B, typename C, typename D>
string to_string(tuple<A, B, C, D> p);
string to_string(const string& s) {
  return '"' + s + '"';
}
string to_string(const char* s) {
  return to_string((string) s);
}
string to_string(bool b) {
  return (b ? "true" : "false");
}
string to_string(vector<bool> v) {
  bool first = true;
  string res = "{";
  for (int i = 0; i < static_cast<int>(v.size()); i++) {
    if (!first) {
      res += ", ";
    }
    first = false;
    res += to_string(v[i]);
  }
  res += "}";
  return res;
}
template <size_t N>
string to_string(bitset<N> v) {
  string res = "";
  for (size_t i = 0; i < N; i++) {
    res += static_cast<char>('0' + v[i]);
  }
  return res;
}
template <typename A>
string to_string(A v) {
  bool first = true;
  string res = "{";
  for (const auto &x : v) {
    if (!first) {
      res += ", ";
    }
    first = false;
    res += to_string(x);
  }
  res += "}";
  return res;
}
template <typename A, typename B>
string to_string(pair<A, B> p) {
  return "(" + to_string(p.first) + ", " + to_string(p.second) + ")";
}
template <typename A, typename B, typename C>
string to_string(tuple<A, B, C> p) {
  return "(" + to_string(get<0>(p)) + ", " + to_string(get<1>(p)) + ", " + to_string(get<2>(p)) + ")";
}
template <typename A, typename B, typename C, typename D>
string to_string(tuple<A, B, C, D> p) {
  return "(" + to_string(get<0>(p)) + ", " + to_string(get<1>(p)) + ", " + to_string(get<2>(p)) + ", " + to_string(get<3>(p)) + ")";
}
void debug_out() { cerr << endl; }
template <typename Head, typename... Tail>
void debug_out(Head H, Tail... T) {
  cerr << " " << to_string(H);
  debug_out(T...);
}
#ifdef LOCAL
#define debug(...) cerr << "[" << #__VA_ARGS__ << "]:", debug_out(__VA_ARGS__)
#else
#define debug(...) 42
#endif
class dsu {
 public:
  vector<int> p;
  int n;
  dsu(int _n) : n(_n) {
    p.resize(n);
    iota(p.begin(), p.end(), 0);
  }
  inline int get(int x) {
    return (x == p[x] ? x : (p[x] = get(p[x])));
  }
  inline bool unite(int x, int y) {
    x = get(x);
    y = get(y);
    if (x != y) {
      p[x] = y;
      return true;
    }
    return false;
  }
};
int main() {
  ios::sync_with_stdio(false);
  cin.tie(0);
  int tt;
  cin >> tt;
  while (tt--) {
    int n, q;
    cin >> n >> q;
    vector<vector<int>> g(n);
    for (int i = 0; i < n - 1; i++) {
      int x, y;
      cin >> x >> y;
      --x; --y;
      g[x].push_back(y);
    }
    auto Ask = [&](int x) {
      cout << x + 1 << endl;
      int y;
      cin >> y;
      return y;
    };
    vector<int> eq(n, 0);
    vector<int> cc(n, 0);
    int cur = Ask(0);
    debug(cur);
    vector<int> pv(n, -1);
    function<void(int, int)> Dfs = [&](int v, int pr) {
      pv[v] = pr;
      int children = 0;
      cc[v] = 0;
      for (int u : g[v]) {
        if (u != pr) {
          Dfs(u, v);
          cc[v] += eq[u];
          children += 1;
        }
      }
      if (pr != -1) {
        int ncur = Ask(v);
        int expected = cur + cc[v] - (children - cc[v]);
        debug(ncur, expected);
        assert(ncur == expected + 1 || ncur == expected - 1);
        eq[v] = (ncur == expected - 1 ? 1 : 0);
        cur = ncur;
      }
    };
    Dfs(0, -1);
    debug(eq);
    dsu d(2 * n);
    for (int i = 1; i < n; i++) {
      int j = pv[i];
      if (j == 0) {
        eq[i] ^= 1;
      }
      if (eq[i] == 0) {
        d.unite(i, j);
        d.unite(i + n, j + n);
      } else {
        d.unite(i, j + n);
        d.unite(i + n, j);
      }
    }
    vector<int> color(n, 0);
    for (int i = 0; i < n; i++) {
      if (d.get(i) == d.get(0)) {
        color[i] = 1;
      }
    }
    int sum = accumulate(color.begin(), color.end(), 0);
    int maj = (2 * sum >= n);
    for (int i = 0; i < n; i++) {
      if (color[i] != maj) {
        cur = Ask(i);
      }
    }
    assert(cur == 0);
    assert(Ask(-1) == 1);
  }
  return 0;
}