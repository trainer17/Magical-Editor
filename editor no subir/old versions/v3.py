import tkinter
from tkinter import ttk


import enum
class Character_fields(enum.IntEnum):
    HP = enum.auto()
    MP = enum.auto()
    STR = enum.auto()
    DEF = enum.auto()
    IQ = enum.auto()
    SPRI = enum.auto()
    AGI = enum.auto()
    spellId = enum.auto()
    nfields = enum.auto()

CHARACTERS = ['ASKA', 'LASSI', 'MOKKA', 'CHAI', 'PICO', 'SORBET']

class MagicalEditor:

    def __init__(self, root):

        root.title("Magical Editor")

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.feet = tk.StringVar()
        feet_entry = ttk.Entry(mainframe, width=7, textvariable=self.feet)
        feet_entry.grid(column=2, row=1, sticky=(W, E))
        self.meters = tk.StringVar()

        ttk.Label(mainframe, textvariable=self.meters).grid(column=2, row=2, sticky=(W, E))
        ttk.Button(mainframe, text="Calculate", command=self.calculate).grid(column=3, row=3, sticky=W)

        ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
        ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
        ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)


        self.char_values = [None]*Character_fields.nfields
        self.char_fields = [None]*Character_fields.nfields

        for statid, stat in enumerate(Charachter_fields):
            c0 = 3
            self.char_values[statid] = tk.StringVar()
            self.char_fields[statid] = ttk.Entry(mainframe, width=7, textvariable=self.char_values[statid])
            self.char_fields[statid].grid(column=c0, row=statid, sticky=(W, E))
            ttk.Label(mainframe, text=stat.name).grid(column=c0-1, row=statid, sticky=W)



        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        feet_entry.focus()
        root.bind("<Return>", self.calculate)

    def calculate(self, *args):
        try:
            value = float(self.feet.get())
            self.meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
        except ValueError:
            pass

root = tk.Tk()
MagicalEditor(root)
root.mainloop()