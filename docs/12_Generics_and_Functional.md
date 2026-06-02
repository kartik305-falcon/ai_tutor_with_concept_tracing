# Generics and Functional Programming in Java

## Generics

Generics allow classes and methods to work with any type while maintaining type safety.

### Generic Classes

```java
// Without generics — unsafe
ArrayList list = new ArrayList();
list.add("hello");
String s = (String) list.get(0);  // cast needed, error-prone

// With generics — type-safe
ArrayList<String> list = new ArrayList<>();
list.add("hello");
String s = list.get(0);  // no cast needed
```

### Writing Generic Classes

```java
public class Pair<A, B> {
    private A first;
    private B second;

    public Pair(A first, B second) {
        this.first = first;
        this.second = second;
    }

    public A getFirst() { return first; }
    public B getSecond() { return second; }

    @Override
    public String toString() {
        return "(" + first + ", " + second + ")";
    }
}

Pair<String, Integer> p = new Pair<>("Alice", 30);
System.out.println(p.getFirst());    // Alice
System.out.println(p.getSecond());   // 30
```

### Generic Methods

```java
public static <T extends Comparable<T>> T max(T a, T b) {
    return a.compareTo(b) >= 0 ? a : b;
}

max(3, 7)           // 7
max("apple", "banana")  // "banana"
max(3.14, 2.71)     // 3.14
```

### Bounded Type Parameters

```java
// T must be a Number or subclass of Number
public static <T extends Number> double sum(List<T> list) {
    double total = 0;
    for (T item : list) total += item.doubleValue();
    return total;
}
```

## Lambda Expressions (Java 8+)

Lambdas are anonymous functions — short, inline implementations of functional interfaces:

```java
// Traditional anonymous class
Runnable r = new Runnable() {
    @Override
    public void run() {
        System.out.println("Running!");
    }
};

// Lambda equivalent
Runnable r = () -> System.out.println("Running!");

// With parameters
Comparator<String> cmp = (a, b) -> a.compareTo(b);

// With block body
Comparator<Integer> comp = (a, b) -> {
    if (a > b) return 1;
    if (a < b) return -1;
    return 0;
};
```

## Functional Interfaces

A functional interface has exactly one abstract method:

```java
@FunctionalInterface
interface MathOperation {
    int operate(int a, int b);
}

MathOperation add = (a, b) -> a + b;
MathOperation multiply = (a, b) -> a * b;

System.out.println(add.operate(3, 4));       // 7
System.out.println(multiply.operate(3, 4));  // 12
```

### Built-in Functional Interfaces (java.util.function)

```java
// Predicate<T> — takes T, returns boolean
Predicate<String> isEmpty = s -> s.isEmpty();
Predicate<Integer> isEven = n -> n % 2 == 0;

// Function<T, R> — takes T, returns R
Function<String, Integer> length = s -> s.length();
Function<Integer, String> toStr = n -> "Number: " + n;

// Consumer<T> — takes T, returns nothing
Consumer<String> printer = s -> System.out.println(s);

// Supplier<T> — takes nothing, returns T
Supplier<Double> random = () -> Math.random();

// BiFunction<T, U, R> — takes T and U, returns R
BiFunction<Integer, Integer, Integer> add = (a, b) -> a + b;
```

## Stream API (Java 8+)

Streams allow functional-style processing of collections:

```java
import java.util.List;
import java.util.stream.*;

List<Integer> numbers = List.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

// Filter even numbers, square them, collect to list
List<Integer> result = numbers.stream()
    .filter(n -> n % 2 == 0)      // [2, 4, 6, 8, 10]
    .map(n -> n * n)               // [4, 16, 36, 64, 100]
    .collect(Collectors.toList()); // collect results

// Sum all numbers
int total = numbers.stream()
    .reduce(0, Integer::sum);      // 55

// Find max
Optional<Integer> max = numbers.stream().max(Integer::compareTo);
max.ifPresent(System.out::println);  // 10

// Convert strings to uppercase and sort
List<String> names = List.of("charlie", "alice", "bob");
List<String> sorted = names.stream()
    .map(String::toUpperCase)
    .sorted()
    .collect(Collectors.toList());
// ["ALICE", "BOB", "CHARLIE"]

// Count matching elements
long evenCount = numbers.stream()
    .filter(n -> n % 2 == 0)
    .count();   // 5

// any/all/none match
boolean anyOver5 = numbers.stream().anyMatch(n -> n > 5);   // true
boolean allPositive = numbers.stream().allMatch(n -> n > 0); // true
```

## Method References

Shorthand for lambdas that call a single method:

```java
// Instead of: n -> System.out.println(n)
numbers.forEach(System.out::println);

// Instead of: s -> s.toUpperCase()
names.stream().map(String::toUpperCase);

// Instead of: (a, b) -> Integer.sum(a, b)
numbers.stream().reduce(0, Integer::sum);
```

## Optional (Java 8+)

Safely handles values that might be null:

```java
Optional<String> opt = Optional.of("hello");
Optional<String> empty = Optional.empty();

opt.isPresent()        // true
opt.get()              // "hello"
empty.orElse("default")        // "default"
opt.orElseGet(() -> "computed") // "hello" (supplier not called)
opt.map(String::toUpperCase)    // Optional["HELLO"]
opt.filter(s -> s.length() > 3) // Optional["hello"]
```
