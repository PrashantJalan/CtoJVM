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

       ; set limits used by this method
       .limit locals 4
       .limit stack 3

       ; setup local variables:

       ;    1 - the PrintStream object held in java.lang.System.out
       getstatic java/lang/System/out Ljava/io/PrintStream;
           astore_1

        bipush  9
        istore_3
        bipush  10
        istore_2
        iload_2
        iload_3
        iadd
        ; istore_1
        invokestatic java/lang/String/valueOf(I)Ljava/lang/String;
       astore_3
       ; ... and print it
       aload_1    ; push the PrintStream object
       aload_3    ; push the string we just created - then ...
       invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V

       return

.end method
