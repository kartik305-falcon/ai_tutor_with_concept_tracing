# Control Flow in Java

## if / else if / else

```java
int score = 75;

if (score >= 90) {
    System.out.println("A");
} else if (score >= 80) {
    System.out.println("B");
} else if (score >= 70) {
    System.out.println("C");
} else {
    System.out.println("F");
}
```

Single-statement bodies can omit braces (not recommended):
```java
if (x > 0) System.out.println("positive");
```

## switch Statement

```java
int day = 3;

switch (day) {
    case 1:
        System.out.println("Monday");
        break;
    case 2:
        System.out.println("Tuesday");
        break;
    case 3:
    case 4:
        System.out.println("Wednesday or Thursday");
        break;
    default:
        System.out.println("Other day");
}
```

`break` exits the switch. Without it, execution "falls through" to the next case.

`switch` works with: `int`, `char`, `String`, `enum`, and wrapper types.

## Switch Expression (Java 14+)

```java
String result = switch (day) {
    case 1 -> "Monday";
    case 2 -> "Tuesday";
    case 3, 4 -> "Wednesday or Thursday";
    default -> "Other";
};
```

Arrow syntax (`->`) automatically breaks — no fall-through.

## while Loop

```java
int i = 0;
while (i < 5) {
    System.out.println(i);
    i++;
}
// Prints: 0 1 2 3 4
```

## do-while Loop

Executes the body at least once, then checks condition:

```java
int n;
do {
    System.out.print("Enter a positive number: ");
    n = scanner.nextInt();
} while (n <= 0);
```

## for Loop

```java
for (int i = 0; i < 5; i++) {
    System.out.println(i);
}
// init; condition; update — all optional
// for (;;) is an infinite loop
```

## Enhanced for Loop (for-each)

Used to iterate over arrays and collections:

```java
int[] numbers = {10, 20, 30, 40};
for (int num : numbers) {
    System.out.println(num);
}

List<String> names = List.of("Alice", "Bob", "Carol");
for (String name : names) {
    System.out.println(name);
}
```

## break and continue

```java
// break — exits the loop immediately
for (int i = 0; i < 10; i++) {
    if (i == 5) break;
    System.out.println(i);   // prints 0 to 4
}

// continue — skips the rest of the current iteration
for (int i = 0; i < 10; i++) {
    if (i % 2 == 0) continue;
    System.out.println(i);   // prints 1 3 5 7 9
}
```

## Labeled break / continue

Used to break out of nested loops:

```java
outer:
for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
        if (j == 1) break outer;   // exits both loops
        System.out.println(i + "," + j);
    }
}
```

## return Statement

Exits a method, optionally returning a value:

```java
public static int add(int a, int b) {
    return a + b;
}

public static void greet(String name) {
    if (name == null) return;   // early exit
    System.out.println("Hello, " + name);
}
```
