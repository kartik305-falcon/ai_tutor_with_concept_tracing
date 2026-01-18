A.8	Declarations
Declarations specify the interpretation given to each identifier; they do not necessarily reserve storage associated with the identifier. Declarations that reserve storage are called definitions.
Declarations have the form declaration: declaration-specifiers init-declarator-listopt;
The declarators in the init-declarator list contain the identifiers being declared; the declaration-specifiers consist of a sequence of type and storage class specifiers. declaration-specifiers: storage-class-specifier declaration-specifiersopt type-specifier declaration-specifiersopt type-qualifier declaration-specifiersopt init-declarator-list: init-declarator init-declarator-list , init-declarator init-declarator: declarator declarator = initializer
Declarators will be discussed later (Par.A.8.5); they contain the names being declared. A declaration must have at least one declarator, or its type specifier must declare a structure tag, a union tag, or the members of an enumeration; empty declarations are not permitted.
A.8.1	Storage Class Specifiers
The storage class specifiers are: storage-class specifier: auto register
  static extern typedef
The meaning of the storage classes were discussed in Par.A.4.4.
The auto and register specifiers give the declared objects automatic storage class, and may be used only within functions. Such declarations also serve as definitions and cause storage to be reserved. A register declaration is equivalent to an auto declaration, but hints that the declared objects will be accessed frequently. Only a few objects are actually placed into registers, and only certain types are eligible; the restrictions are implementation-dependent. However, if an object is declared register, the unary & operator may not be applied to it, explicitly or implicitly.
The rule that it is illegal to calculate the address of an object declared register, but actually taken to be auto, is new.
The static specifier gives the declared objects static storage class, and may be used either inside or outside functions. Inside a function, this specifier causes storage to be allocated, and serves as a definition; for its effect outside a function, see Par.A.11.2.
A declaration with extern, used inside a function, specifies that the storage for the declared objects is defined elsewhere; for its effects outside a function, see Par.A.11.2.
The typedef specifier does not reserve storage and is called a storage class specifier only for syntactic convenience; it is discussed in Par.A.8.9.
At most one storage class specifier may be given in a declaration. If none is given, these rules are used: objects declared inside a function are taken to be auto; functions declared within a function are taken to be extern; objects and functions declared outside a function are taken to be static, with external linkage. See Pars. A.10-A.11.
A.8.2	Type Specifiers
The type-specifiers are type specifier: void char short int long float double signed unsigned struct-or-union-specifier enum-specifier typedef-name
At most one of the words long or short may be specified together with int; the meaning is the same if int is not mentioned. The word long may be specified together with double. At most one of signed or unsigned may be specified together with int or any of its short or long varieties, or with char. Either may appear alone in which case int is understood. The signed specifier is useful for forcing char objects to carry a sign; it is permissible but redundant with other integral types.
 
Otherwise, at most one type-specifier may be given in a declaration. If the type-specifier is missing from a declaration, it is taken to be int.
Types may also be qualified, to indicate special properties of the objects being declared. type-qualifier: const volatile
Type qualifiers may appear with any type specifier. A const object may be initialized, but not thereafter assigned to. There are no implementation-dependent semantics for volatile objects.
The const and volatile properties are new with the ANSI standard. The purpose of const is to announce objects that may be placed in read-only memory, and perhaps to increase opportunities for optimization. The purpose of volatile is to force an implementation to suppress optimization that could otherwise occur. For example, for a machine with memory-mapped input/output, a pointer to a device register might be declared as a pointer to volatile, in order to prevent the compiler from removing apparently redundant references through the pointer. Except that it should diagnose explicit attempts to change const objects, a compiler may ignore these qualifiers.
A.8.3	Structure and Union Declarations
A structure is an object consisting of a sequence of named members of various types. A union is an object that contains, at different times, any of several members of various types. Structure and union specifiers have the same form. struct-or-union-specifier: struct-or-union identifieropt{ struct-declaration-list } struct-or-union identifier struct-or-union: struct union
A struct-declaration-list is a sequence of declarations for the members of the structure or union: struct-declaration-list: struct declaration struct-declaration-list struct declaration struct-declaration:	specifier-qualifier-list struct-declarator-list; specifier-qualifier-list: type-specifier specifier-qualifier-listopt type-qualifier specifier-qualifier-listopt struct-declarator-list: struct-declarator struct-declarator-list , struct-declarator
Usually, a struct-declarator is just a declarator for a member of a structure or union. A structure member may also consist of a specified number of bits. Such a member is also called a bit-field; its length is set off from the declarator for the field name by a colon. struct-declarator: declarator	declaratoropt : constant-expression
 
A type specifier of the form struct-or-union identifier { struct-declaration-list } declares the identifier to be the tag of the structure or union specified by the list. A subsequent declaration in the same or an inner scope may refer to the same type by using the tag in a specifier without the list: struct-or-union identifier
If a specifier with a tag but without a list appears when the tag is not declared, an incomplete type is specified. Objects with an incomplete structure or union type may be mentioned in contexts where their size is not needed, for example in declarations (not definitions), for specifying a pointer, or for creating a typedef, but not otherwise. The type becomes complete on occurrence of a subsequent specifier with that tag, and containing a declaration list. Even in specifiers with a list, the structure or union type being declared is incomplete within the list, and becomes complete only at the } terminating the specifier.
A structure may not contain a member of incomplete type. Therefore, it is impossible to declare a structure or union containing an instance of itself. However, besides giving a name to the structure or union type, tags allow definition of self-referential structures; a structure or union may contain a pointer to an instance of itself, because pointers to incomplete types may be declared.
A very special rule applies to declarations of the form struct-or-union identifier; that declare a structure or union, but have no declaration list and no declarators. Even if the identifier is a structure or union tag already declared in an outer scope (Par.A.11.1), this declaration makes the identifier the tag of a new, incompletely-typed structure or union in the current scope.
This recondite is new with ANSI. It is intended to deal with mutually-recursive structures declared in an inner scope, but whose tags might already be declared in the outer scope.
A structure or union specifier with a list but no tag creates a unique type; it can be referred to directly only in the declaration of which it is a part.
The names of members and tags do not conflict with each other or with ordinary variables. A member name may not appear twice in the same structure or union, but the same member name may be used in different structures or unions.
In the first edition of this book, the names of structure and union members were not associated with their parent. However, this association became common in compilers well before the ANSI standard.
A non-field member of a structure or union may have any object type. A field member (which need not have a declarator and thus may be unnamed) has type int, unsigned int, or signed int, and is interpreted as an object of integral type of the specified length in bits; whether an int field is treated as signed is implementation-dependent. Adjacent field members of structures are packed into implementation-dependent storage units in an implementation-dependent direction. When a field following another field will not fit into a partially-filled storage unit, it may be split between units, or the unit may be padded. An unnamed field with width 0 forces this padding, so that the next field will begin at the edge of the next allocation unit.
The ANSI standard makes fields even more implementation-dependent than did the first edition. It is advisable to read the language rules for storing bit-fields as ``implementation-dependent'' without qualification. Structures with bit-fields may be used as a portable way of attempting to reduce the storage required for a structure (with the probable cost of increasing the instruction space, and time,
  needed to access the fields), or as a non-portable way to describe a storage layout known at the bit-level. In the second case, it is necessary to understand the rules of the local implementation.
The members of a structure have addresses increasing in the order of their declarations. A non-field member of a structure is aligned at an addressing boundary depending on its type; therefore, there may be unnamed holes in a structure. If a pointer to a structure is cast to the type of a pointer to its first member, the result refers to the first member.
A union may be thought of as a structure all of whose members begin at offset 0 and whose size is sufficient to contain any of its members. At most one of the members can be stored in a union at any time. If a pointr to a union is cast to the type of a pointer to a member, the result refers to that member.
A simple example of a structure declaration is
 struct tnode { char tword[20]; int count; struct tnode *left; struct tnode *right;
} which contains an array of 20 characters, an integer, and two pointers to similar structures.
Once this declaration has bene given, the declaration struct tnode s, *sp; declares s to be a structure of the given sort, and sp to be a pointer to a structure of the given sort. With these declarations, the expression sp->count refers to the count field of the structure to which sp points; s.left refers to the left subtree pointer of the structure s, and s.right->tword[0] refers to the first character of the tword member of the right subtree of s.
In general, a member of a union may not be inspected unless the value of the union has been assigned using the same member. However, one special guarantee simplifies the use of unions: if a union contains several structures that share a common initial sequence, and the union currently contains one of these structures, it is permitted to refer to the common initial part of any of the contained structures. For example, the following is a legal fragment:
 union { struct { int type;
} n; struct { int type; int intnode;
} ni; struct { int type; float floatnode;
} nf;
} u;
... u.nf.type = FLOAT; u.nf.floatnode = 3.14;
... if (u.n.type == FLOAT)
 
... sin(u.nf.floatnode) ...
A.8.4	Enumerations
Enumerations are unique types with values ranging over a set of named constants called enumerators. The form of an enumeration specifier borrows from that of structures and unions. enum-specifier: enum identifieropt { enumerator-list } enum identifier enumerator-list: enumerator enumerator-list , enumerator enumerator: identifier identifier = constant-expression
The identifiers in an enumerator list are declared as constants of type int, and may appear wherever constants are required. If no enumerations with = appear, then the values of the corresponding constants begin at 0 and increase by 1 as the declaration is read from left to right. An enumerator with = gives the associated identifier the value specified; subsequent identifiers continue the progression from the assigned value.
Enumerator names in the same scope must all be distinct from each other and from ordinary variable names, but the values need not be distinct.
The role of the identifier in the enum-specifier is analogous to that of the structure tag in a struct-specifier; it names a particular enumeration. The rules for enum-specifiers with and without tags and lists are the same as those for structure or union specifiers, except that incomplete enumeration types do not exist; the tag of an enum-specifier without an enumerator list must refer to an in-scope specifier with a list.
Enumerations are new since the first edition of this book, but have been part of the language for some years.
A.8.5	Declarators
Declarators have the syntax: declarator: pointeropt direct-declarator direct-declarator: identifier
(declarator) direct-declarator [ constant-expressionopt ] direct-declarator ( parameter-type-list ) direct-declarator ( identifier-listopt ) pointer:
*	type-qualifier-listopt
*	type-qualifier-listopt pointer type-qualifier-list: type-qualifier type-qualifier-list type-qualifier
 
The structure of declarators resembles that of indirection, function, and array expressions; the grouping is the same.
A.8.6	Meaning of Declarators
A list of declarators appears after a sequence of type and storage class specifiers. Each declarator declares a unique main identifier, the one that appears as the first alternative of the production for direct-declarator. The storage class specifiers apply directly to this identifier, but its type depends on the form of its declarator. A declarator is read as an assertion that when its identifier appears in an expression of the same form as the declarator, it yields an object of the specified type.
Considering only the type parts of the declaration specifiers (Par. A.8.2) and a particular declarator, a declaration has the form ``T D,'' where T is a type and D is a declarator. The type attributed to the identifier in the various forms of declarator is described inductively using this notation.
In a declaration T D where D is an unadored identifier, the type of the identifier is T.
In a declaration T D where D has the form

( D1 ) then the type of the identifier in D1 is the same as that of D. The parentheses do not alter the type, but may change the binding of complex declarators.
A.8.6.1	Pointer Declarators
In a declaration T D where D has the form
* type-qualifier-listopt D1 and the type of the identifier in the declaration T D1 is ``type-modifier T,'' the type of the identifier of D is ``type-modifier type-qualifier-list pointer to T.'' Qualifiers following * apply to pointer itself, rather than to the object to which the pointer points.
For example, consider the declaration
 int *ap[];
Here, ap[] plays the role of D1; a declaration ``int ap[]'' (below) would give ap the type
``array of int,'' the type-qualifier list is empty, and the type-modifier is ``array of.'' Hence the actual declaration gives ap the type ``array to pointers to int.''
As other examples, the declarations
 int i, *pi, *const cpi = &i; const int ci = 3, *pci; declare an integer i and a pointer to an integer pi. The value of the constant pointer cpi may not be changed; it will always point to the same location, although the value to which it refers may be altered. The integer ci is constant, and may not be changed (though it may be initialized, as here.) The type of pci is ``pointer to const int,'' and pci itself may be changed to point to another place, but the value to which it points may not be altered by assigning through pci.
A.8.6.2	Array Declarators
In a declaration T D where D has the form
D1 [constant-expressionopt]
  and the type of the identifier in the declaration T D1 is ``type-modifier T,'' the type of the identifier of D is ``type-modifier array of T.'' If the constant-expression is present, it must have integral type, and value greater than 0. If the constant expression specifying the bound is missing, the array has an incomplete type.
An array may be constructed from an arithmetic type, from a pointer, from a structure or union, or from another array (to generate a multi-dimensional array). Any type from which an array is constructed must be complete; it must not be an array of structure of incomplete type. This implies that for a multi-dimensional array, only the first dimension may be missing. The type of an object of incomplete aray type is completed by another, complete, declaration for the object (Par.A.10.2), or by initializing it (Par.A.8.7). For example,
 float fa[17], *afp[17]; declares an array of float numbers and an array of pointers to float numbers. Also, static int x3d[3][5][7]; declares a static three-dimensional array of integers, with rank 3 X 5 X 7. In complete detail, x3d is an array of three items: each item is an array of five arrays; each of the latter arrays is an array of seven integers. Any of the expressions x3d, x3d[i], x3d[i][j], x3d[i][j][k] may reasonably appear in an expression. The first three have type ``array,'', the last has type int. More specifically, x3d[i][j] is an array of 7 integers, and x3d[i] is an array of 5 arrays of 7 integers.
The array subscripting operation is defined so that E1[E2] is identical to *(E1+E2). Therefore, despite its asymmetric appearance, subscripting is a commutative operation. Because of the conversion rules that apply to + and to arrays (Pars.A6.6, A.7.1, A.7.7), if E1 is an array and E2 an integer, then E1[E2] refers to the E2-th member of E1.
In the example, x3d[i][j][k] is equivalent to *(x3d[i][j] + k). The first subexpression x3d[i][j] is converted by Par.A.7.1 to type ``pointer to array of integers,'' by Par.A.7.7, the addition involves multiplication by the size of an integer. It follows from the rules that arrays are stored by rows (last subscript varies fastest) and that the first subscript in the declaration helps determine the amount of storage consumed by an array, but plays no other part in subscript calculations.
A.8.6.3	Function Declarators
In a new-style function declaration T D where D has the form
D1 (parameter-type-list) and the type of the identifier in the declaration T D1 is ``type-modifier T,'' the type of the identifier of D is ``type-modifier function with arguments parameter-type-list returning T.''
The syntax of the parameters is parameter-type-list: parameter-list parameter-list , ... parameter-list: parameter-declaration parameter-list , parameter-declaration parameter-declaration: declaration-specifiers declarator declaration-specifiers abstract-declaratoropt
 
In the new-style declaration, the parameter list specifies the types of the parameters. As a special case, the declarator for a new-style function with no parameters has a parameter list consisting soley of the keyword void. If the parameter list ends with an ellipsis ``, ...'', then the function may accept more arguments than the number of parameters explicitly described, see Par.A.7.3.2.
The types of parameters that are arrays or functions are altered to pointers, in accordance with the rules for parameter conversions; see Par.A.10.1. The only storage class specifier permitted in a parameter's declaration is register, and this specifier is ignored unless the function declarator heads a function definition. Similarly, if the declarators in the parameter declarations contain identifiers and the function declarator does not head a function definition, the identifiers go out of scope immediately. Abstract declarators, which do not mention the identifiers, are discussed in Par.A.8.8.
In an old-style function declaration T D where D has the form
D1(identifier-listopt) and the type of the identifier in the declaration T D1 is ``type-modifier T,'' the type of the identifier of D is ``type-modifier function of unspecified arguments returning T.'' The parameters (if present) have the form identifier-list: identifier identifier-list , identifier
In the old-style declarator, the identifier list must be absent unless the declarator is used in the head of a function definition (Par.A.10.1). No information about the types of the parameters is supplied by the declaration.
For example, the declaration
 int f(), *fpi(), (*pfi)(); declares a function f returning an integer, a function fpi returning a pointer to an integer, and a pointer pfi to a function returning an integer. In none of these are the parameter types specified; they are old-style.
In the new-style declaration
 int strcpy(char *dest, const char *source), rand(void); strcpy is a function returning int, with two arguments, the first a character pointer, and the second a pointer to constant characters. The parameter names are effectively comments. The second function rand takes no arguments and returns int.
Function declarators with parameter prototypes are, by far, the most important language change introduced by the ANSI standard. They offer an advantage over the ``old-style'' declarators of the first edition by providing error-detection and coercion of arguments across function calls, but at a cost: turmoil and confusion during their introduction, and the necessity of accomodating both forms. Some syntactic ugliness was required for the sake of compatibility, namely void as an explicit marker of new-style functions without parameters.
The ellipsis notation ``, ...'' for variadic functions is also new, and, together with the macros in the standard header <stdarg.h>, formalizes a mechanism that was officially forbidden but unofficially condoned in the first edition.
These notations were adapted from the C++ language.
A.8.7	Initialization
 
When an object is declared, its init-declarator may specify an initial value for the identifier being declared. The initializer is preceded by =, and is either an expression, or a list of initializers nested in braces. A list may end with a comma, a nicety for neat formatting. initializer: assignment-expression
{ initializer-list }
{ initializer-list , } initializer-list: initializer initializer-list , initializer
All the expressions in the initializer for a static object or array must be constant expressions as described in Par.A.7.19. The expressions in the initializer for an auto or register object or array must likewise be constant expressions if the initializer is a brace-enclosed list. However, if the initializer for an automatic object is a single expression, it need not be a constant expression, but must merely have appropriate type for assignment to the object.
The first edition did not countenance initialization of automatic structures, unions, or arrays. The ANSI standard allows it, but only by constant constructions unless the initializer can be expressed by a simple expression.
A static object not explicitly initialized is initialized as if it (or its members) were assigned the constant 0. The initial value of an automatic object not explicitly intialized is undefined.
The initializer for a pointer or an object of arithmetic type is a single expression, perhaps in braces. The expression is assigned to the object.
The initializer for a structure is either an expression of the same type, or a brace-enclosed list of initializers for its members in order. Unnamed bit-field members are ignored, and are not initialized. If there are fewer initializers in the list than members of the structure, the trailing members are initialized with 0. There may not be more initializers than members. Unnamed bit-field members are ignored,and are not initialized.
The initializer for an array is a brace-enclosed list of initializers for its members. If the array has unknown size, the number of initializers determines the size of the array, and its type becomes complete. If the array has fixed size, the number of initializers may not exceed the number of members of the array; if there are fewer, the trailing members are initialized with 0.
As a special case, a character array may be initialized by a string literal; successive characters of the string initialize successive members of the array. Similarly, a wide character literal (Par.A.2.6) may initialize an array of type wchar_t. If the array has unknown size, the number of characters in the string, including the terminating null character, determines its size; if its size is fixed, the number of characters in the string, not counting the terminating null character, must not exceed the size of the array.
The initializer for a union is either a single expression of the same type, or a brace-enclosed initializer for the first member of the union.
The first edition did not allow initialization of unions. The ``first-member'' rule is clumsy, but is hard to generalize without new syntax. Besides allowing unions to be explicitly initialized in at least a primitive way, this ANSI rule makes definite the semantics of static unions not explicitly initialized.
An aggregate is a structure or array. If an aggregate contains members of aggregate type, the initialization rules apply recursively. Braces may be elided in the initialization as follows: if the initializer for an aggregate's member that itself is an aggregate begins with a left brace, then the succeding comma-separated list of initializers initializes the members of the subaggregate; it is erroneous for there to be more initializers than members. If, however, the initializer for a
  subaggregate does not begin with a left brace, then only enough elements from the list are taken into account for the members of the subaggregate; any remaining members are left to initialize the next member of the aggregate of which the subaggregate is a part.
For example,
 int x[] = { 1, 3, 5 }; declares and initializes x as a 1-dimensional array with three members, since no size was specified and there are three initializers. float y[4][3] = {
{ 1, 3, 5 },
{ 2, 4, 6 },
{ 3, 5, 7 },
}; is a completely-bracketed initialization: 1, 3 and 5 initialize the first row of the array y[0], namely y[0][0], y[0][1], and y[0][2]. Likewise the next two lines initialize y[1] and y[2]. The initializer ends early, and therefore the elements of y[3] are initialized with 0. Precisely the same effect could have been achieved by float y[4][3] = {
1, 3, 5, 2, 4, 6, 3, 5, 7
};
The initializer for y begins with a left brace, but that for y[0] does not; therefore three elements from the list are used. Likewise the next three are taken successively for y[1] and for y[2]. Also, float y[4][3] = {
{ 1 }, { 2 }, { 3 }, { 4 }
}; initializes the first column of y (regarded as a two-dimensional array) and leaves the rest 0. Finally, char msg[] = "Syntax error on line %s\n"; shows a character array whose members are initialized with a string; its size includes the terminating null character.
A.8.8	Type names
In several contexts (to specify type conversions explicitly with a cast, to declare parameter types in function declarators, and as argument of sizeof) it is necessary to supply the name of a data type. This is accomplished using a type name, which is syntactically a declaration for an object of that type omitting the name of the object. type-name: specifier-qualifier-list abstract-declaratoropt abstract-declarator: pointer pointeropt direct-abstract-declarator direct-abstract-declarator:
( abstract-declarator ) direct-abstract-declaratoropt [constant-expressionopt] direct-abstract-declaratoropt (parameter-type-listopt)
 
It is possible to identify uniquely the location in the abstract-declarator where the identifier would appear if the construction were a declarator in a declaration. The named type is then the same as the type of the hypothetical identifier. For example,
 int int * int *[3] int (*)[] int *() int (*[])(void) name respectively the types ``integer,'' ``pointer to integer,'' ``array of 3 pointers to integers,''
``pointer to an unspecified number of integers,'' ``function of unspecified parameters returning pointer to integer,'' and ``array, of unspecified size, of pointers to functions with no parameters each returning an integer.''
A.8.9	Typedef
Declarations whose storage class specifier is typedef do not declare objects; instead they define identifiers that name types. These identifiers are called typedef names. typedef-name: identifier
A typedef declaration attributes a type to each name among its declarators in the usual way (see Par.A.8.6). Thereafter, each such typedef name is syntactically equivalent to a type specifier keyword for the associated type.
For example, after
 typedef long Blockno, *Blockptr; typedef struct { double r, theta; } Complex; the constructions
Blockno b; extern Blockptr bp; Complex z, *zp; are legal declarations. The type of b is long, that of bp is ``pointer to long,'' and that of z is the specified structure; zp is a pointer to such a structure. typedef does not introduce new types, only synonyms for types that could be specified in another way. In the example, b has the same type as any long object.
Typedef names may be redeclared in an inner scope, but a non-empty set of type specifiers must be given. For example,
 extern Blockno; does not redeclare Blockno, but extern int Blockno; does.
A.8.10	Type Equivalence
Two type specifier lists are equivalent if they contain the same set of type specifiers, taking into account that some specifiers can be implied by others (for example, long alone implies long int). Structures, unions, and enumerations with different tags are distinct, and a tagless union, structure, or enumeration specifies a unique type.
 
Two types are the same if their abstract declarators (Par.A.8.8), after expanding any typedef types, and deleting any function parameter specifiers, are the same up to the equivalence of type specifier lists. Array sizes and function parameter types are significant.