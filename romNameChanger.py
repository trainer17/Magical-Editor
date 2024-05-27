
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



class MagicalROMEditor:

    def __init__(self, root):

        ##VARIABLES A USAR:
        self.romPath = tk.StringVar() #String
        self.ROMData = []             #array de bytes
        self.mainFrame = None #tab de protas
        self.romRegion = tk.StringVar() # String que vale 'USA, 'EUR', o 'JP'

        ##INTERFAZ GUI
        root.title("Magical ROM Editor")



        ##PESTAÑAS (no usado aun)

        #Habilitamos y creamos pestañas
        self.tabsystem = ttk.Notebook(root, padding="0 0 0 0")
        #self.eggFrame  = ttk.Frame(self.tabsystem)
        #self.tabsystem.add(self.mainFrame, text = 'Main Characters')
        #self.tabsystem.add(self.eggFrame, text = 'Egg Characters')
        self.tabsystem.grid(column=0, row = 0, sticky=(N, W, E, S), columnspan= 7)

        ##Controles Globales
        self.mainFrame = ttk.Frame(root, padding="1 1 1 1")
        self.mainFrame.grid(column=0, row=0, sticky=(W, S), columnspan = 10)
        self.mainFrame.rowconfigure(0, weight=1, pad = 0)
        #todo el pad este no anda por el que está en "suavizado general" abajo. Se puede usar el "ipad" sino

        #Rom Region Label
        tk.Label(self.mainFrame, text = 'Rom Region: ').grid(row=0, column = 0)
        tk.Label(self.mainFrame, textvariable = self.romRegion, fg ='blue').grid(row = 0, column = 1, sticky = W)

        # MC Default names:
        self.maleName = tk.StringVar()
        self.femaleName = tk.StringVar()
       #tk.Label(self.mainFrame, text ='Male:', fg = 'black').grid(column=1, row=1, sticky=(N, W,S))
        #tk.Label(self.mainFrame, text ='Female:', fg = 'black').grid(column=1, row=2, sticky=(N, W,S))

        ttk.Entry(self.mainFrame, textvariable = self.maleName, width = 12).grid(column = 1, row = 1, sticky = (W,N) )
        ttk.Entry(self.mainFrame, textvariable = self.femaleName, width = 12).grid(column = 1, row = 2, sticky = (W,N) )
        self.ponerImagen('imgs/char0.png', 40, 40, self.mainFrame, row=1, column=0)
        self.ponerImagen('imgs/char1.png', 40, 40, self.mainFrame, row=2, column =0)

        self.maleName.set('Galette')
        self.femaleName.set('Financière')

        #validate_command = self.mainFrame.register(only_time_input)
        #box.configure(validate="key",validatecommand=(validate_command,'%P'))  #Que solo permita numeros



        row = 3
        column =0


        #Boton Open .sav
        self.ponerImagen('imgs/save.png', 40, 40, self.mainFrame, row, column)
        tk.Button(self.mainFrame, text='Open ROM\n(.nds)', command=self.open_ROM).grid(column = column+1, row = row, sticky =  (N,S, W), columnspan = 1, padx = 20)
       # ttk.Label(controlPanel, textvariable=self.savPath).grid(column=column, row=row+1, columnspan=1, sticky=(W, E))

        #Boton Export .sav
        tk.Button(self.mainFrame, text='Patch ROM', command=self.export_ROM).grid(column = column+2, row = row, sticky = (N,S, E), padx = 20)


        #Suavizadogeneral
        for child in self.mainFrame.winfo_children():
            child.grid_configure(padx=9, pady=2)



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
    def export_ROM(self):
        if(self.ROMData==None): return
        self.updateROMNames()

        from tkinter import filedialog
        d = open(self.romPath.get(), mode = 'wb')
        d.write(self.ROMData)
        d.close()

        tk.Label(self.mainFrame, text ='Done!', fg = 'green').grid(column=2, row=4, sticky=(N, W,S,E))



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
        nombre_bytes = characterTable4.makeName(nombre)
        if(char.id>=2): chari = char.id-1
        if(char.id ==0): chari = 0
        self.writeBytes(namesOff+ chari*0x10,nombre_bytes, 8*2)



    #mete a Male/Female en el slot de pje 0 1 2 3 etc a elección
    #genero 1 = Male, 2= Female
    def escribirGeneroSlotPje(self, genero, slot):
        genero = genero.to_bytes(1,'little')

        #Se escribe en el header global y en el header del slot
        for address in genderAdressesHeader:
            self.writeBytes(address+slot, genero, 1,offsetDuplicadoHeader, headerFileOffset)

        for address in charSlotsMain:
            self.writeBytes(address+slot, genero, 1,offsetFiles)




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


def only_numeric_input(input):
    #this is allowing all numeric input and backspace to work
    if input.isdigit() or input =="": return True
    else:  return False




root = tk.Tk()
root.geometry("450x300")
root.resizable(width=True, height=True)
MagicalROMEditor(root)
root.mainloop()