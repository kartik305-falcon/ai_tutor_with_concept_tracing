# Introduction to Java

## What is Java?

Java is a high-level, class-based, object-oriented programming language designed to have as few implementation dependencies as possible. It follows the principle of "Write Once, Run Anywhere" (WORA), meaning compiled Java code can run on any platform that supports Java without recompilation.

Java was created by James Gosling at Sun Microsystems and released in 1995. Today it is maintained by Oracle.

## Key Features of Java

- **Object-Oriented**: Everything in Java is an object (except primitives).
- **Platform Independent**: Java code compiles to bytecode that runs on the JVM (Java Virtual Machine).
- **Strongly Typed**: Every variable must have a declared type.
- **Automatic Memory Management**: Java uses a Garbage Collector to manage memory.
- **Multithreaded**: Java has built-in support for concurrent programming.
- **Robust**: Java has strong compile-time and runtime error checking.

## JDK, JRE, and JVM

- **JVM (Java Virtual Machine)**: Runs Java bytecode. Platform-specific.
- **JRE (Java Runtime Environment)**: JVM + standard libraries. Used to run Java programs.
- **JDK (Java Development Kit)**: JRE + compiler (`javac`) + tools. Used to develop Java programs.

## Your First Java Program

```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

### Breakdown:
- `public class HelloWorld` — every Java program must have a class. The filename must match the class name (`HelloWorld.java`).
- `public static void main(String[] args)` — the entry point of every Java application.
- `System.out.println(...)` — prints text to the console with a newline.

## Compiling and Running Java

```bash
javac HelloWorld.java   # compiles to HelloWorld.class (bytecode)
java HelloWorld         # runs the program using the JVM
```

## Java Program Structure

```java
// Package declaration (optional)
package com.example;

// Import statements
import java.util.Scanner;

// Class definition
public class MyProgram {
    // Fields (class-level variables)
    int value;

    // Methods
    public static void main(String[] args) {
        // Code goes here
    }
}
```

## Comments in Java

```java
// Single-line comment

/*
   Multi-line comment
*/

/**
 * Javadoc comment — used to generate documentation
 * @param args command-line arguments
 */
public static void main(String[] args) { }
```

## Java is Case-Sensitive

`MyClass`, `myclass`, and `MYCLASS` are three different identifiers in Java.
