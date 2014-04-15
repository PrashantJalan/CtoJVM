.class public test
.super java/lang/Object
	.method public <init>()V
   			aload_0
   			invokenonvirtual java/lang/Object/<init>()V
   			return
			.end method 
.method public static f02()V
.limit locals 255
.limit stack 255

.end method
.method public static foo(II)I
.limit locals 255
.limit stack 255

.end method
.method public static main([Ljava/lang/String;)I
.limit locals 255
.limit stack 255

ldc 0
istore 5
ldc 0
istore 6
ldc 0
istore 7
ldc 0
istore 5
label7:
iload 5
ldc 10
if_icmple label1
iconst_0
goto label2
label1:
iconst_1
label2:
ifeq label8
iload 5
ldc 2
irem
ldc 0
if_icmpeq label3
iconst_0
goto label4
label3:
iconst_1
label4:
ifeq label5
iload 6
ldc 1
iadd
istore 6
goto label6
label5:
iload 7
ldc 1
iadd
istore 7
label6:
iload 5
ldc 1
iadd
istore 5
goto label7
label8:
iload 6
	getstatic java/lang/System/out Ljava/io/PrintStream;
    		astore 20
    		invokestatic java/lang/String/valueOf(I)Ljava/lang/String;
    		astore 30
    		aload 20
    		aload 30
    		invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V 
iload 7
	getstatic java/lang/System/out Ljava/io/PrintStream;
    		astore 20
    		invokestatic java/lang/String/valueOf(I)Ljava/lang/String;
    		astore 30
    		aload 20
    		aload 30
    		invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V 
return
.end method
