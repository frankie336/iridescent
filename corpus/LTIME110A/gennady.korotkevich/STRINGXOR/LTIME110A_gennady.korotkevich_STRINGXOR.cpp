/**
 *    author:  tourist
 *    created: 17.07.2022 18:35:52       
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
    string s;
    cin >> s;
    string t;
    cin >> t;
    if (s == t) {
      cout << "YES" << "\n";
      continue;
    }
    if (s == string(n, '0')) {
      cout << "NO" << '\n';
      continue;
    }
    bool ok = false;
    for (int i = 0; i < n - 1; i++) {
      ok |= (t[i] == t[i + 1]);
    }
    cout << (ok ? "YES" : "NO") << '\n';
  }
  return 0;
}