#Otro buen ejemplo: https://www.pythonguis.com/tutorials/create-ui-with-tkinter-grid-layout-manager/
print(__file__)

#todo agregar modificacion de starsigns, egg characters (segunda solapa por ej) con un enable/disable de ellos en la naves, cambiar genero, etc
import tkinter as tk
from tkinter import ttk
from tkinter import N,W,E,S

import characterTable2
path = __file__[:-5]

import enum
class Character_fields(enum.IntEnum):
    HP = 0
    MP = enum.auto()
    STR = enum.auto()
    DEF = enum.auto()
    IQ = enum.auto()
    SPRI = enum.auto()
    AGI = enum.auto()
    spellId = enum.auto()
    MPP = enum.auto()


class CHAR_NAMES(enum.IntEnum): #Todo renombrar a "char_names"
    MALE = 0
    FEMALE = enum.auto()
    MOKKA = enum.auto()
    LASSI = enum.auto()
    PICO = enum.auto()
    CHAI = enum.auto()
    SORBET = enum.auto()

class Character:

    def __init__(self):
        self.offset = None
        self.NAME = None

pow_off = 0x20 #Offset del stat de POW, relativo al inicio del sectr de un pje
maxHP_off = 0x18 #Como pow
sixthSpellId_off = 0x14+pow_off #Offset del 6to spell relativo al inicio del pje
namesOff = 0x8040

class MagicalEditor:

    def __init__(self, root):

        ##VARIABLES A USAR:
        self.savPath = tk.StringVar() #String
        self.savData = None     #string de bytes
        self.char_fields = None #Matriz de entrybox para los stats. Puede volar, no necesito guardarlos
        self.char_stats = None #Matriz de IntVar, a cargar luego a los pjes a la hora de exportar
        self.char_names = None #Array de StringVar
        self.characters = None #Array de pjes


        ##CODIGO DATOS
        #self.open_sav()


        ##INTERFAZ GUI
        root.title("Magical Editor")

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

        #Matriz de IntVar de stats y sus campos
        self.char_stats = [[ tk.IntVar() for _ in enumerate(CHAR_NAMES)] for _ in enumerate(Character_fields)]
        self.char_fields = [ [None for _ in enumerate(CHAR_NAMES)] for _ in enumerate(Character_fields)] #campos gui

        #Array de Stringvar de nombres:
        self.char_names = []
        for namei in range(len(CHAR_NAMES)): self.char_names.append(tk.StringVar())

        #Label nombres
        ttk.Label(mainframe, text='NAME').grid(column=0, row=1, sticky=W) #Nombre (texto)
        #Imagen nombres
        filename = path + r'imgs\name.png' #r"C:\Users\Graciela\Downloads\Games\Romhack\gui editor\imgs\name.png"
        image = openImage(filename, 40, 20)
        name_entry_img = tk.Label(mainframe, image=image)
        name_entry_img.image = image
        name_entry_img.grid(row=1, column=1) #, rowspan=1, padx=5, pady=5)





            ##STATS -  GUI Entrys
        STAT_ROW = 0 #Fila del stat actual
        COLUMN0 = 0 #Primer columna

        #Primer y segunda columna con nombre y foto de stats
        for _, stat in enumerate(Character_fields):
            row = STAT_ROW+2+stat.value
            #Columa 0: Texto
            ttk.Label(mainframe, text=stat.name).grid(column=COLUMN0, row=row, sticky=W) #Nombre (texto)

            #Columa 1: Imagen:

            filename = path + r"imgs\stat" + str(stat.value) + ".png" #r"C:\Users\Graciela\Downloads\Games\Romhack\gui editor\imgs\stat" + str(stat.value) + ".png"
            image = openImage(filename, 20, 20)

            stat_img = tk.Label(mainframe, image=image)#self.fields_img[statid] = tk.Label(mainframe, image=image)
            stat_img.image = image #Tengo que repetir esto para que se muestre
            stat_img.grid(row=row, column=COLUMN0+1) #, rowspan=1, padx=5, pady=5)



        #Matriz con nombres de pjes, portraits y sus stats
        for charid, character in enumerate(CHAR_NAMES):
            c = COLUMN0+charid+2

            #Fila0: Foto de pje
            portrait_path = path + r'imgs\char' + str(charid) + ".png" #r"C:\Users\Graciela\Downloads\Games\Romhack\gui editor\imgs\char" + str(charid) + ".png"
            image = openImage(portrait_path, 40, 40)

                #Poner
            char_portrait = tk.Label(mainframe, image=image)
            char_portrait.image = image #Tengo que repetir esto para que se muestre
            char_portrait.grid(row=0, column=c, sticky = W) #, rowspan=1, padx=5, pady=5)

            #Fila1: Nombre de pje
            ttk.Entry(mainframe, text=character.name, width = 7, textvariable = self.char_names[charid]).grid(column=c, row=STAT_ROW+1, sticky=(W,E))


            #Resto de los stats numéricos
            for statid, stat in enumerate(Character_fields):

                field = self.char_fields[statid][charid]
                field = ttk.Entry(mainframe, width=3, textvariable=self.char_stats[statid][charid])
                validate_command =mainframe.register(only_numeric_input)

                field.configure(validate="key",validatecommand=(validate_command,'%P'))  #Que solo permita numeros
                field.grid(column=c, row=STAT_ROW+2+statid, sticky=(W, E))







        #Suavizadogeneral
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        #feet_entry.focus()
        #root.bind("<Return>", self.calculate)

        ##LLENAR GUI
        #self.mostrar_stats_chars()


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

        self.crearPersonajes()

    def export_sav(self):
        self.updateSavData()

        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(title='Select export Directory') + '.sav'
        d = open(filename, mode = 'wb')
        d.write(self.savData)
        d.close()


    def crearPersonajes(self):
        self.characters = []
        offset  = 0x9050  #File1 ASKA

        for i in range(7):
            char = Character()
            self.characters.append(char)
            char.offset = offset + i*0x50
            self.readload_stats_char(char, i)
            self.readload_name(i)

    #Se llama al leer un .sav externo por primera vez
    def readload_stats_char(self, char, chari):

        starsign = readBytes(self.savData, char.offset,1)

        #pow_off = 0x20 #Offset del POW
        maxHP_off = 0x18
        for stat_i in range(7): #MAX HP, Max MP, Pow to Agi
            stat_val = readBytes(self.savData, char.offset + maxHP_off + stat_i*4, 4)
            #Estoy dejando 4bytes de lectura para los stats... tencnicamente los dos mas significativos son siempre 0, y los stats en si capean en 255 en la pantalla de estados. Si numeros mas altos son tomados en cuenta no sé... pero para no hacer un if de si es stat de HP o de POWetc, leo siempre de a 4 y listo. Sino ver la versión 6, que ahi estaba bien, antes de leer max hp y mp

            box = self.char_stats[stat_i][chari]
            box.set(stat_val >> 4)  #En el juego se muestran valores de 0-255 para los stats, así que descarto 4 ultimos bits, que no se usan en los stats (o son parte decimal que no se muestra)

        #6to Hechizo
        #sixthSpellId_off = 0x14 viejo
        spell_id = readBytes(self.savData, char.offset + sixthSpellId_off,1)
        self.char_stats[7][chari].set(spell_id)

    #Se llama al leer un .sav externo por primera vez
    def readload_name(self,chari):
        name_bytes = readBytes(self.savData, namesOff+ chari*0x10,8*2)
        name_string = characterTable2.readName(name_bytes)

        if(chari==0): #Tomo el nombre de shuujinkou para male y female
            self.char_names[0].set(name_string)
            self.char_names[1].set(name_string)
        elif(chari <6):
            self.char_names[chari+1].set(name_string)



    #Se llama al exportar los datos a un .sav.
    #Lee todos los datos que introdujiste y los carga a un nuevo save
    def updateSavData(self):
        for chari in range(len(self.characters)): self.updateCharacterData(chari)

        self.writeChecksum()

    #Se llama al exportar. podria cambiarse el nombre a otro mas claro...
    def updateCharacterData(self, chari):
        char = self.characters[chari]
        i=0
        offsetDuplicado = 0x4000

        for stat in range(0,7): #Pow to Agi
            stat = self.char_stats[stat][chari].get()
            val = (stat <<4).to_bytes(4,'little') #Shift de 4 bits, porque en el juego se toman solo 12 bits para la parte entera (el resto es valor decimal, no me voy a calentar de implementarlo , ,aunque seria divertido usar un pje con 0,5 o 0,75 de vida)
            address= char.offset+maxHP_off + 4*i
            writeBytes(self.savData, address, val, 4, offsetDuplicado)

            i+=1

        #6th Spell
        spell_id = self.char_stats[7][chari].get()
        val = spell_id.to_bytes(1,'little')
        spellid_address = char.offset + sixthSpellId_off
        writeBytes(self.savData, spellid_address, val, 1, offsetDuplicado)

        #Nombre
        #todo ver que hacer con el tema Male/Female. Acá solo tomo el de male
        if(chari==1): return
        nombre = self.char_names[chari].get()
        nombre = nombre[:8] #trim length sobrante
        nombre_bytes = characterTable2.makeName(nombre)
        if(chari>=2): chari -=1
        writeBytes(self.savData, namesOff+ chari*0x10,nombre_bytes, 8*2,offsetDuplicado)



    def writeChecksum(self):
        return

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
root.geometry("800x450+300+150")
root.resizable(width=True, height=True)
MagicalEditor(root)
root.mainloop()