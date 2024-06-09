#Otro buen ejemplo: https://www.pythonguis.com/tutorials/create-ui-with-tkinter-grid-layout-manager/

import tkinter as tk
from tkinter import ttk
from tkinter import N,W,E,S



import enum
class Character_fields(enum.IntEnum):
   # NAME = enum.auto()
    HP = enum.auto()
    MP = enum.auto()
    STR = enum.auto()
    DEF = enum.auto()
    IQ = enum.auto()
    SPRI = enum.auto()
    AGI = enum.auto()
    spellId = enum.auto()
    nfields = enum.auto()

class CHARACTERS(enum.IntEnum):
    ASKA = enum.auto()
    LASSI = enum.auto()
    MOKKA = enum.auto()
    CHAI = enum.auto()
    PICO = enum.auto()
    SORBET = enum.auto()

class Character:
    offset = None
    NAME = None
    HP = None
    MP = None
    POW = None
    DEF = None
    IQ = None
    SPRI = None
    AGI = None
    spellId = None


class MagicalEditor:

    def __init__(self, root):

        ##VARIABLES A USAR:
        self.savPath = tk.StringVar() #String
        self.savData = None     #string de bytes
        self.char_fields = None #Matriz de entrybox
        self.char_stats = None #Matriz de datos
        self.characters = [Character()]* 6


        ##CODIGO DATOS
        self.open_sav()
        self.crearPersonajes()


        ##CODIGO GUI
        root.title("Magical Editor")

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)


        tk.Button(mainframe, text='Open save file', command=self.open_sav).grid(column = 3, row = 10, sticky = S)
        self.savPath = tk.StringVar()
        ttk.Label(mainframe, textvariable=self.savPath).grid(column=4, row=10, columnspan=10, sticky=(W, E))



        ##STATS PERSONAJES

        #Matriz de stats
        self.char_stats = [ [None for _ in range(Character_fields.nfields)] for _ in enumerate(CHARACTERS)]
        self.char_fields = [ [None for _ in range(Character_fields.nfields)] for _ in enumerate(CHARACTERS)]

        #Imagenes de stats
        self.fields_img =  [None for _ in range(Character_fields.nfields)]


        NAMEROW = 0
        COLUMN0 = 1

        #Columna con nombres de stats
        for statid, stat in enumerate(Character_fields):
            row = NAMEROW+1+statid
            ttk.Label(mainframe, text=stat.name).grid(column=COLUMN0-1, row=row, sticky=W)

            #Imagen del stat:
            from PIL import Image, ImageTk #Con esto puedo resizear la imagen
            filename = r"C:\Users\Graciela\Downloads\Games\Romhack\gui editor\imgs\stat" + str(statid) + ".png"
            image = Image.open(filename)
            image = image.resize((20,20))
            image = ImageTk.PhotoImage(image)
            #small_img = image.subsample(10,10)

            self.fields_img[statid] = tk.Label(mainframe, image=image)
            self.fields_img[statid].image = image #Tengo que repetir esto para que se muestre
            self.fields_img[statid].grid(row=row, column=COLUMN0+len(CHARACTERS)) #, rowspan=1, padx=5, pady=5)



        #Matriz con stats
        for charid, character in enumerate(CHARACTERS):
            ttk.Label(mainframe, text=character.name).grid(column=COLUMN0+charid, row=NAMEROW, sticky=W)
            c0 = COLUMN0+charid

            for statid, stat in enumerate(Character_fields):
                if statid == Character_fields.nfields: continue
                #if statid == Character_fields.NAME: continue

                self.char_stats[charid][statid] = tk.StringVar()
                self.char_fields[charid][statid] = ttk.Entry(mainframe, width=3, textvariable=self.char_stats[charid][statid])
                self.char_fields[charid][statid].grid(column=c0, row=NAMEROW+1+statid, sticky=(W, E))







        #Suavizadogeneral
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        #feet_entry.focus()
        #root.bind("<Return>", self.calculate)

        ##LLENAR GUI
        self.mostrar_stats_chars()


    def calculate(self, *args):
        try:
            value = float(self.feet.get())
            self.meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
        except ValueError:
            pass

    #Todo: Cargar un file dummy al abrir
    def open_sav(self):
        from tkinter import filedialog
        filename = filedialog.askopenfilename(title='Select file')
        self.savPath.set(filename)
        d = open(filename, mode = 'rb')
        self.savData = d.read()
        d.close()

        self.crearPersonajes()


    def crearPersonajes(self):
        offset  = 0x9050  #File1 ASKA
        for char in self.characters:
            char.offset = offset
            offset += 0x50
            self.read_stats_char(char)

    def read_stats_char(self, char):

        starsign = readBytes(self.savData, char.offset,1)
        off = 0x20
        char.POW = readBytes(self.savData, char.offset +off + 0*4,2)
        char.DEF = readBytes(self.savData, char.offset +off + 1*4,2)
        char.IQ = readBytes(self.savData, char.offset +off + 2*4,2)
        char.SPRI = readBytes(self.savData, char.offset +off + 3*4,2)
        char.AGI = readBytes(self.savData, char.offset +off + 4*4,2)

    def mostrar_stats_chars(self):
        row_i = -1
        for row in self.char_stats:
            row_i += 1
            for box in row:
                 box.set(self.characters[row_i].POW)


from PIL import ImageTk, Image
def open_img(path):
    image = tk.PhotoImage(file=path, master = root, height = 200, width=200)
    img = tk.Label(root, image=image)
    img.grid(row=7, column=7, rowspan=6, padx=5, pady=5)

    #img = Image.open(path)
    #img = img.resize((10, 10), Image.ANTIALIAS)
   # img = ImageTk.PhotoImage(img)


def readBytes(file, offset, nBytes, uint = False):
    data= file[offset: offset+nBytes]

    if(nBytes ==1): val= data[0]

    #Read Little Endian Int
    if(nBytes == 2):  val = data[1] + 0x10 * data[0]

    if(nBytes == 4): val = 0

    return val

root = tk.Tk()
root.geometry("550x300+300+150")
root.resizable(width=True, height=True)
MagicalEditor(root)
root.mainloop()