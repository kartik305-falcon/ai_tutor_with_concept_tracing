# Data Types and Variables in Java

## Primitive Data Types

Java has 8 built-in primitive types:

| Type    | Size    | Range / Description                          | Default |
|---------|---------|----------------------------------------------|---------|
| byte    | 1 byte  | -128 to 127                                  | 0       |
| short   | 2 bytes | -32,768 to 32,767                            | 0       |
| int     | 4 bytes | -2^31 to 2^31 - 1 (most common integer)     | 0       |
| long    | 8 bytes | -2^63 to 2^63 - 1                            | 0L      |
| float   | 4 bytes | ~7 decimal digits of precision               | 0.0f    |
| double  | 8 bytes | ~15 decimal digits of precision (default)    | 0.0     |
| char    | 2 bytes | Single Unicode character ('A', '5', '\n')    | '\u0000'|
| boolean | 1 bit   | true or false                                | false   |

```java
int age = 25;
long population = 8_000_000_000L;   // L suffix for long
float pi = 3.14f;                   // f suffix for float
double e = 2.718281828;
char grade = 'A';
boolean isJavaFun = true;
```

## Variable Declaration and Initialization

```java
// Declaration
int x;

// Initialization
x = 10;

// Declaration + Initialization
int y = 20;

// Multiple variables of same type
int a = 1, b = 2, c = 3;
```

## The `var` Keyword (Java 10+)

Java 10 introduced local variable type inference:

```java
var name = "Alice";   // inferred as String
var count = 42;       // inferred as int
var list = new ArrayList<String>(); // inferred as ArrayList<String>
```

`var` can only be used for local variables (inside methods), not fields.

## Type Casting

### Widening (automatic, safe)
```java
int i = 100;
long l = i;      // int → long (automatic)
double d = i;    // int → double (automatic)
```

### Narrowing (manual, may lose data)
```java
double d = 9.99;
int i = (int) d;   // i becomes 9 — decimal part is lost
```

## String Type

`String` is not a primitive — it is an object (class).

```java
String name = "Alice";
String greeting = "Hello, " + name;  // concatenation with +

// String methods
int len = name.length();           // 5
String upper = name.toUpperCase(); // "ALICE"
String sub = name.substring(1, 3); // "li"
boolean has = name.contains("li"); // true
String[] parts = "a,b,c".split(","); // ["a", "b", "c"]
```

## Constants with `final`

```java
final double PI = 3.14159;
final int MAX_SIZE = 100;
// PI = 3.0; // ERROR: cannot reassign a final variable
```

By convention, constants use UPPER_SNAKE_CASE.

## Wrapper Classes

Each primitive has a corresponding wrapper class:

| Primitive | Wrapper   |
|-----------|-----------|
| int       | Integer   |
| double    | Double    |
| char      | Character |
| boolean   | Boolean   |
| long      | Long      |

```java
int x = 5;
Integer obj = Integer.valueOf(x);   // boxing
int y = obj.intValue();             // unboxing

// Autoboxing (Java does this automatically)
Integer auto = 42;  // automatically boxed
int prim = auto;    // automatically unboxed

// Useful Integer methods
int parsed = Integer.parseInt("123");   // String → int
String str = Integer.toString(456);     // int → String
int max = Integer.MAX_VALUE;            // 2147483647
```

## Scope of Variables

```java
public class ScopeDemo {
    static int classVar = 10;    // class-level (field)

    public static void main(String[] args) {
        int methodVar = 20;      // method-level

        if (true) {
            int blockVar = 30;   // block-level
            System.out.println(blockVar);  // OK
        }
        // System.out.println(blockVar);  // ERROR: out of scope
        System.out.println(methodVar);    // OK
        System.out.println(classVar);     // OK
    }
}
```
