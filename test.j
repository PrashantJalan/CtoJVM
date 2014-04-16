.class public test
.super java/lang/Object

	.method public <init>()V
   			aload_0
   			invokenonvirtual java/lang/Object/<init>()V
   			return
			.end method 

.method public static main([Ljava/lang/String;)V
.limit locals 255
.limit stack 255

new z
dup
invokespecial z/<init>()V
astore 54
aload 54
ldc 5
putfield z/b I
iconst_1
pop
aload 54
getfield z/b I
istore 55
iconst_1
pop
iload 55
	getstatic java/lang/System/out Ljava/io/PrintStream;
    		astore 250
    		invokestatic java/lang/String/valueOf(I)Ljava/lang/String;
    		astore 251
    		aload 250
    		aload 251
    		invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V 
return
.end method
