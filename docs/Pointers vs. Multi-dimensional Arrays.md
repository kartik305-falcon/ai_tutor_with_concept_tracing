5.9	Pointers vs. Multi-dimensional Arrays
Newcomers to C are sometimes confused about the difference between a two-dimensional array and an array of pointers, such as name in the example above. Given the definitions int a[10][20]; int *b[10]; then a[3][4] and b[3][4] are both syntactically legal references to a single int. But a is a true two-dimensional array: 200 int-sized locations have been set aside, and the conventional rectangular subscript calculation 20 * row +col is used to find the element a[row,col]. For b, however, the definition only allocates 10 pointers and does not initialize them; initialization must be done explicitly, either statically or with code. Assuming that each element of b does point to a twenty-element array, then there will be 200 ints set aside, plus ten cells for the pointers. The important advantage of the pointer array is that the rows of the array may be of different lengths. That is, each element of b need not point to a twenty-element vector; some may point to two elements, some to fifty, and some to none at all.
Although we have phrased this discussion in terms of integers, by far the most frequent use of arrays of pointers is to store character strings of diverse lengths, as in the function month_name. Compare the declaration and picture for an array of pointers:
 char *name[] = { "Illegal month", "Jan", "Feb", "Mar" };

  with those for a two-dimensional array:
 char aname[][15] = { "Illegal month", "Jan", "Feb", "Mar" };

Exercise 5-9. Rewrite the routines day_of_year and month_day with pointers instead of indexing.