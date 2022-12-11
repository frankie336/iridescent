#include <bits/stdc++.h>
using namespace std;
const int inf = (int) 1e9;
const int N = 1234567;
int x[N];
int k;
vector < pair <int, int> > solve(int from, int to) {
  vector < pair <int, int> > ret;
  if (from + 1 == to) {
    ret.push_back(make_pair(x[from], 0));
    return ret;
  }
  int mid = (from + to) >> 1;
  vector < pair <int, int> > a = solve(from, mid);
  vector < pair <int, int> > b = solve(mid, to);
  int sz = b.size();
  for (int rot = 0; rot < 2; rot++) {
    vector < pair <int, int> > bb = b;
    for (int i = 1; i < sz; i++) {
      bb[i].second = min(bb[i].second, bb[i - 1].second);
    }
    int j = 0, t = 0;
    for (int i = 0; i < sz; i++) {
      while (j < sz && b[j].first < a[i].first) {
        j++;
      }
      while (t < sz && b[t].first <= a[i].first + k) {
        t++;
      }
      int cur = inf;
      if (t > 0) {
        cur = min(cur, a[i].second + bb[t - 1].second + 1);
      }
      if (j > 0) {
        cur = min(cur, a[i].second + bb[j - 1].second);
      }
      ret.push_back(make_pair(a[i].first, cur));
    }
    swap(a, b);
  }
  sort(ret.begin(), ret.end());
  return ret;
}
int main() {
  int tt;
  scanf("%d", &tt);
  while (tt--) {
    int n;
    scanf("%d %d", &n, &k);
    n = (1 << n);
    for (int i = 0; i < n; i++) {
      scanf("%d", x + i);
    }
    vector < pair <int, int> > v = solve(0, n);
    int ans = -1;
    for (int i = 0; i < n; i++) {
      if (v[i].first == x[0]) {
        ans = v[i].second;
      }
    }
    printf("%d\n", ans >= inf ? -1 : ans);
  }
  return 0;
}