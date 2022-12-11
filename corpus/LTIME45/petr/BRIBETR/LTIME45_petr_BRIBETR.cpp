import java.io.OutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.PrintWriter;
import java.util.Arrays;
import java.util.StringTokenizer;
import java.io.IOException;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.InputStream;
/**
 * Built using CHelper plug-in
 * Actual solution is at the top
 */
public class Main {
    public static void main(String[] args) {
        InputStream inputStream = System.in;
        OutputStream outputStream = System.out;
        InputReader in = new InputReader(inputStream);
        PrintWriter out = new PrintWriter(outputStream);
        BearAndBribingTree solver = new BearAndBribingTree();
        int testCount = Integer.parseInt(in.next());
        for (int i = 1; i <= testCount; i++)
            solver.solve(i, in, out);
        out.close();
    }
    static class BearAndBribingTree {
        static final int INF = (int) 1e9;
        public void solve(int testNumber, InputReader in, PrintWriter out) {
            int h = in.nextInt();
            int k = in.nextInt();
            int[] x = new int[1 << h];
            for (int i = 0; i < x.length; ++i) x[i] = in.nextInt();
            int[][] minBribes = new int[h + 1][x.length];
            long[] us = new long[x.length];
            long[] them = new long[x.length];
            long bonus = (((long) k) << 32) + (1L << 31);
            long res = 0;
            for (int layer = 1; layer <= h; ++layer) {
                int blockSize = 1 << (layer - 1);
                for (int block = 0; block < x.length; block += blockSize) {
                    int otherBlock = block ^ blockSize;
                    for (int i = 0; i < blockSize; ++i) {
                        us[i] = (((long) x[block + i]) << 32) + i;
                        them[i] = (((long) x[otherBlock + i]) << 32) + minBribes[layer - 1][otherBlock + i];
                    }
                    Arrays.sort(us, 0, blockSize);
                    Arrays.sort(them, 0, blockSize);
                    int ptrFair = 0;
                    int bestFair = INF;
                    int ptrBribe = 0;
                    int bestBribe = INF;
                    for (int i = 0; i < blockSize; ++i) {
                        long pair = us[i];
                        int strength = (int) (pair >>> 32);
                        int id = (int) (pair & ((1L << 32) - 1));
                        while (ptrFair < blockSize && them[ptrFair] <= pair) {
                            int got = (int) (them[ptrFair] & ((1L << 32) - 1));
                            bestFair = Math.min(bestFair, got);
                            ++ptrFair;
                        }
                        while (ptrBribe < blockSize && them[ptrBribe] <= pair + bonus) {
                            int got = (int) (them[ptrBribe] & ((1L << 32) - 1));
                            bestBribe = Math.min(bestBribe, got);
                            ++ptrBribe;
                        }
                        minBribes[layer][block + id] = Math.min(INF, minBribes[layer - 1][block + id] + Math.min(bestFair, bestBribe + 1));
                    }
                }
            }
            res += minBribes[h][0];
            if (res >= INF) {
                out.println(-1);
                return;
            }
            out.println(res);
        }
    }
    static class InputReader {
        public BufferedReader reader;
        public StringTokenizer tokenizer;
        public InputReader(InputStream stream) {
            reader = new BufferedReader(new InputStreamReader(stream), 32768);
            tokenizer = null;
        }
        public String next() {
            while (tokenizer == null || !tokenizer.hasMoreTokens()) {
                try {
                    tokenizer = new StringTokenizer(reader.readLine());
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
            }
            return tokenizer.nextToken();
        }
        public int nextInt() {
            return Integer.parseInt(next());
        }
    }
}