.class public test2
.super java/lang/Object
	.method public <init>()V
   			aload_0
   			invokenonvirtual java/lang/Object/<init>()V
   			return
			.end method 
.method public static foo(II)V
.limit locals 255
.limit stack 255

iload 0
istore 50
iload 1
istore 51
iload 50
iload 51
isub
istore 52
iload 52
	getstatic java/lang/System/out Ljava/io/PrintStream;
    		astore 250
    		invokestatic java/lang/String/valueOf(I)Ljava/lang/String;
    		astore 251
    		aload 250
    		aload 251
    		invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V 
return
.end method
.method public static main([Ljava/lang/String;)V
.limit locals 255
.limit stack 255

ldc 3
istore 56
ldc 4
istore 56
ldc 5
iload 56
invokestatic test2/foo(II)V
return
.end method
