4.3	External Variables
A C program consists of a set of external objects, which are either variables or functions. The adjective ``external'' is used in contrast to ``internal'', which describes the arguments and variables defined inside functions. External variables are defined outside of any function, and are thus potentionally available to many functions. Functions themselves are always external, because C does not allow functions to be defined inside other functions. By default, external
  variables and functions have the property that all references to them by the same name, even from functions compiled separately, are references to the same thing. (The standard calls this property external linkage.) In this sense, external variables are analogous to Fortran COMMON blocks or variables in the outermost block in Pascal. We will see later how to define external variables and functions that are visible only within a single source file. Because external variables are globally accessible, they provide an alternative to function arguments and return values for communicating data between functions. Any function may access an external variable by referring to it by name, if the name has been declared somehow.
If a large number of variables must be shared among functions, external variables are more convenient and efficient than long argument lists. As pointed out in Chapter 1, however, this reasoning should be applied with some caution, for it can have a bad effect on program structure, and lead to programs with too many data connections between functions.
External variables are also useful because of their greater scope and lifetime. Automatic variables are internal to a function; they come into existence when the function is entered, and disappear when it is left. External variables, on the other hand, are permanent, so they can retain values from one function invocation to the next. Thus if two functions must share some data, yet neither calls the other, it is often most convenient if the shared data is kept in external variables rather than being passed in and out via arguments.
Let us examine this issue with a larger example. The problem is to write a calculator program that provides the operators +, -, * and /. Because it is easier to implement, the calculator will use reverse Polish notation instead of infix. (Reverse Polish notation is used by some pocket calculators, and in languages like Forth and Postscript.)
In reverse Polish notation, each operator follows its operands; an infix expression like

(1 - 2) * (4 + 5) is entered as
1 2 - 4 5 + *
Parentheses are not needed; the notation is unambiguous as long as we know how many operands each operator expects.
The implementation is simple. Each operand is pushed onto a stack; when an operator arrives, the proper number of operands (two for binary operators) is popped, the operator is applied to them, and the result is pushed back onto the stack. In the example above, for instance, 1 and 2 are pushed, then replaced by their difference, -1. Next, 4 and 5 are pushed and then replaced by their sum, 9. The product of -1 and 9, which is -9, replaces them on the stack. The value on the top of the stack is popped and printed when the end of the input line is encountered.
The structure of the program is thus a loop that performs the proper operation on each operator and operand as it appears:
 while (next operator or operand is not end-of-file indicator) if (number) push it else if (operator) pop operands do operation push result else if (newline) pop and print top of stack else error
 
The operation of pushing and popping a stack are trivial, but by the time error detection and recovery are added, they are long enough that it is better to put each in a separate function than to repeat the code throughout the whole program. And there should be a separate function for fetching the next input operator or operand.
The main design decision that has not yet been discussed is where the stack is, that is, which routines access it directly. On possibility is to keep it in main, and pass the stack and the current stack position to the routines that push and pop it. But main doesn't need to know about the variables that control the stack; it only does push and pop operations. So we have decided to store the stack and its associated information in external variables accessible to the push and pop functions but not to main.
Translating this outline into code is easy enough. If for now we think of the program as existing in one source file, it will look like this:
#includes #defines function declarations for main main() { ... } external variables for push and pop
 void push( double f) { ... } double pop(void) { ... } int getop(char s[]) { ... } routines called by getop
Later we will discuss how this might be split into two or more source files.
The function main is a loop containing a big switch on the type of operator or operand; this is a more typical use of switch than the one shown in Section 3.4.

#include <stdio.h>
#include <stdlib.h> /* for atof() */
#define MAXOP	100 /* max size of operand or operator */ #define NUMBER '0' /* signal that a number was found */ int getop(char []); void push(double); double pop(void);
/* reverse Polish calculator */ main()
{ int type; double op2; char s[MAXOP]; while ((type = getop(s)) != EOF) { switch (type) { case NUMBER: push(atof(s)); break; case '+': push(pop() + pop()); break; case '*': push(pop() * pop());
  break; case '-': op2 = pop(); push(pop() - op2); break; case '/': op2 = pop(); if (op2 != 0.0) push(pop() / op2); else printf("error: zero divisor\n"); break; case '\n': printf("\t%.8g\n", pop()); break; default: printf("error: unknown command %s\n", s); break;
}
} return 0;
}
Because + and * are commutative operators, the order in which the popped operands are combined is irrelevant, but for - and / the left and right operand must be distinguished. In push(pop() - pop());	/* WRONG */ the order in which the two calls of pop are evaluated is not defined. To guarantee the right order, it is necessary to pop the first value into a temporary variable as we did in main.
#define MAXVAL 100 /* maximum depth of val stack */ int sp = 0;	/* next free stack position */ double val[MAXVAL]; /* value stack */
/* push: push f onto value stack */ void push(double f)
{ if (sp < MAXVAL) val[sp++] = f; else printf("error: stack full, can't push %g\n", f);
}
/* pop: pop and return top value from stack */ double pop(void)
{ if (sp > 0) return val[--sp]; else { printf("error: stack empty\n"); return 0.0;
}
}
A variable is external if it is defined outside of any function. Thus the stack and stack index that must be shared by push and pop are defined outside these functions. But main itself does not refer to the stack or stack position - the representation can be hidden.
Let us now turn to the implementation of getop, the function that fetches the next operator or operand. The task is easy. Skip blanks and tabs. If the next character is not a digit or a hexadecimal point, return it. Otherwise, collect a string of digits (which might include a decimal point), and return NUMBER, the signal that a number has been collected.

#include <ctype.h>
  int getch(void); void ungetch(int);
/* getop: get next character or numeric operand */ int getop(char s[])
{ int i, c; while ((s[0] = c = getch()) == ' ' || c == '\t')
; s[1] = '\0'; if (!isdigit(c) && c != '.') return c;	/* not a number */ i = 0; if (isdigit(c))	/* collect integer part */ while (isdigit(s[++i] = c = getch()))
; if (c == '.')	/* collect fraction part */ while (isdigit(s[++i] = c = getch()))
; s[i] = '\0'; if (c != EOF) ungetch(c); return NUMBER;
}
What are getch and ungetch? It is often the case that a program cannot determine that it has read enough input until it has read too much. One instance is collecting characters that make up a number: until the first non-digit is seen, the number is not complete. But then the program has read one character too far, a character that it is not prepared for.
The problem would be solved if it were possible to ``un-read'' the unwanted character. Then, every time the program reads one character too many, it could push it back on the input, so the rest of the code could behave as if it had never been read. Fortunately, it's easy to simulate un-getting a character, by writing a pair of cooperating functions. getch delivers the next input character to be considered; ungetch will return them before reading new input.
How they work together is simple. ungetch puts the pushed-back characters into a shared buffer -- a character array. getch reads from the buffer if there is anything else, and calls getchar if the buffer is empty. There must also be an index variable that records the position of the current character in the buffer.
Since the buffer and the index are shared by getch and ungetch and must retain their values between calls, they must be external to both routines. Thus we can write getch, ungetch, and their shared variables as:

#define BUFSIZE 100 char buf[BUFSIZE];	/* buffer for ungetch */ int bufp = 0;	/* next free position in buf */ int getch(void) /* get a (possibly pushed-back) character */
{ return (bufp > 0) ? buf[--bufp] : getchar();
} void ungetch(int c)	/* push character back on input */
{ if (bufp >= BUFSIZE) printf("ungetch: too many characters\n"); else buf[bufp++] = c;
}
 
The standard library includes a function ungetch that provides one character of pushback; we will discuss it in Chapter 7. We have used an array for the pushback, rather than a single character, to illustrate a more general approach.
Exercise 4-3. Given the basic framework, it's straightforward to extend the calculator. Add the modulus (%) operator and provisions for negative numbers.
Exercise 4-4. Add the commands to print the top elements of the stack without popping, to duplicate it, and to swap the top two elements. Add a command to clear the stack.
Exercise 4-5. Add access to library functions like sin, exp, and pow. See <math.h> in Appendix B, Section 4.
Exercise 4-6. Add commands for handling variables. (It's easy to provide twenty-six variables with single-letter names.) Add a variable for the most recently printed value.
Exercise 4-7. Write a routine ungets(s) that will push back an entire string onto the input. Should ungets know about buf and bufp, or should it just use ungetch?
Exercise 4-8. Suppose that there will never be more than one character of pushback. Modify getch and ungetch accordingly.
Exercise 4-9. Our getch and ungetch do not handle a pushed-back EOF correctly. Decide what their properties ought to be if an EOF is pushed back, then implement your design.
Exercise 4-10. An alternate organization uses getline to read an entire input line; this makes getch and ungetch unnecessary. Revise the calculator to use this approach.