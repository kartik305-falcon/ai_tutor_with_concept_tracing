# Methods in Java

## What is a Method?

A method is a named block of code that performs a specific task. Methods promote code reuse and organization.

## Method Syntax

```java
accessModifier returnType methodName(parameterType param1, ...) {
    // body
    return value; // required if returnType != void
}
```

## Basic Examples

```java
// No parameters, no return value
public static void greet() {
    System.out.println("Hello!");
}

// With parameters
public static void greetUser(String name) {
    System.out.println("Hello, " + name + "!");
}

// With return value
public static int add(int a, int b) {
    return a + b;
}

// Calling methods
greet();
greetUser("Alice");
int result = add(3, 4);   // result = 7
```

## `static` vs Instance Methods

```java
public class MathUtils {
    // static: belongs to the class, called as MathUtils.square(5)
    public static int square(int n) {
        return n * n;
    }
}

public class Counter {
    private int count = 0;

    // instance: belongs to an object, called as counter.increment()
    public void increment() {
        count++;
    }

    public int getCount() {
        return count;
    }
}
```

## Method Overloading

Multiple methods with the same name but different parameter lists:

```java
public static int multiply(int a, int b) {
    return a * b;
}

public static double multiply(double a, double b) {
    return a * b;
}

public static int multiply(int a, int b, int c) {
    return a * b * c;
}

// Java chooses the right version based on the arguments
multiply(2, 3);           // → int version → 6
multiply(2.5, 3.0);       // → double version → 7.5
multiply(2, 3, 4);        // → 3-arg version → 24
```

## Varargs (Variable Arguments)

```java
public static int sum(int... numbers) {
    int total = 0;
    for (int n : numbers) total += n;
    return total;
}

sum(1, 2, 3);        // 6
sum(10, 20);         // 30
sum(5);              // 5
sum();               // 0
```

## Pass by Value

Java always passes arguments by value — primitives pass a copy, objects pass a copy of the reference:

```java
public static void tryToChange(int x) {
    x = 100;   // only changes local copy
}

public static void changeArray(int[] arr) {
    arr[0] = 100;   // modifies the original array through reference
}

int n = 5;
tryToChange(n);
System.out.println(n);   // still 5

int[] nums = {1, 2, 3};
changeArray(nums);
System.out.println(nums[0]);   // 100
```

## Recursion

A method that calls itself:

```java
public static int factorial(int n) {
    if (n <= 1) return 1;          // base case
    return n * factorial(n - 1);   // recursive case
}

factorial(5);   // 5 * 4 * 3 * 2 * 1 = 120
```

```java
public static int fibonacci(int n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}
```

Always ensure a base case exists — otherwise you get `StackOverflowError`.

## `Math` Class Utilities

```java
Math.abs(-5)           // 5
Math.max(3, 7)         // 7
Math.min(3, 7)         // 3
Math.pow(2, 10)        // 1024.0
Math.sqrt(16.0)        // 4.0
Math.floor(3.9)        // 3.0
Math.ceil(3.1)         // 4.0
Math.round(3.5)        // 4
Math.random()          // random double in [0.0, 1.0)
Math.PI                // 3.141592653589793
```

## Access Modifiers for Methods

| Modifier    | Accessible from               |
|-------------|-------------------------------|
| `public`    | Anywhere                      |
| `protected` | Same package + subclasses     |
| (default)   | Same package only             |
| `private`   | Same class only               |
