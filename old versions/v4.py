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

class CHARACTERS(enum.IntEnum):
    ASKA = enum.auto()
    LASSI = enum.auto()
    MOKKA = enum.auto()
    CHAI = enum.auto()
    PICO = enum.auto()
    SORBET = enum.auto()



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

        self.char_values = [ [None for _ in range(Character_fields.nfields)] for _ in range(len(CHARACTERS))]
        self.char_fields = [ [None for _ in range(Character_fields.nfields)] for _ in range(len(CHARACTERS))]

        NAMEROW = 0
        COLUMN0 = 1


        for statid, stat in enumerate(Charachter_fields):
            ttk.Label(mainframe, text=stat.name).grid(column=COLUMN0-1, row=NAMEROW+1+statid, sticky=W)

        for charid, character in enumerate(CHARACTERS):
            ttk.Label(mainframe, text=character.name).grid(column=COLUMN0+charid, row=NAMEROW, sticky=W)
            c0 = COLUMN0+charid

            for statid, stat in enumerate(Charachter_fields):
                self.char_values[charid][statid] = tk.StringVar()
                self.char_fields[charid][statid] = ttk.Entry(mainframe, width=3, textvariable=self.char_values[charid][statid])
                self.char_fields[charid][statid].grid(column=c0, row=NAMEROW+1+statid, sticky=(W, E))



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