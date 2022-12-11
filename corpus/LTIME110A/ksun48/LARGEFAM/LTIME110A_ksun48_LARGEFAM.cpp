#include <bits/stdc++.h>
using namespace std;
void solve(){
    int n;
    cin >> n;
    vector<int> a(n);
    for(int& x : a) cin >> x;
    sort(a.begin(), a.end());
    int R = n-1;
    int ans = 0;
    for(int x : a){
        if(R >= x){
            R -= x;
            ans++;
        }
    }
    cout << ans << '\n';
}
int main(){
    ios_base::sync_with_stdio(false), cin.tie(nullptr);
    int T;
    cin >> T;
    while(T--) solve();
}