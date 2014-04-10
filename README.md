CAVA
======

A compiler for running a C code on Java virtual machine. Just use the command 

python parser.py source-file.c

to produce the Java executable class file which can run by using

java source-file

This program compiles a C program into Java byte code (the .j file) and uses the Java assembler Jasmine to convert the bytecode into an executable Java class file.

Dependency:
PLY module for python
Jasmine

Dependency if debugging:
pydot module for python

Salient features:
Proper error handling for undeclared, redeclared and out of scope variables using Symbol Table.
Error handling for out of scope break or continue and array index length mismatch.
Type checking.
Short circuiting for evaluating control flow statements.
Backpatching for break and continue statements.
Handling postfix expressions (a=3; b=a++; then b=3 not 4).
Can represent the AST and Symbol table graphically (use DEBUG mode).

Supports comments.
Limitations:
Doesn't support any header files in C.
Doesn't support pointer.
Doesn't support struct.
Doesn't support function declaration.
