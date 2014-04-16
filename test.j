.class public test
.super java/lang/Object
	.method public <init>()V
   			aload_0
   			invokenonvirtual java/lang/Object/<init>()V
   			return
			.end method 
.method public static foo([I)F
.limit locals 255
.limit stack 255

aload 0
astore 50
aload 50
ldc 9
ldc 56
iastore
iconst_1
pop
aload 50
ldc 9
iaload
istore 51
ldc 8.994
fstore 52
fload 52
	getstatic java/lang/System/out Ljava/io/PrintStream;
    		astore 250
    		invokestatic java/lang/String/valueOf(F)Ljava/lang/String;
    		astore 251
    		aload 250
    		aload 251
    		invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V 
fload 52
freturn
.end method
.method public static main([Ljava/lang/String;)V
.limit locals 255
.limit stack 255

ldc 10
newarray int
astore 54
aload 54
invokestatic test/foo([I)F
fstore 55
fload 55
	getstatic java/lang/System/out Ljava/io/PrintStream;
    		astore 250
    		invokestatic java/lang/String/valueOf(F)Ljava/lang/String;
    		astore 251
    		aload 250
    		aload 251
    		invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V 
return
.end method
