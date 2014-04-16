.class public test
.super java/lang/Object
	.method public <init>()V
   			aload_0
   			invokenonvirtual java/lang/Object/<init>()V
   			return
			.end method 
.method public static foo([F)F
.limit locals 255
.limit stack 255

aload 0
astore 50
aload 50
ldc 9
ldc 56.2343
fastore
iconst_1
pop
aload 50
ldc 9
faload
freturn
.end method
.method public static main([Ljava/lang/String;)V
.limit locals 255
.limit stack 255

ldc 10
newarray float
astore 52
aload 52
invokestatic test/foo([F)F
fstore 53
fload 53
	getstatic java/lang/System/out Ljava/io/PrintStream;
    		astore 250
    		invokestatic java/lang/String/valueOf(F)Ljava/lang/String;
    		astore 251
    		aload 250
    		aload 251
    		invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V 
return
.end method
