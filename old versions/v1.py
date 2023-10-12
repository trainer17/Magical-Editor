##0- Importar librerias
import tkinter as tk
from tkinter import ttk
from tkinter import N,W,E,S

##1- Crear Main Window
root = tk.Tk()
root.title('Magical Editor v1')

##2- Crear primer content frame

mainframe = ttk.Frame(root, padding = "3 3 12 12")
mainframe.grid(column=0, row = 0, sticky=(N,W,E,S))
root.columnconfigure(0, weight = 1)
root.rowconfigure(0,weight=1)

##3- Crear contenido

#3.1 - Variable y caja 1
feet = tk.StringVar()
feet_entry = ttk.Entry(mainframe, width=7, textvariable= feet)
feet_entry.grid(column=2, row = 1, sticky=(W,E))

#3.2 - Botón
meters = tk.StringVar()
ttk.Label(mainframe, textvariable = meters).grid(column=2, row=2, sticky=(W,E))
ttk.Button(mainframe, text = "Calculate", command = calculate).grid(column = 3, row = 3, sticky=W)

#3.3 - Variable y caja 2
ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

##4 - Polish positions
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)
feet_entry.focus() #empieza con el cursor acá
root.bind("<Return>", calculate) #Indica que "Enter" funciona como llamar a "calculate"


##5- Cuentas
def calculate(*args):
    try:
        value = float(feet.get())
        meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
    except ValueError:
        pass

##Final - Abrir app
root.mainloop()