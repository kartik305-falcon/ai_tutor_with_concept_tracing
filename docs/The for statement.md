1.3	The for statement
There are plenty of different ways to write a program for a particular task. Let's try a variation on the temperature converter.
#include <stdio.h>
 
/* print Fahrenheit-Celsius table */ main()
{ int fahr; for (fahr = 0; fahr <= 300; fahr = fahr + 20) printf("%3d %6.1f\n", fahr, (5.0/9.0)*(fahr-32));
}
This produces the same answers, but it certainly looks different. One major change is the elimination of most of the variables; only fahr remains, and we have made it an int. The lower and upper limits and the step size appear only as constants in the for statement, itself a new construction, and the expression that computes the Celsius temperature now appears as the third argument of printf instead of a separate assignment statement.
This last change is an instance of a general rule - in any context where it is permissible to use the value of some type, you can use a more complicated expression of that type. Since the third argument of printf must be a floating-point value to match the %6.1f, any floating-point expression can occur here.
The for statement is a loop, a generalization of the while. If you compare it to the earlier while, its operation should be clear. Within the parentheses, there are three parts, separated by semicolons. The first part, the initialization
 fahr = 0
  is done once, before the loop proper is entered. The second part is the test or condition that controls the loop: fahr <= 300
This condition is evaluated; if it is true, the body of the loop (here a single ptintf) is executed. Then the increment step fahr = fahr + 20 is executed, and the condition re-evaluated. The loop terminates if the condition has become false. As with the while, the body of the loop can be a single statement or a group of statements enclosed in braces. The initialization, condition and increment can be any expressions.
The choice between while and for is arbitrary, based on which seems clearer. The for is usually appropriate for loops in which the initialization and increment are single statements and logically related, since it is more compact than while and it keeps the loop control statements together in one place.
Exercise 1-5. Modify the temperature conversion program to print the table in reverse order, that is, from 300 degrees to 0.