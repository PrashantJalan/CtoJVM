.class public BubbleSort
.super java/lang/Object
	.method public <init>()V
   			aload_0
   			invokenonvirtual java/lang/Object/<init>()V
   			return
			.end method 
.method public static main([Ljava/lang/String;)V
.limit locals 255
.limit stack 255

ldc 10
newarray int
astore 52
ldc 0
istore 50
iconst_1
pop
label3:
iload 50
ldc 10
if_icmplt label1
iconst_0
goto label2
label1:
iconst_1
label2:
ifeq label4
aload 52
iload 50
ldc 10
iload 50
isub
iastore
iconst_1
pop
iconst_1
iload 50
iadd
istore 50
iload 50
pop
goto label3
label4:
ldc 0
istore 50
iconst_1
pop
label16:
iload 50
ldc 10
if_icmplt label6
iconst_0
goto label7
label6:
iconst_1
label7:
ifeq label17
ldc 0
istore 51
iconst_1
pop
label13:
iload 51
ldc 10
iload 50
isub
ldc 1
isub
if_icmplt label8
iconst_0
goto label9
label8:
iconst_1
label9:
ifeq label14
aload 52
iload 51
iaload
aload 52
iload 51
ldc 1
iadd
iaload
if_icmpgt label10
iconst_0
goto label11
label10:
iconst_1
label11:
ifeq label12
aload 52
iload 51
iaload
istore 53
iconst_1
pop
aload 52
iload 51
aload 52
iload 51
ldc 1
iadd
iaload
iastore
iconst_1
pop
aload 52
iload 51
ldc 1
iadd
iload 53
iastore
iconst_1
pop
label12:
iconst_1
iload 51
iadd
istore 51
iload 51
pop
goto label13
label14:
iconst_1
iload 50
iadd
istore 50
iload 50
pop
goto label16
label17:
ldc 0
istore 50
iconst_1
pop
label21:
iload 50
ldc 10
if_icmplt label19
iconst_0
goto label20
label19:
iconst_1
label20:
ifeq label22
aload 52
iload 50
iaload
istore 51
iconst_1
pop
iload 51
	getstatic java/lang/System/out Ljava/io/PrintStream;
    		astore 250
    		invokestatic java/lang/String/valueOf(I)Ljava/lang/String;
    		astore 251
    		aload 250
    		aload 251
    		invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V 
iconst_1
iload 50
iadd
istore 50
iload 50
pop
goto label21
label22:
return
.end method
