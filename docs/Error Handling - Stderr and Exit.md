7.6	Error Handling - Stderr and Exit
 
The treatment of errors in cat is not ideal. The trouble is that if one of the files can't be accessed for some reason, the diagnostic is printed at the end of the concatenated output. That might be acceptable if the output is going to a screen, but not if it's going into a file or into another program via a pipeline.
To handle this situation better, a second output stream, called stderr, is assigned to a program in the same way that stdin and stdout are. Output written on stderr normally appears on the screen even if the standard output is redirected.
Let us revise cat to write its error messages on the standard error.

#include <stdio.h>
/* cat: concatenate files, version 2 */ main(int argc, char *argv[])
{
FILE *fp; void filecopy(FILE *, FILE *); char *prog = argv[0]; /* program name for errors */ if (argc == 1 ) /* no args; copy standard input */ filecopy(stdin, stdout);
  else
  while (--argc > 0) if ((fp = fopen(*++argv, "r")) == NULL) { fprintf(stderr, "%s: can't open %s\n", prog, *argv); exit(1);
} else { filecopy(fp, stdout); fclose(fp);
 
} if (ferror(stdout)) { fprintf(stderr, "%s: error writing stdout\n", prog); exit(2);
} exit(0);
}
The program signals errors in two ways. First, the diagnostic output produced by fprintf goes to stderr, so it finds its way to the screen instead of disappearing down a pipeline or into an output file. We included the program name, from argv[0], in the message, so if this program is used with others, the source of an error is identified.
Second, the program uses the standard library function exit, which terminates program execution when it is called. The argument of exit is available to whatever process called this one, so the success or failure of the program can be tested by another program that uses this one as a sub-process. Conventionally, a return value of 0 signals that all is well; non-zero values usually signal abnormal situations. exit calls fclose for each open output file, to flush out any buffered output.
Within main, return expr is equivalent to exit(expr). exit has the advantage that it can be called from other functions, and that calls to it can be found with a pattern-searching program like those in Chapter 5.
The function ferror returns non-zero if an error occurred on the stream fp.
 int ferror(FILE *fp)
Although output errors are rare, they do occur (for example, if a disk fills up), so a production program should check this as well.
 
The function feof(FILE *) is analogous to ferror; it returns non-zero if end of file has occurred on the specified file.
 int feof(FILE *fp)
We have generally not worried about exit status in our small illustrative programs, but any serious program should take care to return sensible, useful status values.