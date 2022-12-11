import java.io.*;
import java.util.*;
import java.math.BigInteger;
public class Main {
    public static void main(String[] args){
      Scanner in = new Scanner(System.in);
      int p[], num[], gg[][];
      BigInteger a[][], b[][], tmp, ta, tb, ca, cb, gcd;
      String aa[] = new String[33];
      p = new int[33];
      num = new int[33];
      gg = new int[33][33];
      a = new BigInteger[33][33];
      b = new BigInteger[33][33];
      int tt = in.nextInt(), qq, i, j, t, e;
      for (qq=1;qq<=tt;qq++) {
        int n = in.nextInt();
        in.nextLine();
        for (i=0;i<n;i++) aa[i] = in.nextLine();
        for (i=0;i<n;i++) p[i] = i;
        int m = in.nextInt(), ok = 1;
        for (i=0;i<m;i++) {
          int s = in.nextInt(), f = in.nextInt();
          int x = p[s-1], y = p[f-1];
          if (x == y) ok = 0; else
            for (j=0;j<n;j++)
              if (p[j] == y) p[j] = x;
        }
        if (ok == 0) {
          System.out.println(0);
          continue;
        }
        Arrays.fill(num,0);
        for (i=0;i<n;i++) num[p[i]] = 1;
        t = 0;
        for (i=0;i<n;i++)
          if (num[i] > 0) {
            num[i] = t;
            t++;
          }
        for (i=0;i<n;i++)
          for (j=0;j<n;j++) gg[i][j] = 0;
        for (i=0;i<n;i++)
          for (j=0;j<n;j++)
            if (aa[i].charAt(j) == '1') gg[num[p[i]]][num[p[j]]]++;
        n = t;
        for (i=0;i<n;i++) gg[i][i] = 0;
        for (i=0;i<n;i++)
          for (j=0;j<n;j++)
            if (i != j) {
              gg[i][i] += gg[i][j];
              gg[i][j] = -gg[i][j];
            }
        n--;
        for (i=0;i<n;i++)
          for (j=0;j<n;j++) a[i][j] = BigInteger.ZERO;
        for (i=0;i<n;i++)
          for (j=0;j<n;j++) b[i][j] = BigInteger.ZERO;
        for (i=0;i<n+1;i++)
          for (j=0;j<n+1;j++) {
            a[i][j] = BigInteger.valueOf(gg[i][j]);
            b[i][j] = BigInteger.ONE;
          }
        ok = 1;
        for (e=0;e<n;e++) {
          for (i=e;i<n;i++)
            if (!(a[i][e].equals(BigInteger.ZERO))) {
              for (j=e;j<n;j++) {
                tmp = a[i][j]; a[i][j] = a[e][j]; a[e][j] = tmp;
                tmp = b[i][j]; b[i][j] = b[e][j]; b[e][j] = tmp;
              }
              break;
            }
          if (a[e][e].equals(BigInteger.ZERO)) {
            ok = 0;
            break;
          }
          for (i=e+1;i<n;i++)
            if (!(a[i][e].equals(BigInteger.ZERO))) {
              ta = a[i][e].multiply(b[e][e]);
              tb = b[i][e].multiply(a[e][e]);
              if (tb.compareTo(BigInteger.ZERO) < 0) {
                ta = ta.negate();
                tb = tb.negate();
              }
              gcd = ta.gcd(tb);
              ta = ta.divide(gcd);
              tb = tb.divide(gcd);
              for (j=e;j<n;j++) {
                ca = ta.multiply(a[e][j]);
                cb = tb.multiply(b[e][j]);
                a[i][j] = a[i][j].multiply(cb).subtract(ca.multiply(b[i][j]));
                b[i][j] = b[i][j].multiply(cb);
                if (a[i][j].equals(BigInteger.ZERO)) b[i][j] = BigInteger.ONE; else {
                  gcd = a[i][j].gcd(b[i][j]);
                  a[i][j] = a[i][j].divide(gcd);
                  b[i][j] = b[i][j].divide(gcd);
                }
              }
            }
        }
        if (ok == 0) System.out.println(0); else {
          ta = BigInteger.ONE;
          tb = ta;
          for (i=0;i<n;i++) {
            ta = ta.multiply(a[i][i]);
            tb = tb.multiply(b[i][i]);
            gcd = ta.gcd(tb);
            ta = ta.divide(gcd);
            tb = tb.divide(gcd);
          }
          System.out.println(ta);
        }
      }
    }
}