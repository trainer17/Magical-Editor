#Otro buen ejemplo: https://www.pythonguis.com/tutorials/create-ui-with-tkinter-grid-layout-manager/

#todo cambiar genero, asignar male/Female a slots, desbloquear todos los warp points, desbloquear   resetear flags de historia y cofres/leafs/items recogidos
#todo para que puedas abrir el mapa tenes que tener el flag de Erd Visitado activado. Hay un flag de "Planeta visitado" para cada planeta, independientemente de si aparece en Neumann o no
#todo recordar cambios al cambiar de file
#todo devolver .sav a su estado original
#todo imagen de los elementos de c/u
#todo desplegable de 6th spell. Sino, catch de error de overflow si es muy grande lo que le pasas (spinbox)
#todo idem catch de errores de numeros muy grandes
#todo poner de yapa un "play time" y "bira"?
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
    STAT('spellId',0x18+4*7, 1, 8, 0)
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
        self.stats[-1] = tk.StringVar()
        self.id = None  #0 Male, 1 Female, etc


elems_dic = {'Fire': 0, 'Wood': 1, 'Wind': 2, 'Earth': 3, 'Water': 4, 'Light': 5, 'Dark': 6,
           0:'Fire', 1: 'Wood', 2: 'Wind', 3: 'Earth', 4: 'Water', 5: 'Light', 6: 'Dark'}


##Defino diccionario que guarda los offsets de cada stat en el .sav, relativo al offset del slot de pje


namesOff = 0x8040
char1Offset = 0x9050  #File1 ASKA
bestiaryOffset = 0x8780
bestiarySize = 0x6E
enciclopedymapdiaryOffset = 0x856E
enciclopedymapdiarySize = 0x1D
eggstatusOffset = 0x8BC0
magicEggAddress = 0x85BB

offsetDuplicado = 0x4000

offsetSlots = 0x8000 #Los datos de Slot2 están en dato de Slot 1 + 0x8000, y de Slot 3 en +2*0x8000

class MagicalEditor:

    def __init__(self, root):

        ##VARIABLES A USAR:
        self.savPath = tk.StringVar() #String
        self.savData = None     #string de bytes
        self.characters = None #Array de pjes
        self.labelsDone = None #Array de StringVars para cuando desbloqueas cosas
        self.fileSelectedActual = None #1, 2 o 3. Un int
        self.fileSelected = None #1, 2 o 3. Un intvar ligado a los radiobox. Al hacer click cambia instantaneamente, mientras que selectedActual cambia solo cuando yo le digo (despues de actualizar los datos internos)
        self.mainFrame = None #tab de protas
        self.eggFrame = None #tab de egg char


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

        #File Select
        self.fileSelected = tk.IntVar(value=1)
        for i in range(1,4):
            filei = tk.Radiobutton(controlPanel, text = 'File '+ str(i), value = i, variable = self.fileSelected)
            filei.grid(column = 0, row = i, sticky = W )
        #todo preservar cambios al cambiar de File
        self.fileSelected.trace('w', self.cambiarSlot)

        row = 1
        column =3

        #Boton Open .sav
        tk.Button(controlPanel, text='Open save file', command=self.open_sav).grid(column = column, row = row, sticky =  (N,S, E), columnspan = 2, padx = 10000)
       # ttk.Label(controlPanel, textvariable=self.savPath).grid(column=column, row=row+1, columnspan=1, sticky=(W, E))

        #Boton Export .sav
        tk.Button(controlPanel, text='Export save file', command=self.export_sav).grid(column = column, row = row+1, sticky = (N,S, E, W))


        row = 1
        column =5

        #Botones desbloquear cosas
        botonBestiario = tk.Button(controlPanel, text= "Unlock Bestiary", command= self.desbloquearBestiario).grid(column = column, row = row, sticky = (N, S))
        botonMapaEnciclopediaDiario = tk.Button(controlPanel, text= "Unlock Maps/Diary/Encl", command= self.desbloquearMapas).grid(column = column, row = row+1, sticky = (N, S)) #todo imagen
        botonEggs = tk.Button(controlPanel, text= "Unlock Egg Characters", command= self.desbloquearHuevos).grid(column = column, row = row+2, sticky = (N, S))

        #todo corregir el segundo que no anda

        self.labelsDone = []
        for i in range(4):
            label= tk.Label(controlPanel, text = '')
            label.grid(column = column+1, row = row+i)
            self.labelsDone.append(label)


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
            child.grid_configure(padx=5, pady=5)
        for child in self.mainFrame.winfo_children():
            child.grid_configure(padx=9, pady=2)
        for child in self.eggFrame.winfo_children():
            child.grid_configure(padx=9, pady=2)


        #feet_entry.focus()
        #root.bind("<Return>", self.calculate)


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
        for elem_id in range(7):
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
            simg = self.star_imgs
            elemImgs_dic = {'Fire': simg[0], 'Wood': simg[1], 'Wind': simg[2], 'Earth': simg[3], 'Water': simg[4], 'Light': simg[5], 'Dark': simg[6]}
            elem_menu = tk.OptionMenu(tab, char.stats[-1] , 'Fire', 'Wood', 'Wind', 'Earth', 'Water', 'Light', 'Dark')
            menu = elem_menu.nametowidget(elem_menu.menuname)
            for label, image in elemImgs_dic.items():
                menu.entryconfigure(label, image= image, compound = 'left')
            elem_menu.grid(row=2, column = c, sticky= W)

            #Resto de los stats numéricos
            for stat in CHAR_STATS:
                if stat.id<0: continue
                field = ttk.Entry(tab, width=3, textvariable=char.stats[stat.id])
                validate_command =tab.register(only_numeric_input)

                field.configure(validate="key",validatecommand=(validate_command,'%P'))  #Que solo permita numeros
                field.grid(column=c, row=3+stat.id, sticky=(W, E))


    #Llamado al abrir un .sav por primera vez
    def open_sav(self):
        from tkinter import filedialog
        filename = filedialog.askopenfilename(title='Select file')
        self.savPath.set(filename)
        d = open(filename, mode = 'rb')
        self.savData = bytearray(d.read())
        d.close()
        self.fileSelectedActual = self.fileSelected.get()
        self.readload_characters()

    #LLamado al leer los datos de un slot (1,2 o 3)
    def readload_characters(self, *args):

        #Leo los datos del slot al que voy
        for char in self.characters:
            self.readload_stats_char(char) #stats numéricos, incluido Starsign
            self.readload_name(char) #Nombre

        for label in self.labelsDone: label.configure(text='')


    #guardo los cambios que hice en el slot actual y paso a leer el seleccionado
    def cambiarSlot(self, *args):
        if(self.savData != None): self.updateSavData()

        self.fileSelectedActual = self.fileSelected.get()
        self.readload_characters()


    #LLamdo al exportar el .sav editando actual a un nuevo archivo
    def export_sav(self):
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


     #Se llama al leer los datos del slot que esté seleccionado
    #Recordar que el almacenamiento de nombres es distinto al de stats, y que solo se guarda el nombre de un Shujinkoo y no de Male y Female
    def readload_name(self,char):
        if  char.id ==0 : chari = 0
        if char.id == 1 : return
        if char.id >=2  : chari = char.id-1

        name_bytes = self.readBytes(namesOff+ chari*0x10,8*2)
        name_string = characterTable2.readName(name_bytes)
        char.name.set(name_string)


    #Se llama al exportar los datos a un .sav o al cambiar de un archivo (1,2,3) a otro
    #Lee todos los datos que introdujiste y los carga a un nuevo save
    def updateSavData(self):
        for char in self.characters: self.updateCharacterData(char)


    #Se llama con la función de arriba
    def updateCharacterData(self, char):
        i=0

        for stat in CHAR_STATS:
            stat_val = char.stats[stat.id].get()
            if(stat.id == STARSIGN_ID): stat_val = elems_dic[stat_val]
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



    #Desbloquea bestiario, enciclopedia, y diario
    def desbloquearBestiario(self):
        checkAll = [0xFF for _ in range(bestiarySize)]
        self.writeBytes(bestiaryOffset, checkAll, bestiarySize)
        self.labelsDone[0].configure(text = 'Done!')
        return

    #Desbloquea mapas y warp points (no de Neumann)
    #Todo desbloquear de neumann, diary no anda aun
    def desbloquearMapas(self):
        checkAll = [0xFF for _ in range(enciclopedymapdiarySize)]
        self.writeBytes(enciclopedymapdiaryOffset , checkAll, enciclopedymapdiarySize)
        self.labelsDone[1].configure(text = 'Done!')
        return

    def desbloquearEquipamientoFigurinesAmigo(self):

        return

    def desbloquearHuevos(self):
        for egg_id in range(7):
            off = eggstatusOffset+ egg_id*0x10
            byte1, byte2 = self.savData[off: off+2]
            byte2 |=0b00000011
            byte1 |=0b00000011
            #byte1 |=0b10000000
            self.savData[off: off+2] = [byte1, byte2]
            self.savData[magicEggAddress] = 0xFF

        self.labelsDone[2].configure(text = 'Done!')
        return

    #Llamada al apretar el boton de undo. Deja los stats como estaban en el archivo original
    def undoChanges(self):
        if(self.savData == None):return
        with open(self.savPath.get(), mode = 'rb') as d:
            self.savData = bytearray(d.read())
        self.readload_characters()


    #Lee bytes como si representaran un uint, ojo!
    def readBytes(self, offset, nBytes):

        offset += offsetSlots*(self.fileSelectedActual-1)

        data= self.savData[offset: offset+nBytes]

        if(nBytes ==1): val= data[0]

        #Read Little Endian
        if(nBytes == 2):  val = data[0] +  (data[1] << 8)

        if(nBytes == 4): val =  data[0] +  (data[1] << 8) +  (data[2] << 16) +  (data[3] << 24)

        if(nBytes not in [1,2,4]): val = data #estas leyendo un chunk grande para procesar aparte, lo devuelvo asi nomas

        return val

    def writeBytes(self, address, val, nBytes, dup_offset = offsetDuplicado):
        address += offsetSlots*(self.fileSelectedActual-1)
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