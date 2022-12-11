#include <bits/stdc++.h>
using namespace std;
int main() {
  int tt;
  scanf("%d", &tt);
  while (tt--) {
    int n;
    scanf("%d", &n);
    vector <string> s(n);
    for (int i = 0; i < n; i++) {
      cin >> s[i];
    }
    bool ok = true;
    for (int i = 0; i < n; i++) {
      if (s[i] == "cookie" && (i == n - 1 || s[i + 1] != "milk")) {
        ok = false;
      }
    }
    puts(ok ? "YES" : "NO");
  }
  return 0;
}