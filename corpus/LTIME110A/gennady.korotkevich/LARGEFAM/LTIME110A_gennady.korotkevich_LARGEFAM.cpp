/**
 *    author:  tourist
 *    created: 17.07.2022 18:30:57
**/
#include <bits/stdc++.h>
using namespace std;
#ifdef LOCAL
#include "algo/debug.h"
#else
#define debug(...) 42
#endif
int main() {
  ios::sync_with_stdio(false);
  cin.tie(0);
  int tt;
  cin >> tt;
  while (tt--) {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) {
      cin >> a[i];
    }
    sort(a.begin(), a.end());
    int k = 0;
    int s = 0;
    while (k < n && s + a[k] <= n - 1) {
      s += a[k];
      k += 1;
    }
    cout << k << '\n';
  }
  return 0;
}