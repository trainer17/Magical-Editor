
##Cambia el nombre de los MC a lo que vos elijas

#########################  Requirements  ###########################

#pip install tkinter


##################################################################


#Otro buen ejemplo: https://www.pythonguis.com/tutorials/create-ui-with-tkinter-grid-layout-manager/

#todo resetear flags de historia y cofres/leafs/items recogidos

#todo imagen de los elementos de c/u
#todo idem catch de errores de numeros muy grandes
#todo poner de yapa un "play time" y "bira"?
#todo dejar una notita para explicar el funcionamiento de tener a Male y Female a la vez (usar teleport enseguida. Se repone a Lassi en Neumann).
#todo interfaz linda de elegir male/female (click portraits?)
#todo change character portraits/overworld sprites (pirate otther, brownie, pyrite, etc=
#todo v15: Agregar para elegir ataque físico tamb
#todo unlcock diary Falta... no importa
import tkinter as tk
from tkinter import ttk
from tkinter import N,W,E,S

import characterTable4
import magicalChecksum
path = __file__[:-6]


CHAR_NAMES = ['Male', 'Female', 'Mokka', 'Lassi', 'Pico', 'Chai', 'Sorbet']
CHAR_FIELDS = ['Phys Attack', 'Spell']

##Defino diccionario que guarda los offsets de cada stat en el .sav, relativo al offset del slot de pje

##MALE Name offsets

#ES:
eur_EN  = [0x12F65BC, 0x12F72A4]

#FR
eur_FR = [0x131ACD0, 0x131B9C6]

#DE
eur_DE = [0x133EE98, 0x133FB86]

#ES
eur_ES = [0x1363A60, 0x1364757]

#IT
eur_IT = [0x138AC54, 0x138B93E]

#US
us = [0x06C1E4, 0x6CECC]


class Character:

    def __init__(self):
        self.offset = None #Offset del slot de pje
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



class MagicalROMEditor:

    def __init__(self, root):

        ##VARIABLES A USAR:
        self.romPath = tk.StringVar() #String
        self.ROMData = []             #array de bytes
        self.namesFrame = None #tab de protas
        self.romRegion = tk.StringVar() # String que vale 'USA, 'EUR', o 'JP'

        ##GUI CON PESTAÑAS
        root.title("Magical ROM Editor")

        #Habilitamos y creamos pestañas
        self.tabsystem = ttk.Notebook(root, padding="0 0 0 0")

        #self.eggFrame  = ttk.Frame(self.tabsystem)
        #self.tabsystem.add(self.mainFrame, text = 'Main Characters')
        #self.tabsystem.add(self.eggFrame, text = 'Egg Characters')
        self.tabsystem.grid(column=0, row = 0, sticky=(N, W, E, S), columnspan= 7)

        ##Cambio de nombres
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

        ##Cambio de phys attacks

        self.charactersFrame = ttk.Frame(root, padding="1 1 1 1")
        self.charactersFrame.grid(column=0, row=0, sticky=(W, S), columnspan = 10)
        self.charactersFrame.rowconfigure(0, weight=1, pad = 0)

        ##PERSONAJES - TkVars

        self.crearPersonajes()
        char_fields = [ [None for _ in CHAR_NAMES] for _ in CHAR_FIELDS] #campos gui

        self.crearColumna0(self.charactersFrame)


        self.crearGuiEntries(self.charactersFrame)



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



        #Suavizadogeneral
        for child in self.namesFrame.winfo_children():
            child.grid_configure(padx=9, pady=2)


        #Termino de implementar las pestañas
        self.tabsystem.add(self.namesFrame, text = 'Protagonists Names')
        self.tabsystem.add(self.charactersFrame, text = 'Physical Attacks')

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

        #Determino la región del ROM: lo dice el byte 0xF
        region = self.ROMData[0xF]
        if(region == 0x45): self.romRegion.set('USA')
        elif(region == 0x50): self.romRegion.set('EUR')
        elif(region == 0x4A): self.romRegion.set('JP (Not supported)')
        else: (self.romRegion.set('Not a valid ROM file'))


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



    #Se llama con la función de arriba
    def crearPersonajes(self):
        self.characters = []

        for i in range(14):
            char = Character()
            self.characters.append(char)
            char.offset = char1Offset + i*0x50 #todo revisar estooo
            char.id = i

    def crearColumna0(self, frame):

        self.crearRowNombres(tab) #string Fields
        self.crearRowStarsigns(tab) #Option Menu Fields

        #Columna con foto de los stats
        for stat in ['phys', 'spell']:

            #Columa 0: Imagen:

            filename = path + r"imgs/" + stat + ".png"
            self.ponerImagen(filename,20,20,tab,row = row, column = 0) #, rowspan=1, padx=5, pady=5)




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




root = tk.Tk()
root.geometry("450x300")
root.resizable(width=True, height=True)
MagicalROMEditor(root)
root.mainloop()