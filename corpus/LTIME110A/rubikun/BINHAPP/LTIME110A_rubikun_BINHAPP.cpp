#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
template<class T>bool chmax(T &a, const T &b) { if (a<b) { a=b; return true; } return false; }
template<class T>bool chmin(T &a, const T &b) { if (b<a) { a=b; return true; } return false; }
#define all(x) (x).begin(),(x).end()
#define fi first
#define se second
#define mp make_pair
#define si(x) int(x.size())
const int mod=998244353,MAX=300005,INF=1<<30;
// BIT セグ木 遅延セグ木 のみ
// from: https://gist.github.com/yosupo06/ddd51afb727600fd95d9d8ad6c3c80c9
// (based on AtCoder STL)
#include <algorithm>
#include <array>
#ifdef _MSC_VER
#include <intrin.h>
#endif
namespace atcoder {
    namespace internal {
        int ceil_pow2(int n) {
            int x = 0;
            while ((1U << x) < (unsigned int)(n)) x++;
            return x;
        }
        int bsf(unsigned int n) {
#ifdef _MSC_VER
            unsigned long index;
            _BitScanForward(&index, n);
            return index;
#else
            return __builtin_ctz(n);
#endif
        }
    }  // namespace internal
    }  // namespace atcoder
#include <cassert>
#include <numeric>
#include <type_traits>
namespace atcoder {
        namespace internal {
        #ifndef _MSC_VER
        template <class T>
        using is_signed_int128 =
        typename std::conditional<std::is_same<T, __int128_t>::value ||
        std::is_same<T, __int128>::value,
        std::true_type,
        std::false_type>::type;
                template <class T>
        using is_unsigned_int128 =
        typename std::conditional<std::is_same<T, __uint128_t>::value ||
        std::is_same<T, unsigned __int128>::value,
        std::true_type,
        std::false_type>::type;
                template <class T>
        using make_unsigned_int128 =
        typename std::conditional<std::is_same<T, __int128_t>::value,
        __uint128_t,
        unsigned __int128>;
                template <class T>
        using is_integral = typename std::conditional<std::is_integral<T>::value ||
        is_signed_int128<T>::value ||
        is_unsigned_int128<T>::value,
        std::true_type,
        std::false_type>::type;
                template <class T>
        using is_signed_int = typename std::conditional<(is_integral<T>::value &&
                                                         std::is_signed<T>::value) ||
        is_signed_int128<T>::value,
        std::true_type,
        std::false_type>::type;
                template <class T>
        using is_unsigned_int =
        typename std::conditional<(is_integral<T>::value &&
                                   std::is_unsigned<T>::value) ||
        is_unsigned_int128<T>::value,
        std::true_type,
        std::false_type>::type;
                template <class T>
        using to_unsigned = typename std::conditional<
        is_signed_int128<T>::value,
        make_unsigned_int128<T>,
        typename std::conditional<std::is_signed<T>::value,
        std::make_unsigned<T>,
        std::common_type<T>>::type>::type;
        #else
                template <class T> using is_integral = typename std::is_integral<T>;
                template <class T>
        using is_signed_int =
        typename std::conditional<is_integral<T>::value && std::is_signed<T>::value,
        std::true_type,
        std::false_type>::type;
                template <class T>
        using is_unsigned_int =
        typename std::conditional<is_integral<T>::value &&
        std::is_unsigned<T>::value,
        std::true_type,
        std::false_type>::type;
                template <class T>
        using to_unsigned = typename std::conditional<is_signed_int<T>::value,
        std::make_unsigned<T>,
        std::common_type<T>>::type;
        #endif
                template <class T>
        using is_signed_int_t = std::enable_if_t<is_signed_int<T>::value>;
                template <class T>
        using is_unsigned_int_t = std::enable_if_t<is_unsigned_int<T>::value>;
                template <class T> using to_unsigned_t = typename to_unsigned<T>::type;
            }  // namespace internal
    }  // namespace atcoder
#include <cassert>
#include <vector>
namespace atcoder {
        template <class T> struct fenwick_tree {
        using U = internal::to_unsigned_t<T>;
            public:
        fenwick_tree() : _n(0) {}
        fenwick_tree(int n) : _n(n), data(n) {}
                void add(int p, T x) {
            assert(0 <= p && p < _n);
            p++;
            while (p <= _n) {
                data[p - 1] += U(x);
                p += p & -p;
            }
        }
                T sum(int l, int r) {
            assert(0 <= l && l <= r && r <= _n);
            return sum(r) - sum(l);
        }
            private:
        int _n;
        std::vector<U> data;
                U sum(int r) {
            U s = 0;
            while (r > 0) {
                s += data[r - 1];
                r -= r & -r;
            }
            return s;
        }
    };
    }  // namespace atcoder
#include <algorithm>
#include <cassert>
#include <iostream>
#include <vector>
namespace atcoder {
        template <class S,
    S (*op)(S, S),
    S (*e)(),
    class F,
    S (*mapping)(F, S),
    F (*composition)(F, F),
    F (*id)()>
    struct lazy_segtree {
    public:
        lazy_segtree() : lazy_segtree(0) {}
        lazy_segtree(int n) : lazy_segtree(std::vector<S>(n, e())) {}
        lazy_segtree(const std::vector<S>& v) : _n(int(v.size())) {
            log = internal::ceil_pow2(_n);
            size = 1 << log;
            d = std::vector<S>(2 * size, e());
            lz = std::vector<F>(size, id());
            for (int i = 0; i < _n; i++) d[size + i] = v[i];
            for (int i = size - 1; i >= 1; i--) {
                update(i);
            }
        }
                void set(int p, S x) {
            assert(0 <= p && p < _n);
            p += size;
            for (int i = log; i >= 1; i--) push(p >> i);
            d[p] = x;
            for (int i = 1; i <= log; i++) update(p >> i);
        }
                S get(int p) {
            assert(0 <= p && p < _n);
            p += size;
            for (int i = log; i >= 1; i--) push(p >> i);
            return d[p];
        }
                S prod(int l, int r) {
            assert(0 <= l && l <= r && r <= _n);
            if (l == r) return e();
                        l += size;
            r += size;
                        for (int i = log; i >= 1; i--) {
                if (((l >> i) << i) != l) push(l >> i);
                if (((r >> i) << i) != r) push(r >> i);
            }
                        S sml = e(), smr = e();
            while (l < r) {
                if (l & 1) sml = op(sml, d[l++]);
                if (r & 1) smr = op(d[--r], smr);
                l >>= 1;
                r >>= 1;
            }
                        return op(sml, smr);
        }
                S all_prod() { return d[1]; }
                void apply(int p, F f) {
            assert(0 <= p && p < _n);
            p += size;
            for (int i = log; i >= 1; i--) push(p >> i);
            d[p] = mapping(f, d[p]);
            for (int i = 1; i <= log; i++) update(p >> i);
        }
        void apply(int l, int r, F f) {
            assert(0 <= l && l <= r && r <= _n);
            if (l == r) return;
                        l += size;
            r += size;
                        for (int i = log; i >= 1; i--) {
                if (((l >> i) << i) != l) push(l >> i);
                if (((r >> i) << i) != r) push((r - 1) >> i);
            }
                        {
                int l2 = l, r2 = r;
                while (l < r) {
                    if (l & 1) all_apply(l++, f);
                    if (r & 1) all_apply(--r, f);
                    l >>= 1;
                    r >>= 1;
                }
                l = l2;
                r = r2;
            }
                        for (int i = 1; i <= log; i++) {
                if (((l >> i) << i) != l) update(l >> i);
                if (((r >> i) << i) != r) update((r - 1) >> i);
            }
        }
                template <bool (*g)(S)> int max_right(int l) {
            return max_right(l, [](S x) { return g(x); });
        }
        template <class G> int max_right(int l, G g) {
            assert(0 <= l && l <= _n);
            assert(g(e()));
            if (l == _n) return _n;
            l += size;
            for (int i = log; i >= 1; i--) push(l >> i);
            S sm = e();
            do {
                while (l % 2 == 0) l >>= 1;
                if (!g(op(sm, d[l]))) {
                    while (l < size) {
                        push(l);
                        l = (2 * l);
                        if (g(op(sm, d[l]))) {
                            sm = op(sm, d[l]);
                            l++;
                        }
                    }
                    return l - size;
                }
                sm = op(sm, d[l]);
                l++;
            } while ((l & -l) != l);
            return _n;
        }
                template <bool (*g)(S)> int min_left(int r) {
            return min_left(r, [](S x) { return g(x); });
        }
        template <class G> int min_left(int r, G g) {
            assert(0 <= r && r <= _n);
            assert(g(e()));
            if (r == 0) return 0;
            r += size;
            for (int i = log; i >= 1; i--) push((r - 1) >> i);
            S sm = e();
            do {
                r--;
                while (r > 1 && (r % 2)) r >>= 1;
                if (!g(op(d[r], sm))) {
                    while (r < size) {
                        push(r);
                        r = (2 * r + 1);
                        if (g(op(d[r], sm))) {
                            sm = op(d[r], sm);
                            r--;
                        }
                    }
                    return r + 1 - size;
                }
                sm = op(d[r], sm);
            } while ((r & -r) != r);
            return 0;
        }
            private:
        int _n, size, log;
        std::vector<S> d;
        std::vector<F> lz;
                void update(int k) { d[k] = op(d[2 * k], d[2 * k + 1]); }
        void all_apply(int k, F f) {
            d[k] = mapping(f, d[k]);
            if (k < size) lz[k] = composition(f, lz[k]);
        }
        void push(int k) {
            all_apply(2 * k, lz[k]);
            all_apply(2 * k + 1, lz[k]);
            lz[k] = id();
        }
    };
    }  // namespace atcoder
#include <algorithm>
#include <cassert>
#include <vector>
namespace atcoder {
        template <class S, S (*op)(S, S), S (*e)()> struct segtree {
    public:
        segtree() : segtree(0) {}
        segtree(int n) : segtree(std::vector<S>(n, e())) {}
        segtree(const std::vector<S>& v) : _n(int(v.size())) {
            log = internal::ceil_pow2(_n);
            size = 1 << log;
            d = std::vector<S>(2 * size, e());
            for (int i = 0; i < _n; i++) d[size + i] = v[i];
            for (int i = size - 1; i >= 1; i--) {
                update(i);
            }
        }
                void set(int p, S x) {
            assert(0 <= p && p < _n);
            p += size;
            d[p] = x;
            for (int i = 1; i <= log; i++) update(p >> i);
        }
                S get(int p) {
            assert(0 <= p && p < _n);
            return d[p + size];
        }
                S prod(int l, int r) {
            assert(0 <= l && l <= r && r <= _n);
            S sml = e(), smr = e();
            l += size;
            r += size;
                        while (l < r) {
                if (l & 1) sml = op(sml, d[l++]);
                if (r & 1) smr = op(d[--r], smr);
                l >>= 1;
                r >>= 1;
            }
            return op(sml, smr);
        }
                S all_prod() { return d[1]; }
                template <bool (*f)(S)> int max_right(int l) {
            return max_right(l, [](S x) { return f(x); });
        }
        template <class F> int max_right(int l, F f) {
            assert(0 <= l && l <= _n);
            assert(f(e()));
            if (l == _n) return _n;
            l += size;
            S sm = e();
            do {
                while (l % 2 == 0) l >>= 1;
                if (!f(op(sm, d[l]))) {
                    while (l < size) {
                        l = (2 * l);
                        if (f(op(sm, d[l]))) {
                            sm = op(sm, d[l]);
                            l++;
                        }
                    }
                    return l - size;
                }
                sm = op(sm, d[l]);
                l++;
            } while ((l & -l) != l);
            return _n;
        }
                template <bool (*f)(S)> int min_left(int r) {
            return min_left(r, [](S x) { return f(x); });
        }
        template <class F> int min_left(int r, F f) {
            assert(0 <= r && r <= _n);
            assert(f(e()));
            if (r == 0) return 0;
            r += size;
            S sm = e();
            do {
                r--;
                while (r > 1 && (r % 2)) r >>= 1;
                if (!f(op(d[r], sm))) {
                    while (r < size) {
                        r = (2 * r + 1);
                        if (f(op(d[r], sm))) {
                            sm = op(d[r], sm);
                            r--;
                        }
                    }
                    return r + 1 - size;
                }
                sm = op(d[r], sm);
            } while ((r & -r) != r);
            return 0;
        }
            private:
        int _n, size, log;
        std::vector<S> d;
                void update(int k) { d[k] = op(d[2 * k], d[2 * k + 1]); }
    };
    }  // namespace atcoder
struct T{
    int ma;
    int sum;
    pair<int,int> pref1;
    pair<int,int> pref2;
    pair<int,int> suff1;
    pair<int,int> suff2;
};
T f(T a,T b){
    T res;
    res.ma=max(a.ma,b.ma);
    res.sum=a.sum+b.sum;
    if(a.pref1>b.pref1){
        res.pref1=a.pref1;
        res.pref2=max(a.pref2,b.pref1);
    }else{
        res.pref1=b.pref1;
        res.pref2=max(a.pref1,b.pref2);
    }
    if(a.suff1>b.suff1){
        res.suff1=a.suff1;
        res.suff2=max(a.suff2,b.suff1);
    }else{
        res.suff1=b.suff1;
        res.suff2=max(a.suff1,b.suff2);
    }
    return res;
}
T ti(){
    return {0,0,mp(0,-1),mp(0,-1),mp(0,-1),mp(0,-1)};
}
int main(){
        std::ifstream in("text.txt");
    std::cin.rdbuf(in.rdbuf());
    cin.tie(0);
    ios::sync_with_stdio(false);
        int N,Q;cin>>N>>Q;
    vector<T> def(N);
    for(int i=0;i<N;i++){
        int K;cin>>K;
        vector<int> rui(K+1);
        int mi=0,ma=0,sum=0;
        string S;cin>>S;
        for(int j=0;j<K;j++){
            if(S[j]=='1') sum++;
            else sum--;
            chmax(ma,sum-mi);
            chmin(mi,sum);
            rui[j+1]=sum;
        }
        def[i].ma=ma;
        chmax(sum,0);
        def[i].sum=sum;
        int pre=0;
        for(int j=0;j<=K;j++) chmax(pre,rui[j]-rui[0]);
        pre-=sum;
        chmax(pre,0);
        def[i].pref1=mp(pre,i);
        def[i].pref2=mp(0,-1);
                int suf=0;
        for(int j=0;j<=K;j++) chmax(suf,rui[K]-rui[j]);
        suf-=sum;
        chmax(suf,0);
        def[i].suff1=mp(suf,i);
        def[i].suff2=mp(0,-1);
    }
        //for(int i=0;i<N;i++) cout<<def[i].ma<<" "<<def[i].sum<<" "<<def[i].pref1.fi<<" "<<def[i].pref2.fi<<" "<<def[i].suff1.fi<<" "<<def[i].suff2.fi<<endl;
    atcoder::segtree<T,f,ti> seg(def);
        while(Q--){
        int l,r;cin>>l>>r;l--;
        auto res=seg.prod(l,r);
        int ma=0;
        if(res.pref1.se!=res.suff1.se){
            chmax(ma,res.pref1.fi+res.suff1.fi);
        }else{
            chmax(ma,res.pref1.fi+res.suff2.fi);
            chmax(ma,res.pref2.fi+res.suff1.fi);
        }
        cout<<max(res.ma,res.sum+ma)<<"\n";
    }
}