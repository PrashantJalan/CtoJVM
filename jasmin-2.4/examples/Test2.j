; --- Copyright Jonathan Meyer 1996. All rights reserved. -----------------
; File:      jasmin/examples/Count.j
; Author:    Jonathan Meyer, 10 July 1996
; Purpose:   Counts from 0 to 9, printing out the value
; -------------------------------------------------------------------------

.class public examples/Test2
.super java/lang/Object

;
; standard initializer
.method public <init>()V
   aload_0
   invokenonvirtual java/lang/Object/<init>()V
   return
.end method

.method public static foo(II)V
   .limit locals 255
   .limit stack 255
    iload_0
    iload_1
    iadd
    getstatic java/lang/System/out Ljava/io/PrintStream;
            astore 20
            invokestatic java/lang/String/valueOf(I)Ljava/lang/String;
            astore 30
            aload 20
            aload 30
            invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V 
    return

.end method

.method public static main([Ljava/lang/String;)V

    .limit locals 255
    .limit stack 255
    bipush 5
    bipush 3
    ;istore_1
    ;iload_1
    ; bipush 6
    invokestatic examples/Test2/foo(II)V
    return

.end method
