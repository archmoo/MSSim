import Tkinter
from equiplib import EquipLib
from inventory import Inventory

class MainWidget(Tkinter.Frame):

    m_inventory = None
    
    def __init__(self, parent):

        self.m_inventory = Inventory()
        
        Tkinter.Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def equipCreateButtonClicked(self):
        def update(self):
            equips = EquipLib.m_lib[chosenType.get()].keys()
            equipOptionMenu['menu'].delete(0, 'end')
            for equip in equips:
                equipOptionMenu['menu'].add_command(label=equip,
                                                    command=Tkinter._setit(chosenEquip, equip))
        def select():
            equip = chosenEquip.get()
            if equip != '- Choose Equip -':
                self.equipListbox.insert(Tkinter.END, equip)
                self.m_inventory.createEquip(equip)
            toplevel.destroy()
            
        toplevel = Tkinter.Toplevel(self)
        toplevel.title('Create Equipment')
        toplevel.geometry('200x150+300+300')
        toplevel.columnconfigure(0, weight=1)
        toplevel.rowconfigure(2, weight=1)

        equips = ['']
        chosenEquip = Tkinter.StringVar()
        chosenEquip.set('- Choose Equip -')

        types = EquipLib.m_lib.keys()
        chosenType = Tkinter.StringVar()
        chosenType.set('- Choose Type -')
        typeOptionMenu = Tkinter.OptionMenu(toplevel, chosenType, *types, command=update)
        equipOptionMenu = Tkinter.OptionMenu(toplevel, chosenEquip, *equips)
        equipOptionMenu['menu'].delete(0, 'end')        

        selectButton = Tkinter.Button(toplevel, text='Select', command=select)
        quitButton = Tkinter.Button(toplevel, text='Cancel', command=toplevel.destroy)

        typeOptionMenu.grid(row=0, pady=5)
        equipOptionMenu.grid(row=1)
        selectButton.grid(row=3)
        quitButton.grid(row=4, pady=5)
        
    def initUI(self):
        self.parent.title('MS Sim')
        self.pack(fill=Tkinter.BOTH, expand=1)
        
        self.rowconfigure(0, weight=1)
        for col in range(20):
            self.columnconfigure(col, weight=1)
        
        self.equipListbox = Tkinter.Listbox(self)
        self.equipListbox.grid(row=0, column=0,
                    rowspan=5, columnspan=3,
                    padx=5, pady=5,
                    sticky=Tkinter.W+Tkinter.E+Tkinter.N+Tkinter.S)

        self.equipCreateButton = Tkinter.Button(self, text='Create', command=self.equipCreateButtonClicked)
        self.equipCreateButton.grid(row=5, column=0, padx=5, pady=5, sticky=Tkinter.W)
        self.equipDeleteButton = Tkinter.Button(self, text='Delete')
        self.equipDeleteButton.grid(row=5, column=2, padx=5, pady=5, sticky=Tkinter.E)

##        self.equipStats = Tkinter.StringVar()
##        self.equipStatsLabel = Tkinter.Label(self,
##                                          textvariable=self.equipStats,
##                                          anchor=Tkinter.NW)
##        self.equipStatsLabel.grid(row=0, column=3,
##                        rowspan=3, columnspan=3,
##                        padx=5, pady=5,
##                        )
##        self.equipStats.set('')
        

if __name__ == '__main__':

    root = Tkinter.Tk()
    root.geometry('600x400+200+200')
    app = MainWidget(root)
    root.mainloop()
    
