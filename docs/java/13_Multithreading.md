# Multithreading and Concurrency in Java

## What is a Thread?

A thread is the smallest unit of execution within a process. Java supports multithreading natively — multiple threads can run concurrently, sharing the same memory space.

## Creating Threads

### Method 1: Extending Thread

```java
public class MyThread extends Thread {
    private String name;

    public MyThread(String name) {
        this.name = name;
    }

    @Override
    public void run() {
        for (int i = 1; i <= 5; i++) {
            System.out.println(name + ": " + i);
            try { Thread.sleep(100); } catch (InterruptedException e) {}
        }
    }
}

MyThread t1 = new MyThread("Thread-1");
MyThread t2 = new MyThread("Thread-2");
t1.start();   // do NOT call run() directly — that runs on current thread
t2.start();
```

### Method 2: Implementing Runnable (Preferred)

```java
public class MyTask implements Runnable {
    @Override
    public void run() {
        System.out.println("Running in: " + Thread.currentThread().getName());
    }
}

Thread t = new Thread(new MyTask());
t.start();

// With lambda:
Thread t2 = new Thread(() -> System.out.println("Lambda thread!"));
t2.start();
```

## Thread Lifecycle

- **NEW** — created, not yet started
- **RUNNABLE** — running or ready to run
- **BLOCKED** — waiting for a monitor lock
- **WAITING** — waiting indefinitely for another thread
- **TIMED_WAITING** — waiting for a specified time
- **TERMINATED** — finished execution

## Thread Methods

```java
Thread t = new Thread(() -> { /* ... */ });

t.start();                    // start the thread
t.join();                     // wait for this thread to finish
t.join(1000);                 // wait at most 1 second
t.interrupt();                // interrupt a sleeping/waiting thread
t.isAlive();                  // true if thread is running
t.getName();                  // get thread name
t.setName("MyWorker");        // set thread name
t.getPriority();              // 1-10 (default 5)
t.setPriority(Thread.MAX_PRIORITY); // 10

Thread.sleep(500);            // pause current thread for 500ms
Thread.currentThread();       // reference to the current thread
Thread.yield();               // hint to scheduler to pause current thread
```

## Race Conditions and Synchronization

```java
// UNSAFE — multiple threads modifying shared state
public class Counter {
    private int count = 0;
    public void increment() { count++; }   // NOT atomic!
    public int getCount() { return count; }
}

// SAFE — synchronized keyword
public class SafeCounter {
    private int count = 0;

    public synchronized void increment() { count++; }
    public synchronized int getCount() { return count; }
}

// SAFE — using AtomicInteger
import java.util.concurrent.atomic.AtomicInteger;
AtomicInteger counter = new AtomicInteger(0);
counter.incrementAndGet();   // atomic increment
counter.get();               // read value
```

## synchronized Block

```java
public class SharedResource {
    private final Object lock = new Object();
    private int value = 0;

    public void update(int newVal) {
        synchronized (lock) {   // only one thread can be here at a time
            value = newVal;
        }
    }
}
```

## ExecutorService (Thread Pools)

Managing threads manually is error-prone. Use thread pools:

```java
import java.util.concurrent.*;

// Fixed thread pool with 4 threads
ExecutorService executor = Executors.newFixedThreadPool(4);

// Submit tasks
for (int i = 0; i < 10; i++) {
    final int taskId = i;
    executor.submit(() -> {
        System.out.println("Task " + taskId + " by " + Thread.currentThread().getName());
    });
}

// Shutdown — waits for all tasks to finish
executor.shutdown();
executor.awaitTermination(10, TimeUnit.SECONDS);
```

## Future and Callable

`Callable` returns a result, unlike `Runnable`:

```java
Callable<Integer> task = () -> {
    Thread.sleep(1000);
    return 42;
};

ExecutorService exec = Executors.newSingleThreadExecutor();
Future<Integer> future = exec.submit(task);

System.out.println("Waiting for result...");
int result = future.get();   // blocks until done
System.out.println("Result: " + result);  // 42
exec.shutdown();
```

## volatile Keyword

Ensures a variable's value is always read from main memory (not CPU cache):

```java
public class StopFlag {
    private volatile boolean running = true;

    public void stop() { running = false; }

    public void run() {
        while (running) {   // will always see updated value
            // do work
        }
    }
}
```

## Deadlock

Occurs when two threads each hold a lock that the other needs:

```java
// Thread 1 holds lockA, waits for lockB
// Thread 2 holds lockB, waits for lockA
// → Neither can proceed = deadlock

// Prevention: always acquire locks in the same order
```
