.class public test2
.super java/lang/Object
	.method public <init>()V
   			aload_0
   			invokenonvirtual java/lang/Object/<init>()V
   			return
			.end method 
.method public static foo([II)V
.limit locals 255
.limit stack 255

aload 0
astore 50
iload 1
istore 51
aload 50
ldc 9
iload 51
iastore
iconst_1
pop
ldc 2
istore 52
ldc 2.2
fstore 55
ldc 2.5
fstore 53
iconst_1
pop
ldc 2
istore 56
iload 56
i2f
fload 53
fmul
fload 55
fadd
fstore 54
iconst_1
pop
aload 50
ldc 9
iaload
istore 57
fload 54
	getstatic java/lang/System/out Ljava/io/PrintStream;
    		astore 250
    		invokestatic java/lang/String/valueOf(F)Ljava/lang/String;
    		astore 251
    		aload 250
    		aload 251
    		invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V 
return
.end method
.method public static main([Ljava/lang/String;)V
.limit locals 255
.limit stack 255

ldc 10
newarray int
astore 59
aload 59
ldc 5
ldc 6
imul
ldc 3
idiv
invokestatic test2/foo([II)V
iconst_1
pop
return
.end method
