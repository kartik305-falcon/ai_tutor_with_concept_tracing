2.10	Assignment Operators and Expressions
An expression such as i = i + 2 in which the variable on the left side is repeated immediately on the right, can be written in the compressed form i += 2	
The operator += is called an assignment operator.
Most binary operators (operators like + that have a left and right operand) have a corresponding assignment operator op=, where op is one of

+	-	*	/	%	<<	>>	&	^	|
If expr1 and expr2 are expressions, then expr1 op= expr2 is equivalent to expr1 = (expr1) op (expr2) except that expr1 is computed only once. Notice the parentheses around expr2: x *= y + 1 means x = x * (y + 1) rather than x = x * y + 1
As an example, the function bitcount counts the number of 1-bits in its integer argument.
/* bitcount: count 1 bits in x */ int bitcount(unsigned x)
{ int b; for (b = 0; x != 0; x >>= 1) if (x & 01) b++; return b;
}
Declaring the argument x to be an unsigned ensures that when it is right-shifted, vacated bits will be filled with zeros, not sign bits, regardless of the machine the program is run on.
 
Quite apart from conciseness, assignment operators have the advantage that they correspond better to the way people think. We say ``add 2 to i'' or ``increment i by 2'', not ``take i, add 2, then put the result back in i''. Thus the expression i += 2 is preferable to i = i+2. In addition, for a complicated expression like
 yyval[yypv[p3+p4] + yypv[p1]] += 2 the assignment operator makes the code easier to understand, since the reader doesn't have to check painstakingly that two long expressions are indeed the same, or to wonder why they're not. And an assignment operator may even help a compiler to produce efficient code.
We have already seen that the assignment statement has a value and can occur in expressions; the most common example is
 while ((c = getchar()) != EOF)
...
The other assignment operators (+=, -=, etc.) can also occur in expressions, although this is less frequent.
In all such expressions, the type of an assignment expression is the type of its left operand, and the value is the value after the assignment.
Exercise 2-9. In a two's complement number system, x &= (x-1) deletes the rightmost 1-bit in x. Explain why. Use this observation to write a faster version of bitcount.