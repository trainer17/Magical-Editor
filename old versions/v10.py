#Otro buen ejemplo: https://www.pythonguis.com/tutorials/create-ui-with-tkinter-grid-layout-manager/

#todo egg characters (segunda solapa por ej) con un enable/disable de todos, cambiar genero, asignar male/Female a slots, desbloquear todos los warp points, desbloquear todo bestiario
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


class MagicalEditor:

    def __init__(self, root):

        ##VARIABLES A USAR:
        self.savPath = tk.StringVar() #String
        self.savData = None     #string de bytes
        self.characters = None #Array de pjes



        ##CODIGO DATOS
        #self.open_sav()


        ##INTERFAZ GUI
        root.title("Magical Editor")

        global mainframe #esto es por pajero y no haberlo hecho self.mainframe antes
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

            #Boton Open .sav
        row = 12
        tk.Button(mainframe, text='Open save file', command=self.open_sav).grid(column = 3, row = row, sticky = S)
        ttk.Label(mainframe, textvariable=self.savPath).grid(column=4, row=row, columnspan=10, sticky=(W, E))

            #Boton Export .sav
        row = 12
        tk.Button(mainframe, text='Export save file', command=self.export_sav).grid(column = 5, row = row, sticky = S)

            ##PERSONAJES - TkVars

        #Vars de los personajes y los Entrybox
        self.crearPersonajes()
        char_fields = [ [None for _ in enumerate(CHAR_NAMES)] for _ in CHAR_STATS] #campos gui

        self.crearColumnas01LabelsyImg()
        self.crearGuiEntries()


        #Suavizadogeneral
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        #feet_entry.focus()
        #root.bind("<Return>", self.calculate)

        ##LLENAR GUI
        #self.mostrar_stats_chars()

    def crearRowNombres(self):
        #Label nombres
        ttk.Label(mainframe, text='NAME').grid(column=0, row=1, sticky=W)
        #Imagen nombres
        filename = path + r'imgs\name.png'
        image = openImage(filename, 40, 20)
        name_entry_img = tk.Label(mainframe, image=image)
        name_entry_img.image = image
        name_entry_img.grid(row=1, column=1) #, rowspan=1, padx=5, pady=5)

    def crearRowStarsigns(self):
        #Label Starsign
        ttk.Label(mainframe, text='Star').grid(column=0, row=2, sticky=W)
        #Imagen Starisgn Select
        filename = path + r'imgs\elemSelect.png'
        image = openImage(filename, 20, 20)
        starsign_img = tk.Label(mainframe, image=image)
        starsign_img.image = image
        starsign_img.grid(row=2, column=1) #, rowspan=1, padx=5, pady=5)
        #Imagenesde starsigns
        star_imgs = []
        for elem_id in range(7):
            star_imgs.append(openImage(path+r'imgs\elem' + str(elem_id) +'.png', 20, 20))
        self.star_imgs = star_imgs #Si no lo guardo, se pierde por el garbage collector luego



    def crearColumnas01LabelsyImg(self):

        self.crearRowNombres() #string Fields
        self.crearRowStarsigns() #Option Menu Fields

        #Primer y segunda columna con nombre y foto de stats
        for stat in CHAR_STATS:
            if(stat.id <0): continue
            row = 3+stat.id
            #Columa 0: Texto
            ttk.Label(mainframe, text=stat.name).grid(column=0, row=row, sticky=W) #Nombre (texto)

            #Columa 1: Imagen:

            filename = path + r"imgs\stat" + str(stat.id) + ".png" #r"C:\Users\Graciela\Downloads\Games\Romhack\gui editor\imgs\stat" + str(stat.value) + ".png"
            image = openImage(filename, 20, 20)

            stat_img = tk.Label(mainframe, image=image)#self.fields_img[statid] = tk.Label(mainframe, image=image)
            stat_img.image = image #Tengo que repetir esto para que se muestre
            stat_img.grid(row=row, column=1) #, rowspan=1, padx=5, pady=5)


    def crearGuiEntries(self):

        #Fila 0 : Char Portraits
        #Fila 1: Char Name Entry
        #Fila 2: Char Starsign
        #Fila 3: Stats Numéricos

        #Matriz con nombres de pjes, portraits y sus stats
        for char in self.characters:
            c = char.id+2

            ##Fila 0: Foto de pje
            portrait_path = path + r'imgs\char' + str(char.id) + ".png"
            image = openImage(portrait_path, 40, 40)
                #Poner
            char_portrait = tk.Label(mainframe, image=image)
            char_portrait.image = image #Tengo que repetir esto para que se muestre
            char_portrait.grid(row=0, column=c, sticky = W) #, rowspan=1, padx=5, pady=5)

            ##Fila 1: Nombre de pje
            ttk.Entry(mainframe, text='', width = 7, textvariable = char.name).grid(column=c, row=1, sticky=(W,E))

            ##Fila 2: Selección de Starsign
            simg = self.star_imgs
            elemImgs_dic = {'Fire': simg[0], 'Wood': simg[1], 'Wind': simg[2], 'Earth': simg[3], 'Water': simg[4], 'Light': simg[5], 'Dark': simg[6]}
            elem_menu = tk.OptionMenu(mainframe, char.stats[-1] , 'Fire', 'Wood', 'Wind', 'Earth', 'Water', 'Light', 'Dark')
            menu = elem_menu.nametowidget(elem_menu.menuname)
            for label, image in elemImgs_dic.items():
                menu.entryconfigure(label, image= image, compound = 'left')
            elem_menu.grid(row=2, column = c, sticky= W)

            #Resto de los stats numéricos
            for stat in CHAR_STATS:
                if stat.id<0: continue
                field = ttk.Entry(mainframe, width=3, textvariable=char.stats[stat.id])
                validate_command =mainframe.register(only_numeric_input)

                field.configure(validate="key",validatecommand=(validate_command,'%P'))  #Que solo permita numeros
                field.grid(column=c, row=3+stat.id, sticky=(W, E))





    def calculate(self, *args):
        try:
            value = float(self.feet.get())
            self.meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
        except ValueError:
            pass

    #Todo: Cargar un file dummy al abrir?
    def open_sav(self):
        from tkinter import filedialog
        filename = filedialog.askopenfilename(title='Select file')
        self.savPath.set(filename)
        d = open(filename, mode = 'rb')
        self.savData = bytearray(d.read())
        d.close()

        for char in self.characters:
            self.readload_stats_char(char) #stats numéricos, incluido Starsign
            self.readload_name(char) #Nombre

    def export_sav(self):
        self.updateSavData()

        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(title='Select export Directory') + '.sav'
        d = open(filename, mode = 'wb')
        d.write(self.savData)
        d.close()

        magicalChecksum.correct_magical_checksums(filename)


    def crearPersonajes(self):
        self.characters = []

        for i in range(7):
            char = Character()
            self.characters.append(char)
            char.offset = char1Offset + i*0x50
            char.id = i
        self.characters[1].name = self.characters[0].name #Linkeo los nombres de Male y Female


    #Se llama al leer un .sav externo por primera vez
    def readload_stats_char(self, char):

        for stat in CHAR_STATS: #LVL, MAX HP, Max MP, Pow to Agi
            stat_val = readBytes(self.savData, char.offset + stat.offset, stat.nBytes)
            #Estoy dejando 4bytes de lectura para los stats... tencnicamente los dos mas significativos son siempre 0, y los stats en si capean en 255 en la pantalla de estados. Si numeros mas altos son tomados en cuenta no sé... pero para no hacer un if de si es stat de HP o de POWetc, leo siempre de a 4 y listo. Sino ver la versión 6, que ahi estaba bien, antes de leer max hp y mp

            stat_val = stat_val >> stat.bits_descarte

            if stat.id == STARSIGN_ID:
                stat_val = elems_dic[stat_val]

            char.stats[stat.id].set(stat_val)



    #Se llama al leer un .sav externo por primera vez
    #Recordar que el almacenamiento de nombres es distinto al de stats, y que solo se guarda el nombre de Shujinkoo
    def readload_name(self,char):
        if  char.id ==0 : chari = 0
        if char.id == 1 : return
        if char.id >=2  : chari = char.id-1

        name_bytes = readBytes(self.savData, namesOff+ chari*0x10,8*2)
        name_string = characterTable2.readName(name_bytes)
        char.name.set(name_string)


    #Se llama al exportar los datos a un .sav.
    #Lee todos los datos que introdujiste y los carga a un nuevo save
    def updateSavData(self):
        for char in self.characters: self.updateCharacterData(char)


    #Se llama al exportar. podria cambiarse el nombre a otro mas claro...
    def updateCharacterData(self, char):
        i=0
        offsetDuplicado = 0x4000

        for stat in CHAR_STATS:
            stat_val = char.stats[stat.id].get()
            if(stat.id == STARSIGN_ID): stat_val = elems_dic[stat_val]
            val = (stat_val << stat.bits_descarte).to_bytes(stat.nBytes,'little') #Shift de 4 bits, porque en el juego se toman solo 12 bits para la parte entera (el resto es valor decimal, no me voy a calentar de implementarlo , ,aunque seria divertido usar un pje con 0,5 o 0,75 de vida)
            writeBytes(self.savData, char.offset + stat.offset, val, stat.nBytes, offsetDuplicado)

            i+=1


        #Nombre
        #todo ver que hacer con el tema Male/Female. Acá solo tomo el de male
        if(char.id ==1): return
        nombre = char.name.get()
        nombre = nombre[:8] #trim length sobrante
        nombre_bytes = characterTable2.makeName(nombre)
        if(char.id>=2): chari = char.id-1
        if(char.id ==0): chari = 0
        writeBytes(self.savData, namesOff+ chari*0x10,nombre_bytes, 8*2,offsetDuplicado)



from PIL import ImageTk, Image
def open_img(path):
    image = tk.PhotoImage(file=path, master = root, height = 200, width=200)
    img = tk.Label(root, image=image)
    img.grid(row=7, column=7, rowspan=6, padx=5, pady=5)

    #img = Image.open(path)
    #img = img.resize((10, 10), Image.ANTIALIAS)
   # img = ImageTk.PhotoImage(img)


def readBytes(file, offset, nBytes, uint = True):
    data= file[offset: offset+nBytes]

    if(nBytes ==1): val= data[0]

    #Read Little Endian
    if(nBytes == 2):  val = data[0] +  (data[1] << 8)

    if(nBytes == 4): val =  data[0] +  (data[1] << 8) +  (data[2] << 16) +  (data[3] << 24)

    if(nBytes not in [1,2,4]): val = data #estas leyendo un chunk grande para procesar aparte, lo devuelvo asi nomas

    return val

def writeBytes(file, address, val, nBytes, dup_offset):
    file[address : address+nBytes] = val
    file[address+dup_offset : address+dup_offset+nBytes] = val #file duplicado

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
mainframe = None
root.geometry("800x500+300+150")
root.resizable(width=True, height=True)
MagicalEditor(root)
root.mainloop()