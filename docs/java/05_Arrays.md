# Arrays in Java

## What is an Array?

An array is a fixed-size, ordered collection of elements of the same type.

## Declaring and Creating Arrays

```java
// Declaration only
int[] numbers;

// Declaration + creation
int[] numbers = new int[5];   // array of 5 ints, all initialized to 0

// Declaration + creation + initialization
int[] primes = {2, 3, 5, 7, 11};
String[] days = {"Mon", "Tue", "Wed", "Thu", "Fri"};
```

## Accessing Elements

```java
int[] arr = {10, 20, 30, 40, 50};

arr[0]   // 10  (first element)
arr[4]   // 50  (last element)
arr[2]   // 30

arr.length   // 5 (not a method — it's a field)
```

Attempting to access an index outside the valid range throws `ArrayIndexOutOfBoundsException`.

## Modifying Elements

```java
arr[0] = 99;   // arr is now {99, 20, 30, 40, 50}
```

## Iterating Over Arrays

```java
int[] arr = {10, 20, 30, 40};

// Classic for loop
for (int i = 0; i < arr.length; i++) {
    System.out.println("Index " + i + ": " + arr[i]);
}

// Enhanced for loop
for (int val : arr) {
    System.out.println(val);
}
```

## Multi-dimensional Arrays

```java
// 2D array (matrix)
int[][] matrix = new int[3][4];   // 3 rows, 4 columns

// 2D array with initialization
int[][] grid = {
    {1, 2, 3},
    {4, 5, 6},
    {7, 8, 9}
};

// Access: row then column
int val = grid[1][2];   // 6 (row 1, col 2)

// Iterate
for (int r = 0; r < grid.length; r++) {
    for (int c = 0; c < grid[r].length; c++) {
        System.out.print(grid[r][c] + " ");
    }
    System.out.println();
}
```

## Jagged Arrays

Arrays where each row can have a different length:

```java
int[][] jagged = new int[3][];
jagged[0] = new int[]{1, 2};
jagged[1] = new int[]{3, 4, 5};
jagged[2] = new int[]{6};
```

## Useful Array Operations (java.util.Arrays)

```java
import java.util.Arrays;

int[] arr = {5, 3, 1, 4, 2};

Arrays.sort(arr);                      // sorts in-place: {1,2,3,4,5}
int idx = Arrays.binarySearch(arr, 3); // 2 (index of 3 after sorting)
int[] copy = Arrays.copyOf(arr, 3);    // {1, 2, 3} (first 3 elements)
int[] range = Arrays.copyOfRange(arr, 1, 4); // {2, 3, 4}
boolean eq = Arrays.equals(arr, copy); // false
String s = Arrays.toString(arr);       // "[1, 2, 3, 4, 5]"
Arrays.fill(arr, 0);                   // {0, 0, 0, 0, 0}
```

## Passing Arrays to Methods

Arrays are passed by reference — changes inside the method affect the original:

```java
public static void doubleAll(int[] arr) {
    for (int i = 0; i < arr.length; i++) {
        arr[i] *= 2;
    }
}

int[] nums = {1, 2, 3};
doubleAll(nums);
// nums is now {2, 4, 6}
```

## Returning Arrays from Methods

```java
public static int[] createRange(int n) {
    int[] result = new int[n];
    for (int i = 0; i < n; i++) result[i] = i + 1;
    return result;
}

int[] range = createRange(5);   // {1, 2, 3, 4, 5}
```

## Common Pitfalls

- Array size is fixed at creation — use `ArrayList` if you need dynamic sizing.
- `arr.length` is a field, not a method (no parentheses).
- Index starts at 0, so the last valid index is `arr.length - 1`.
