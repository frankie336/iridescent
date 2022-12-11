#include <bits/stdc++.h>
using namespace std;
bool query(int x, int y) {
  printf("? %d %d\n", x, y);
  fflush(stdout);
  string foo;
  cin >> foo;
  return (foo == "YES");
}
int main() {
  int low = 0, high = 1000;
  while (low < high) {
    int mid = (low + high + 1) >> 1;
    bool x = query(mid, 0);
    if (x) {
      low = mid;
    } else {
      high = mid - 1;
    }
  }
  int s = low * 2;
  low = 0, high = 1000;
  while (low < high) {
    int mid = (low + high + 1) >> 1;
    bool x = query(mid, s);
    if (x) {
      low = mid;
    } else {
      high = mid - 1;
    }
  }
  int A = low;
  low = s, high = 1000;
  while (low < high) {
    int mid = (low + high + 1) >> 1;
    bool x = query(0, mid);
    if (x) {
      low = mid;
    } else {
      high = mid - 1;
    }
  }
  int B = low - s;
  printf("! %d\n", s * s + A * B);
  fflush(stdout);
  return 0;
}