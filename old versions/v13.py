#Otro buen ejemplo: https://www.pythonguis.com/tutorials/create-ui-with-tkinter-grid-layout-manager/

#todo resetear flags de historia y cofres/leafs/items recogidos

#todo imagen de los elementos de c/u
#todo idem catch de errores de numeros muy grandes
#todo poner de yapa un "play time" y "bira"?
#todo dejar una notita para explicar el funcionamiento de tener a Male y Female a la vez (usar teleport enseguida. Se repone a Lassi en Neumann).
#todo interfaz linda de elegir male/female (click portraits?)

#todo unlcock diary Falta... no importa
import tkinter as tk
from tkinter import ttk
from tkinter import N,W,E,S

import characterTable2
import magicalChecksum
path = __file__[:-6]



class STAT:
   def  __init__(self, name, off, nBytes, internalId, bits_descarte):
        self.name = name
        self.offset = off
        self.nBytes = nBytes
        self.id = internalId
        self.bits_descarte = bits_descarte


STARSIGN_ID = -1
SPELL6_ID = 8
#Cada stat es una tupla de datos: Nombre del stat, offset relativo al slot de un pje en el .sav y tamaño en bytes. El ultimo es un id que le doy yo para las fotos, codigo etc
CHAR_STATS =[
    STAT('STAR',   0x00, 1, STARSIGN_ID,2), #id negativo porque le creo el gui aparte
    STAT('LVL',    0x08, 4, 0, 0),
    STAT('HP',     0x18, 4, 1, 4),
    STAT('MP',     0x18+4, 4, 2,4),
    STAT('STR',    0x18+4*2, 4, 3, 4),
    STAT('DEF',    0x18+4*3, 4, 4, 4),
    STAT('IQ',     0x18+4*4, 4, 5, 4),
    STAT('SPRI',   0x18+4*5, 4, 6, 4),
    STAT('AGI',    0x18+4*6, 4, 7, 4),
    STAT('6th Spell',0x18+4*7, 1, 8, 0)
]

import enum

class CHAR_NAMES(enum.IntEnum):
    MALE = 0
    FEMALE = enum.auto()
    MOKKA = enum.auto()
    LASSI = enum.auto()
    PICO = enum.auto()
    CHAI = enum.auto()
    SORBET = enum.auto()

class Character:

    def __init__(self):
        self.offset = None #Offset del slot de pje
        self.name = tk.StringVar()
        self.stats = [] #array propio con los tk.stringvar y tk.intvar
        for stat in CHAR_STATS:
            self.stats.append(tk.IntVar())
        self.stats[STARSIGN_ID] = tk.StringVar()
        self.id = None  #0 Male, 1 Female, etc
        self.spell6Name = tk.StringVar()

    def asignarSpell6(self, *args):
        #args[0] : id y nombre
        spellId = spellsDic[args[0]] #id
        self.stats[SPELL6_ID].set(spellId)

        textShow = str(spellId) +'-' + spells[spellId].name[0:3]
        self.spell6Name.set(textShow) #seteo solo el id, para que no sea tan largo.
        #todo poner nombre. Si es muy largo, trimear
        return



##Defino diccionario que guarda los offsets de cada stat en el .sav, relativo al offset del slot de pje


namesOff = 0x8040
char1Offset = 0x9050  #File1 ASKA
bestiaryOffset = 0x8780
bestiarySize = 0x6E
enciclopedymapdiaryOffset = 0x856E
enciclopedymapdiarySize = 0x1D
eggstatusOffset = 0x8BC0
magicEggAddress = 0x85BB
storyFlagsOffset = 0x85CB
storyFlagsSize = 0x54

#Genero de shujinkou y slots de personajes
genderAdressesHeader = [0x1A, 0x2C, 0x2D] #en el header global
charSlotsMain =  [0x800C, 0xAA48]   #en la region de cada file

#offsets de los duplicados y entre los datos de cada file
headerFileOffset = 0x50 #offset entre Files en el header global
offsetDuplicadoHeader = 0x1000

offsetDuplicado = 0x4000 #de cada file
offsetFiles = 0x8000 #Los datos de File2 están en dato de File 1 + 0x8000, y de File 3 en +2*0x8000


#Carta genérica de amigo
amigoLetter = bytes([
    0xA1, 0x87, 0x00, 0x00, 0x17, 0x5D, 0x0B, 0x3A, 0x01, 0x01, 0x68, 0x00, 0x0B, 0x00, 0x23, 0x00,
    0x2A, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x08, 0x00, 0x1F, 0x00,
    0x21, 0x00, 0x29, 0x00, 0x00, 0x00, 0x2B, 0x00, 0x1F, 0x00, 0x22, 0x00, 0x23, 0x00, 0x00, 0x00,
    0x20, 0x00, 0x37, 0x00, 0x00, 0x00, 0x01, 0x00, 0x13, 0x00, 0x0B, 0x00, 0x01, 0x00, 0x00, 0x00,
    0x49, 0x00, 0x00, 0x00, 0x01, 0xFF, 0x3F, 0x00, 0x3D, 0x00, 0x3F, 0x00, 0x40, 0x00, 0x00, 0x00,
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x34, 0x82,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
])
amigoLetter = bytearray(amigoLetter)


class Spell:
    def __init__(self, name, id, elemId, label):
        self.name = name
        self.id = id
        self.elemId = elemId
        self.label = label

elems_dic = {'Fire': 0, 'Wood': 1, 'Wind': 2, 'Earth': 3, 'Water': 4, 'Light': 5, 'Dark': 6,
           0:'Fire', 1: 'Wood', 2: 'Wind', 3: 'Earth', 4: 'Water', 5: 'Light', 6: 'Dark',
    'F':0, 'H':1, 'V': 2, 'T': 3, 'A':4, 'L': 5, 'O':6, 'S': 7  }

#Crear diccionario de spells (id, nombre y elemento)
# F = Fuego, H = Hierba, A = Agua, V = Viento, T = Tierra, L = Luz, O = Oscuridad, S = Sin
spellIdsNames = []
spellsDic = {}
spells = []

with open('spellIds.txt', mode = 'r') as d:
    lines = d.readlines()
    for line in lines:
        separada = line.partition('-')
        if(separada[2]==''): separada = line.partition(':')
        nombreElem = separada[2].strip() #saco el \n
        line = line[0:-3] #saco el \n y elem

        spellId = int(separada[0])
        spellName = nombreElem[0:-2]
        spellElem = nombreElem[-1]
        spellElemId = elems_dic[spellElem]
        spell = Spell(spellName, spellId, spellElemId,line )

        spellsDic[line] = spellId
        spellsDic[spellId] = line
        spellIdsNames.append(line)
        spells.append(spell)



class MagicalEditor:

    def __init__(self, root):

        ##VARIABLES A USAR:
        self.savPath = tk.StringVar() #String
        self.savData = None     #string de bytes
        self.characters = None #Array de pjes
        self.changesDone = None #Array de bools para cuando desbloqueas cosas (un array por file)
        self.labelsDoneGUI = None #AArray de StringVars para el slot actual, lo que se muestra en pantalla
        self.fileSelectedActual = None
        self.fileSelected = None # 0,1 o 2 para slots 1, 2 o 3. Un intvar ligado a los radiobox. Al hacer click cambia instantaneamente, mientras que selectedActual cambia solo cuando yo le digo (despues de actualizar los datos internos)
        self.mainFrame = None #tab de protas
        self.eggFrame = None #tab de egg char
        self.mainGenderActual = None #el del slot actual


        ##INTERFAZ GUI
        root.title("Magical Editor")

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        ##PESTAÑAS

        #Habilitamos y creamos pestañas
        self.tabsystem = ttk.Notebook(root, padding="3 3 12 12")
        self.mainFrame = ttk.Frame(self.tabsystem)
        self.eggFrame  = ttk.Frame(self.tabsystem)
        self.tabsystem.add(self.mainFrame, text = 'Main Characters')
        self.tabsystem.add(self.eggFrame, text = 'Egg Characters')
        self.tabsystem.grid(column=0, row = 0, sticky=(N, W, E, S), columnspan= 7)

        ##Controles Globales
        controlPanel = ttk.Frame(root, padding="1 1 1 1")
        controlPanel.grid(column=0, row=1, sticky=(W, S), columnspan = 10)
        #controlPanel.columnconfigure(0, weight=1, pad = 1)
        controlPanel.rowconfigure(0, weight=1, pad = 1000)
        #todo el pad este no anda por el que está en "suavizado general" abajo

        #File Select
        self.fileSelected = tk.IntVar(value=0)
        for i in range(3):
            filei = tk.Radiobutton(controlPanel, text = 'File '+ str(i+1), value = i, variable = self.fileSelected)
            filei.grid(column = 0, row = i+1, sticky = W )
        self.fileSelected.trace('w', self.cambiarSlot)


        #Main character Gender
        self.mainGenderActual = tk.IntVar()
        genders = ['Male', 'Female', 'Both']
        genderValues = [1,2,0]
        tk.Label(self.mainFrame, text =' Main character gender:').grid(column=10, row=0, sticky=(E,S))
        for i in range(3):
            genderButton = tk.Radiobutton(self.mainFrame, text = genders[i], value = genderValues[i], variable = self.mainGenderActual)
            genderButton.grid(column = 10, row = i+1, sticky = (W,N, E) )

        row = 1
        column =3


        #Boton Open .sav
        tk.Button(controlPanel, text='Open save file', command=self.open_sav).grid(column = column, row = row, sticky =  (N,S, W), columnspan = 2, padx = 20)
       # ttk.Label(controlPanel, textvariable=self.savPath).grid(column=column, row=row+1, columnspan=1, sticky=(W, E))

        #Boton Export .sav
        tk.Button(controlPanel, text='Export save file', command=self.export_sav).grid(column = column, row = row+1, sticky = (N,S, E, W), padx = 20)

        image = openImage('imgs/save.png', 40, 40)
        save_img = tk.Label(controlPanel, image=image)
        save_img.image = image
        save_img.grid(row=row+2, column=column)

        row = 1
        column =5

        #Botones de desbloquear cosas
        self.crearBotones(controlPanel)


        #Separador gráfico
        separator = ttk.Separator(root, orient='horizontal')
        separator.grid(row=1, sticky = (W, E, N))

        #Boton volver a dejar el save original
        imagenRedo = openImage('imgs/redo.png', 20,20)
        botonRedo = tk.Button(root, text = 'Redo', image = imagenRedo, command = self.undoChanges).grid( column = 2, row = 0, sticky = (N, E))
        self.img = imagenRedo
        tk.Label(root, text = '(Undo changes)').grid(column =1, row = 0, sticky = (N, E))



            ##PERSONAJES - TkVars

        #Vars de los personajes y los Entrybox
        self.crearPersonajes()
        char_fields = [ [None for _ in enumerate(CHAR_NAMES)] for _ in CHAR_STATS] #campos gui

        self.crearColumnas01LabelsyImg(self.mainFrame)
        self.crearColumnas01LabelsyImg(self.eggFrame)

        self.crearGuiEntries(self.mainFrame)
        self.crearGuiEntries(self.eggFrame)



        #Suavizadogeneral
        for child in controlPanel.winfo_children():
            padx = child.grid_info()['padx']
            child.grid_configure(padx= padx + 5, pady=5)
        for child in self.mainFrame.winfo_children():
            child.grid_configure(padx=9, pady=2)
        for child in self.eggFrame.winfo_children():
            child.grid_configure(padx=9, pady=2)


        #feet_entry.focus()
        #root.bind("<Return>", self.calculate)

    #Botones desbloquear cosas
    def crearBotones(self,controlPanel):

        row = 1
        column =5

        botonBestiario = tk.Button(controlPanel, text= "Unlock Bestiary", command= self.desbloquearBestiario).grid(column = column, row = row, sticky = (N, S, W), padx = 0)
        img = openImage('imgs/bestiary.png', 25,25)
        self.im = img
        logo = tk.Label(controlPanel, image=img)
        logo.grid(column = column-1, row = row, sticky = E)



        botonMapaEnciclopediaDiario = tk.Button(controlPanel, text= "Unlock Maps/Diary/Encl", command= self.desbloquearMapas).grid(column = column, row = row+1, sticky = (N, S, W, E))
        img = openImage('imgs/map.png', 25,25)
        self.im2 = img
        logo = tk.Label(controlPanel, image=img)
        logo.grid(column = column-1, row = row+1, sticky = E)


        botonEggs = tk.Button(controlPanel, text= "Unlock Egg Characters", command= self.desbloquearHuevos).grid(column = column, row = row+2, sticky = (N, S, W, E))
        img = openImage('imgs/egg.png', 25,25)
        self.im3 = img
        logo = tk.Label(controlPanel, image=img)
        logo.grid(column = column-1, row = row+2, sticky = E)


        botonAmigoItems = tk.Button(controlPanel, text= "Unlock Amigo Items", command= self.desbloquearAmigoItems).grid(column = column+3, row = row, sticky = (N, S))
        img = openImage('imgs/amigo3.png', 30,25)
        self.im4 = img
        logo = tk.Label(controlPanel, image=img)
        logo.grid(column = column+2, row = row, sticky = W) #columnspan = 2")


        botonFlags = tk.Button(controlPanel, text= "Reset Story Flags (Buggy)", command= self.resetearStoryFlags).grid(column = column+3, row = row+1, sticky = (N, S))


            #Textos de al hacer click en boton
        self.changesDone = [ [ False for _ in range(6)] for file in range(3)]
        self.labelsDoneGUI = []
        for fila in range(3): #primeras 3 columnas
            label= tk.Label(controlPanel, text = '')
            label.grid(column = column+1, row = row+fila)
            self.labelsDoneGUI.append(label)
        for fila in range(3): #siguientes 3 columnas
            label= tk.Label(controlPanel, text = '')
            label.grid(column = column+4, row = row+fila, padx= 40)
            self.labelsDoneGUI.append(label)




    def crearRowNombres(self, tab):
        #Label nombres
        ttk.Label(tab, text='NAME').grid(column=0, row=1, sticky=W)
        #Imagen nombres
        filename = path + r'imgs\name.png'
        image = openImage(filename, 40, 20)
        name_entry_img = tk.Label(tab, image=image)
        name_entry_img.image = image
        name_entry_img.grid(row=1, column=1) #, rowspan=1, padx=5, pady=5)

    def crearRowStarsigns(self, tab):
        #Label Starsign
        ttk.Label(tab, text='Star').grid(column=0, row=2, sticky=W)
        #Imagen Starisgn Select
        filename = path + r'imgs\elemSelect.png'
        image = openImage(filename, 20, 20)
        starsign_img = tk.Label(tab, image=image)
        starsign_img.image = image
        starsign_img.grid(row=2, column=1) #, rowspan=1, padx=5, pady=5)
        #Imagenesde starsigns
        star_imgs = []
        for elem_id in range(8):
            star_imgs.append(openImage(path+r'imgs\elem' + str(elem_id) +'.png', 20, 20))
        self.star_imgs = star_imgs #Si no lo guardo, se pierde por el garbage collector luego



    def crearColumnas01LabelsyImg(self, tab):

        self.crearRowNombres(tab) #string Fields
        self.crearRowStarsigns(tab) #Option Menu Fields

        #Primer y segunda columna con nombre y foto de stats
        for stat in CHAR_STATS:
            if(stat.id <0): continue

            row = 3+stat.id

            #Columa 0: Texto
            ttk.Label(tab, text=stat.name).grid(column=0, row=row, sticky=W) #Nombre (texto)

            #Columa 1: Imagen:
            filename = path + r"imgs\stat" + str(stat.id) + ".png" #r"C:\Users\Graciela\Downloads\Games\Romhack\gui editor\imgs\stat" + str(stat.value) + ".png"
            image = openImage(filename, 20, 20)

            stat_img = tk.Label(tab, image=image)#self.fields_img[statid] = tk.Label(mainframe, image=image)
            stat_img.image = image #Tengo que resguardar la iamgen del recolector de basura para que se muestre
            stat_img.grid(row=row, column=1) #, rowspan=1, padx=5, pady=5)




    def crearGuiEntries(self, tab):

        #Fila 0 : Char Portraits
        #Fila 1: Char Name Entry
        #Fila 2: Char Starsign
        #Fila 3: Stats Numéricos

        if tab == self.mainFrame:
            chars = self.characters[:7]
        if tab == self.eggFrame:
             chars = self.characters[7:]

        #Imagenes de elementos (para starsign y 6th spell)
        elemImgs_dic, spellImgs_dic = self.asignarImgsStarsigns()

        #Matriz con nombres de pjes, portraits y sus stats
        for char in chars:
            c = char.id+2

            ##Fila 0: Foto de pje
            portrait_path = path + r'imgs\\char' + str(char.id) + ".png"
            image = openImage(portrait_path, 40, 40)
                #Poner
            char_portrait = tk.Label(tab, image=image)
            char_portrait.image = image #Tengo que repetir esto para que se muestre
            char_portrait.grid(row=0, column=c, sticky = W) #, rowspan=1, padx=5, pady=5)

            ##Fila 1: Nombre de pje
            ttk.Entry(tab, text='', width = 7, textvariable = char.name).grid(column=c, row=1, sticky=(W,E))

            ##Fila 2: Selección de Starsign
            elem_menu = tk.OptionMenu(tab, char.stats[STARSIGN_ID] , 'Fire', 'Wood', 'Wind', 'Earth', 'Water', 'Light', 'Dark')
            menu = elem_menu.nametowidget(elem_menu.menuname)
            for label, image in elemImgs_dic.items():
                menu.entryconfigure(label, image= image, compound = 'left')
            elem_menu.grid(row=2, column = c, sticky= W)
            #self.ponerImagen(path, sizex, sizey, tab, row, column)



            ##Fila >= 3:  Resto de los stats numéricos
            for stat in CHAR_STATS:
                if stat.id<0: continue

                if(stat.id != SPELL6_ID):

                    field = ttk.Entry(tab, width=3, textvariable=char.stats[stat.id])
                    validate_command =tab.register(only_numeric_input)
                    field.configure(validate="key",validatecommand=(validate_command,'%P'))  #Que solo permita numeros

                #6th Spell: Menu desplegable en vez de text/num entry
                if(stat.id == SPELL6_ID):
                    field.forget()
                    field = tk.OptionMenu(tab, char.spell6Name, 'Empty',  *spellIdsNames, command = char.asignarSpell6)
                    field.configure(font =('Calibri', 10) )
                    #field['menu'].configure(font = ('Calibri', 5))

                    menu = field.nametowidget(field.menuname)
                    for label, image in spellImgs_dic.items():
                        menu.entryconfigure(label, image= image, compound = 'left')

                field.grid(column=c, row=3+stat.id, sticky=(W, E))

    def ponerImagen(self, path, sizex, sizey, tab, row, column):

        image = openImage(path, sizex, sizey)
        imagen = tk.Label(tab, image=image)
        imagen.image = image
        imagen.grid(row=row, column=column) #, rowspan=1, padx=5, pady=5)
        return imagen

    def asignarImgsStarsigns(self):
        simg = self.star_imgs

        #Nombre de elemento e imagen
        elemImgs_dic =  {'Fire': simg[0], 'Wood': simg[1], 'Wind': simg[2], 'Earth': simg[3], 'Water': simg[4], 'Light': simg[5], 'Dark': simg[6]}

        #nombre de spell e imagen
        spellImgs_dic = {}
        for spell in spells:
            spellImgs_dic[spell.label] = simg[spell.elemId]

        return elemImgs_dic,spellImgs_dic


    #Llamado al abrir un .sav por primera vez
    def open_sav(self):
        from tkinter import filedialog
        filename = filedialog.askopenfilename(title='Select file')
        if(filename== ''): return
        self.savPath.set(filename)
        d = open(filename, mode = 'rb')
        self.savData = bytearray(d.read())
        d.close()
        self.fileSelectedActual = self.fileSelected.get()

        #Pongo los labels, todos en 0
        for file in range(0,3):
            for i in range(len(self.changesDone[0])):
                self.changesDone[file][i] = False
                self.setearLabelChangeDone(i, write = False)

        self.readload_characters()

    #LLamado al leer los datos de un slot (1,2 o 3)
    def readload_characters(self, *args):

        #Leo los datos del slot al que voy
        for char in self.characters:
            self.readload_stats_char(char) #stats numéricos, incluido Starsign
            self.readload_name(char) #Nombre

        #Leo el genero de shujinkoo
        #Veo si le puse dos mains (slot #2 tiene a Male/Female)
        if(self.readBytes(genderAdressesHeader[0]+1, 1, offsetFile = headerFileOffset) in [1, 2]): genero =0
        else: genero = self.readBytes(genderAdressesHeader[0], 1, offsetFile = headerFileOffset)

        self.mainGenderActual.set(genero)

        #Pongo los labels de cambios hechos en este slot
        for i in range(len(self.labelsDoneGUI)): self.setearLabelChangeDone(i, write = False)

    #guardo los cambios que hice en el slot actual y paso a leer el seleccionado
    def cambiarSlot(self, *args):
        if(self.savData != None): self.updateSavData()

        self.fileSelectedActual = self.fileSelected.get()
        if(self.savData != None): self.readload_characters()


    #LLamdo al exportar el .sav editando actual a un nuevo archivo
    def export_sav(self):
        if(self.savData==None): return
        self.updateSavData()

        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(title='Select export Directory') + '.sav'
        d = open(filename, mode = 'wb')
        d.write(self.savData)
        d.close()

        magicalChecksum.correct_magical_checksums(filename)

    #Creación de personajes. Llamado solo una vez, al correr el editor
    def crearPersonajes(self):
        self.characters = []

        for i in range(14):
            char = Character()
            self.characters.append(char)
            char.offset = char1Offset + i*0x50
            char.id = i
        self.characters[1].name = self.characters[0].name #Linkeo los nombres de Male y Female


    #Se llama al leer los datos del slot que esté seleccionado
    def readload_stats_char(self, char):

        for stat in CHAR_STATS: #LVL, MAX HP, Max MP, Pow to Agi
            stat_val = self.readBytes(char.offset + stat.offset, stat.nBytes)
            #Estoy dejando 4bytes de lectura para los stats... tencnicamente los dos mas significativos son siempre 0, y los stats en si capean en 255 en la pantalla de estados. Si numeros mas altos son tomados en cuenta no sé... pero para no hacer un if de si es stat de HP o de POWetc, leo siempre de a 4 y listo. Sino ver la versión 6, que ahi estaba bien, antes de leer max hp y mp

            stat_val = stat_val >> stat.bits_descarte

            if stat.id == STARSIGN_ID:
                stat_val = elems_dic[stat_val]

            char.stats[stat.id].set(stat_val)

        #char.spell6Name.set(spellsDic[char.stats[SPELL6_ID].get()]) # nombre completo, muy largo
        char.spell6Name.set(char.stats[SPELL6_ID].get())


     #Se llama al leer los datos del slot que esté seleccionado
    #Recordar que el almacenamiento de nombres es distinto al de stats, y que solo se guarda el nombre de un Shujinkoo y no de Male y Female
    def readload_name(self,char):
        if char.id == 0 : chari = 0
        if char.id == 1 : return
        if char.id >= 2 : chari = char.id-1

        name_bytes = self.readBytes(namesOff+ chari*0x10,8*2)
        name_string = characterTable2.readName(name_bytes)
        char.name.set(name_string)


    #Se llama al exportar los datos a un .sav o al cambiar de un archivo (1,2,3) a otro
    #Lee todos los datos que introdujiste y los carga al .sav interno
    def updateSavData(self):
        for char in self.characters: self.updateCharacterData(char)
        self.updateGender()

    #Se llama con la función de arriba
    def updateCharacterData(self, char):
        i=0

        for stat in CHAR_STATS:
            stat_val = char.stats[stat.id].get()
            max_val = (2**(stat.nBytes*8 - stat.bits_descarte))-1
            if(stat.id == STARSIGN_ID): stat_val = elems_dic[stat_val]
            stat_val = min(stat_val, max_val)
            val = (stat_val << stat.bits_descarte).to_bytes(stat.nBytes,'little') #Shift de 4 bits, porque en el juego se toman solo 12 bits para la parte entera (el resto es valor decimal, no me voy a calentar de implementarlo , ,aunque seria divertido usar un pje con 0,5 o 0,75 de vida)
            self.writeBytes(char.offset + stat.offset, val, stat.nBytes)

            i+=1


        #Nombre
        if(char.id ==1): return
        nombre = char.name.get()
        nombre = nombre[:8] #trim length sobrante
        nombre_bytes = characterTable2.makeName(nombre)
        if(char.id>=2): chari = char.id-1
        if(char.id ==0): chari = 0
        self.writeBytes(namesOff+ chari*0x10,nombre_bytes, 8*2)

    #Llamado con la funcin de arriba. Al cambiar de slot o antes de exportar el .sav
    def updateGender(self):
        #Genero
        genero = self.mainGenderActual.get()

        #Si es Male o Female, lo escribo directamente
        if(genero == 1 or genero == 2):
            self.escribirGeneroSlotPje(genero, 0) #escribo en el slot de shujinkou


        #Si son ambos, en el slot de Lassi meto al otro prota
        elif(genero == 0):
            genero_canonico = self.readBytes(genderAdressesHeader[0], 1, offsetFile = headerFileOffset)
            if(genero_canonico == 1): otro_genero = 2
            if(genero_canonico == 2): otro_genero = 1
            self.escribirGeneroSlotPje(otro_genero, 1)

    #mete a Male/Female en el slot de pje 0 1 2 3 etc a elección
    #genero 1 = Male, 2= Female
    def escribirGeneroSlotPje(self, genero, slot):
        genero = genero.to_bytes(1,'little')

        #Se escribe en el header global y en el header del slot
        for address in genderAdressesHeader:
            self.writeBytes(address+slot, genero, 1,offsetDuplicadoHeader, headerFileOffset)

        for address in charSlotsMain:
            self.writeBytes(address+slot, genero, 1,offsetFiles)


    #Desbloquea bestiario, enciclopedia, y diario
    def desbloquearBestiario(self):
        checkAll = [0xFF for _ in range(bestiarySize)]
        self.writeBytes(bestiaryOffset, checkAll, bestiarySize)
        self.setearLabelChangeDone(0,write = True)
        return

    #Desbloquea mapas y warp points (no de Neumann)
    #Todo desbloquear de neumann, diary no anda aun
    def desbloquearMapas(self):
        checkAll = [0xFF for _ in range(enciclopedymapdiarySize)]
        self.writeBytes(enciclopedymapdiaryOffset , checkAll, enciclopedymapdiarySize)
        self.setearLabelChangeDone(1, write = True)
        return

    def resetearStoryFlags(self):
        checkAll = [0x0 for _ in range(storyFlagsSize)]
        self.writeBytes(storyFlagsOffset,checkAll, storyFlagsSize)
        self.setearLabelChangeDone(4, write = True)
        return

    #desbloquea Amigo Figurines (para contra Macadameus), Frogs
    def desbloquearAmigoItems(self):

        addresses = []

        #Frogs
        for address in range(0x820E, 0x828B, 2):
            addresses.append(address)

        #Figurines
        for address in range(0x820E, 0x828B, 2):
            addresses.append(address)

        #Balls
        for address in range(0x8186, 0x818F, 2):
            addresses.append(address)

        #Spell Books (Amigo Book)
        for address in range(0x817E, 0x817E+2, 2):
            addresses.append(address)

        #Key Items
        for address in range(0x811A, 0x8142, 2):
            addresses.append(address)

        #Equipment (Egg & Justice Sets)
        for address in range(0x848A, 0x849D, 2):
            addresses.append(address)

        #Equipment (Luck Set)
        for address in range(0x843A, 0x8443, 2):
            addresses.append(address)

        #Equipment (Magic Set)
        for address in range(0x8476, 0x847F, 2):
            addresses.append(address)

        #Equipment (Force Set)
        for address in range(0x8458, 0x8462, 2):
            addresses.append(address)

        #Equipment (Shiny Watch)
        for address in range(0x82EA, 0x82EA+2, 2):
            addresses.append(address)

        #Battle Items (Jewel Bombs )
        for address in range(0x81D4, 0x81DD, 2):
            addresses.append(address)

        #Battle Items (Jellies )
        for address in range(0x81E8, 0x81F1, 2):
            addresses.append(address)

        #Escribir x77 en todo lo anterior:
        for address in addresses:
            data = 0x4D.to_bytes(2,'little')
            self.writeBytes(address, data, 2)

        self.setearLabelChangeDone(3, write = True)

        self.ponerCartasAmigo()

        return


    #poner 100 cartas de amigo
    #esto es para el Amigo parade
    def ponerCartasAmigo(self):
        letterOffset = 0x2080 #primer carta de amigo
        letterSize  = 120 #bytes

        #77 =  0100 1101 ,  en 2do y 3er byte de letter
        amigoLetter[1] |= 0b00000000  #cantidad de encuentros = 77
        amigoLetter[2] |= 0b00010011  #cantidad de encuentros = 77
        amigoLetter[12:28] = characterTable2.makeName('ASKA') # name = ASKA
        amigoLetter[2] &= 0b00011111

        diseño = 0 #de 0 a 7
        id = 7777
        element = 0
        gender = 1
        for i in range(100):
            letter = amigoLetter.copy()
            letter[2]  |=  (diseño<< 5) #tarjetas
            letter[110:112] = id.to_bytes(2,'little')  #secret id (uno cualquiera)
            letter[0] |= element << 3 #elemento
            letter[8] = gender
            letter[9] = gender #todo probar... si acá meto un 7... quien aparece para pegar?

            id += 1
            diseño = (diseño +1) % 8
            element = 1 - element #0 o 1
            gender =  gender %2 + 1 #1 o 2
            self.writeBytes(letterOffset+letterSize*i, letter, letterSize, dup_offset = 0x3000, offsetFile = 0)


    def desbloquearHuevos(self):
        if(self.savData == None): return
        for egg_id in range(7):
            off = eggstatusOffset+ egg_id*0x10 + self.fileSelectedActual*offsetFiles
            offdup = eggstatusOffset
            byte1, byte2 = self.savData[off: off+2]
            byte2 |=0b00000011
            byte1 |=0b00000011
            #byte1 |=0b10000000
            data = ((byte1<<8) + byte2).to_bytes(2,'little')
            self.writeBytes(off, data, 2)
            self.writeBytes(magicEggAddress, 0xFF.to_bytes(1,'little'), 1)
            self.writeBytes(magicEggAddress+1, 0xFF.to_bytes(1,'little'), 1)


        self.setearLabelChangeDone(2, write = True)
        return

    #todo todoooo
    def desbloquearTodo(self):
        return


    def setearLabelChangeDone(self, id, write = False):
        if(self.savData ==None): return
        if(write): self.changesDone[self.fileSelectedActual][id] = True
        if(self.changesDone[self.fileSelectedActual][id]):
            self.labelsDoneGUI[id].configure(text= 'Done!')
        else: self.labelsDoneGUI[id].configure(text = '')


    #Llamada al apretar el boton de undo. Deja los stats como estaban en el archivo original
    def undoChanges(self):
        if(self.savData == None):return
        with open(self.savPath.get(), mode = 'rb') as d:
            self.savData = bytearray(d.read())
        self.readload_characters()
        for label in self.labelsDoneGUI: label.configure(text='')


    #Lee bytes como si representaran un uint, ojo!
    def readBytes(self, offset, nBytes, offsetFile = offsetFiles):

        offset += offsetFile*self.fileSelectedActual

        data= self.savData[offset: offset+nBytes]

        if(nBytes ==1): val= data[0]

        #Read Little Endian
        if(nBytes == 2):  val = data[0] +  (data[1] << 8)

        if(nBytes == 4): val =  data[0] +  (data[1] << 8) +  (data[2] << 16) +  (data[3] << 24)

        if(nBytes not in [1,2,4]): val = data #estas leyendo un chunk grande para procesar aparte, lo devuelvo asi nomas

        return val

    def writeBytes(self, address, val, nBytes, dup_offset = offsetDuplicado, offsetFile = offsetFiles):

        if(self.savData==None): return

        address += offsetFile*self.fileSelectedActual
        self.savData[address : address+nBytes] = val
        self.savData[address+dup_offset : address+dup_offset+nBytes] = val #file duplicado




from PIL import ImageTk, Image

def openImage(path, sizeX, sizeY):
    from PIL import Image, ImageTk #Con esto puedo resizear la imagen

    image = Image.open(path)
    image = image.resize((sizeX,sizeY))
    image = ImageTk.PhotoImage(image)
    return image


def only_numeric_input(input):
    #this is allowing all numeric input and backspace to work
    if input.isdigit() or input =="": return True
    else:  return False

def only_numeric_input(input):
    #this is allowing all numeric input and backspace to work
    if input.isdigit() or input =="": return True
    else:  return False




root = tk.Tk()
root.geometry("900x560+300+150")
root.resizable(width=True, height=True)
MagicalEditor(root)
root.mainloop()