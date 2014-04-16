.class public test2
.super java/lang/Object
	.method public <init>()V
   			aload_0
   			invokenonvirtual java/lang/Object/<init>()V
   			return
			.end method 
.method public static main([Ljava/lang/String;)V
.limit locals 255
.limit stack 255

iconst_0
ifeq label1
ldc 1
istore 50
iconst_1
pop
goto label2
label1:
ldc 0
istore 50
iconst_1
pop
label2:
iload 50
	getstatic java/lang/System/out Ljava/io/PrintStream;
    		astore 250
    		invokestatic java/lang/String/valueOf(I)Ljava/lang/String;
    		astore 251
    		aload 250
    		aload 251
    		invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V 
return
.end method
