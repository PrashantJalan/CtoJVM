.class public test3
.super java/lang/Object
.field static count I

	.method public <init>()V
   			aload_0
   			invokenonvirtual java/lang/Object/<init>()V
   			return
			.end method 

.method public static foo()V
.limit locals 255
.limit stack 255

getstatic test3/count I
ldc 2
iadd
putstatic test3/count I
iconst_1
pop
getstatic test3/count I
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

ldc 0
istore 52
iconst_1
pop
label3:
iload 52
ldc 5
if_icmplt label1
iconst_0
goto label2
label1:
iconst_1
label2:
ifeq label4
invokestatic test3/foo()V
iconst_1
pop
iload 52
ldc 1
iadd
istore 52
iconst_1
pop
goto label3
label4:
return
.end method
