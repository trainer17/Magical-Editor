

#Toma un action replay code y me dice que hace
#1XXXXXXX ????YYYY
def readCheat(s):

    opcode = s[0]

    if opcode == '0':
        VAL = s[9:]
        ADDR = s[1:8] + '(0xOFFSET)'
        exp = 'WRITE ' +VAL +' to address 0x' + ADDR + ' (32bit)'

    if opcode == '1':
        VAL = s[-4:]
        ADDR = s[1:8] + '(0xOFFSET)'
        exp = 'WRITE ' +VAL +' to address 0x' + ADDR + ' (16bit)'

    if opcode == '2':
        VAL = s[-2:]
        ADDR = s[1:8] + '(0xOFFSET)'
        exp = 'WRITE ' +VAL +' to address 0x' + ADDR + ' (8bit)'


    if opcode == '9':

        MASK = s[9:13]
        VAL  = s[-4:]
        ADDR = s[1:8]
        if(ADDR=='00000000'): ADDR = 'OFFSET'
        exp = 'IF ( [0x' + ADDR +'] && 0x'+ MASK +' ) == 0x'+VAL+ ' THEN:'

    if opcode == 'C':

        N = s[9:]
        exp = 'REPEAT '+  N +' TIMES'


    if opcode == 'D':
        if s[1] == '0': exp = 'END IF'
        if s[1] == '1': exp = 'END WHILE'
        if s[1] == '2': exp = 'END WHILE, OFFSET <-- 0x00'

        if s[1] == '3':
            VAL = s[9:]
            exp = 'SET OFFSET = 0x' + VAL

        if s[1] == 'C':
            VAL = s[9:]
            exp = 'ADD 0x' + VAL + ' TO OFFSET'

        if s[1] == '5':
            VAL = s[9:]
            exp = 'SET STORED = 0x' + VAL

        if s[1] == '6':
            ADDR = s[9:]
            exp = 'WRITE STORED TO ADDRESS (0x' +ADDR + 'OFFSET) (32bit) ; OFFSET += 4'

    return exp
