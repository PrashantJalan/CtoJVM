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
istore 0
ldc 0
istore 1
ldc 0
istore 2
ldc 0
istore 0
label7:
iload 0
ldc 10
if_icmple label1
iconst_0
goto label2
label1:
iconst_1
label2:
ifeq label8
iload 0
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
iload 1
ldc 1
iadd
istore 1
goto label6
label5:
iload 2
ldc 1
iadd
istore 2
label6:
iload 0
ldc 1
iadd
istore 0
goto label7
label8:
iload 1
	getstatic java/lang/System/out Ljava/io/PrintStream;
    		astore 20
    		invokestatic java/lang/String/valueOf(I)Ljava/lang/String;
    		astore 30
    		aload 20
    		aload 30
    		invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V 
iload 2
	getstatic java/lang/System/out Ljava/io/PrintStream;
    		astore 20
    		invokestatic java/lang/String/valueOf(I)Ljava/lang/String;
    		astore 30
    		aload 20
    		aload 30
    		invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V 
return
.end method
