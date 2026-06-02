4.8	Block Structure
C is not a block-structured language in the sense of Pascal or similar languages, because functions may not be defined within other functions. On the other hand, variables can be defined in a block-structured fashion within a function. Declarations of variables (including initializations) may follow the left brace that introduces any compound statement, not just the one that begins a function. Variables declared in this way hide any identically named variables in outer blocks, and remain in existence until the matching right brace. For example, in if (n > 0) {	 int i; /* declare a new i */ for (i = 0; i < n; i++)
...
} the scope of the variable i is the ``true'' branch of the if; this i is unrelated to any i outside the block. An automatic variable declared and initialized in a block is initialized each time the block is entered.
Automatic variables, including formal parameters, also hide external variables and functions of the same name. Given the declarations
 int x; int y; f(double x)
{ double y;
} then within the function f, occurrences of x refer to the parameter, which is a double; outside f, they refer to the external int. The same is true of the variable y.
As a matter of style, it's best to avoid variable names that conceal names in an outer scope; the potential for confusion and error is too great.