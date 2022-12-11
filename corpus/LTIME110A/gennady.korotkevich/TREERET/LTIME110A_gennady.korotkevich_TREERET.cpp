/**
 *    author:  tourist
 *    created: 17.07.2022 19:20:52       
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
    auto Ask = [&](const vector<int>& v) {
      cout << "? " << v.size();
      for (int x : v) {
        cout << " " << x;
      }
      cout << endl;
      int x, y;
      cin >> x >> y;
      return make_pair(x, y);
    };
    vector<pair<int, int>> es;
    vector<int> all(n);
    iota(all.begin(), all.end(), 1);
    auto got = Ask(all);
    vector<int> leaves;
    while (all.size() > 2) {
      int any = got.first;
      all.erase(find(all.begin(), all.end(), any));
      auto new_got = Ask(all);
      if (new_got.second == got.second - got.first) {
        leaves.push_back(any);
        got = new_got;
        continue;
      }
      int on = new_got.second - (got.second - got.first);
      es.emplace_back(on, any);
      debug(on, any);
      int ptr = 0;
      while (true) {
        int low = ptr, high = (int) leaves.size();
        while (low < high) {
          int mid = (low + high + 1) >> 1;
          auto new_all = all;
          int goal = got.second - got.first;
          for (int i = ptr; i < mid; i++) {
            new_all.push_back(leaves[i]);
            goal += leaves[i];
          }
          if (Ask(new_all).second == goal) {
            high = mid - 1;
          } else {
            low = mid;
          }
        }
        if (low == (int) leaves.size()) {
          break;
        }
        es.emplace_back(on, leaves[low]);
        debug(on, leaves[low]);
        leaves.erase(leaves.begin() + low);
        ptr = low;
      }
      got = new_got;
    }
    es.emplace_back(all[0], all[1]);
    assert((int) es.size() == n - 1);
    cout << "!" << endl;
    for (auto& e : es) {
      cout << e.first << " " << e.second << endl;
    }
    int foo;
    cin >> foo;
    if (foo != 1) {
      break;
    }
  }
  return 0;
}