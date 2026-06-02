8.3	Open, Creat, Close, Unlink
Other than the default standard input, output and error, you must explicitly open files in order to read or write them. There are two system calls for this, open and creat [sic]. open is rather like the fopen discussed in Chapter 7, except that instead of returning a file pointer, it returns a file descriptor, which is just an int. open returns -1 if any error occurs.

#include <fcntl.h> int fd; int open(char *name, int flags, int perms); fd = open(name, flags, perms);
As with fopen, the name argument is a character string containing the filename. The second argument, flags, is an int that specifies how the file is to be opened; the main values are
O_RDONLY open for reading only
O_WRONLY open for writing only
O_RDWR	open for both reading and writing
These constants are defined in <fcntl.h> on System V UNIX systems, and in <sys/file.h> on Berkeley (BSD) versions.
To open an existing file for reading,
 fd = open(name, O_RDONLY,0);
The perms argument is always zero for the uses of open that we will discuss.
It is an error to try to open a file that does not exist. The system call creat is provided to create new files, or to re-write old ones.
 int creat(char *name, int perms); fd = creat(name, perms); returns a file descriptor if it was able to create the file, and -1 if not. If the file already exists, creat will truncate it to zero length, thereby discarding its previous contents; it is not an error to creat a file that already exists.
If the file does not already exist, creat creates it with the permissions specified by the perms argument. In the UNIX file system, there are nine bits of permission information associated with a file that control read, write and execute access for the owner of the file, for the owner's group, and for all others. Thus a three-digit octal number is convenient for specifying the
  permissions. For example, 0775 specifies read, write and execute permission for the owner, and read and execute permission for the group and everyone else.
To illustrate, here is a simplified version of the UNIX program cp, which copies one file to another. Our version copies only one file, it does not permit the second argument to be a directory, and it invents permissions instead of copying them.

#include <stdio.h> #include <fcntl.h> #include "syscalls.h"
#define PERMS 0666	/* RW for owner, group, others */ void error(char *, ...);
/* cp: copy f1 to f2 */ main(int argc, char *argv[])
{ int f1, f2, n; char buf[BUFSIZ]; if (argc != 3) error("Usage: cp from to"); if ((f1 = open(argv[1], O_RDONLY, 0)) == -1) error("cp: can't open %s", argv[1]); if ((f2 = creat(argv[2], PERMS)) == -1) error("cp: can't create %s, mode %03o", argv[2], PERMS); while ((n = read(f1, buf, BUFSIZ)) > 0) if (write(f2, buf, n) != n) error("cp: write error on file %s", argv[2]); return 0;
}
This program creates the output file with fixed permissions of 0666. With the stat system call, described in Section 8.6, we can determine the mode of an existing file and thus give the same mode to the copy.
Notice that the function error is called with variable argument lists much like printf. The implementation of error illustrates how to use another member of the printf family. The standard library function vprintf is like printf except that the variable argument list is replaced by a single argument that has been initialized by calling the va_start macro. Similarly, vfprintf and vsprintf match fprintf and sprintf.

#include <stdio.h> #include <stdarg.h>
/* error: print an error message and die */ void error(char *fmt, ...)
{ va_list args; va_start(args, fmt); fprintf(stderr, "error: "); vprintf(stderr, fmt, args); fprintf(stderr, "\n"); va_end(args); exit(1);
}
There is a limit (often about 20) on the number of files that a program may open simultaneously. Accordingly, any program that intends to process many files must be prepared to re-use file descriptors. The function close(int fd) breaks the connection between a file descriptor and an open file, and frees the file descriptor for use with some other file; it
  corresponds to fclose in the standard library except that there is no buffer to flush. Termination of a program via exit or return from the main program closes all open files.
The function unlink(char *name) removes the file name from the file system. It corresponds to the standard library function remove.
Exercise 8-1. Rewrite the program cat from Chapter 7 using read, write, open, and close instead of their standard library equivalents. Perform experiments to determine the relative speeds of the two versions.