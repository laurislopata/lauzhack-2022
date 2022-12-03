import java.io.BufferedWriter;
import java.io.IOException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.io.Writer;
import java.util.Arrays;
import java.util.InputMismatchException;
import java.util.Iterator;
import java.util.NoSuchElementException;

/**
 * Built using CHelper plug-in
 * Actual solution is at the top
 *
 * @author aryssoncf
 */
public class Main {

  public static void main(String[] args) {
    InputStream inputStream = System.in;
    OutputStream outputStream = System.out;
    InputReader in = new InputReader(inputStream);
    OutputWriter out = new OutputWriter(outputStream);
    TaskD solver = new TaskD();
    solver.solve(1, in, out);
    out.close();
  }

  static class TaskD {

    public void solve(int testNumber, InputReader in, OutputWriter out) {
      try {
        int n = in.readInt();
        int[] x = new int[n], w = new int[n];
        in.readIntArrays(x, w);
        int[] begin = new int[n], end = new int[n];
        Arrays.setAll(begin, i -> x[i] - w[i]);
        Arrays.setAll(end, i -> x[i] + w[i]);
        int m = ArrayUtils.compress(begin, end).length;
        int[] dp = new int[m + 1], order = ArrayUtils.order(end);
        int idx = 0;
        for (int i = 0; i < m; i++) {
          if (i > 0) {
            dp[i] = dp[i - 1];
          }
          while (idx < n && end[order[idx]] == i) {
            dp[i] = Math.max(dp[i], dp[begin[order[idx]]] + 1);
            idx++;
          }
        }
        int res = dp[m - 1];
        out.printLine(res);
      } catch (Exception e) {
        e.printStackTrace();
      }
    }
  }

  static class Sorter {

    private static final int INSERTION_THRESHOLD = 16;

    private Sorter() {}

    public static void sort(IntList list, IntComparator comparator) {
      quickSort(
        list,
        0,
        list.size() - 1,
        (Integer.bitCount(Integer.highestOneBit(list.size()) - 1) * 5) >> 1,
        comparator
      );
    }

    private static void quickSort(
      IntList list,
      int from,
      int to,
      int remaining,
      IntComparator comparator
    ) {
      if (to - from < INSERTION_THRESHOLD) {
        insertionSort(list, from, to, comparator);
        return;
      }
      if (remaining == 0) {
        heapSort(list, from, to, comparator);
        return;
      }
      remaining--;
      int pivotIndex = (from + to) >> 1;
      int pivot = list.get(pivotIndex);
      list.swap(pivotIndex, to);
      int storeIndex = from;
      int equalIndex = to;
      for (int i = from; i < equalIndex; i++) {
        int value = comparator.compare(list.get(i), pivot);
        if (value < 0) {
          list.swap(storeIndex++, i);
        } else if (value == 0) {
          list.swap(--equalIndex, i--);
        }
      }
      quickSort(list, from, storeIndex - 1, remaining, comparator);
      for (int i = equalIndex; i <= to; i++) {
        list.swap(storeIndex++, i);
      }
      quickSort(list, storeIndex, to, remaining, comparator);
    }

    private static void heapSort(
      IntList list,
      int from,
      int to,
      IntComparator comparator
    ) {
      for (int i = (to + from - 1) >> 1; i >= from; i--) {
        siftDown(list, i, to, comparator, from);
      }
      for (int i = to; i > from; i--) {
        list.swap(from, i);
        siftDown(list, from, i - 1, comparator, from);
      }
    }

    private static void siftDown(
      IntList list,
      int start,
      int end,
      IntComparator comparator,
      int delta
    ) {
      int value = list.get(start);
      while (true) {
        int child = ((start - delta) << 1) + 1 + delta;
        if (child > end) {
          return;
        }
        int childValue = list.get(child);
        if (child + 1 <= end) {
          int otherValue = list.get(child + 1);
          if (comparator.compare(otherValue, childValue) > 0) {
            child++;
            childValue = otherValue;
          }
        }
        if (comparator.compare(value, childValue) >= 0) {
          return;
        }
        list.swap(start, child);
        start = child;
      }
    }

    private static void insertionSort(
      IntList list,
      int from,
      int to,
      IntComparator comparator
    ) {
      for (int i = from + 1; i <= to; i++) {
        int value = list.get(i);
        for (int j = i - 1; j >= from; j--) {
          if (comparator.compare(list.get(j), value) <= 0) {
            break;
          }
          list.swap(j, j + 1);
        }
      }
    }
  }

  static interface IntList extends IntReversableCollection {
    public abstract int get(int index);

    public abstract void set(int index, int value);

    public abstract void addAt(int index, int value);

    public abstract void removeAt(int index);

    public default void swap(int first, int second) {
      if (first == second) {
        return;
      }
      int temp = get(first);
      set(first, get(second));
      set(second, temp);
    }

    public default IntIterator intIterator() {
      return new IntIterator() {
        private int at;
        private boolean removed;

        public int value() {
          if (removed) {
            throw new IllegalStateException();
          }
          return get(at);
        }

        public boolean advance() {
          at++;
          removed = false;
          return isValid();
        }

        public boolean isValid() {
          return !removed && at < size();
        }

        public void remove() {
          removeAt(at);
          at--;
          removed = true;
        }
      };
    }

    public default void add(int value) {
      addAt(size(), value);
    }

    public default IntList sort(IntComparator comparator) {
      Sorter.sort(this, comparator);
      return this;
    }

    default IntList unique() {
      int last = Integer.MIN_VALUE;
      IntList result = new IntArrayList();
      int size = size();
      for (int i = 0; i < size; i++) {
        int current = get(i);
        if (current != last) {
          result.add(current);
          last = current;
        }
      }
      return result;
    }

    public default IntList subList(final int from, final int to) {
      return new IntList() {
        private final int shift;
        private final int size;

        {
          if (from < 0 || from > to || to > IntList.this.size()) {
            throw new IndexOutOfBoundsException(
              "from = " + from + ", to = " + to + ", size = " + size()
            );
          }
          shift = from;
          size = to - from;
        }

        public int size() {
          return size;
        }

        public int get(int at) {
          if (at < 0 || at >= size) {
            throw new IndexOutOfBoundsException(
              "at = " + at + ", size = " + size()
            );
          }
          return IntList.this.get(at + shift);
        }

        public void addAt(int index, int value) {
          throw new UnsupportedOperationException();
        }

        public void removeAt(int index) {
          throw new UnsupportedOperationException();
        }

        public void set(int at, int value) {
          if (at < 0 || at >= size) {
            throw new IndexOutOfBoundsException(
              "at = " + at + ", size = " + size()
            );
          }
          IntList.this.set(at + shift, value);
        }

        public IntList compute() {
          return new IntArrayList(this);
        }
      };
    }
  }

  static interface IntComparator {
    IntComparator DEFAULT = Integer::compare;

    int compare(int first, int second);
  }

  static class Range {

    public static IntList range(int from, int to) {
      int[] result = new int[Math.abs(from - to)];
      int current = from;
      if (from <= to) {
        for (int i = 0; i < result.length; i++) {
          result[i] = current++;
        }
      } else {
        for (int i = 0; i < result.length; i++) {
          result[i] = current--;
        }
      }
      return new IntArray(result);
    }
  }

  static interface IntReversableCollection extends IntCollection {}

  static class OutputWriter {

    private final PrintWriter writer;

    public OutputWriter(OutputStream outputStream) {
      writer =
        new PrintWriter(
          new BufferedWriter(new OutputStreamWriter(outputStream))
        );
    }

    public OutputWriter(Writer writer) {
      this.writer = new PrintWriter(writer);
    }

    public void close() {
      writer.close();
    }

    public void printLine(int i) {
      writer.println(i);
    }
  }

  static interface IntStream extends Iterable<Integer>, Comparable<IntStream> {
    IntIterator intIterator();

    default Iterator<Integer> iterator() {
      return new Iterator<Integer>() {
        private IntIterator it = intIterator();

        public boolean hasNext() {
          return it.isValid();
        }

        public Integer next() {
          int result = it.value();
          it.advance();
          return result;
        }
      };
    }

    default int compareTo(IntStream c) {
      IntIterator it = intIterator();
      IntIterator jt = c.intIterator();
      while (it.isValid() && jt.isValid()) {
        int i = it.value();
        int j = jt.value();
        if (i < j) {
          return -1;
        } else if (i > j) {
          return 1;
        }
        it.advance();
        jt.advance();
      }
      if (it.isValid()) {
        return 1;
      }
      if (jt.isValid()) {
        return -1;
      }
      return 0;
    }
  }

  static class InputReader {

    private InputStream stream;
    private byte[] buf = new byte[1024];
    private int curChar;
    private int numChars;
    private InputReader.SpaceCharFilter filter;

    public InputReader(InputStream stream) {
      this.stream = stream;
    }

    public void readIntArrays(int[]... arrays) {
      for (int i = 0; i < arrays[0].length; i++) {
        for (int j = 0; j < arrays.length; j++) {
          arrays[j][i] = readInt();
        }
      }
    }

    public int read() {
      if (numChars == -1) {
        throw new InputMismatchException();
      }
      if (curChar >= numChars) {
        curChar = 0;
        try {
          numChars = stream.read(buf);
        } catch (IOException e) {
          throw new InputMismatchException();
        }
        if (numChars <= 0) {
          return -1;
        }
      }
      return buf[curChar++];
    }

    public int readInt() {
      int c = read();
      while (isSpaceChar(c)) {
        c = read();
      }
      int sgn = 1;
      if (c == '-') {
        sgn = -1;
        c = read();
      }
      int res = 0;
      do {
        if (c < '0' || c > '9') {
          throw new InputMismatchException();
        }
        res *= 10;
        res += c - '0';
        c = read();
      } while (!isSpaceChar(c));
      return res * sgn;
    }

    public boolean isSpaceChar(int c) {
      if (filter != null) {
        return filter.isSpaceChar(c);
      }
      return isWhitespace(c);
    }

    public static boolean isWhitespace(int c) {
      return c == ' ' || c == '\n' || c == '\r' || c == '\t' || c == -1;
    }

    public interface SpaceCharFilter {
      boolean isSpaceChar(int ch);
    }
  }

  static interface IntCollection extends IntStream {
    public int size();

    public default void add(int value) {
      throw new UnsupportedOperationException();
    }

    public default int[] toArray() {
      int size = size();
      int[] array = new int[size];
      int i = 0;
      for (IntIterator it = intIterator(); it.isValid(); it.advance()) {
        array[i++] = it.value();
      }
      return array;
    }

    public default IntCollection addAll(IntStream values) {
      for (IntIterator it = values.intIterator(); it.isValid(); it.advance()) {
        add(it.value());
      }
      return this;
    }
  }

  static class IntArray extends IntAbstractStream implements IntList {

    private int[] data;

    public IntArray(int[] arr) {
      data = arr;
    }

    public int size() {
      return data.length;
    }

    public int get(int at) {
      return data[at];
    }

    public void addAt(int index, int value) {
      throw new UnsupportedOperationException();
    }

    public void removeAt(int index) {
      throw new UnsupportedOperationException();
    }

    public void set(int index, int value) {
      data[index] = value;
    }
  }

  static class ArrayUtils {

    public static int[] range(int from, int to) {
      return Range.range(from, to).toArray();
    }

    public static int[] createOrder(int size) {
      return range(0, size);
    }

    public static int[] sort(int[] array, IntComparator comparator) {
      return sort(array, 0, array.length, comparator);
    }

    public static int[] sort(
      int[] array,
      int from,
      int to,
      IntComparator comparator
    ) {
      if (from == 0 && to == array.length) {
        new IntArray(array).sort(comparator);
      } else {
        new IntArray(array).subList(from, to).sort(comparator);
      }
      return array;
    }

    public static int[] order(final int[] array) {
      return sort(
        createOrder(array.length),
        (first, second) -> Integer.compare(array[first], array[second])
      );
    }

    public static int[] unique(int[] array) {
      return new IntArray(array).unique().toArray();
    }

    public static int[] compress(int[]... arrays) {
      int totalLength = 0;
      for (int[] array : arrays) {
        totalLength += array.length;
      }
      int[] all = new int[totalLength];
      int delta = 0;
      for (int[] array : arrays) {
        System.arraycopy(array, 0, all, delta, array.length);
        delta += array.length;
      }
      sort(all, IntComparator.DEFAULT);
      all = unique(all);
      for (int[] array : arrays) {
        for (int i = 0; i < array.length; i++) {
          array[i] = Arrays.binarySearch(all, array[i]);
        }
      }
      return all;
    }
  }

  static interface IntIterator {
    public int value() throws NoSuchElementException;

    public boolean advance();

    public boolean isValid();
  }

  static class IntArrayList extends IntAbstractStream implements IntList {

    private int size;
    private int[] data;

    public IntArrayList() {
      this(3);
    }

    public IntArrayList(int capacity) {
      data = new int[capacity];
    }

    public IntArrayList(IntCollection c) {
      this(c.size());
      addAll(c);
    }

    public IntArrayList(IntStream c) {
      this();
      if (c instanceof IntCollection) {
        ensureCapacity(((IntCollection) c).size());
      }
      addAll(c);
    }

    public IntArrayList(IntArrayList c) {
      size = c.size();
      data = c.data.clone();
    }

    public IntArrayList(int[] arr) {
      size = arr.length;
      data = arr.clone();
    }

    public int size() {
      return size;
    }

    public int get(int at) {
      if (at >= size) {
        throw new IndexOutOfBoundsException("at = " + at + ", size = " + size);
      }
      return data[at];
    }

    private void ensureCapacity(int capacity) {
      if (data.length >= capacity) {
        return;
      }
      capacity = Math.max(2 * data.length, capacity);
      data = Arrays.copyOf(data, capacity);
    }

    public void addAt(int index, int value) {
      ensureCapacity(size + 1);
      if (index > size || index < 0) {
        throw new IndexOutOfBoundsException(
          "at = " + index + ", size = " + size
        );
      }
      if (index != size) {
        System.arraycopy(data, index, data, index + 1, size - index);
      }
      data[index] = value;
      size++;
    }

    public void removeAt(int index) {
      if (index >= size || index < 0) {
        throw new IndexOutOfBoundsException(
          "at = " + index + ", size = " + size
        );
      }
      if (index != size - 1) {
        System.arraycopy(data, index + 1, data, index, size - index - 1);
      }
      size--;
    }

    public void set(int index, int value) {
      if (index >= size) {
        throw new IndexOutOfBoundsException(
          "at = " + index + ", size = " + size
        );
      }
      data[index] = value;
    }

    public int[] toArray() {
      return Arrays.copyOf(data, size);
    }
  }

  abstract static class IntAbstractStream implements IntStream {

    public String toString() {
      StringBuilder builder = new StringBuilder();
      boolean first = true;
      for (IntIterator it = intIterator(); it.isValid(); it.advance()) {
        if (first) {
          first = false;
        } else {
          builder.append(' ');
        }
        builder.append(it.value());
      }
      return builder.toString();
    }

    public boolean equals(Object o) {
      if (!(o instanceof IntStream)) {
        return false;
      }
      IntStream c = (IntStream) o;
      IntIterator it = intIterator();
      IntIterator jt = c.intIterator();
      while (it.isValid() && jt.isValid()) {
        if (it.value() != jt.value()) {
          return false;
        }
        it.advance();
        jt.advance();
      }
      return !it.isValid() && !jt.isValid();
    }

    public int hashCode() {
      int result = 0;
      for (IntIterator it = intIterator(); it.isValid(); it.advance()) {
        result *= 31;
        result += it.value();
      }
      return result;
    }
  }
}
