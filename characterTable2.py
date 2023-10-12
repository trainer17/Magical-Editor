##Table guarda qué caracter es cada par de bytes
##Cada caracter se guarda en little endian
#En v2 dejé todo como little endian y solo cuando exporto la tabla cambio eso
#0x0001 = 'A'
#0x0002 = 'B
#... etc
#0x001A = 'Z'
#0x001F = 'a'
#0x0020 = 'b'

#Null char = 0xFFFF (String terminate)


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

#MINUSCULAS
i = 0
a = 0x001F
for v in range(a, a + nchars*step, step):
    char =  chr(ord('a') + i)
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

z = table['z']
z = int(z,0)
table[z+step*1] = '*'
table[z+step*2] = '&'
table[z+step*3] = ' ' # ...,  puntos suspensivos, no sé que caracter es
table[z+step*4] = '='


table[0x0088] = '('
table[0x0089] = ')'
table[0x00D6] = '¿'
table[0x00D7] = '?'
table[0x00D8] = '¡'
table[0x0099] = '_'

table[0x0000] = ' '
table[0xFFFF] = chr(0)
table[0x00AB] = 'ñ'
table[0x009C] = 'á'
table[0x00A7] = 'í'
table[0x00A3] = 'é'
table[0x00AD] = 'ó'
table[0x0084] = 'ú'
table[0x00A2] = 'è'
table[0xFF01] = '\\n'

#05FF 0100 es un solo símbolo que aparece bastante... no sé que bien que será

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
table[cero+step*13] = 'x' #en realidad, x de multiplicación
table[cero+step*14] = '%' #en realidad, símbolo de división
table[cero +step*15] = '.'
table[cero +step*16] = ','
table[cero +step*17] = ':'
table[cero +step*18] = ';'
table[cero +step*19] = "'"
table[cero +step*20] = '"'
table[cero +step*21] = '/'
table[cero +step*22] = '\\'
table[cero +step*23] = '$'
table[cero +step*24] = 'c' #centavo. Siguen Yen, Euro, libra, dos espacios, y termina la primer página de caracteres

#Después de los números, vienen +, - , x, %,  . , ;  etc
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

#Ojo que creo que para que funcione little tiene que ser true
def crearArchivoTBL():
    ##Exportar a un archivo .tbl para usar en el hex editor ImHex
    d = open('Magical_Starsign_USA2.tbl', mode ='w')
    for key in table.keys():

        #Saltear chars, solo escribir hexs
        if type(key) != type(0x0100): continue
        if(key == 0xFFFF):
            d.write('FFFF=NUL\n')
            continue
        char = table[key]
        h = hex(key) # 0x0001 -->  '0x1'
        h = h[2:] # '1'
        if(len(h) % 2 ==1): h = '0' + h  #01
        if len(h) ==2: h = '00' + h #'0001'
        d.write(h)
        d.write('=')
        d.write(table[key])
        d.write('\n')

    d.close()

#Me da la lista de hexs de un string segun esta tabla
def code(s):
    out = ''
    for c in s:
        out += table[c][2:] + ' '
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


###############################################3

