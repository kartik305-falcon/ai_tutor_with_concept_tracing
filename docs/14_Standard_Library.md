# Java Standard Library Essentials

## java.util — Core Utilities

### Date and Time (java.time, Java 8+)

```java
import java.time.*;
import java.time.format.DateTimeFormatter;

// Current date/time
LocalDate today = LocalDate.now();           // 2025-02-19
LocalTime now = LocalTime.now();             // 14:30:45.123
LocalDateTime dt = LocalDateTime.now();      // 2025-02-19T14:30:45

// Creating specific dates
LocalDate birthday = LocalDate.of(1995, Month.JUNE, 15);
LocalDate same = LocalDate.of(1995, 6, 15);

// Arithmetic
LocalDate nextWeek = today.plusWeeks(1);
LocalDate lastMonth = today.minusMonths(1);
long days = ChronoUnit.DAYS.between(birthday, today);

// Formatting
DateTimeFormatter fmt = DateTimeFormatter.ofPattern("dd/MM/yyyy");
String formatted = today.format(fmt);             // "19/02/2025"
LocalDate parsed = LocalDate.parse("19/02/2025", fmt);

// Comparing
today.isAfter(birthday);    // true
today.isBefore(nextWeek);   // true
today.equals(LocalDate.now()); // true
```

### Random Numbers

```java
import java.util.Random;

Random rand = new Random();
int n = rand.nextInt(10);       // 0 to 9
int range = rand.nextInt(50) + 1; // 1 to 50
double d = rand.nextDouble();   // 0.0 to 1.0
boolean b = rand.nextBoolean(); // true or false

// Java 17+ — better random
import java.util.random.RandomGenerator;
RandomGenerator rng = RandomGenerator.getDefault();
int x = rng.nextInt(100);
```

### Collections Utilities

```java
import java.util.*;

List<Integer> list = new ArrayList<>(List.of(3,1,4,1,5,9,2,6));
Collections.sort(list);                        // ascending sort
Collections.sort(list, Comparator.reverseOrder()); // descending
Collections.shuffle(list);
Collections.reverse(list);
Collections.swap(list, 0, 1);                 // swap index 0 and 1
int max = Collections.max(list);
int min = Collections.min(list);
int freq = Collections.frequency(list, 1);   // count occurrences
List<Integer> immutable = Collections.unmodifiableList(list);
```

## java.lang — Always Available (Auto-imported)

### Math

```java
Math.abs(-7)           // 7
Math.max(5, 10)        // 10
Math.min(5, 10)        // 5
Math.pow(2, 8)         // 256.0
Math.sqrt(144.0)       // 12.0
Math.cbrt(27.0)        // 3.0
Math.log(Math.E)       // 1.0 (natural log)
Math.log10(1000)       // 3.0
Math.floor(3.7)        // 3.0
Math.ceil(3.2)         // 4.0
Math.round(3.5)        // 4 (long)
Math.sin(Math.PI/2)    // 1.0
Math.PI                // 3.141592653589793
Math.E                 // 2.718281828459045
```

### Object Class (root of all Java classes)

Every Java class inherits from `Object`:

```java
Object.equals(Object other)  // equality
Object.hashCode()            // hash code (should match equals)
Object.toString()            // string representation
Object.getClass()            // returns Class<?>

// Override these in your classes:
@Override
public boolean equals(Object o) {
    if (this == o) return true;
    if (!(o instanceof MyClass)) return false;
    MyClass other = (MyClass) o;
    return this.field.equals(other.field);
}

@Override
public int hashCode() {
    return Objects.hash(field1, field2);
}

@Override
public String toString() {
    return "MyClass{field=" + field + "}";
}
```

## java.util.stream.Collectors

```java
import java.util.stream.Collectors;

List<String> names = List.of("Alice", "Bob", "Charlie", "Alice");

// Collect to various types
List<String> list = names.stream().collect(Collectors.toList());
Set<String> set = names.stream().collect(Collectors.toSet());

// Joining
String joined = names.stream().collect(Collectors.joining(", "));
// "Alice, Bob, Charlie, Alice"

// Counting
long count = names.stream().collect(Collectors.counting());

// Grouping
Map<Integer, List<String>> byLength = names.stream()
    .collect(Collectors.groupingBy(String::length));
// {5=[Alice, Alice], 3=[Bob], 7=[Charlie]}

// Partitioning
Map<Boolean, List<String>> partitioned = names.stream()
    .collect(Collectors.partitioningBy(s -> s.length() > 3));
// {true=[Alice, Charlie, Alice], false=[Bob]}

// Averaging
double avg = names.stream()
    .collect(Collectors.averagingInt(String::length));
```

## java.util.Objects

```java
import java.util.Objects;

Objects.equals(a, b)         // null-safe equals
Objects.hash(field1, field2) // combined hash code
Objects.toString(obj, "def") // null-safe toString with default
Objects.requireNonNull(obj, "message") // throw NPE if null
Objects.isNull(obj)          // true if null
Objects.nonNull(obj)         // true if not null
```
