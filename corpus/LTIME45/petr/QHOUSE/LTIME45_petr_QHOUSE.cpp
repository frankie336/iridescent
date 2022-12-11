import java.io.OutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.PrintWriter;
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
        QHouse solver = new QHouse();
        solver.solve(1, in, out);
        out.close();
    }
    static class QHouse {
        public void solve(int testNumber, InputReader in, PrintWriter out) {
            int left = 1;
            int right = 500;
            while (right - left > 1) {
                int middle = (left + right) >> 1;
                out.println("? " + middle + " 0");
                out.flush();
                if (in.next().equals("YES")) {
                    left = middle;
                } else {
                    right = middle;
                }
            }
            int squarex = left;
            left = squarex + 1;
            right = 1001;
            while (right - left > 1) {
                int middle = (left + right) >> 1;
                out.println("? " + middle + " " + (2 * squarex));
                out.flush();
                if (in.next().equals("YES")) {
                    left = middle;
                } else {
                    right = middle;
                }
            }
            int trix = left;
            left = 2 * squarex + 1;
            right = 1001;
            while (right - left > 1) {
                int middle = (left + right) >> 1;
                out.println("? " + "0 " + middle);
                out.flush();
                if (in.next().equals("YES")) {
                    left = middle;
                } else {
                    right = middle;
                }
            }
            int triy = left;
            out.println("! " + (4 * squarex * squarex + trix * (triy - 2 * squarex)));
            out.flush();
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
    }
}