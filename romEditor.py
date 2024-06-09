
##Cambia el nombre de los MC a lo que vos elijas

#########################  Requirements  ###########################

#pip install tkinter
#pip install image


##################################################################

#Se basa en el save editor pero mejorando varias cuestiones

import tkinter as tk
from tkinter import ttk
from tkinter import N,W,E,S

import characterTable4
path = __file__[:-12]


CHAR_NAMES = ['Male', 'Female', 'Mokka', 'Lassi', 'Pico', 'Chai', 'Sorbet']

##OFFSETS
#Los offsets cambian según la región del ROM.... voy a tener cada offset a un bloque como una tupla. Offset de USA va en [0], EUR [1], eventualmente JP en [2]
char1Offset = [0x0003A1D8,0x0003A47C]

##Defino diccionario que guarda los offsets de cada stat en el .sav, relativo al offset del slot de pje

##MALE Name offsets

eur_EN  = [0x12F65BC, 0x12F72A4]
eur_FR = [0x131ACD0, 0x131B9C6]
eur_DE = [0x133EE98, 0x133FB86]
eur_ES = [0x1363A60, 0x1364757]
eur_IT = [0x138AC54, 0x138B93E]
us = [0x06C1E4, 0x6CECC]



##Crear diccionario de acciones (id, nombre)
actionsDic = {}
actionsList = []

with open('data/actions.txt', mode = 'r') as d:
    lines = d.readlines()
    for line in lines:

        splitted = line.split(' ')

        actionId = int(splitted[0])
        actionName = line[len(splitted[0])+1:]

        actionsDic[actionId] = actionName.strip()

        actionsList.append(line)


##Crear lista de spells
spellsList = []

with open('data/spellIds.txt', mode = 'r') as d:
    lines = d.readlines()
    for line in lines:
        spellsList.append(line[:-2])





#Cada personaje tiene un array de stats
#Cada stat es una tupla de datos
class STAT:
    def  __init__(self, name, off, nBytes, row, img_path, nbits_decimales=0):
        self.name = name #Nombre para el usuario
        self.offset = off #relativo al offset del bloque del personaje
        self.nBytes = nBytes #tamaño
        self.row = row #id que le doy yo para definir el orden en el gui
        self.decimal_bits = nbits_decimales #Para mostrar solo la parte entera de los datos fixed-points
        self.img_path = img_path #nombre de la fotito del stat
        self.entryBox = None #Objeto tk.gui. Caja númerica o menu desplegable según el stat
        self.tkVar = None #tk.IntVar()
        self.tkText = None  #tk.StringVar() . Solo para los que llevan menú desplegable


    #Para cuando le doy un valor a través de un menú desplegable
    def asignarDesplegable(self, texto):
        #Acá la cagué por no ser más consistente antes.... voy de una por lo que necesito ahora y de ultima despues adapto
        #Leo los primeros 1, 2 o 3 chars del texto y veo cual tiene el numero

        i = 0
        while texto[0:i+1].isdecimal(): i+=1
        val = int(texto[0:i])
        self.tkVar.set(val)
        return

    #Para cuando leo el ROM, y tengo que setear en la GUI a partir de lo que leo
    def setearValorDesplegable(self, *args):
        val = self.tkVar.get()

        if(self.name == 'Action'): optionsList = actionsList
        if(self.name.startswith('Spell')): optionsList = spellsList
        self.tkText.set(optionsList[val])






STATS_EXCLUSIVOS =[ #Estos stats no se pueden cambiar desde el .sav, de aqui la motivación de este editor de ROM.
    STAT('Action',0x40, 2, 0, 'action.png'),
    STAT('MP %',    0x20, 4, 1, 'stat9.png'),
    STAT('LVL-UP HP Modifier', 0x24, 4, 2, 'HP.png'),
    STAT('LVL-UP MP Modifier', 0x28, 4, 3, 'MP.png'),
    STAT('LVL-UP POW Modifier', 0x2C, 4, 4, 'stat3.png'),
    STAT('LVL-UP DEF Modifier', 0x30, 4, 5, 'stat4.png'),
    STAT('LVL-UP IQ Modifier',  0x34, 4, 6,'stat5.png'),
    STAT('LVL-UP SPRI Modifier', 0x38, 4, 7,'stat6.png'),
    STAT('LVL-UP AGI Modifier',  0x3c, 4, 8, 'stat7.png')
]

#Hechizos 1 - 5
SPELL_STATS = [ STAT('Spell '+str(i+1),0x42+4*i, 2, i+2, 'spell' +str(i+1) +'.png' ) for i in range(5)]

#Unlock Level Hezhizos 1 - 5
UNLOCK_LVL_STATS = [ STAT('Unlock LVL '+ str(i+1),0x44+4*i, 2, i+2, 'spell' +str(i+1) +'.png' ) for i in range(5)]



class Character:

    def __init__(self, id):
        self.offset = None #Offset del slot de pje en el rom

        self.stats = {} #dic, con el nombre accedo al stat
        for stat in STATS_EXCLUSIVOS + SPELL_STATS + UNLOCK_LVL_STATS:
            self.stats[stat.name] = STAT(stat.name, stat.offset, stat.nBytes, stat.row, stat.img_path, stat.decimal_bits)


        self.id = id  #0 Male, 1 Female, etc

#Lo confuso quizas es esto: Cada pje tiene un array de tk.Intvar, con un var por cada stat. Ahi se guarda el valor de su stat.

#Creo los personajes (solo les doy id, y luego, al cargar el rom, les doy su offset en memoria
CHARACTERS = []
for i in range(14):
    CHARACTERS.append(Character(i))

class MagicalROMEditor:

    def __init__(self, root):

        ##VARIABLES A USAR:
        self.romPath = tk.StringVar()
        self.ROMData = []             #array de bytes
        self.namesFrame = None #tab de solo los dos protas
        self.statsFrame = None #tab con los stats que solo se editan desde el ROM
        self.romRegion = tk.StringVar() # String que vale 'USA, 'EUR', o 'JP'
        self.romRegionId = None # 0 = USA, 1 = EUR, 2 = JP

        ##GUI CON PESTAÑAS
        root.title("Magical ROM Editor")

        #Habilitamos y creamos pestañas
        self.tabsystem = ttk.Notebook(root, padding="0 0 0 0")
        self.tabsystem.grid(column=0, row = 0, sticky=(N, W, E, S), columnspan= 7)

        ##Pestaña 1 - Cambio de nombres
        self.namesFrame = ttk.Frame(root, padding="1 1 1 1")
        self.namesFrame.grid(column=0, row=0, sticky=(W, S), columnspan = 10)
        self.namesFrame.rowconfigure(0, weight=1, pad = 0)
        #todo el pad este no anda por el que está en "suavizado general" abajo. Se puede usar el "ipad" sino

        #Rom Region Label
        tk.Label(self.namesFrame, text = 'Rom Region: ').grid(row=0, column = 0)
        tk.Label(self.namesFrame, textvariable = self.romRegion, fg ='blue').grid(row = 0, column = 1, sticky = W)

        # MC Default names:
        self.maleName = tk.StringVar()
        self.femaleName = tk.StringVar()
        validate_command = self.namesFrame.register(name_input) #max 8 caracteres


        ttk.Entry(self.namesFrame, textvariable = self.maleName, width = 12, validate="key",validatecommand=(validate_command,'%P')).grid(column = 1, row = 1, sticky = (W,N) )
        ttk.Entry(self.namesFrame, textvariable = self.femaleName, width = 12, validate="key",validatecommand=(validate_command,'%P')).grid(column = 1, row = 2, sticky = (W,N) )
        self.ponerImagen('imgs/char0.png', 40, 40, self.namesFrame, row=1, column=0)
        self.ponerImagen('imgs/char1.png', 40, 40, self.namesFrame, row=2, column =0)

        self.maleName.set('Galette')
        self.femaleName.set('Financiè') #Financière, no entra D:



        row = 3
        column =0


        #Boton Open .nds
        self.ponerImagen('imgs/save.png', 40, 40, self.namesFrame, row, column)
        tk.Button(self.namesFrame, text='Open ROM\n(.nds)', command=self.open_ROM).grid(column = column+1, row = row, sticky =  (N,S, W), columnspan = 1, padx = 20)
       # ttk.Label(controlPanel, textvariable=self.savPath).grid(column=column, row=row+1, columnspan=1, sticky=(W, E))

        #Boton Export .nds
        tk.Button(self.namesFrame, text='Patch ROM', command=self.patch_ROM).grid(column = column+2, row = row, sticky = (N,S, E), padx = 20)


        ##PERSONAJES

        #Creo las variables de los stats
        for char in CHARACTERS:
            for stat in char.stats.values(): #"stats" es un dic, asi que lo accedo asi para iterarlo
                stat.tkVar = tk.IntVar()


        mainchars = CHARACTERS[:7]
        eggchars = CHARACTERS[7:]



        ##Pestaña 2 - Cambio de STATS Exclusivos

        self.statsFrame = ttk.Frame(root, padding="1 1 1 1")
        self.statsFrame.grid(column=0, row=0, sticky=(W, S), columnspan = 10)
        self.statsFrame.rowconfigure(0, weight=1, pad = 0)

        self.crearColumnasSTATS(self.statsFrame, mainchars, STATS_EXCLUSIVOS)



        ##Pestaña 3 - Cambio de Hechizos

        self.spellsFrame = ttk.Frame(root, padding="1 1 1 1")
        self.spellsFrame.grid(column=0, row=0, sticky=(W, S), columnspan = 10)
        self.spellsFrame.rowconfigure(0, weight=1, pad = 0)

        self.crearColumnasSPELLS(self.spellsFrame, mainchars, SPELL_STATS, UNLOCK_LVL_STATS)


        ##Pestaña 4 - Cambio de STATS Exclusivos EGGS

        self.statsEggsFrame = ttk.Frame(root, padding="1 1 1 1")
        self.statsEggsFrame.grid(column=0, row=0, sticky=(W, S), columnspan = 10)
        self.statsEggsFrame.rowconfigure(0, weight=1, pad = 0)

        self.crearColumnasSTATS(self.statsEggsFrame, eggchars, STATS_EXCLUSIVOS)



        ##Pestaña 5 - Cambio de Hechizos EGGS

        self.spellsEggsFrame = ttk.Frame(root, padding="1 1 1 1")
        self.spellsEggsFrame.grid(column=0, row=0, sticky=(W, S), columnspan = 10)
        self.spellsEggsFrame.rowconfigure(0, weight=1, pad = 0)

        self.crearColumnasSPELLS(self.spellsEggsFrame, eggchars, SPELL_STATS, UNLOCK_LVL_STATS)



        #Suavizadogeneral
        for frame in [root, self.namesFrame, self.statsFrame, self.spellsFrame]:
            for child in frame.winfo_children():
                try:
                    padx = child.grid_info()['padx']
                    pady = child.grid_info()['padx']
                    child.grid_configure(padx= padx + 1, pady=pady + 2)
                except: pass


        #feet_entry.focus()
        #root.bind("<Return>", self.calculate)



        #Termino de implementar las pestañas
        self.tabsystem.add(self.namesFrame, text = 'Protagonist Names')
        self.tabsystem.add(self.statsFrame, text = 'Exclusive Stats')
        self.tabsystem.add(self.spellsFrame, text = 'Spells')
        self.tabsystem.add(self.statsEggsFrame, text = 'Eggs (Stats)')
        self.tabsystem.add(self.spellsEggsFrame, text = 'Eggs (Spells)')
        return

        #feet_entry.focus()
        #root.bind("<Return>", self.calculate)

    def ponerImagen(self, path, sizex, sizey, tab, row, column, sticky = None, columnspan = 1):
        image = openImage(path, sizex, sizey)
        imagen = tk.Label(tab, image=image)
        imagen.image = image #Tengo que resguardar la iamgen del recolector de basura para que se muestre
        imagen.grid(row=row, column=column, sticky = sticky, columnspan = columnspan)
        return imagen

    #Llamado al abrir un .sav por primera vez
    def open_ROM(self):
        from tkinter import filedialog
        filename = filedialog.askopenfilename(title='Select file')
        if(filename== ''): return
        self.romPath.set(filename)
        d = open(filename, mode = 'rb')
        self.ROMData = bytearray(d.read())
        d.close()

        self.determineROMRegion()

        self.updateCharacterData()




    def determineROMRegion(self):
        #Determino la región del ROM: lo dice el byte 0xF
        region = self.ROMData[0xF]
        if(region == 0x45): self.romRegion.set('USA') ; self.romRegionId = 0
        elif(region == 0x50): self.romRegion.set('EUR') ; self.romRegionId = 1
        elif(region == 0x4A): self.romRegion.set('JP (Not supported)') ; self.romRegionId = 2
        else: (self.romRegion.set('Not a valid ROM file')) ; self.romRegionId = -1


    def updateCharacterData(self):

        #Cargo los offsets de los pjes
        for i in range(len(CHARACTERS)):
            char = CHARACTERS[i]

            char.offset = char1Offset[self.romRegionId] + i*100

            #Leo sus stats
            for stat in char.stats.values():
                val = self.readBytes(char.offset + stat.offset, stat.nBytes)
                stat.tkVar.set(val)



    #LLamdo al exportar el .nds. Sobreescribe el archivo original, ojo!
    def patch_ROM(self):
        if(self.ROMData==None): return
        self.updateROMNames()
        self.updateStats()

        from tkinter import filedialog
        d = open(self.romPath.get(), mode = 'wb')
        d.write(self.ROMData)
        d.close()

        #Todo resetear esta label al abrir otros
        tk.Label(self.namesFrame, text ='Done!', fg = 'green').grid(column=2, row=4, sticky=(N, W,S,E))

    #Cambia los nombres por defecto de Male y Female en el ROM
    def updateROMNames(self):

        #Male name offsets
        if(self.romRegion.get() == 'EUR'):
            addrs = [eur_EN, eur_FR, eur_DE, eur_ES, eur_IT]
        if(self.romRegion.get() == 'USA'): addrs = [us]

        #es algo chiquito... no voy a poner un "else return..."

        bi = 0 #bytes escritos hasta el momento

        for name in [self.maleName.get(), self.femaleName.get(), 'Mokka', 'Lassi', 'Pico', 'Chai', 'Sorbet', 'Kir', 'Nogg', 'Fondue', 'Tom Yam', 'Gelato', 'Star', 'Pooka']:
            for addr in addrs:

                nombre = name[:8] #trim length sobrante
                n = 2*len(nombre) + 2 #cada caracter son 2 bytes, y además está el string terminator que es 0xFF 0xFF
                nombre_bytes = characterTable4.makeName(nombre)[0:n] #guardo solo un string terminator char acá (0xFF 0xFF). O sea, recorto los 0xFF sobrantes
                self.writeBytesROM(addr[0]+ bi,nombre_bytes, n, dup_addr = addr[1]+bi)

            bi += n

        return

    def updateStats(self):
        for char in CHARACTERS:
            for stat in char.stats.values():
                val = stat.tkVar.get().to_bytes(stat.nBytes,'little')
                self.writeBytesROM( char.offset + stat.offset, val, stat.nBytes, dup_addr = None  )
        return


    #Crea las columnas donde editar los stats
    def crearColumnasSTATS(self, tab, chars, STATS):

        #Imagenes de los pjes (Fila 0)
        self.ponerFotosPjes(tab, chars, column0 = 2, columnspan = 1)


        validate_command =tab.register(only_numeric_input)

        #Primer y segunda columna con nombre y foto de stat
        for i in range(len(STATS)):
            stat = STATS[i]

            #row 0 : Foto de los pjes
            #--> Empiezo en row1
            row = 1+stat.row

            #Columa 0: Nombre del stat
            ttk.Label(tab, text=stat.name).grid(column=0, row=row, sticky=W)

            #Columa 1: Imagen del stat
            img_path =  r"imgs/" + stat.img_path
            self.ponerImagen(img_path,22,22,tab,row = row, column = 1) #, rowspan=1, padx=5, pady=5)

            #Columna n: La de cada personaje
            for char_i in range(len(chars)):
                char = chars[char_i]


                if(stat.name == 'Action'):
                    field = crearBoxDesplegable(char.stats['Action'], tab, actionsList)

                else:
                    field = ttk.Entry(tab, textvariable = char.stats[stat.name].tkVar, width=1, validate="key",validatecommand=(validate_command,'%P'))
                    validate_command = tab.register(only_numeric_input)

                field.grid(column=2+char_i, row=1+stat.row, sticky=(W, E))

        return



    #Crea las columnas donde editar los spells
    def crearColumnasSPELLS(self, tab, chars, SPELLS, UNLOCK_LVLS):

        #Imagenes de los pjes
        self.ponerFotosPjes(tab, chars, column0 = 1, columnspan = 3)


        #row 1: 3 columnas por pje: dos de texto (una con "Spell" y otra con "Unlock lvl") y una con separador
        for i in range(len(chars)):
            tk.Label(tab, text = 'LVL', fg ='blue', width = 3).grid(row = 1, column = 1+3*i, sticky = (E,W))
            tk.Label(tab, text = 'Spell', fg = 'blue', width = 4).grid(row=1, column = 2+3*i, sticky = N)



        validate_command =tab.register(only_numeric_input)

        #Primer y segunda columna con nombre y foto de stat
        for spell_i in range(5):
            spell = SPELLS[spell_i]
            unlock_lvl = UNLOCK_LVLS[spell_i]



            #row 0 : Foto de los pjes
            #row 1: Texto
            #--> Empiezo en row 2
            row = 2+spell_i

            #Columa 0: Imagen del hechizo
            img_path =  r"imgs/" + spell.img_path
            self.ponerImagen(img_path,22,22,tab,row = row, column = 0) #, rowspan=1, padx=5, pady=5)



            #Columna 1+ 2n: La de cada personaje
            #cada pje tiene 2 columnas: El hechizo y unlock lvl
            for char_i in range(len(chars)):
                char = chars[char_i]

                statName = SPELL_STATS[spell_i].name

                lvl_field = ttk.Entry(tab, textvariable = char.stats[unlock_lvl.name].tkVar, width=1, validate="key",validatecommand=(validate_command,'%P'))
                validate_command = tab.register(only_numeric_input)
                lvl_field.grid(column=1+3*char_i, row=row, sticky=(W, E))
                lvl_field.configure(font =('Calibri', 10) ,  width = 1, justify="center")


                spell_field = crearBoxDesplegable(char.stats[statName], tab, spellsList)
                spell_field.grid(column=2+3*char_i, row=row, sticky=(W, E))


                #Separador gráfico vertical
                separator = ttk.Separator(tab, orient='vertical')
                separator.grid(row = 2, column = 3+3*char_i, sticky = (W, E, N, S), rowspan = 15, padx = 2)





    #Fotos de pjes. Especifico cuantas columnas ocupa cada pje (1 para stats, 2 para hechizos)
    def ponerFotosPjes(self, tab, chars, column0 = 2, columnspan = 1):

        for i in range(len(chars)):
            char = chars[i]
            c = column0 + i*columnspan #columna
            portrait_path = path + r'imgs\\char' + str(char.id) + ".png"
            self.ponerImagen(portrait_path,40,40,tab,row = 0, column = c, sticky = (E,W, S), columnspan = columnspan) #, rowspan=1, padx=5, pady=5)
            #Le puse STicky S porque en el tab de los spells me hace cualquier cosa sino... no sé por que, crea el primer row GIGANTE
        return










    def writeBytesROM(self, address, val, nBytes, dup_addr):

        if(self.ROMData==None): return

        self.ROMData[address : address+nBytes] = val
        if(dup_addr != None): self.ROMData[dup_addr : dup_addr+nBytes] = val #data duplicada

    #Lee bytes como si representaran un uint. Solo lee de esta forma si son 1, 2 o 4 bytes
    def readBytes(self, offset, nBytes):

        data = self.ROMData[offset: offset+nBytes]

        if(nBytes ==1): val= data[0]

        #Read Little Endian
        if(nBytes == 2):  val = data[0] +  (data[1] << 8)

        if(nBytes == 4): val =  data[0] +  (data[1] << 8) +  (data[2] << 16) +  (data[3] << 24)

        if(nBytes not in [1,2,4]): val = data #estas leyendo un chunk grande para procesar aparte, lo devuelvo asi nomas

        return val



from PIL import ImageTk, Image

def openImage(path, sizeX, sizeY):
    from PIL import Image, ImageTk #Con esto puedo resizear la imagen

    image = Image.open(path)
    image = image.resize((sizeX,sizeY))
    image = ImageTk.PhotoImage(image)
    return image


def name_input(input):
    if len(input)<=8: return True
    else:  return False


def only_numeric_input(input):
    #this is allowing all numeric input and backspace to work
    if (input.isdigit() and int(input)<=0xFFFFFF) or input =="": return True
    else:  return False


# Menu desplegable para elegir actions
# le pasas el stat asociado, una lista con las opciones posibles,
#y si querés un diccionaro con imagenes (para los spells)

#El tema es que el desplegable tiene el valor numerico y un nombre para los humanos, pero el stat necesita un valor posta. Así que le asigno una funcion que al elegir un valor, se quede solo con la parte numérica
def crearBoxDesplegable(stat, tab, optionsList, imgDic = {}):

    #Inicializo el tkVar acá, y no arriba en la funcion principal, para hacer más claro que solo uso estas variables con algunos stats...
    stat.tkText = tk.StringVar()


    # Hago que cuando el valor numerico del stat cambie (unico caso posible, al leer el ROM),  también se actualice la gui
    stat.tkVar.trace_add('write', stat.setearValorDesplegable)


    field = tk.OptionMenu(tab, stat.tkText, '',  *optionsList, command = stat.asignarDesplegable)
    field.configure(font =('Calibri', 10) , height = 2, bg = 'light blue', padx= 5, wraplength=70, justify="center")


    #Si hay dic de imagenes:
    #todo
    if(imgDic != {}):
        menu = field.nametowidget(field.menuname)
        for label, image in spellImgs_dic.items():
            menu.entryconfigure(label, image= image, compound = 'left')

    return field

#def crearNumericBox(stat,)



root = tk.Tk()
root.geometry("450x300")
root.resizable(width=True, height=True)
MagicalROMEditor(root)
root.mainloop()