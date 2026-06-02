# Strings in Java — In Depth

## String Basics

`String` is an immutable class — once created, its content cannot be changed.

```java
String s = "Hello";
s = s + " World";   // creates a NEW string, "Hello" is unchanged
```

## Common String Methods

```java
String s = "  Hello, Java World!  ";

// Length and access
s.length()            // 22 (includes spaces)
s.charAt(2)           // 'H' (after trim)
s.indexOf("Java")     // 9
s.lastIndexOf("o")    // 18

// Comparison
s.equals("hello")              // false (case-sensitive)
s.equalsIgnoreCase("hello")    // false (wrong content)
s.compareTo("Abc")             // positive (H > A)
s.startsWith("  Hello")        // true
s.endsWith("!  ")              // true

// Transformation
s.trim()                       // "Hello, Java World!" (removes leading/trailing spaces)
s.strip()                      // same as trim(), handles Unicode whitespace
s.toLowerCase()                // "  hello, java world!  "
s.toUpperCase()                // "  HELLO, JAVA WORLD!  "
s.replace("Java", "Python")    // "  Hello, Python World!  "
s.replaceAll("\\s+", "_")      // replaces all whitespace groups

// Extraction
s.substring(2)                 // "Hello, Java World!  "
s.substring(2, 7)              // "Hello"

// Splitting and joining
"a,b,c".split(",")             // ["a", "b", "c"]
String.join("-", "a","b","c")  // "a-b-c"
String.join(", ", List.of("x","y","z"))  // "x, y, z"

// Checking content
s.contains("Java")             // true
s.isEmpty()                    // false
s.isBlank()                    // false (Java 11+, checks for only whitespace)
"  ".isBlank()                 // true

// Converting to/from other types
String.valueOf(42)             // "42"
String.valueOf(3.14)           // "3.14"
Integer.parseInt("123")        // 123
Double.parseDouble("3.14")     // 3.14
```

## String Interning and == vs .equals()

```java
String a = "hello";
String b = "hello";
String c = new String("hello");

a == b          // true  (same string pool reference)
a == c          // false (c is a new object)
a.equals(c)     // true  (same content)

// ALWAYS use .equals() to compare strings
```

## String.format() and Formatted Strings

```java
String name = "Alice";
int age = 30;

String msg = String.format("Name: %s, Age: %d", name, age);
// Java 15+:
String msg2 = "Name: %s, Age: %d".formatted(name, age);
```

## Text Blocks (Java 15+)

Multi-line strings without escape characters:

```java
String json = """
        {
            "name": "Alice",
            "age": 30
        }
        """;

String html = """
        <html>
            <body>Hello</body>
        </html>
        """;
```

## StringBuilder vs StringBuffer

- `StringBuilder` — NOT thread-safe, faster (use in single-threaded code)
- `StringBuffer` — thread-safe, slower (use in multi-threaded code)

```java
// Efficient string building
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 1000; i++) {
    sb.append(i).append(",");
}
sb.deleteCharAt(sb.length() - 1);   // remove trailing comma
String result = sb.toString();
```

## Regular Expressions with String

```java
// matches — entire string must match
"hello123".matches("[a-z]+\\d+")    // true
"hello".matches("\\d+")             // false

// replaceAll with regex
"hello world".replaceAll("\\s+", "_")   // "hello_world"
"abc123def".replaceAll("[0-9]", "*")    // "abc***def"

// split with regex
"one  two   three".split("\\s+")   // ["one", "two", "three"]

// Full regex with Pattern and Matcher
import java.util.regex.*;

Pattern p = Pattern.compile("\\d+");
Matcher m = p.matcher("abc 123 def 456");
while (m.find()) {
    System.out.println(m.group());   // prints 123, then 456
}
```

## Converting Between char[] and String

```java
char[] chars = {'J', 'a', 'v', 'a'};
String s = new String(chars);       // "Java"
char[] back = s.toCharArray();      // {'J','a','v','a'}
```
