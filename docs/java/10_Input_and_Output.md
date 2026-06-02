# Input and Output in Java

## Console Input with Scanner

`Scanner` is the standard way to read user input in beginner Java:

```java
import java.util.Scanner;

Scanner sc = new Scanner(System.in);

// Reading different types
int n = sc.nextInt();             // reads an integer
double d = sc.nextDouble();       // reads a double
String word = sc.next();          // reads one word (stops at whitespace)
String line = sc.nextLine();      // reads a full line

// Always close scanner when done
sc.close();
```

### Common Input Patterns

```java
Scanner sc = new Scanner(System.in);

// Read N numbers
int n = sc.nextInt();
int[] arr = new int[n];
for (int i = 0; i < n; i++) {
    arr[i] = sc.nextInt();
}

// Read until end of input
while (sc.hasNextInt()) {
    int val = sc.nextInt();
    System.out.println(val * 2);
}

// Read a line after reading a number (common bug fix)
int x = sc.nextInt();
sc.nextLine();         // consume leftover newline
String text = sc.nextLine();
```

### Scanner from String (useful for testing)

```java
Scanner sc = new Scanner("10 20 30");
while (sc.hasNextInt()) {
    System.out.println(sc.nextInt());
}
```

## Console Output

```java
System.out.print("No newline");
System.out.println("With newline");
System.out.printf("Formatted: %d %.2f %s%n", 42, 3.14, "hello");

// String.format (same syntax, returns a String)
String s = String.format("Name: %-10s Age: %3d", "Alice", 25);
```

### printf Format Specifiers

| Specifier | Type             | Example           |
|-----------|------------------|-------------------|
| `%d`      | integer          | `42`              |
| `%f`      | float/double     | `3.140000`        |
| `%.2f`    | 2 decimal places | `3.14`            |
| `%s`      | String           | `hello`           |
| `%c`      | char             | `A`               |
| `%b`      | boolean          | `true`            |
| `%n`      | newline          | (platform-safe)   |
| `%5d`     | width 5, right   | `   42`           |
| `%-5d`    | width 5, left    | `42   `           |
| `%05d`    | zero-padded      | `00042`           |

## File I/O

### Writing to a File

```java
import java.io.FileWriter;
import java.io.PrintWriter;
import java.io.IOException;

try (PrintWriter pw = new PrintWriter(new FileWriter("output.txt"))) {
    pw.println("Line 1");
    pw.printf("Number: %d%n", 42);
} catch (IOException e) {
    System.out.println("Error writing file: " + e.getMessage());
}
```

### Reading from a File

```java
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

try (BufferedReader br = new BufferedReader(new FileReader("input.txt"))) {
    String line;
    while ((line = br.readLine()) != null) {
        System.out.println(line);
    }
} catch (IOException e) {
    System.out.println("Error reading file: " + e.getMessage());
}
```

### Modern File I/O (java.nio, Java 7+)

```java
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

Path path = Paths.get("data.txt");

// Read all lines at once
List<String> lines = Files.readAllLines(path);

// Write all lines at once
Files.write(path, List.of("Line 1", "Line 2", "Line 3"));

// Read entire file as String
String content = Files.readString(path);  // Java 11+

// Write a String to file
Files.writeString(path, "Hello World");   // Java 11+
```

## StringBuilder

Efficiently build strings without creating many intermediate objects:

```java
StringBuilder sb = new StringBuilder();
sb.append("Hello");
sb.append(", ");
sb.append("World");
sb.append("!");
sb.insert(5, " there");   // insert at index 5
sb.delete(5, 11);         // remove range
sb.reverse();             // reverses the content

String result = sb.toString();
```

Use `StringBuilder` inside loops; avoid `String` concatenation with `+` in loops (creates many objects).
