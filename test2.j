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

ldc 1
istore 50
iload 50
ifeq label1
iconst_0
goto label2
label1:
iconst_1
label2:
ifeq label3
ldc 0
istore 51
iconst_1
pop
goto label4
label3:
ldc 1
istore 51
iconst_1
pop
label4:
iload 51
	getstatic java/lang/System/out Ljava/io/PrintStream;
    		astore 250
    		invokestatic java/lang/String/valueOf(I)Ljava/lang/String;
    		astore 251
    		aload 250
    		aload 251
    		invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V 
return
.end method
