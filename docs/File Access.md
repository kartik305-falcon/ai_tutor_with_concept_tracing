7.5	File Access
The examples so far have all read the standard input and written the standard output, which are automatically defined for a program by the local operating system.
The next step is to write a program that accesses a file that is not already connected to the program. One program that illustrates the need for such operations is cat, which concatenates a set of named files into the standard output. cat is used for printing files on the screen, and as a general-purpose input collector for programs that do not have the capability of accessing files by name. For example, the command
 cat x.c y.c
  prints the contents of the files x.c and y.c (and nothing else) on the standard output.
The question is how to arrange for the named files to be read - that is, how to connect the external names that a user thinks of to the statements that read the data.
The rules are simple. Before it can be read or written, a file has to be opened by the library function fopen. fopen takes an external name like x.c or y.c, does some housekeeping and negotiation with the operating system (details of which needn't concern us), and returns a pointer to be used in subsequent reads or writes of the file.
This pointer, called the file pointer, points to a structure that contains information about the file, such as the location of a buffer, the current character position in the buffer, whether the file is being read or written, and whether errors or end of file have occurred. Users don't need to know the details, because the definitions obtained from <stdio.h> include a structure declaration called FILE. The only declaration needed for a file pointer is exemplified by

FILE *fp;
FILE *fopen(char *name, char *mode);
This says that fp is a pointer to a FILE, and fopen returns a pointer to a FILE. Notice that FILE is a type name, like int, not a structure tag; it is defined with a typedef. (Details of how fopen can be implemented on the UNIX system are given in Section 8.5.)
The call to fopen in a program is
 fp = fopen(name, mode);
The first argument of fopen is a character string containing the name of the file. The second argument is the mode, also a character string, which indicates how one intends to use the file. Allowable modes include read ("r"), write ("w"), and append ("a"). Some systems distinguish between text and binary files; for the latter, a "b" must be appended to the mode string.
If a file that does not exist is opened for writing or appending, it is created if possible. Opening an existing file for writing causes the old contents to be discarded, while opening for appending preserves them. Trying to read a file that does not exist is an error, and there may be other causes of error as well, like trying to read a file when you don't have permission. If there is any error, fopen will return NULL. (The error can be identified more precisely; see the discussion of error-handling functions at the end of Section 1 in Appendix B.)
The next thing needed is a way to read or write the file once it is open. getc returns the next character from a file; it needs the file pointer to tell it which file.
 int getc(FILE *fp) getc returns the next character from the stream referred to by fp; it returns EOF for end of file or error. putc is an output function:
 int putc(int c, FILE *fp) putc writes the character c to the file fp and returns the character written, or EOF if an error occurs. Like getchar and putchar, getc and putc may be macros instead of functions.
When a C program is started, the operating system environment is responsible for opening three files and providing pointers for them. These files are the standard input, the standard output, and the standard error; the corresponding file pointers are called stdin, stdout, and stderr, and are declared in <stdio.h>. Normally stdin is connected to the keyboard and stdout and stderr are connected to the screen, but stdin and stdout may be redirected to files or pipes as described in Section 7.1.
  getchar and putchar can be defined in terms of getc, putc, stdin, and stdout as follows:

#define getchar()	getc(stdin) #define putchar(c)	putc((c), stdout)
For formatted input or output of files, the functions fscanf and fprintf may be used. These are identical to scanf and printf, except that the first argument is a file pointer that specifies the file to be read or written; the format string is the second argument. int fscanf(FILE *fp, char *format, ...) int fprintf(FILE *fp, char *format, ...)
With these preliminaries out of the way, we are now in a position to write the program cat to concatenate files. The design is one that has been found convenient for many programs. If there are command-line arguments, they are interpreted as filenames, and processed in order. If there are no arguments, the standard input is processed.
#include <stdio.h>
/* cat: concatenate files, version 1 */ main(int argc, char *argv[])
{
FILE *fp; void filecopy(FILE *, FILE *) if (argc == 1) /* no args; copy standard input */ filecopy(stdin, stdout); else while(--argc > 0) if ((fp = fopen(*++argv, "r")) == NULL) { printf("cat: can't open %s\n, *argv); return 1;
} else { filecopy(fp, stdout); fclose(fp);
} return 0;
}
/* filecopy: copy file ifp to file ofp */ void filecopy(FILE *ifp, FILE *ofp)
{ int c; while ((c = getc(ifp)) != EOF) putc(c, ofp);
}
The file pointers stdin and stdout are objects of type FILE *. They are constants, however, not variables, so it is not possible to assign to them.
The function
 int fclose(FILE *fp) is the inverse of fopen, it breaks the connection between the file pointer and the external name that was established by fopen, freeing the file pointer for another file. Since most operating systems have some limit on the number of files that a program may have open simultaneously, it's a good idea to free the file pointers when they are no longer needed, as we did in cat. There is also another reason for fclose on an output file - it flushes the buffer in which putc is collecting output. fclose is called automatically for each open file when a program terminates normally. (You can close stdin and stdout if they are not needed. They can also be reassigned by the library function freopen.)