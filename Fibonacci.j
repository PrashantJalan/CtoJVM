.class public Fibonacci
.super java/lang/Object
	.method public <init>()V
   			aload_0
   			invokenonvirtual java/lang/Object/<init>()V
   			return
			.end method 
.method public static fib(I)I
.limit locals 255
.limit stack 255

iload 0
istore 52
iload 52
ldc 0
if_icmpeq label1
iconst_0
goto label2
label1:
iconst_1
label2:
ifeq label8
ldc 0
istore 55
goto label9
label8:
iload 52
ldc 1
if_icmpeq label3
iconst_0
goto label4
label3:
iconst_1
label4:
ifeq label6
ldc 1
istore 55
goto label7
label6:
iload 52
ldc 1
isub
istore 56
iload 52
ldc 2
isub
istore 57
iload 56
invokestatic Fibonacci/fib(I)I
istore 53
iload 57
invokestatic Fibonacci/fib(I)I
istore 54
iload 53
iload 54
iadd
istore 55
label7:
label9:
iload 55
ireturn
.end method
.method public static main([Ljava/lang/String;)V
.limit locals 255
.limit stack 255

ldc 7
invokestatic Fibonacci/fib(I)I
istore 58
iload 58
	getstatic java/lang/System/out Ljava/io/PrintStream;
    		astore 250
    		invokestatic java/lang/String/valueOf(I)Ljava/lang/String;
    		astore 251
    		aload 250
    		aload 251
    		invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V 
return
.end method
