7.4	Formatted Input - Scanf
The function scanf is the input analog of printf, providing many of the same conversion facilities in the opposite direction. int scanf(char *format, ...) scanf reads characters from the standard input, interprets them according to the specification in format, and stores the results through the remaining arguments. The format argument is described below; the other arguments, each of which must be a pointer, indicate where the corresponding converted input should be stored. As with printf, this section is a summary of the most useful features, not an exhaustive list. scanf stops when it exhausts its format string, or when some input fails to match the control specification. It returns as its value the number of successfully matched and assigned input items. This can be used to decide how many items were found. On the end of file, EOF is returned; note that this is different from 0, which means that the next input character does not match the first specification in the format string. The next call to scanf resumes searching immediately after the last character already converted.
There is also a function sscanf that reads from a string instead of the standard input:
 int sscanf(char *string, char *format, arg1, arg2, ...)
It scans the string according to the format in format and stores the resulting values through arg1, arg2, etc. These arguments must be pointers.
The format string usually contains conversion specifications, which are used to control conversion of input. The format string may contain:
•	Blanks or tabs, which are not ignored.
 
•	Ordinary characters (not %), which are expected to match the next non-white space character of the input stream.
•	Conversion specifications, consisting of the character %, an optional assignment suppression character *, an optional number specifying a maximum field width, an optional h, l or L indicating the width of the target, and a conversion character.
A conversion specification directs the conversion of the next input field. Normally the result is places in the variable pointed to by the corresponding argument. If assignment suppression is indicated by the * character, however, the input field is skipped; no assignment is made. An input field is defined as a string of non-white space characters; it extends either to the next white space character or until the field width, is specified, is exhausted. This implies that scanf will read across boundaries to find its input, since newlines are white space. (White space characters are blank, tab, newline, carriage return, vertical tab, and formfeed.)
The conversion character indicates the interpretation of the input field. The corresponding argument must be a pointer, as required by the call-by-value semantics of C. Conversion characters are shown in Table 7.2.
Table 7.2: Basic Scanf Conversions

Character	Input Data; Argument type d	decimal integer; int * i	integer; int *. The integer may be in octal (leading 0) or hexadecimal (leading
0x or 0X). o	octal integer (with or without leading zero); int * u	unsigned decimal integer; unsigned int * x	hexadecimal integer (with or without leading 0x or 0X); int *
 c	characters; char *. The next input characters (default 1) are placed at the indicated spot. The normal skip-over white space is suppressed; to read the next non-white space character, use %1s s	character string (not quoted); char *, pointing to an array of characters long enough for the string and a terminating '\0' that will be added. e,f,g	floating-point number with optional sign, optional decimal point and optional exponent; float *
%	literal %; no assignment is made.
The conversion characters d, i, o, u, and x may be preceded by h to indicate that a pointer to short rather than int appears in the argument list, or by l (letter ell) to indicate that a pointer to long appears in the argument list.
As a first example, the rudimentary calculator of Chapter 4 can be written with scanf to do the input conversion:

#include <stdio.h> main() /* rudimentary calculator */
{ double sum, v; sum = 0; while (scanf("%lf", &v) == 1) printf("\t%.2f\n", sum += v); return 0;
}
Suppose we want to read input lines that contain dates of the form
 

25 Dec 1988
The scanf statement is int day, year; char monthname[20]; scanf("%d %s %d", &day, monthname, &year);
No & is used with monthname, since an array name is a pointer.
Literal characters can appear in the scanf format string; they must match the same characters in the input. So we could read dates of the form mm/dd/yy with the scanf statement:
 int day, month, year; scanf("%d/%d/%d", &month, &day, &year); scanf ignores blanks and tabs in its format string. Furthermore, it skips over white space (blanks, tabs, newlines, etc.) as it looks for input values. To read input whose format is not fixed, it is often best to read a line at a time, then pick it apart with scanf. For example, suppose we want to read lines that might contain a date in either of the forms above. Then we could write while (getline(line, sizeof(line)) > 0) { if (sscanf(line, "%d %s %d", &day, monthname, &year) == 3) printf("valid: %s\n", line); /* 25 Dec 1988 form */ else if (sscanf(line, "%d/%d/%d", &month, &day, &year) == 3) printf("valid: %s\n", line); /* mm/dd/yy form */
  else
}
  printf("invalid: %s\n", line); /* invalid form */
 
Calls to scanf can be mixed with calls to other input functions. The next call to any input function will begin by reading the first character not read by scanf.
A final warning: the arguments to scanf and sscanf must be pointers. By far the most common error is writing
 scanf("%d", n); instead of scanf("%d", &n);
This error is not generally detected at compile time.
Exercise 7-4. Write a private version of scanf analogous to minprintf from the previous section.
Exercise 5-5. Rewrite the postfix calculator of Chapter 4 to use scanf and/or sscanf to do the input and number conversion.