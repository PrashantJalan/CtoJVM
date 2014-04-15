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

ldc 0
istore 50
iconst_1
pop
ldc 0
istore 51
iconst_1
pop
ldc 0
istore 52
iconst_1
pop
ldc 0
istore 50
iconst_1
pop
label5:
iload 50
ldc 10
if_icmple label1
iconst_0
goto label2
label1:
iconst_1
label2:
ifeq label6
ldc 2
istore 52
iconst_1
ifeq label3
iload 51
ldc 1
iadd
istore 51
iconst_1
pop
goto label4
label3:
iload 52
ldc 1
iadd
istore 52
iconst_1
pop
label4:
iconst_1
iload 50
iadd
istore 50
iload 50
pop
goto label5
label6:
iload 51
	getstatic java/lang/System/out Ljava/io/PrintStream;
    		astore 250
    		invokestatic java/lang/String/valueOf(I)Ljava/lang/String;
    		astore 251
    		aload 250
    		aload 251
    		invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V 
iload 52
	getstatic java/lang/System/out Ljava/io/PrintStream;
    		astore 250
    		invokestatic java/lang/String/valueOf(I)Ljava/lang/String;
    		astore 251
    		aload 250
    		aload 251
    		invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V 
return
return
.end method
