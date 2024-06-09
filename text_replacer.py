from characterTable4 import read2Bytes, table, readText

##Reemplaza texto del juego. Los pasos esquematicos son estos:
'''

1-Genero mi nuevo archivo de texto (escribo manual)
2-Lo paso a binario (encode)
3-Lo comprimo con ./lzss de CUE (compress)
4-Reemplazo esa región del ROM original por la del nuevo archivo
...y  a probar!

'''

#Still... el camino no es este. No anda bien en general y solo reemplaza datos apuntados por punteros, sin cambiar sin embargo esos punteros. Por lo que, creo, que si


#Acá creo una clase que tenga el texto de un archivo, con los comandos especiales, etc tenidos en cuenta
#Lo útil es que lo guardo como un array donde el texto es mi string común y las instrucciones mantienen su código

comandosIDPje = [0xFF40 + i for i in range(0xD)]

comandos2Bytes = [0xFF05, 0xFF04, 0xFF0C, 0xFF06, 0xFFA1] + [0xFF20, 0xFF21, 0xFF22, 0xFF23, 0xFF61] + [0xFF61, 0xFFB4]
comandos1Byte =  [0xFFA5, 0xFFA6, 0xFFA7, 0xFFA8, 0xFFA9] + [0xFF03, 0xFF01, 0xFFFF] + comandosIDPje
comandosOptionMenu = [0xFF06, 0xFFA1, 0xFF02]


class encodedDialog:

    #Le pasas un array de bytes que termina en [0xFFFF] y crea una instancia
    def __init__(self, bytedata = []):

        self.encoded_text = bytedata #array de bytes que la RAM entiende
        self.decoded_text = [] #Array de instrucciones y texto que el humano entiende

    def decode(self):
        #Básicamente readapto el código de "readText()"

        self.decoded_text  = []
        data = self.encoded_text
        i = 0
        current_string = ''

        while(i<len(data)):

            val = read2Bytes(data[i:i+2])

            #Si voy a leer un  comando, corto el string actual y lo guardo
            if (val in ( comandos2Bytes  + comandos1Byte)):
                if(current_string != ''): self.decoded_text.append(current_string)
                current_string = ''

            #Sino, es un caracter común, lo leo normalmente
            else:
                current_string += table[val]

            #Comandos de 2 bytes
            if(val in comandos2Bytes):
                next_val = read2Bytes(data[i+2:i+4]) #Leo el siguiente dato. Sin chequeos ni nada, que tire error
                par = (val, next_val)
                self.decoded_text.append(par) #appendeo el par (COMANDO, PARAMETRO)
                i += 2

            #Comandos de 1 byte
            if(val in comandos1Byte):
                self.decoded_text.append(val)

            i += 2

    def prettyPrint(self):

        for line in readText(self.encoded_text):
            print(line)

    def printContents(self):
        print(self.decoded_text)


    #Le pasas un string con el formato editable y te crea un texto codificado en bytearray que la RAM entiende
    #Por ahora, sin codigos de control

    def encode(self, text):

        self.encoded_text = []

        #Hago una pasada rápida para convertir mis codigos de control en texto, tipo [SPEAKER NAME:] lo convierto a mi propio codigo, digamos "$". Como solo soporto pocos códigos y estoy probando ideas lo dejo así temporalmente
        text = text.replace(table[0xFF09], '$') #[SPEAKER NAME:]
        text = text.replace(table[0xFFFF], '%') #[END]\n\n
        text = text.replace(table[0xFF03], '=') #'[WAIT TOUCH TO CONTINUE]'

        for c in text:

            #Decodificacion manual de los msjes de control de recien
            if(c == '$'): byteCode = 0xFF09
            elif(c == '%'): byteCode = 0xFFFF
            elif(c == '='): byteCode = 0xFF03
            else:  byteCode = int(table[c], 16) #y los caracteres comunes x tabla

            lsb = byteCode & 0x00FF
            msb = byteCode >> 8

            self.encoded_text.append(lsb)
            self.encoded_text.append(msb)
        return





#Ejemplo de uso: Acá hay Fondue Trivia en el Rom EUR
trivia_demo = [0x00E25278, 0xE25800]
#data = readROMregion(trivia_demo[0], trivia_demo[1])
#demo_dialog = codedDialog(data)
#demo_dialog.printContents()
#demo_dialog.prettyPrint()


##Paso 1)  Recibo un archivo .txt con el texto que quiero, y creo un nuevo archivo binario que al decodificarlo dé ese texto
def txt2bin(path):

    with d.open(path, mode = 'r') as txt_file :
        text = txt_file.read()
        lines = text.splitlines()

    bin_file = d.open('NEW_TEXT.bin', mode = 'wb')

    #Primeros 4 bytes: Cantidad de diálogos en el archivo.
    #Típicamente la cantidad de 0xFFFF que hay
    numDialogs = text.count('[END]')
    data = numDialogs.to_bytes(4, byteorder = 'little')
    bin_file.write(data)

    #A partir de acá, pura data. A decodificar mi archivo nomás
    for line in lines[1:]:
        data = string2bin(line)



    bin_file.close()

#Recibe un string ASCII, lo convierte a los bytes que irian en el ROM y representarian eso (decomprimidos)
def string2bin(s):

    s = s.replace('[SET COLOR: Red] ', 0xFF050001)
    s = s.replace('[SET COLOR: Blue] ', 0xFF050002)
    s = s.replace('[SET COLOR: Normal] ', 0xFF050000)

    s= s.replace('[SHORT OPTION:] ', 0xFFA10001)
    s= s.replace('[LONG OPTION:] ', 0xFFA10002)




##------------------------------------------------------------------------------------------------

##PASO 2 : Recibe un directorio de txts y los paso a archivos binarios decomprimidos que la RAM puede entender

def encodeFile(path):

    with open(path, mode = 'r') as d:
        lines = d.readlines()

    fullText = ''.join(lines) #Con esto calculo los primeros 4 bytes
    text =''.join(lines[1:]) #Con esto el resto

    #Pongo los 4 prmeros bytes del archivo, que es un uint con la cantidad de [0xFFFF] que hay
    numDialogs = fullText.count('[END]')
    data = numDialogs.to_bytes(4, byteorder = 'little')


    #Paso el string a array de bytes tal como irian codificados en la ram
    s = encodedDialog()
    s.encode(text) #codifico acá
    data += bytearray(s.encoded_text)

    pathNuevo = path[:-4] + '.bin'
    with open(pathNuevo, mode ='wb') as d:
        d.write(data)

    print(path + ' encoded')
    return

def encodeDir(path):

    for file in os.listdir(path):
        if file.find('.txt') <0: continue #me salteo todos los archivos que no sean de texto
        encodeFile(path + file)

    return

##------------------------------------------------------------------------------------------------


##PASO 3: CODIFICO ARCHIVOS CON LZSS DE CUE
import shutil
lzssProgram_path = 'lzss.exe'


#comprime un archivo binario con algoritmo lzss
#Devuelve el path a ese archivo
def lzssCompressFile(path):

    pathNuevo = path[:-4] + '_compressed.bin'

    #1-Copio el archivo para sobreescribir la copia
    shutil.copy(path, pathNuevo )

    #2-Lo comprimo
    os.system(lzssProgram_path + ' -evn ' + '"' + pathNuevo +'"') #comillas por si hay un espacio en un path. Windows cmd lo pide

    #os.system(lzssProgram_path + ' -evn ' + path)

    return pathNuevo

#Comprime un directorio usando la funcion de arrriba
#Devuelve lista de nombres de los archivos comprimidos
def lzssCompressDir(dir):

    compressed_paths = []
    for file in os.listdir(dir):
        if file.find('compressed') > 0: continue #Me salteo los archivos ya comprimidos
        if file.find('.bin') < 0: continue #Me salteo los archivos .txt y todo lo que no sea binario

        compressed_path = lzssCompressFile(dir + file)
        compressed_paths.append(compressed_path)

    return compressed_paths


##------------------------------------------------------------------------------------------------


##PASO 4: HAGO UNA COPIA DEL ROM MODIFICADO

from characterTable4 import EURPath

#Recibe un rompath y un array de paths a los files modificadas, y las reemplaza en una copia del ROM
#El formato de los files modificados debe ser dir_[offset] (size). Por ejemplo, dir_00CC7F28 (4295)
#Esto es lo que exporta LZZRECONSTRUCTOR 2 por defecto llamando "dir" a  los archivos exportados, asi que es directo
def replaceModdedFiles(ROMPath, moddedFiles):

    #1-Abro el ROM original y lo cargo completo en memoria
    with open(ROMPath, mode = 'rb') as d:
        ROMDATA =  bytearray(d.read())

    #2-Copio el contenido de los archivos al rom

    #2.0 itero todos los archivos
    for file in moddedFiles:
        #2.1 los leo
        with open(file, mode = 'rb') as d:
            newdata = bytearray(d.read())

        #2.2 consigo su offset inicial a partir del titulo
        offset = file[file.find('_')+1:] #descarto el "dir_"
        offset = offset.split()[0] #me quedo con el hex 00cc7f28
        offset = int(offset, 16) #Lo leo como hexa
        #todo CHEQUEAR BIEN ESTO!! Si el directorio tiene un _ en el nombre por ej ya la cago. lo mas seguro es trimear el nombre del directorio del path y ahi asegurarse que este es el unico guin bajo

        #2.3 copio los contenidos
        ROMDATA[offset: offset+len(newdata)] = newdata


    #3- Guardo el ROM modificado como una copia
    pathNuevo = ROMPath[:-4] + ' EDITED.nds'
    with open(pathNuevo, mode = 'wb') as d:
        d.write(ROMDATA)

    print('Listo! Rom editado' )
    return


## PUESTA EN PRACTICA

encodeDir('edited text 2/')
lzssCompressDir('edited text 2/')
modded = lzssCompressDir('edited text 2/')
replaceModdedFiles(EURPath, modded)