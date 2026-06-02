4.10	Recursion
C functions may be used recursively; that is, a function may call itself either directly or indirectly. Consider printing a number as a character string. As we mentioned before, the digits are generated in the wrong order: low-order digits are available before high-order digits, but they have to be printed the other way around.
There are two solutions to this problem. On is to store the digits in an array as they are generated, then print them in the reverse order, as we did with itoa in section 3.6. The alternative is a recursive solution, in which printd first calls itself to cope with any leading digits, then prints the trailing digit. Again, this version can fail on the largest negative number.

#include <stdio.h>
/* printd: print n in decimal */ void printd(int n)
{ if (n < 0) { putchar('-'); n = -n;
} if (n / 10) printd(n / 10); putchar(n % 10 + '0');
}
 
When a function calls itself recursively, each invocation gets a fresh set of all the automatic variables, independent of the previous set. This in printd(123) the first printd receives the argument n = 123. It passes 12 to a second printd, which in turn passes 1 to a third. The third-level printd prints 1, then returns to the second level. That printd prints 2, then returns to the first level. That one prints 3 and terminates.
Another good example of recursion is quicksort, a sorting algorithm developed by C.A.R. Hoare in 1962. Given an array, one element is chosen and the others partitioned in two subsets
- those less than the partition element and those greater than or equal to it. The same process is then applied recursively to the two subsets. When a subset has fewer than two elements, it doesn't need any sorting; this stops the recursion.
Our version of quicksort is not the fastest possible, but it's one of the simplest. We use the middle element of each subarray for partitioning.

/* qsort: sort v[left]...v[right] into increasing order */ void qsort(int v[], int left, int right)
{ int i, last; void swap(int v[], int i, int j); if (left >= right) /* do nothing if array contains */ return;	/* fewer than two elements */ swap(v, left, (left + right)/2); /* move partition elem */ last = left;	/* to v[0] */ for (i = left + 1; i <= right; i++) /* partition */ if (v[i] < v[left]) swap(v, ++last, i); swap(v, left, last);	/* restore partition elem */ qsort(v, left, last-1); qsort(v, last+1, right);
}
We moved the swapping operation into a separate function swap because it occurs three times in qsort.
/* swap: interchange v[i] and v[j] */ void swap(int v[], int i, int j)
{ int temp; temp = v[i]; v[i] = v[j]; v[j] = temp;
}
The standard library includes a version of qsort that can sort objects of any type.
Recursion may provide no saving in storage, since somewhere a stack of the values being processed must be maintained. Nor will it be faster. But recursive code is more compact, and often much easier to write and understand than the non-recursive equivalent. Recursion is especially convenient for recursively defined data structures like trees, we will see a nice example in Section 6.6.
Exercise 4-12. Adapt the ideas of printd to write a recursive version of itoa; that is, convert an integer into a string by calling a recursive routine.
Exercise 4-13. Write a recursive version of the function reverse(s), which reverses the string s in place.