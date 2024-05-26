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
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

mainPath = r"C:\Users\Graciela\Downloads\Games\Romhack/"


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
table[0x00D6] = '¿' #0x00D5 es como < pero más abierto
table[0x00D7] = '?'
table[0x00D8] = '¡'
table[0x00D9] = '!'
table[0x0099] = '_'
table[0x00C9] = '>'
table[0x0095] = '§'

table[0x0000] = ' '
table[0x00AB] = 'ñ'
table[0x009C] = 'á'
table[0x00A7] = 'í'
table[0x00A3] = 'é'
table[0x00AD] = 'ó'
table[0x0084] = '%'
table[0x00B4] = 'ú'
table[0x00B6] = 'ü'
table[0x00A2] = 'è'
table[0x0063] = 'É'
table[0x005C] = 'Á'
table[0x00e0] = '♪'

table[0x00C3] = '"' #en cursiva
table[0x00C4] = '"' #muy finita


##Caracteres de control:

table[0xFF00] =  chr(10) #'\\n' newline.
table[0xFF01] =  chr(10) #'\\n' newline. Usado para indicar FIN DE NOMBRE DE PERSONAJE.  En texto común, intercambiable con 0xFF00. En nombre de pje, no

table[0xFF03] = ' [WAIT TOUCH TO CONTINUE]'
table[0xFFFF] = ' [END]\n\n' # WAIT TOUCH TO CLOSE o bien, chr(0) == Text End / String Terminator
table[0xFF05] = '[SET COLOR] ' #siguen dos bytes de id de color. Solo 0x0, 0x1 o 0x2
table[0xFF09] = '[SPEAKER NAME:] ' #Indica que el texto entre esto y un 0xFF01 es lo que va en el "encabezado" del dialog box (donde va el nombre de pje)
 #Previamente:'[DIALOG BEGIN] \n' #Indica el comienzo de un nombre de personaje, *o una fila nueva en un dialog menu

table[0xFF0D] = chr(9) # '\☺t' tab


table[0xFF0C] = '[SET TEXT SPEED: ] ' #lee el siguiente byte, que indica a qué PERIODO cicla el texto. O sea, 0x0 es lo más rápido, y de ahí vas multiplicando 0x1 para aumentar. Ej 0x10 es el doble de rapido que 0x20
#Algo así es, pero no exactamente. Porque poniendo entre 0x0 y 0x8 lo desconfigura de otras maneras raras

table[0xFF04] = '[WAIT N frames]'
table[0xFF0A] = '[SET: AUTO CLOSE THIS DIALOG WHEN FINISHED (dont wait player touch)]'

table[0xFF06] = '[CREATE OPTION MENU WITH N ENTRIES]'# Lee los siguientes dos bytes para determinar cuantas opciones hay
table[0xFFA1] = '[OPTION] ' #sigue x0001 o 0x0002 siempre. Si no, no sé bien que pasa.
table[0xFF02] = '[MENU END]' #sigue xFFFF



##Character Portrait change. Usado por Sorbet y Pico en el post -tutorial, por ej.
#Cambia el portrait del personaje que se muestra actualmente
table[0xFFA5] = '[SET PORTRAIT: Normal] '
table[0xFFA6] = '[SET PORTRAIT: Happy] '
table[0xFFA7] = '[SET PORTRAIT: Angry] '
table[0xFFA8] = '[SET PORTRAIT: Sad] '
table[0xFFA9] = '[SET PORTRAIT: Surprised] '
#Otros: No hacen efectt


##ids de nombre de personaje

table[0xFF61] = '[CHARACTER IN PARTY POSITION:] ' #lee los siguientes dos bytes, que van de 0x0000 a 0x0005
table[0xFFB4] = '[CHARACTER WITH NAME ID:] ' #lee los siguientes dos bytes, que van de 0xFF40 a 0xFF4C. Indexacion 0xFF40 + i igual que en el .sav creo
#todo: REEMPLAZAR ESTOS DOS BLOQUES POR, POR EJ,  [SORBET] [LASSI] ETC!! y volver a dumpear el texto
#El problema es que a veces precede el 0xFFB4, y a veces no....
#Se me ocurre, que 0xFF61 puede ser un switch, y que afecta a todo lo que sigue, no al caracter inmediatamente siguiente... probar luego

table[0xFF40] = '[MAIN CHARACTER]'
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


## Nombres de otras cosas (Lee los siguientes dos bytes)

table[0xFF20] ='[MAP ID:] ' #Lee los siguientes dos bytes para buscar en memoria el nombre de un mapa.
table[0xFF21] ='[MAIN CHARACTER ID:] '
# Va de 0x1 (MALE) a 0x7 (sorbet). Incluye a Female.  Vacio, y de 0xD a 0x10 tiene 4 pjes huevo. 0x14 water,
table[0xFF22] ='[ITEM ID:] '   #Va al menos hasta 0x0155
table[0xFF23] ='[SPELL ID:] '


#0xFFB5, 0xFFB6 algo relacionado a mayusculas y minusculas. Toma codigos de control 0x0001 y 0x0002 creo



#0xFF02: Nada, 0xFF04 y FF06: Traba y rompe


# crear un nuevo juego y ver los caracteres en la pantalla de nombres. Están en orden

##Ahora, cargo tambien los pares a la inversa
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
    d_big = open('Magical_Starsign_TABLE_BIG_ENDIAN.tbl', mode ='w')

    for key in table.keys():

        #Saltear chars, solo escribir hexs
        if type(key) != type(0x0100): continue

        #char = table[key]
        h = hex(key) # '0x0001' -->  '0x1'
        h = h[2:] # '1'
        if(len(h) % 2 ==1): h = '0' + h  #01
        if len(h) ==2: h = '00' + h #'0001'

        hex_little = h
        hex_big = h[2:] + h[:2]

        try:
            d_little.write(hex_little + '=' + table[key] + '\n')
            d_big.write(hex_big + '=' + table[key] + '\n')

        except:
            print('Error exportando el caracter ', table[key])

    d_little.close()
    d_big.close()

#Me da un string con los hexs de un string codificado segun esta tabla
def code(s):
    out = ''
    for c in s:
        out += table[c][2:] + ' '
    return out

#Lo mismo pero agregando los bytes relleno . Solo para caracteres normales!!! Usar solo para buscar palabras en imhex
def codeImhex(s):
    out = ''
    for c in s:
        out += '00 ' + table[c][2:] + ' '
    return out


#Recibe un string y devuelve un bytearray a escribiren el rom. Recorta a 8 caracteres si se pasa
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









##############################################################################################################


# Lee un chunk de datos (array de bytes) que obtengo del ROM. Si no reconoce algo mete "?"
# Formatealindos algunos codigos de control, para que lo lea un humano

def readText(data):

    lines = []
    s  = ''
    i = 0

    while(i<len(data)):

        val = read2Bytes(data[i:i+2])

        #Códigos de control que leen el siguiente byte:

        if(i<len(data)-2):
            next_val = read2Bytes(data[i+2:i+4])
        else: next_val = 0x0

        if(val == 0xFF05): #Color change, leo los siguientes dos bytes
            if(next_val == 0x01): c = '[SET COLOR: Red] '
            if(next_val == 0x02): c = '[SET COLOR: Blue] '
            if(next_val == 0x00): c = '[SET COLOR: Normal] '
            i += 2

        elif(val == 0xFF04):
            c = ' [WAIT  '+ str(next_val) + ' FRAMES]'
            i += 2

        elif(val == 0xFF0C):
            c = '[SET TEXT PERIOD = '+ str(next_val) + ']'
            i += 2

        elif(val == 0xFF06):
            c = '[MENU WITH '+ str(next_val) + ' OPTIONS] \n'
            i += 2

        elif(val == 0xFFA1):
            if next_val == 0x0001: c = '[SHORT OPTION:] '
            if next_val == 0x0002: c = '[LONG OPTION:] '

            i+= 2

        #Estos leen el siguiente byte omo como un ID normal

        elif(val in [0xFF20, 0xFF21, 0xFF22, 0xFF23, 0xFF61] ):
            c = table[val][:-2] + str(next_val) + '] '
            #c = '[CHARACTER IN PARTY POSITION ' + str(next_val) + ']'
            i+=2

    #caracter común, lo leo normalmente
        else:
            try: c = table[val] #Lo intento leer
            except: c = '[' + hex(val) + ']' # ? #Caracter o código aún desconocido

        s += c

        if(val == 0xFFFF): #End current message
            lines.append(s)
            s = ''

        i+= 2


    #for line in lines: print(line)
    return lines




#Le pasas el path de un directorio con ficheros de binarios de texto y te genera un txt con el mismo nombre pero legible en un editor de texto.
#Tipicamente, el directorio es "./decompressed_text"

def readTextInDir(path):

    os.chdir(path)

    for file in os.listdir():

        if not file.endswith('.bin'): continue #solo hace los binarios
        readTextInFile(file)

# Le pasas el path de un archivo binario con el texto del juego (ya descomprimido) y te crea un txt usando el "readtext" de arriba
def readTextInFile(file):

    with open(file, mode = 'rb') as d:
        data = d.read()

    print('Doing ' + file)

    try:
        numDialogs = read4Bytes(data[0:4]) #Los primeros cuatro bytes te indican cuantos diálogos hay.
                        #Ej: Podes hablar con Pico y con Lassi, y solo tienen un dialogo en este mapa, entonces esto vale 2, por más que tengan 300 lineas cu
                            # El assert simple es que numDialogs == cantidad de 0xFFFF en el file
    except:
        print('Archivo muy chiquito! Abortando')
        return

    try: text = readText(data[4:])
    except:
        print('Hubo error con archivo ' + file)
        return

    #creo un archivo con el dump de texto decodeado por la tabla
    with open(file[:-3] + '.txt', mode = 'w', encoding='utf-8') as d: #El encoding es utf8 para poder poner la corcheita de los putty pea
        d.write('Number of dialogues in this file: ' + str(numDialogs) +'\n')
        d.writelines(text)


    return



#Lee dos bytes en el orden correcto. Pasale una lista con esos dos bytes en el orden que esta en memoria
def read2Bytes(bytes):
    return  bytes[0] +  (bytes[1]<<8)

def read4Bytes(bytes):
    return  bytes[0] +  (bytes[1]<<8) + (bytes[2] << 16) +  (bytes[3] << 24)


###############################################

EURPath = mainPath + r"\roms\Magical Starsign\0845 - Magical Starsign (Europe) (En,Fr,De,Es,It).nds"
USAPath = mainPath + r"\roms\Magical Starsign\0614 - Magical Starsign (USA).nds"

#Lee bytes del rom a un array
def readROMregion(addr_from, addr_to, ROMPath = EURPath ):

    with open(ROMPath, mode = 'rb') as d:
        d.seek(addr_from)
        ROMdata =  bytearray(d.read(addr_to - addr_from))

    return ROMdata


#Lee texto de una region del ROM EUR
def decodeROMregionText(addr_from, addr_to, ROMPath = EURPath):

    ROMdata = readROMregion(addr_from, addr_to, ROMPath)

    return readText(ROMdata)

#Le pasas el ROM, y de que a qué direccion, y te saca un archivo de texto con el formato "linea_i - texto_i"s
def dumpROMText(addr_from, addr_to, ROMPath, file_out ):

    file_out = mainPath + 'textdumps/' +file_out +'.txt'

    decoded_text = decodeROMregionText(addr_from, addr_to, ROMPath)

    with open(file_out, mode = 'w') as d:

        d.write(hex(addr_from) + '\n\n')

        for i in range(len(decoded_text)):
            line_i = str(i) + ' - ' + decoded_text[i]
            line_i = line_i.replace(' [END]', '') #Quito el código de control para leerlo yo más bonito... no olvidar que está!
            d.write(line_i)

        d.write(hex(addr_to))
    return




##VIEJOS

#Recibe un bytearray representando un nombre, tal como está en el rom y devuelve el string decodificado
#Se aprovecha de saber que no hay códigos de control para cortar ni bien encuentra un 0xFFFF
def readName(L):
    s = ''
    for i in range(0,len(L),2):
        val = L[i] +  (L[i+1]<<8)
        if(val == 0xFFFF): break #string terminator
        s += table[val]
    return s


#Lee palabras individuales de una region del ROM EUR, separadas por el marcador 0xFFFF
def readROMregionWords(addr_from, addr_to, ROMpath = r"..\roms\Magical Starsign\0845 - Magical Starsign (Europe) (En,Fr,De,Es,It).nds"):

    d=open(ROMpath, mode = 'rb')
    ROMdata = bytearray(d.read())
    d.close()

    words = []
    addr = addr_from

    while addr < addr_to:
        word = ''
        char_read = 'HOLAA'
        while(char_read != ''):
            char_read = readName(ROMdata[addr:addr+2])
            word += char_read
            addr += 2
        words.append(word)
    return words

#Nombres de ataques fisicos:  0x012FA568 - 0x012FB7BF
#y acciones en general: hasta 0x012FBC16
physical_attacks = readROMregionWords(0x012FA568, 0x012FB7BF)


