# Java Collections Framework

## Overview

The Java Collections Framework provides interfaces and classes for storing and manipulating groups of objects. Key interfaces: `List`, `Set`, `Map`, `Queue`.

## ArrayList

A dynamic-size array — grows automatically:

```java
import java.util.ArrayList;
import java.util.Collections;

ArrayList<String> names = new ArrayList<>();

// Adding
names.add("Alice");
names.add("Bob");
names.add(1, "Charlie");   // insert at index 1

// Accessing
String first = names.get(0);   // "Alice"
int size = names.size();       // 3

// Removing
names.remove("Bob");           // by value
names.remove(0);               // by index

// Iterating
for (String name : names) {
    System.out.println(name);
}

// Checking
boolean has = names.contains("Alice");   // true
int idx = names.indexOf("Alice");        // 0

// Sorting
Collections.sort(names);

// Convert to array
String[] arr = names.toArray(new String[0]);
```

## LinkedList

Better for frequent insertions/deletions at the front:

```java
import java.util.LinkedList;

LinkedList<Integer> list = new LinkedList<>();
list.addFirst(1);
list.addLast(2);
list.add(3);
int head = list.getFirst();   // 1
list.removeFirst();
```

## HashMap

Stores key-value pairs; no guaranteed order:

```java
import java.util.HashMap;
import java.util.Map;

HashMap<String, Integer> scores = new HashMap<>();

// Adding
scores.put("Alice", 95);
scores.put("Bob", 82);
scores.put("Alice", 98);   // overwrites previous value

// Accessing
int score = scores.get("Alice");         // 98
int val = scores.getOrDefault("Carol", 0); // 0 — key not found

// Checking
boolean hasAlice = scores.containsKey("Alice");   // true
boolean has95 = scores.containsValue(95);         // false

// Removing
scores.remove("Bob");

// Iterating
for (Map.Entry<String, Integer> entry : scores.entrySet()) {
    System.out.println(entry.getKey() + " → " + entry.getValue());
}

// Keys and values separately
for (String key : scores.keySet()) { ... }
for (int val2 : scores.values()) { ... }
```

## HashSet

Stores unique elements, no duplicates, no order:

```java
import java.util.HashSet;

HashSet<String> set = new HashSet<>();
set.add("apple");
set.add("banana");
set.add("apple");   // ignored — already exists

set.size();              // 2
set.contains("apple");   // true
set.remove("banana");

// Iteration
for (String item : set) {
    System.out.println(item);
}
```

## TreeMap and TreeSet

Sorted versions:

```java
import java.util.TreeMap;
import java.util.TreeSet;

TreeMap<String, Integer> sorted = new TreeMap<>();
sorted.put("banana", 2);
sorted.put("apple", 1);
sorted.put("cherry", 3);
// Iteration is in alphabetical order: apple, banana, cherry

TreeSet<Integer> sortedNums = new TreeSet<>();
sortedNums.add(5); sortedNums.add(1); sortedNums.add(3);
// {1, 3, 5}
sortedNums.first();   // 1
sortedNums.last();    // 5
```

## Queue and Stack

```java
import java.util.Queue;
import java.util.LinkedList;
import java.util.Deque;
import java.util.ArrayDeque;

// Queue (FIFO)
Queue<String> queue = new LinkedList<>();
queue.offer("first");
queue.offer("second");
String head = queue.peek();    // "first" (doesn't remove)
String removed = queue.poll(); // "first" (removes it)

// Stack / Deque (LIFO)
Deque<Integer> stack = new ArrayDeque<>();
stack.push(1);
stack.push(2);
stack.push(3);
int top = stack.peek();   // 3
stack.pop();              // removes 3
```

## Generics

Collections use generics (`<T>`) for type safety:

```java
ArrayList<Integer> ints = new ArrayList<>();
ints.add(42);
// ints.add("hello");   // compile error — type mismatch

// Generic method
public static <T> void printAll(ArrayList<T> list) {
    for (T item : list) System.out.println(item);
}
```

## Collections Utility Class

```java
import java.util.Collections;

ArrayList<Integer> list = new ArrayList<>(List.of(3,1,4,1,5));
Collections.sort(list);                    // [1,1,3,4,5]
Collections.reverse(list);                 // [5,4,3,1,1]
Collections.shuffle(list);                 // random order
int max = Collections.max(list);           // largest element
int min = Collections.min(list);           // smallest element
Collections.fill(list, 0);                 // all zeros
Collections.frequency(list, 1);            // count of 1s
```
