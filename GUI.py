import Tkinter, ttk
from equiplib import EquipLib
from inventory import Inventory

class InventoryWidget(Tkinter.Frame):

    m_selectedEquipIdx = -1
    
    def __init__(self, parent):
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
                self.parent.m_inventory.createEquip(equip)
                self.parent.m_sysMessage.set(equip + ' created.')
            
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

    def equipDeleteButtonClicked(self):
        if self.m_selectedEquipIdx != -1:
            self.parent.m_sysMessage.set(self.parent.m_inventory.m_equip[self.m_selectedEquipIdx].m_name + ' deleted.')
            self.equipListbox.delete(self.m_selectedEquipIdx)
            self.parent.m_inventory.deleteEquip(self.m_selectedEquipIdx)
            self.equipStats.set('')
            self.m_selectedEquipIdx = -1
            
    def equipListboxSelect(self, event):
        listbox = event.widget
        choice = listbox.curselection()
        if len(choice) != 0:
            idx = choice[0]
            value = listbox.get(choice[0])
            self.m_selectedEquipIdx = idx
            equip = self.parent.m_inventory.m_equip[idx]
            self.equipStats.set(equip.showEquip())
        else:
            self.m_selectedEquipIdx = -1

    def initUI(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        
        self.Frameleft = Tkinter.Frame(self, padx=5, pady=5)
        self.Frameright = Tkinter.Frame(self, padx=5, pady=5)

        self.Frameleft.rowconfigure(1, weight=1)
        
        self.equipListbox = Tkinter.Listbox(self.Frameleft, selectmode='single')
        self.equipListbox.bind('<<ListboxSelect>>', self.equipListboxSelect)

        self.equipCreateButton = Tkinter.Button(self.Frameleft, text='Create', command=self.equipCreateButtonClicked)
        self.equipModifyButton = Tkinter.Button(self.Frameleft, text='Modify')
        self.equipDeleteButton = Tkinter.Button(self.Frameleft, text='Delete', command=self.equipDeleteButtonClicked)
 
        self.equipStats = Tkinter.StringVar()
        self.equipStatsContent = Tkinter.Label(self.Frameright,
                                             textvariable=self.equipStats,
                                             anchor=Tkinter.N,
                                             justify=Tkinter.LEFT)
        self.equipStats.set('')

        self.equipListboxLabel = Tkinter.Label(self.Frameleft, text='Inventory List')
        self.equipStatsLabel = Tkinter.Label(self.Frameright, text='Stats')

        self.equipListboxLabel.grid(row=0, column=0, rowspan=1, columnspan=3, padx=5, pady=5)
        self.equipListbox.grid(row=1, column=0,
                               rowspan=5, columnspan=3,
                               padx=5, pady=5,
                               sticky=Tkinter.W+Tkinter.E+Tkinter.N+Tkinter.S)
        self.equipCreateButton.grid(row=6, column=0, padx=5, pady=5, sticky=Tkinter.W)
        self.equipModifyButton.grid(row=6, column=1, padx=5, pady=5)
        self.equipDeleteButton.grid(row=6, column=2, padx=5, pady=5, sticky=Tkinter.E)
        self.equipStatsLabel.grid(row=0, column=0, rowspan=1, columnspan=3, padx=5, pady=5)
        self.equipStatsContent.grid(row=1, column=0,
                                  rowspan=5, columnspan=3,
                                  padx=5, pady=5,
                                  sticky=Tkinter.N+Tkinter.S+Tkinter.W,
                                  )
        
        self.Frameleft.pack(fill=Tkinter.BOTH, expand=1, side=Tkinter.LEFT)
        self.Frameright.pack(fill=Tkinter.BOTH, expand=1, side=Tkinter.RIGHT)

class MainWidget(Tkinter.Frame):

    m_inventory = None
    m_sysMessage = None
    
    def __init__(self, parent):

        self.m_inventory = Inventory()
        self.m_sysMessage = Tkinter.StringVar()
        self.m_sysMessage.set('Welcome!')
        Tkinter.Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title('MS Sim')
        self.pack(fill=Tkinter.BOTH, expand=1)
        self.tabs = ttk.Notebook(self)
        self.tabInventory = InventoryWidget(self)
        self.tabEquip = Tkinter.Frame(self)
        self.tabPurchase = Tkinter.Frame(self)
        self.tabs.add(self.tabInventory, text='Inventory')
        self.tabs.add(self.tabEquip, text='Equip')
        self.tabs.add(self.tabPurchase, text='Purchase')

        self.sysMessage = Tkinter.Label(self,
                                        textvariable=self.m_sysMessage,
                                        justify=Tkinter.LEFT)
        self.quitButton = Tkinter.Button(self, text='Quit', command=self.parent.destroy)
        
        self.tabs.pack(fill=Tkinter.BOTH, expand=1)
        self.sysMessage.pack(padx=5, pady=5, side=Tkinter.LEFT)
        self.quitButton.pack(padx=5, pady=5, side=Tkinter.RIGHT)
        
if __name__ == '__main__':

    root = Tkinter.Tk()
    root.geometry('600x600+200+200')
    app = MainWidget(root)
    root.mainloop()
    
