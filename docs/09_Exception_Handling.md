# Exception Handling in Java

## What is an Exception?

An exception is an event that disrupts the normal flow of a program. Java uses exception objects to signal errors.

## Exception Hierarchy

```
Throwable
├── Error        (serious problems — don't catch these: OutOfMemoryError, StackOverflowError)
└── Exception
    ├── RuntimeException  (unchecked — don't have to catch)
    │   ├── NullPointerException
    │   ├── ArrayIndexOutOfBoundsException
    │   ├── ClassCastException
    │   ├── NumberFormatException
    │   └── ArithmeticException (e.g. divide by zero)
    └── IOException, SQLException, ...  (checked — MUST catch or declare)
```

## try-catch-finally

```java
try {
    int result = 10 / 0;   // throws ArithmeticException
    System.out.println(result);
} catch (ArithmeticException e) {
    System.out.println("Cannot divide by zero: " + e.getMessage());
} finally {
    System.out.println("This always runs — use for cleanup");
}
```

- `try` — code that might throw
- `catch` — handles the exception
- `finally` — always runs, even if exception occurs (use for closing files, DB connections)

## Multiple Catch Blocks

```java
try {
    String s = null;
    int n = Integer.parseInt(s);   // NullPointerException or NumberFormatException
} catch (NullPointerException e) {
    System.out.println("Null value!");
} catch (NumberFormatException e) {
    System.out.println("Invalid number format!");
} catch (Exception e) {
    System.out.println("Something else: " + e.getMessage());
}
```

More specific exceptions must come before more general ones.

## Multi-catch (Java 7+)

```java
try {
    // ...
} catch (IOException | SQLException e) {
    System.out.println("IO or SQL error: " + e.getMessage());
}
```

## try-with-resources (Java 7+)

Automatically closes resources that implement `AutoCloseable`:

```java
try (FileReader fr = new FileReader("file.txt");
     BufferedReader br = new BufferedReader(fr)) {
    String line;
    while ((line = br.readLine()) != null) {
        System.out.println(line);
    }
} catch (IOException e) {
    System.out.println("File error: " + e.getMessage());
}
// No need for finally — resources are closed automatically
```

## Throwing Exceptions

```java
public static double divide(double a, double b) {
    if (b == 0) {
        throw new ArithmeticException("Denominator cannot be zero");
    }
    return a / b;
}
```

## Checked vs Unchecked Exceptions

### Checked Exceptions
Must be handled (caught or declared with `throws`):

```java
public static void readFile(String path) throws IOException {
    FileReader fr = new FileReader(path);   // throws IOException
    // ...
}

// Caller must either catch it or also declare throws
try {
    readFile("data.txt");
} catch (IOException e) {
    System.out.println("File not found");
}
```

### Unchecked Exceptions (RuntimeException)
Don't have to be caught — but you should handle them when expected:

```java
int[] arr = {1, 2, 3};
// arr[5] would throw ArrayIndexOutOfBoundsException at runtime
// No compile-time warning
```

## Creating Custom Exceptions

```java
// Custom checked exception
public class InsufficientFundsException extends Exception {
    private double amount;

    public InsufficientFundsException(double amount) {
        super("Insufficient funds: needed " + amount);
        this.amount = amount;
    }

    public double getAmount() { return amount; }
}

// Custom unchecked exception
public class InvalidAgeException extends RuntimeException {
    public InvalidAgeException(String message) {
        super(message);
    }
}

// Usage
public void withdraw(double amount) throws InsufficientFundsException {
    if (amount > balance) {
        throw new InsufficientFundsException(amount);
    }
    balance -= amount;
}
```

## Exception Best Practices

- Catch specific exceptions, not just `Exception`.
- Never swallow exceptions silently (`catch (Exception e) {}`).
- Use `finally` or try-with-resources to clean up resources.
- Log exceptions rather than just printing stack traces in production.
- Don't use exceptions for normal control flow — they're expensive.
- Create meaningful custom exceptions for your domain.
