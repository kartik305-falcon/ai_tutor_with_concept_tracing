B.7	Variable Argument Lists: <stdarg.h>
The header <stdarg.h> provides facilities for stepping through a list of function arguments of unknown number and type.
Suppose lastarg is the last named parameter of a function f with a variable number of arguments. Then declare within f a variable of type va_list that will point to each argument in turn:
 va_list ap; ap must be initialized once with the macro va_start before any unnamed argument is accessed: va_start(va_list ap, lastarg);
Thereafter, each execution of the macro va_arg will produce a value that has the type and value of the next unnamed argument, and will also modify ap so the next use of va_arg returns the next argument: type va_arg(va_list ap, type);
The macro
 void va_end(va_list ap); must be called once after the arguments have been processed but before f is exited.