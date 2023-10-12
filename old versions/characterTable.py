##Table guarda qué caracter es cada grupo de dos bytes
#0x0100 = 'A'
#0x0200 = 'B
#... etc
#0x1A00 = 'Z'
#0x1F00 = 'a'
#0x2000 = 'b'

#Null char = 0xFFFF (String terminate)

little = False #Little endian. Es, pero para lo de makeName me facilita dejarlo en falsey entregarlo big, y luego guardarlo little

table = {}
step = 0x0001
if(little): step = 0x0100

nchars = ord('Z') - ord('A') + 1

#MAYUSCULAS
i = 0
A = 0x0001
if(little): A = 0x0100

for v in range(A, A + nchars*step, step):
    char =  chr(ord('A') + i)
    table[v] = char
    table[char] = hex(v)
    i+= 1

#MINUSCULAS
i = 0
a = 0x001F
if(little): a = 0x1F00
for v in range(a, a + nchars*step, step):
    char =  chr(ord('a') + i)
    table[v] = char
    table[char] = hex(v)
    i+= 1
#todo arreglar el tema de endiannes... por favor
#CUSTOM CHARACTERS
Z = table['Z']
Z = int(Z,0)
table[Z+step*1] = '@'
table[Z+step*2] = '!'
table[Z+step*3] = '?'
table[Z+step*4] = ' '

z = table['z']
z = int(z,0)
table[z+step*1] = '*'
table[z+step*2] = '&'
table[z+step*3] = ' ' # ...,  puntos suspensivos, no sé que caracter es
table[z+step*4] = '='

table[0x8800] = '('
table[0x8900] = ')'
table[0xD600] = '¿'
table[0xD700] = '?'
table[0xD800] = '¡'
table[0x9900] = '_'

table[0x0000] = ' '
table[0xFFFF] = chr(0)
table[0xAB00] = 'ñ'
table[0x9C00] = 'á'
table[0xA700] = 'í'
table[0xA300] = 'é'
table[0xAD00] = 'ó'
table[0xB400] = 'ú'
table[0x01FF] = '\\n'

#05FF 0100 es un solo símbolo que aparece bastante... no sé que bien que será

#Números
cero = z + step*5
i = 0
for v in range(cero, cero + 10*step, step):
    char = chr(ord('0')+i)
    table[v] = char
    table[char] = hex(v)
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

#######################################################################################
#######################################################################################

#Ojo que creo que para que funcione little tiene que ser true
def crearArchivoTBL():
    ##Exportar a un archivo .tbl para usar en el hex editor ImHex
    d = open('Magical_Starsign_USA.tbl', mode ='w')
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
        if not little and len(h) ==2: h = '00' + h #'0001'
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

#Recibe un string y devuelve la lista de bytes a escribir para meter en el rom. Recorta a 8 caracteres si se pasa
def makeName(s):
    s= s[:8]
    out = []
    for char in s:
        out.append(int(table[char], 16)) #Paso el string a int

    return out

#Recibe una lista de bytes tal como está en el rom y devuelve el string decodificado
#Podria hacerme el boludo y descartar los bytes impares pero na
def readName(L):
    s = ''
    for i in range(0,len(L),2):
        val = L[i] + (L[i+1]<<8)
        if(val == 0xFFFF): break #string terminator
        s += table[val]

    return s


###############################################3

