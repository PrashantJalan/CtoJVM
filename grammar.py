f=open('grammar.txt','r')
# constant nonterminal, TYPE_NAME REMOVE, 
tokens=['IDENTIFIER', 'CONSTANT', 'STRING_LITERAL' 'SIZEOF', 'PTR_OP', 'INC_OP', 'DEC_OP', 'LEFT_OP', 'RIGHT_OP', 'LE_OP', 'GE_OP', 'EQ_OP', 'NE_OP', 'AND_OP', 'OR_OP', 'MUL_ASSIGN', 'DIV_ASSIGN', 'MOD_ASSIGN', 'ADD_ASSIGN', 'SUB_ASSIGN', 'LEFT_ASSIGN', 'RIGHT_ASSIGN', 'AND_ASSIGN', 'XOR_ASSIGN', 'OR_ASSIGN', 'TYPEDEF', 'EXTERN', 'STATIC', 'AUTO', 'REGISTER', 'CHAR', 'SHORT', 'INT', 'LONG', 'SIGNED', 'UNSIGNED', 'FLOAT', 'DOUBLE', 'CONST', 'VOLATILE', 'VOID', 'STRUCT', 'UNION', 'ENUM', 'ELLIPSIS', 'CASE', 'DEFAULT', 'IF', 'ELSE', 'SWITCH', 'WHILE', 'DO', 'FOR', 'GOTO', 'CONTINUE', 'BREAK', 'RETURN']
token2=['{', '(', '}' , ')', '[', ']', '.', ',', '%', '&', '!', '+', '-', '*', '/', '~', '#', '<', '>', '<=', '=', '>=', '+=', '-=', '^', '|', '?', ':', ';']
tokenrep = ['IDENTIFIER', 'CONSTANT', 'STRING' 'SIZEOF', 'PTR_OP', 'INC_OP', 'DEC_OP', 'LEFT_OP', 'RIGHT_OP', 'LE_OP', 'GE_OP', 'EQ_OP', 'NE_OP', 'AND_OP', 'OR_OP', 'MUL_ASSIGN', 'DIV_ASSIGN', 'MOD_ASSIGN', 'ADD_ASSIGN', 'SUB_ASSIGN', 'LEFT_ASSIGN', 'RIGHT_ASSIGN', 'AND_ASSIGN', 'XOR_ASSIGN', 'OR_ASSIGN', 'TYPEDEF', 'EXTERN', 'STATIC', 'AUTO', 'REGISTER', 'CHAR', 'SHORT', 'INT', 'LONG', 'SIGNED', 'UNSIGNED', 'FLOAT', 'DOUBLE', 'CONST', 'VOLATILE', 'VOID', 'STRUCT', 'UNION', 'ENUM', 'ELLIPSIS', 'CASE', 'DEFAULT', 'IF', 'ELSE', 'SWITCH', 'WHILE', 'DO', 'FOR', 'GOTO', 'CONTINUE', 'BREAK', 'RETURN']
token2rep=['LEFT_CURL','LEFT_ROUND','RIGHT_CURL','RIGHT_ROUND','LEFT_SQUARE','RIGHT_SQUARE','DOT','COMMA','MODULO','AMPERSAND','EXCLAMATION','PLUS','MINUS','MULTIPLY','DIVIDE','TILDA','HASH','L_OP','G_OP','LE_OP','EQUAL','GE_OP','ADD_ASSIGN','SUB_ASSIGN','POWER','PIPE','QUESTION','COLON','SEMICOLON']
#for line in f.readline():

lines = f.readlines();
k=-1;
while k < len(lines):
    k=k+1;
#for k in range(0,len(lines)):
    #print lines[k]
    #print k;
    if(lines[k].strip() == ';'):
        flag=1;
        k=k+1;
        #print "yes";
        continue;
    x = lines[k].strip();
    i=1
    k=k+1
    func = 'def p_'+x+'_'+str(i)+'(t):\n\t\''+x+' : '
    y= lines[k].strip();
    #func=func+ y[1:]+'\'\n\tt[0]=Node(\''+x+'\', ['
    list1 = y[1:].split()
    for j in range(0,len(list1)):
        if(list1[j][1:-1] in token2):
            index= token2.index(list1[j][1:-1])
            func = func + token2rep[index] + ' ' 
        else:
            func=func+ list1[j]+' '
    func= func[:-1] +'\'\n\tt[0]=Node(\''+x+'\', ['
    #print"LIST1", list1
    for j in range(0,len(list1)):
        if(list1[j][0]== '\'' or list1[j] in tokens):
            func=func+'Node(t['+str(j+1)+'], []),'
        else:
            func=func+'t['+str(j+1)+'],'
    func=func[:-1]+'])'
    print func
    while(flag):
        if(lines[k].strip() == ';'):
            flag=0;
            k=k-1;
            #print "yes";
            break;
        i=i+1
        k=k+1
        func = 'def p_'+x+'_'+str(i)+'(t):\n\t\''+x+' : '
        y= lines[k].strip();
        if y != ';':
            list1=y[1:].split()
            for j in range(0,len(list1)):
                if(list1[j][1:-1] in token2):
                    index= token2.index(list1[j][1:-1])
                    func = func+ token2rep[index]+' ' 
                else:
                    func=func+ list1[j]+' '
            func= func[:-1] +'\'\n\tt[0]=Node(\''+x+'\', ['
            for j in range(0,len(list1)):
                if(list1[j][0]== '\'' or list1[j] in tokens):
                    func=func+'Node(t['+str(j+1)+'], []),'
                else:
                    func=func+'t['+str(j+1)+'],'
            func=func[:-1]+'])'
            print func
        
        
    
