
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



STATS_EXCLUSIVOS =[ #Estos stats no se pueden cambiar desde el .sav, de aqui la motivación de este editor de ROM.
    STAT('Action',0x40, 4, 0, 'action.png'),
    STAT('MP %',    0x20, 4, 1, 'stat9.png'),
    STAT('LVL-UP HP Modifier', 0x24, 4, 2, 'HP.png'),
    STAT('LVL-UP MP Modifier', 0x28, 4, 3, 'MP.png'),
    STAT('LVL-UP POW Modifier', 0x2C, 4, 4, 'stat3.png'),
    STAT('LVL-UP DEF Modifier', 0x30, 4, 5, 'stat4.png'),
    STAT('LVL-UP IQ Modifier',  0x34, 4, 6,'stat5.png'),
    STAT('LVL-UP SPRI Modifier', 0x38, 4, 7,'stat6.png'),
    STAT('LVL-UP AGI Modifier',  0x3c, 4, 8, 'stat7.png')
]



class Character:

    def __init__(self):
        self.offset = None #Offset del slot de pje en el rom
        self.stats = []
        for stat in STATS_EXCLUSIVOS:
            self.stats.append(stat)
        self.id = None  #0 Male, 1 Female, etc


class MagicalROMEditor:

    def __init__(self, root):

        ##VARIABLES A USAR:
        self.romPath = tk.StringVar() #String
        self.ROMData = []             #array de bytes
        self.namesFrame = None #tab de protas
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

        ##Cambio de STATS Exclusivos

        self.statsFrame = ttk.Frame(root, padding="1 1 1 1")
        self.statsFrame.grid(column=0, row=0, sticky=(W, S), columnspan = 10)
        self.statsFrame.rowconfigure(0, weight=1, pad = 0)

        ##PERSONAJES

        self.crearPersonajes()

        mainchars = self.characters[:7]
        eggchars = self.characters[7:]

        self.crearFila0(self.statsFrame, mainchars)
        self.crearColumnas(self.statsFrame, mainchars)


        #self.crearGuiEntries(self.charactersFrame)



        #Suavizadogeneral
        for frame in [root, self.namesFrame, self.statsFrame]:
            for child in frame.winfo_children():
                padx = child.grid_info()['padx']
                child.grid_configure(padx= padx + 1, pady=2)



        #feet_entry.focus()
        #root.bind("<Return>", self.calculate)



        #Termino de implementar las pestañas
        self.tabsystem.add(self.namesFrame, text = 'Protagonist Names')
        self.tabsystem.add(self.statsFrame, text = 'Exclusive Stats')

        #feet_entry.focus()
        #root.bind("<Return>", self.calculate)

    def ponerImagen(self, path, sizex, sizey, tab, row, column, sticky = None):
        image = openImage(path, sizex, sizey)
        imagen = tk.Label(tab, image=image)
        imagen.image = image #Tengo que resguardar la iamgen del recolector de basura para que se muestre
        imagen.grid(row=row, column=column, sticky = sticky)
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

        self.analyzeROMRegion()



    def analyzeROMRegion(self):
        #Determino la región del ROM: lo dice el byte 0xF
        region = self.ROMData[0xF]
        if(region == 0x45): self.romRegion.set('USA') ; self.romRegionId = 0
        elif(region == 0x50): self.romRegion.set('EUR') ; self.romRegionId = 1
        elif(region == 0x4A): self.romRegion.set('JP (Not supported)') ; self.romRegionId = 2
        else: (self.romRegion.set('Not a valid ROM file')) ; self.romRegionId = -1


    #LLamdo al exportar el .sav editando actual a un nuevo archivo
    def patch_ROM(self):
        if(self.ROMData==None): return
        self.updateROMNames()

        from tkinter import filedialog
        d = open(self.romPath.get(), mode = 'wb')
        d.write(self.ROMData)
        d.close()

        tk.Label(self.namesFrame, text ='Done!', fg = 'green').grid(column=2, row=4, sticky=(N, W,S,E))



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



    #Se llama al inicio de todo, antes de leer el ROM
    def crearPersonajes(self):
        self.characters = []

        for i in range(14):
            char = Character()
            self.characters.append(char)
            char.id = i

    def updatedata(self): #todo
        for i in range(14):
            self.characters[i].offset = char1Offset[self.romRegionId] + i*100

    def crearColumnas(self, tab, chars):

        validate_command =tab.register(only_numeric_input)

        #Primer y segunda columna con nombre y foto de stat
        for stat in STATS_EXCLUSIVOS:

            #row 0 : Foto de los pjes
            row = 1+stat.row

            #Columa 0: Nombre del stat
            ttk.Label(tab, text=stat.name).grid(column=0, row=row, sticky=W)

            #Columa 1: Imagen del stat
            img_path =  r"imgs/" + stat.img_path
            self.ponerImagen(img_path,22,22,tab,row = row, column = 1) #, rowspan=1, padx=5, pady=5)

            #Columna n: La de cada personaje
            for char in chars:
                field = ttk.Entry(tab, width=1, validate="key",validatecommand=(validate_command,'%P'))
                validate_command =tab.register(only_numeric_input)
                field.grid(column=2+char.id, row=1+stat.row, sticky=(W, E))





    def crearFila0(self, tab, chars): #Fotos de pjes
        for char in chars:
            c = char.id+2
            portrait_path = path + r'imgs\\char' + str(char.id) + ".png"
            self.ponerImagen(portrait_path,40,40,tab,row = 0, column = c, sticky = W) #, rowspan=1, padx=5, pady=5)











    def writeBytesROM(self, address, val, nBytes, dup_addr):

        if(self.ROMData==None): return

        self.ROMData[address : address+nBytes] = val
        self.ROMData[dup_addr : dup_addr+nBytes] = val #data duplicada




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



root = tk.Tk()
root.geometry("450x300")
root.resizable(width=True, height=True)
MagicalROMEditor(root)
root.mainloop()