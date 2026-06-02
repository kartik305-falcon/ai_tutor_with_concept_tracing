5.12	Complicated Declarations
C is sometimes castigated for the syntax of its declarations, particularly ones that involve pointers to functions. The syntax is an attempt to make the declaration and the use agree; it works well for simple cases, but it can be confusing for the harder ones, because declarations cannot be read left to right, and because parentheses are over-used. The difference between
 

 
 and
  int *f();	/* f: function returning pointer to int */

 int (*pf)();	/* pf: pointer to function returning int */
  illustrates the problem: * is a prefix operator and it has lower precedence than (), so parentheses are necessary to force the proper association.
Although truly complicated declarations rarely arise in practice, it is important to know how to understand them, and, if necessary, how to create them. One good way to synthesize declarations is in small steps with typedef, which is discussed in Section 6.7. As an alternative, in this section we will present a pair of programs that convert from valid C to a word description and back again. The word description reads left to right.
The first, dcl, is the more complex. It converts a C declaration into a word description, as in these examples:
 char **argv argv: pointer to char int (*daytab)[13] daytab: pointer to array[13] of int int *daytab[13] daytab: array[13] of pointer to int void *comp() comp: function returning pointer to void void (*comp)() comp: pointer to function returning void char (*(*x())[])() x: function returning pointer to array[] of pointer to function returning char char (*(*x[3])())[5] x: array[3] of pointer to function returning pointer to array[5] of char dcl is based on the grammar that specifies a declarator, which is spelled out precisely in Appendix A, Section 8.5; this is a simplified form:
 dcl:	optional *'s direct-dcl direct-dcl name
(dcl) direct-dcl() direct-dcl[optional size]
In words, a dcl is a direct-dcl, perhaps preceded by *'s. A direct-dcl is a name, or a parenthesized dcl, or a direct-dcl followed by parentheses, or a direct-dcl followed by brackets with an optional size.
This grammar can be used to parse functions. For instance, consider this declarator:

(*pfa[])() pfa will be identified as a name and thus as a direct-dcl. Then pfa[] is also a direct-dcl. Then
*pfa[] is recognized as a dcl, so (*pfa[]) is a direct-dcl. Then (*pfa[])() is a direct-dcl and thus a dcl. We can also illustrate the parse with a tree like this (where direct-dcl has been abbreviated to dir-dcl):
 

 

The heart of the dcl program is a pair of functions, dcl and dirdcl, that parse a declaration according to this grammar. Because the grammar is recursively defined, the functions call each other recursively as they recognize pieces of a declaration; the program is called a recursive-descent parser.

/* dcl: parse a declarator */ void dcl(void)
{ int ns; for (ns = 0; gettoken() == '*'; ) /* count *'s */ ns++; dirdcl(); while (ns-- > 0) strcat(out, " pointer to");
}
/* dirdcl: parse a direct declarator */ void dirdcl(void)
{ int type; if (tokentype == '(') {	/* ( dcl ) */ dcl(); if (tokentype != ')') printf("error: missing )\n");
} else if (tokentype == NAME) /* variable name */ strcpy(name, token);
  else
  printf("error: expected name or (dcl)\n");
  while ((type=gettoken()) == PARENS || type == BRACKETS)
  if (type == PARENS) strcat(out, " function returning"); else { strcat(out, " array"); strcat(out, token); strcat(out, " of");
}
}
Since the programs are intended to be illustrative, not bullet-proof, there are significant restrictions on dcl. It can only handle a simple data type line char or int. It does not handle argument types in functions, or qualifiers like const. Spurious blanks confuse it. It doesn't do much error recovery, so invalid declarations will also confuse it. These improvements are left as exercises.
Here are the global variables and the main routine:

#include <stdio.h> #include <string.h> #include <ctype.h>
#define MAXTOKEN 100 enum { NAME, PARENS, BRACKETS }; void dcl(void); void dirdcl(void); int gettoken(void); int tokentype;	/* type of last token */ char token[MAXTOKEN];	/* last token string */ char name[MAXTOKEN];	/* identifier name */ char datatype[MAXTOKEN]; /* data type = char, int, etc. */ char out[1000]; main() /* convert declaration to words */
{ while (gettoken() != EOF) {	/* 1st token on line */ strcpy(datatype, token); /* is the datatype */ out[0] = '\0'; dcl();	/* parse rest of line */ if (tokentype != '\n') printf("syntax error\n"); printf("%s: %s %s\n", name, out, datatype);
} return 0;
}
The function gettoken skips blanks and tabs, then finds the next token in the input; a ``token'' is a name, a pair of parentheses, a pair of brackets perhaps including a number, or any other single character. int gettoken(void) /* return next token */
{ int c, getch(void); void ungetch(int); char *p = token; while ((c = getch()) == ' ' || c == '\t')
; if (c == '(') { if ((c = getch()) == ')') { strcpy(token, "()"); return tokentype = PARENS;
} else { ungetch(c); return tokentype = '(';
 
}
} else if (c == '[') { for (*p++ = c; (*p++ = getch()) != ']'; )
;
*p = '\0'; return tokentype = BRACKETS;
} else if (isalpha(c)) { for (*p++ = c; isalnum(c = getch()); )
*p++ = c;
*p = '\0'; ungetch(c); return tokentype = NAME;
} else return tokentype = c;
} getch and ungetch are discussed in Chapter 4.
Going in the other direction is easier, especially if we do not worry about generating redundant parentheses. The program undcl converts a word description like ``x is a function returning a pointer to an array of pointers to functions returning char,'' which we will express as
 x () * [] * () char to char (*(*x())[])()
The abbreviated input syntax lets us reuse the gettoken function. undcl also uses the same external variables as dcl does.
/* undcl: convert word descriptions to declarations */ main()
{ int type; char temp[MAXTOKEN]; while (gettoken() != EOF) { strcpy(out, token); while ((type = gettoken()) != '\n') if (type == PARENS || type == BRACKETS) strcat(out, token); else if (type == '*') { sprintf(temp, "(*%s)", out); strcpy(out, temp);
} else if (type == NAME) { sprintf(temp, "%s %s", token, out); strcpy(out, temp);
} else printf("invalid input at %s\n", token);
} return 0;
}
Exercise 5-18. Make dcl recover from input errors.
Exercise 5-19. Modify undcl so that it does not add redundant parentheses to declarations.
Exercise 5-20. Expand dcl to handle declarations with function argument types, qualifiers like const, and so on.