; --- Copyright Jonathan Meyer 1996. All rights reserved. -----------------
; File:      jasmin/examples/Count.j
; Author:    Jonathan Meyer, 10 July 1996
; Purpose:   Counts from 0 to 9, printing out the value
; -------------------------------------------------------------------------

.class public examples/Test
.super java/lang/Object

;
; standard initializer
.method public <init>()V
   aload_0
   invokenonvirtual java/lang/Object/<init>()V
   return
.end method

.method public static main([Ljava/lang/String;)V

    .limit locals 4
    .limit stack 3

    bipush  9
    istore_1
    bipush  10
    istore_2
    iload_1
    iload_2
    iadd
    istore_1
    iload_1

    ; will print the Integer in stack
    getstatic java/lang/System/out Ljava/io/PrintStream;
    astore_1
    invokestatic java/lang/String/valueOf(I)Ljava/lang/String;
    astore_3
    aload_1
    aload_3
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V

    return

.end method
