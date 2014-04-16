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

new Point2D
dup
invokespecial Point2D/<init>()V
astore 54
new Point2D
dup
invokespecial Point2D/<init>()V
astore 55
new Point2D
dup
invokespecial Point2D/<init>()V
astore 56
aload 54
ldc 1
putfield Point2D/x I
iconst_1
pop
aload 54
ldc 2
putfield Point2D/y I
iconst_1
pop
aload 54
ldc 97
putfield Point2D/id I
iconst_1
pop
aload 55
ldc 2
putfield Point2D/x I
iconst_1
pop
aload 55
ldc 3
putfield Point2D/y I
iconst_1
pop
aload 55
ldc 98
putfield Point2D/id I
iconst_1
pop
aload 56
aload 54
getfield Point2D/x I
aload 55
getfield Point2D/x I
isub
putfield Point2D/x I
iconst_1
pop
aload 56
aload 54
getfield Point2D/y I
aload 55
getfield Point2D/y I
isub
putfield Point2D/y I
iconst_1
pop
aload 56
ldc 99
putfield Point2D/id I
iconst_1
pop
aload 56
getfield Point2D/x I
istore 57
iconst_1
pop
aload 56
getfield Point2D/y I
istore 58
iconst_1
pop
aload 56
getfield Point2D/id I
istore 59
iconst_1
pop
iload 57
	getstatic java/lang/System/out Ljava/io/PrintStream;
    		astore 250
    		invokestatic java/lang/String/valueOf(I)Ljava/lang/String;
    		astore 251
    		aload 250
    		aload 251
    		invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V 
iload 58
	getstatic java/lang/System/out Ljava/io/PrintStream;
    		astore 250
    		invokestatic java/lang/String/valueOf(I)Ljava/lang/String;
    		astore 251
    		aload 250
    		aload 251
    		invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V 
iload 59
	getstatic java/lang/System/out Ljava/io/PrintStream;
    		astore 250
    		invokestatic java/lang/String/valueOf(C)Ljava/lang/String;
    		astore 251
    		aload 250
    		aload 251
    		invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V 
return
.end method
