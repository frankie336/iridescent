#include <bits/stdc++.h>
using namespace std;
bool works(string s, string t){
    if(s == t) return true;
    int n = (int)s.size();
    if(s == string(n, '0')) return false;
    if(t == "11" || t == "00") return true;
    if(n == 2) return false;
    for(int i = 0; i < 2; i++){
        string z;
        for(int j = 0; j < n; j++){
            z += char('0' + ((j + i) & 1));
        }
        cerr << z << '\n';
        if(t == z) return false;
    }
    return true;
}
void solve(){
    int n;
    cin >> n;
    string s, t;
    cin >> s >> t;
    cout << (works(s, t) ? "YES" : "NO") << '\n';
}
int main(){
    ios_base::sync_with_stdio(false), cin.tie(nullptr);
    int T;
    cin >> T;
    while(T--) solve();
}