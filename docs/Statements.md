A.9	Statements
Except as described, statements are executed in sequence. Statements are executed for their effect, and do not have values. They fall into several groups. statement: labeled-statement expression-statement compound-statement selection-statement iteration-statement jump-statement
A.9.1	Labeled Statements
Statements may carry label prefixes. labeled-statement: identifier : statement case constant-expression : statement default : statement
A label consisting of an identifier declares the identifier. The only use of an identifier label is as a target of goto. The scope of the identifier is the current function. Because labels have their own name space, they do not interfere with other identifiers and cannot be redeclared. See Par.A.11.1.
Case labels and default labels are used with the switch statement (Par.A.9.4). The constant expression of case must have integral type.
Labels themselves do not alter the flow of control.
A.9.2	Expression Statement
Most statements are expression statements, which have the form expression-statement: expressionopt;
Most expression statements are assignments or function calls. All side effects from the expression are completed before the next statement is executed. If the expression is missing, the construction is called a null statement; it is often used to supply an empty body to an iteration statement to place a label.
A.9.3	Compound Statement
So that several statements can be used where one is expected, the compound statement (also called ``block'') is provided. The body of a function definition is a compound statement. compound-statement:
{ declaration-listopt statement-listopt } declaration-list: declaration declaration-list declaration
  statement-list: statement statement-list statement
If an identifier in the declaration-list was in scope outside the block, the outer declaration is suspended within the block (see Par.A.11.1), after which it resumes its force. An identifier may be declared only once in the same block. These rules apply to identifiers in the same name space (Par.A.11); identifiers in different name spaces are treated as distinct.
Initialization of automatic objects is performed each time the block is entered at the top, and proceeds in the order of the declarators. If a jump into the block is executed, these initializations are not performed. Initialization of static objects are performed only once, before the program begins execution.
A.9.4	Selection Statements
Selection statements choose one of several flows of control. selection-statement: if (expression) statement if (expression) statement else statement switch (expression) statement
In both forms of the if statement, the expression, which must have arithmetic or pointer type, is evaluated, including all side effects, and if it compares unequal to 0, the first substatement is executed. In the second form, the second substatement is executed if the expression is 0. The else ambiguity is resolved by connecting an else with the last encountered else-less if at the same block nesting level.
The switch statement causes control to be transferred to one of several statements depending on the value of an expression, which must have integral type. The substatement controlled by a switch is typically compound. Any statement within the substatement may be labeled with one or more case labels (Par.A.9.1). The controlling expression undergoes integral promotion (Par.A.6.1), and the case constants are converted to the promoted type. No two of these case constants associated with the same switch may have the same value after conversion. There may also be at most one default label associated with a switch. Switches may be nested; a case or default label is associated with the smallest switch that contains it.
When the switch statement is executed, its expression is evaluated, including all side effects, and compared with each case constant. If one of the case constants is equal to the value of the expression, control passes to the statement of the matched case label. If no case constant matches the expression, and if there is a default label, control passes to the labeled statement. If no case matches, and if there is no default, then none of the substatements of the swtich is executed.
In the first edition of this book, the controlling expression of switch, and the case constants, were required to have int type.
A.9.5	Iteration Statements
Iteration statements specify looping. iteration-statement: while (expression) statement do statement while (expression); for (expressionopt; expressionopt; expressionopt) statement
 
In the while and do statements, the substatement is executed repeatedly so long as the value of the expression remains unequal to 0; the expression must have arithmetic or pointer type. With while, the test, including all side effects from the expression, occurs before each execution of the statement; with do, the test follows each iteration.
In the for statement, the first expression is evaluated once, and thus specifies initialization for the loop. There is no restriction on its type. The second expression must have arithmetic or pointer type; it is evaluated before each iteration, and if it becomes equal to 0, the for is terminated. The third expression is evaluated after each iteration, and thus specifies a re-initialization for the loop. There is no restriction on its type. Side-effects from each expression are completed immediately after its evaluation. If the substatement does not contain continue, a statement for (expression1; expression2; expression3) statement is equivalent to
 expression1; while (expression2) { statement expression3;
}
Any of the three expressions may be dropped. A missing second expression makes the implied test equivalent to testing a non-zero element.
A.9.6	Jump statements
Jump statements transfer control unconditionally. jump-statement: goto identifier; continue; break; return expressionopt;
In the goto statement, the identifier must be a label (Par.A.9.1) located in the current function. Control transfers to the labeled statement.
A continue statement may appear only within an iteration statement. It causes control to pass to the loop-continuation portion of the smallest enclosing such statement. More precisely, within each of the statements
 while (...)
...	{	do {
...	for (...) {
... contin: ;	contin:	;	contin: ;
}	} while	(...);	} a continue not contained in a smaller iteration statement is the same as goto contin.
A break statement may appear only in an iteration statement or a switch statement, and terminates execution of the smallest enclosing such statement; control passes to the statement following the terminated statement.
A function returns to its caller by the return statement. When return is followed by an expression, the value is returned to the caller of the function. The expression is converted, as by assignment, to the type returned by the function in which it appears.
Flowing off the end of a function is equivalent to a return with no expression. In either case, the returned value is undefined.