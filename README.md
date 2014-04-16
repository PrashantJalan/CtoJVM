C To JVM
======

A compiler for running a C code on Java virtual machine. Just use the command 

python parser.py source-file.c

to produce the Java executable class file which can run by using

java source-file

This program compiles a C program into Java byte code (the .j file) and uses the Java assembler Jasmine to convert the bytecode into an executable Java class file.

<b>Dependency</b>:
<br>PLY module for python
<br>Jasmine

<b>Dependency if debugging</b>:
<br>pydot module for python

<b>Salient features</b>:
<br>Proper error handling for undeclared, redeclared and out of scope variables using Symbol Table.
<br>Error handling for out of scope break or continue and array index length mismatch.
<br>Type checking.
<br>Short circuiting for evaluating control flow statements.
<br>Backpatching for break and continue statements.
<br>Handling postfix expressions (a=3; b=a++; then b=3 not 4).
<br>Can represent the AST and Symbol table graphically (use DEBUG mode).
<br>Supports comments.

<b>Limitations</b>:
<br>Works only for INT, FLOAT and CHAR for now.
<br>Doesn't support any header files in C.
<br>Doesn't support pointer.
