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
aload 50
ldc 9
iaload
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

ldc 10
newarray int
astore 54
aload 54
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
