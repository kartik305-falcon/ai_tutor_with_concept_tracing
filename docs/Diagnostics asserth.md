B.6	Diagnostics: <assert.h>
The assert macro is used to add diagnostics to programs: void assert(int expression)
If expression is zero when	 assert(expression) is executed, the assert macro will print on stderr a message, such as
Assertion failed: expression, file filename, line nnn
It then calls abort to terminate execution. The source filename and line number come from the preprocessor macros   FILE and  LINE .
If NDEBUG is defined at the time <assert.h> is included, the assert macro is ignored.