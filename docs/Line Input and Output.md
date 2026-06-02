7.7	Line Input and Output
The standard library provides an input and output routine fgets that is similar to the getline function that we have used in earlier chapters: char *fgets(char *line, int maxline, FILE *fp) fgets reads the next input line (including the newline) from file fp into the character array line; at most maxline-1 characters will be read. The resulting line is terminated with '\0'. Normally fgets returns line; on end of file or error it returns NULL. (Our getline returns the line length, which is a more useful value; zero means end of file.)
For output, the function fputs writes a string (which need not contain a newline) to a file:
 int fputs(char *line, FILE *fp)
It returns EOF if an error occurs, and non-negative otherwise.
The library functions gets and puts are similar to fgets and fputs, but operate on stdin and stdout. Confusingly, gets deletes the terminating '\n', and puts adds it.
To show that there is nothing special about functions like fgets and fputs, here they are, copied from the standard library on our system:

/* fgets: get at most n chars from iop */ char *fgets(char *s, int n, FILE *iop)
{ register int c; register char *cs; cs = s; while (--n > 0 && (c = getc(iop)) != EOF) if ((*cs++ = c) == '\n') break;
*cs = '\0'; return (c == EOF && cs == s) ? NULL : s;
}
/* fputs: put string s on file iop */ int fputs(char *s, FILE *iop)
{ int c; while (c = *s++) putc(c, iop); return ferror(iop) ? EOF : 0;
}
For no obvious reason, the standard specifies different return values for ferror and fputs. It is easy to implement our getline from fgets:
/* getline: read a line, return length */ int getline(char *line, int max)
{ if (fgets(line, max, stdin) == NULL) return 0; else
  return strlen(line);
}
Exercise 7-6. Write a program to compare two files, printing the first line where they differ.
Exercise 7-7. Modify the pattern finding program of Chapter 5 to take its input from a set of named files or, if no files are named as arguments, from the standard input. Should the file name be printed when a matching line is found?
Exercise 7-8. Write a program to print a set of files, starting each new one on a new page, with a title and a running page count for each file.