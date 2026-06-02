# Operators and Expressions in Java

## Arithmetic Operators

```java
int a = 10, b = 3;

int sum  = a + b;   // 13
int diff = a - b;   // 7
int prod = a * b;   // 30
int quot = a / b;   // 3  (integer division — truncates)
int rem  = a % b;   // 1  (modulus / remainder)

// Floating-point division
double result = 10.0 / 3;  // 3.3333...
```

## Assignment Operators

```java
int x = 5;
x += 3;   // x = x + 3  → 8
x -= 2;   // x = x - 2  → 6
x *= 4;   // x = x * 4  → 24
x /= 6;   // x = x / 6  → 4
x %= 3;   // x = x % 3  → 1
```

## Increment and Decrement

```java
int n = 5;
n++;      // post-increment: use n then add 1 → n becomes 6
++n;      // pre-increment: add 1 then use n  → n becomes 7
n--;      // post-decrement
--n;      // pre-decrement

// Key difference:
int a = 5;
int b = a++;   // b = 5, then a becomes 6
int c = ++a;   // a becomes 7, then c = 7
```

## Comparison (Relational) Operators

Return `boolean` (`true` or `false`):

```java
int x = 5, y = 10;

x == y   // false — equal to
x != y   // true  — not equal to
x < y    // true  — less than
x > y    // false — greater than
x <= y   // true  — less than or equal
x >= y   // false — greater than or equal
```

**Important:** Use `==` for primitives. Use `.equals()` for objects:
```java
String a = "hello";
String b = "hello";
a == b          // unreliable for Strings (compares references)
a.equals(b)     // true — compares content (always use this)
```

## Logical Operators

```java
boolean p = true, q = false;

p && q   // false — AND: both must be true
p || q   // true  — OR:  at least one must be true
!p       // false — NOT: negates the value

// Short-circuit evaluation:
// In A && B, if A is false, B is never evaluated
// In A || B, if A is true,  B is never evaluated
```

## Bitwise Operators

```java
int a = 0b1010;  // 10 in binary
int b = 0b1100;  // 12 in binary

a & b    // 0b1000 = 8   (AND)
a | b    // 0b1110 = 14  (OR)
a ^ b    // 0b0110 = 6   (XOR)
~a       // bitwise NOT
a << 1   // left shift  = 20 (multiply by 2)
a >> 1   // right shift = 5  (divide by 2)
a >>> 1  // unsigned right shift
```

## Ternary Operator

```java
// condition ? valueIfTrue : valueIfFalse
int max = (a > b) ? a : b;
String label = (score >= 50) ? "Pass" : "Fail";
```

## instanceof Operator

```java
Object obj = "Hello";
if (obj instanceof String) {
    System.out.println("It's a String!");
}

// Java 16+ pattern matching:
if (obj instanceof String s) {
    System.out.println(s.toUpperCase());
}
```

## Operator Precedence (High to Low)

1. Postfix: `expr++`, `expr--`
2. Unary: `++expr`, `--expr`, `+expr`, `-expr`, `~`, `!`
3. Multiplicative: `*`, `/`, `%`
4. Additive: `+`, `-`
5. Shift: `<<`, `>>`, `>>>`
6. Relational: `<`, `>`, `<=`, `>=`, `instanceof`
7. Equality: `==`, `!=`
8. Bitwise AND: `&`
9. Bitwise XOR: `^`
10. Bitwise OR: `|`
11. Logical AND: `&&`
12. Logical OR: `||`
13. Ternary: `?:`
14. Assignment: `=`, `+=`, `-=`, etc.

When in doubt, use parentheses `()` to make precedence explicit.
