##Table guarda qué caracter es cada par de bytes
##Cada caracter se guarda en little endian
#En v2 dejé todo como little endian y solo cuando exporto la tabla cambio eso
#0x0001 = 'A'
#0x0002 = 'B
#... etc
#0x001A = 'Z'
#0x001F = 'a'
#0x0020 = 'b'

#Null char = 0xFFFF (String terminate
import os
os.chdir(__file__[:-18])


table = {}
step = 0x0001

nchars = ord('Z') - ord('A') + 1

#MAYUSCULAS
i = 0
A = 0x0001

for v in range(A, A + nchars*step, step):
    char =  chr(ord('A') + i)
    table[v] = char
    table[char] = hex(v)
    i+= 1

#CUSTOM CHARACTERS
Z = table['Z']
Z = int(Z,0)
table[Z+step*1] = '@'
table[Z+step*2] = '!' #Revisar este
table[Z+step*3] = '?'
table[Z+step*4] = ' '

#MINUSCULAS
i = 0
a = 0x001F
for v in range(a, a + nchars*step, step):
    char =  chr(ord('a') + i)
    table[v] = char
    table[char] = hex(v)
    i+= 1

#CUSTOM CHARACTERS

z = table['z']
z = int(z,0)
table[z+step*1] = '*'
table[z+step*2] = '&'
table[z+step*3] = '…' # ...,  puntos suspensivos
table[z+step*4] = '='

#Números
cero = z + step*5
i = 0
for digit_val in range(cero, cero + 10*step, step):
    char = chr(ord('0')+i)
    table[digit_val] = char
    table[char] = hex(digit_val)
    i+=1

table[cero+step*11] = '+'
table[cero+step*12] = '-'
table[cero+step*13] = '×'
table[cero+step*14] = '÷'
table[cero +step*15] = '.'
table[cero +step*16] = ','
table[cero +step*17] = ':'
table[cero +step*18] = ';'
table[cero +step*19] = "'"
table[cero +step*20] = '"'
table[cero +step*21] = '/'
table[cero +step*22] = '\\'
table[cero +step*23] = '$'
table[cero +step*24] = '¢'
table[cero +step*25] = '¥'
table[cero +step*26] = '€'
table[cero +step*27] = '£'
table[cero +step*28] = ' '
table[cero +step*29] = ' ' # acá termina la primer página de caracteres

#MAS CUSTOM CHARACTERS

table[0x0088] = '('
table[0x0089] = ')'
table[0x00D6] = '¿'
table[0x00D7] = '?'
table[0x00D8] = '¡'
table[0x00D9] = '!'
table[0x0099] = '_'

table[0x0000] = ' '
table[0x00AB] = 'ñ'
table[0x009C] = 'á'
table[0x00A7] = 'í'
table[0x00A3] = 'é'
table[0x00AD] = 'ó'
table[0x0084] = 'ú' #mal creo
table[0x00B4] = 'ú'
table[0x00A2] = 'è'
table[0x0063] = 'É'

##Caracteres de control:

table[0xFF00] =  chr(10) #'\\n' newline
table[0xFF01] =  chr(10) #'\\n' newline. Usado para indicar FIN DEL MENSAJE, por ejemplo, en FIN DE NOMBRE DE PERSONAJE
table[0xFF03] = ' [WAIT TOUCH TO CONTINUE]'
table[0xFFFF] = ' [END] \n' # WAIT TOUCH TO CLOSE o bien, chr(0) == Text End / String Terminator
table[0xFF05] = ' [SET COLOR] '
table[0xFF09] = ' [DIALOG BEGIN] \n' #Indica el comienzo de un nombre de personaje


table[0xFF61] = ' [CHARACTER IN PARTY POSITION: ]' #lee los siguientes dos bytes, que van de 0x0000 a 0x0005
table[0xFFB4] = ' [CHARACTER WITH NAME ID :]' #lee los siguientes dos bytes, que van de 0xFF40 a 0xFF4C


#ids de nombre de personaje
table[0xFF40] = '[MAIN CHARACTER NAME]'
table[0xFF41] = 'Mokka'
table[0xFF42] = 'Lassi'
table[0xFF43] = 'Pico'
table[0xFF44] = 'Chai'
table[0xFF45] = 'Sorbet'
table[0xFF46] = 'Wind? Egg'
table[0xFF47] = 'Earth? Egg'
table[0xFF48] = 'Fire Egg'
table[0xFF49] = 'Wood? Egg'
table[0xFF4A] = 'Water Egg'
table[0xFF4B] = 'Light? Egg'
table[0xFF4C] = 'Dark? Egg'

#Notar que esto implica que puede haber 3 caracteres de control para el nombre de un pje
# [0xFF09] [0xFFB4] [0xFF40] es equivalente a [0xFF09] [0xFF40]   por alguna razon

#0xFF48 0xFF49 posiblemente Punteros
#0xFF02: Nada, 0xFF04 y FF06: Traba y rompe

#05FF 0100 es un solo símbolo que aparece bastante... no sé que bien que será


# crear un nuevo juego y ver los caracteres en la pantalla de nombres. Están en orden

#Ahora, cargo tambien los pares a la inversa
for int_key, char_val in table.copy().items():
    if type(int_key) != type(0x01): continue
    table[char_val] = hex(int_key)


#Recibe un string de hexadecimal de un caracter y lo formatea a una lista de dos bytes como para escribir en memoria (pre-swap por endiannes). Totalmente al pedo porque nunca escribo strings, olvidar
def hexToBytes(hex_val):
    if len(hex_val)==3: #0xA --> [0x00, 0x0A]
        hex_val = '0x0'+hex_val[-1]
        final_val = ['0x00', hex_val]
    elif  len(hex_val) ==4: #0xAA --> [0x00, 0xAA]
        final_val = ['0x00', hex_val]

    elif len(hex_val) == 5: #0xAAA --> [0x0A, 0xAA]
        hex_val1 = '0x0'+ hex_val[2]
        final_val = [hex_val1, '0x00' + hex_val[3:]]

    else:  #0xAAAA--> [0xAA. 0xAA]
        final_val = [hex_val[0:4], '0x00'+hex_val[4:] ]

    return final_val

#######################################################################################
#######################################################################################

def crearArchivoTBL(path = 'Magical_Starsign_TABLE.tbl' ):
    ##Exportar a un archivo .tbl para usar en el hex editor ImHex u otro
    d_little = open(path, mode ='w')
    #d_big = open('Magical_Starsign_TABLE_BIG_ENDIAN.tbl', mode ='w')
    for key in table.keys():

        #Saltear chars, solo escribir hexs
        if type(key) != type(0x0100): continue
        if(key == 0xFFFF):
            d_little.write('FFFF=NUL\n')
            #d_big.write('FFFF=NUL\n')

            continue

        char = table[key]
        h = hex(key) # '0x0001' -->  '0x1'
        h = h[2:] # '1'
        if(len(h) % 2 ==1): h = '0' + h  #01
        if len(h) ==2: h = '00' + h #'0001'

        hex_little = h
        hex_big = h[2:] + h[2:]

        d_little.write(hex_little + '=' + table[key] + '\n')
        #d_big.write(hex_big + '=' + table[key] + '\n')


    d_little.close()
    #d_big.close()

#Me da un string con los hexs de un string codificado segun esta tabla
def code(s):
    out = ''
    for c in s:
        out += table[c][2:] + ' '
    return out

#Lo mismo pero sin trimear el header de 0x00. Solo para caracteres normales!!! Usar solo para buscar palabras en imhex
def codeImhex(s):
    out = ''
    for c in s:
        out += '00 ' + table[c][2:] + ' '
    return out


#Recibe un string y devuelve un bytearray a escribir para meter en el rom. Recorta a 8 caracteres si se pasa
#Lo devuelve en little endian.
def makeName(s, typeInt = False):
    s= s[:8]
    out = bytearray()
    for char in s:
        char_bytes = hexToBytes(table[char])
        out.append(int(char_bytes[1], 16))
        out.append(int(char_bytes[0], 16))


    while(len(out)<8*2):
        out.append(int('0xFF', 16))

    return out

#Recibe un bytearray tal como está en el rom y devuelve el string decodificado
#Podria hacerme el boludo y descartar los bytes impares pero na
def readName(L):
    s = ''
    for i in range(0,len(L),2):
        val = L[i] +  (L[i+1]<<8)
        if(val == 0xFFFF): break #string terminator
        s += table[val]

    return s

#Lee un chunk de datos que le copio y pego del ROM. Si no reconoce algo mete "?"
def readText(data):

    lines = []
    s  = ''
    for i in range(0,len(data),2):
        val = data[i] +  (data[i+1]<<8)
        try: c = table[val]
        except: c = '?'
        s += c
        if(val == 0xFFFF):
            lines.append(s)
            s = ''

    for line in lines: print(line)
    #return lines


###############################################




#Lee palabras individuales de una region del ROM EUR
def readROMregionWords(addr_from, addr_to, ROMpath = r"..\roms\Magical Starsign\0845 - Magical Starsign (Europe) (En,Fr,De,Es,It).nds"):

    d=open(ROMpath, mode = 'rb')
    ROMdata = bytearray(d.read())
    d.close()

    words = []
    addr = addr_from

    while addr < addr_to:
        word = ''
        char_read = 'cualquier cosa, valor inicial'
        while(char_read != ''):
            char_read = readName(ROMdata[addr:addr+2])
            word += char_read
            addr += 2
        words.append(word)
    return words

#Nombres de ataques fisicos:  0x012FA568 - 0x012FB7BF
#y acciones en general: hasta 0x012FBC16
physical_attacks = readROMregionWords(0x012FA568, 0x012FB7BF)