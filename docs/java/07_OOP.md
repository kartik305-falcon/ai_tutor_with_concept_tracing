# Object-Oriented Programming in Java

## Classes and Objects

A **class** is a blueprint. An **object** is an instance of a class.

```java
// Class definition
public class Dog {
    // Fields (instance variables)
    String name;
    String breed;
    int age;

    // Constructor
    public Dog(String name, String breed, int age) {
        this.name = name;
        this.breed = breed;
        this.age = age;
    }

    // Method
    public void bark() {
        System.out.println(name + " says: Woof!");
    }

    public String toString() {
        return name + " (" + breed + ", " + age + " yrs)";
    }
}

// Creating objects
Dog d1 = new Dog("Rex", "German Shepherd", 3);
Dog d2 = new Dog("Bella", "Labrador", 5);

d1.bark();                      // Rex says: Woof!
System.out.println(d2.name);    // Bella
System.out.println(d1);         // Rex (German Shepherd, 3 yrs)
```

## Encapsulation

Hide internal state using `private` fields + `public` getters/setters:

```java
public class BankAccount {
    private double balance;   // cannot be accessed directly from outside

    public BankAccount(double initialBalance) {
        this.balance = initialBalance;
    }

    public double getBalance() {
        return balance;
    }

    public void deposit(double amount) {
        if (amount > 0) balance += amount;
    }

    public boolean withdraw(double amount) {
        if (amount > 0 && balance >= amount) {
            balance -= amount;
            return true;
        }
        return false;
    }
}
```

## Constructors

```java
public class Point {
    double x, y;

    // Default constructor (no args)
    public Point() {
        this.x = 0;
        this.y = 0;
    }

    // Parameterized constructor
    public Point(double x, double y) {
        this.x = x;
        this.y = y;
    }

    // Constructor chaining with this()
    public Point(double val) {
        this(val, val);   // calls the 2-arg constructor
    }
}
```

If no constructor is defined, Java provides a default no-arg constructor automatically.

## Inheritance

```java
// Parent (superclass)
public class Animal {
    String name;

    public Animal(String name) {
        this.name = name;
    }

    public void eat() {
        System.out.println(name + " is eating.");
    }

    public void makeSound() {
        System.out.println("...");
    }
}

// Child (subclass) — uses `extends`
public class Cat extends Animal {
    public Cat(String name) {
        super(name);   // calls parent constructor
    }

    @Override
    public void makeSound() {
        System.out.println(name + " says: Meow!");
    }

    public void purr() {
        System.out.println(name + " purrs...");
    }
}

Cat c = new Cat("Whiskers");
c.eat();         // inherited: Whiskers is eating.
c.makeSound();   // overridden: Whiskers says: Meow!
c.purr();        // new method
```

Java supports single inheritance only (one parent class), but a class can implement multiple interfaces.

## Polymorphism

```java
Animal a = new Cat("Tom");   // Cat stored as Animal reference
a.makeSound();               // still calls Cat's version → "Tom says: Meow!"
```

This is **runtime polymorphism** — the actual method called depends on the object's real type, not the reference type.

## Abstract Classes

Cannot be instantiated; meant to be subclassed:

```java
public abstract class Shape {
    abstract double area();   // must be implemented by subclass

    public void describe() {
        System.out.println("This shape has area: " + area());
    }
}

public class Circle extends Shape {
    double radius;
    public Circle(double r) { radius = r; }

    @Override
    public double area() { return Math.PI * radius * radius; }
}
```

## Interfaces

Defines a contract — what a class CAN do, not how:

```java
public interface Drawable {
    void draw();                          // abstract by default
    default void show() {                 // default method (Java 8+)
        System.out.println("Showing...");
    }
}

public interface Resizable {
    void resize(double factor);
}

// A class can implement multiple interfaces
public class Square implements Drawable, Resizable {
    double side;
    public Square(double s) { side = s; }

    @Override
    public void draw() {
        System.out.println("Drawing a square with side " + side);
    }

    @Override
    public void resize(double factor) {
        side *= factor;
    }
}
```

## `static` Members

Belong to the class, not instances:

```java
public class Counter {
    private static int count = 0;   // shared across all instances

    public Counter() { count++; }

    public static int getCount() { return count; }
}

new Counter();
new Counter();
new Counter();
System.out.println(Counter.getCount());   // 3
```
