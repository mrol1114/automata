def PROGRAM():
    return PROG() and ID() and VAR()

def PROG():
    global s
    temp_s = s[0]
    s = s[1:]

    return temp_s == 'PROG'

def ID():
    global s
    temp_s = s[0]
    s = s[1:]

    return temp_s == 'a' or temp_s == 'b'

def VAR():
    global s
    temp_s = s[0]
    s = s[1:]
    return temp_s == 'VAR' and IDLIST()

def BEGIN():
    global s
    temp_s = s[0]
    s = s[1:]
    return temp_s == 'BEGIN'

def END():
    global s
    temp_s = s[0]
    s = s[1:]
    return temp_s == 'END.'

def COMMA():
    global s
    temp_s = s[0]
    s = s[1:]
    return temp_s == ','

def IDLIST():
    global s
    temp_s = s[0]
    s = s[1:]
    print(temp_s, temp_s in 'ab')
    return (temp_s in 'ab') and E()

def E():
    global s
    temp_s = s[0]
    s = s[1:]
    return temp_s == ',' and IDLIST() or temp_s == 'BEGIN' and STMS()

def STMS():
    global s
    temp_s = s[0]
    s = s[1:]
    return temp_s == 'st' and B()

def B():
    global s
    temp_s = s[0]
    s = s[1:]
    return temp_s == 'END.' or temp_s == ';' and STMS()

def ST():
    global s
    temp_s = s[0]
    s = s[1:]
    return temp_s == 'st'


s = 'PROG a VAR aa BEGIN st  END.'.split()
print(s)
if (PROGRAM()): print('OK')
else: print('NOT OK')
