8.2	Low Level I/O - Read and Write
Input and output uses the read and write system calls, which are accessed from C programs through two functions called read and write. For both, the first argument is a file descriptor. The second argument is a character array in your program where the data is to go to or to come from. The third argument is the number is the number of bytes to be transferred. int n_read = read(int fd, char *buf, int n); int n_written = write(int fd, char *buf, int n);
Each call returns a count of the number of bytes transferred. On reading, the number of bytes returned may be less than the number requested. A return value of zero bytes implies end of file, and -1 indicates an error of some sort. For writing, the return value is the number of bytes written; an error has occurred if this isn't equal to the number requested.
Any number of bytes can be read or written in one call. The most common values are 1, which means one character at a time (``unbuffered''), and a number like 1024 or 4096 that corresponds to a physical block size on a peripheral device. Larger sizes will be more efficient because fewer system calls will be made.
Putting these facts together, we can write a simple program to copy its input to its output, the equivalent of the file copying program written for Chapter 1. This program will copy anything to anything, since the input and output can be redirected to any file or device.

#include "syscalls.h" main() /* copy input to output */
{ char buf[BUFSIZ]; int n; while ((n = read(0, buf, BUFSIZ)) > 0) write(1, buf, n); return 0;
}
We have collected function prototypes for the system calls into a file called syscalls.h so we can include it in the programs of this chapter. This name is not standard, however.
The parameter BUFSIZ is also defined in syscalls.h; its value is a good size for the local system. If the file size is not a multiple of BUFSIZ, some read will return a smaller number of bytes to be written by write; the next call to read after that will return zero.
It is instructive to see how read and write can be used to construct higher-level routines like getchar, putchar, etc. For example, here is a version of getchar that does unbuffered input, by reading the standard input one character at a time.

#include "syscalls.h"
/* getchar: unbuffered single character input */ int getchar(void)
{ char c; return (read(0, &c, 1) == 1) ? (unsigned char) c : EOF;
} c must be a char, because read needs a character pointer. Casting c to unsigned char in the return statement eliminates any problem of sign extension.
The second version of getchar does input in big chunks, and hands out the characters one at a time.
 
#include "syscalls.h"
/* getchar: simple buffered version */ int getchar(void)
{ static char buf[BUFSIZ]; static char *bufp = buf; static int n = 0; if (n == 0) { /* buffer is empty */ n = read(0, buf, sizeof buf); bufp = buf;
} return (--n >= 0) ? (unsigned char) *bufp++ : EOF;
}
If these versions of getchar were to be compiled with <stdio.h> included, it would be necessary to #undef the name getchar in case it is implemented as a macro.