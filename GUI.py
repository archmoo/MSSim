import Tkinter, ttk, tkMessageBox
import ScrolledText
from equiplib import EquipLib
from scrolllib import ScrollLib
from speciallib import SpecialLib
from inventory import Inventory, SUCCESS, FAIL, BOOM, INVALID

class InventoryWidget(Tkinter.Frame):

    m_selectedEquipIdx = -1
    
    def __init__(self, parent):
        Tkinter.Frame.__init__(self, parent)
        self.parent = parent
        self.m_selectedEquipIdx = -1
        self.initUI()

    def equipCreateButtonClicked(self):
        def update(self):
            equips = EquipLib.m_lib[chosenType.get()].keys()
            equipOptionMenu['menu'].delete(0, 'end')
            for equip in equips:
                equipOptionMenu['menu'].add_command(label=equip,
                                                    command=Tkinter._setit(chosenEquip, equip))
            chosenEquip.set('- Choose Equip -')

        def select():
            equip = chosenEquip.get()
            if equip != '- Choose Equip -':
                self.equipListbox.insert(Tkinter.END, equip)
                self.parent.m_inventory.createEquip(equip)
                self.parent.m_sysMessage.set(equip + ' created.')
            
        toplevel = Tkinter.Toplevel(self)
        toplevel.grab_set()
        toplevel.title('Create Equipment')
        toplevel.geometry('200x150+300+300')

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

        toplevel.columnconfigure(0, weight=1)
        toplevel.rowconfigure(2, weight=1)
        
        typeOptionMenu.grid(row=0, pady=5)
        equipOptionMenu.grid(row=1)
        selectButton.grid(row=3)
        quitButton.grid(row=4, pady=5)

    def equipModifyButtonClicked(self):
        if self.m_selectedEquipIdx == -1:
            return

        def update(self):
            usesLib = {}
            usesLib.update(ScrollLib.m_lib)
            usesLib.update(SpecialLib.m_lib)
            uses = [key for key in usesLib.keys() if usesLib[key]['type'] == chosenType.get()]
            useOptionMenu['menu'].delete(0, 'end')
            for use in uses:
                useOptionMenu['menu'].add_command(label=use,
                                                    command=Tkinter._setit(chosenUse, use))
            chosenUse.set('- Choose Use Item -')

        def use():
            useItem = chosenUse.get()
            equipName = self.parent.m_inventory.m_equip[self.m_selectedEquipIdx].m_name
            if useItem != '- Choose Use Item -':
                message = 'Use ' + useItem + ' on ' + equipName + '?'
                tkMessageBox.askquestion("Use Item", message, type='yesno')
                res = self.parent.m_inventory.useItem(useItem, self.m_selectedEquipIdx)
                if res == INVALID:
                    sysMessage.set('Can not use ' + useItem + '.')
                    tkMessageBox.showwarning('Invalid', 'Can not use ' + useItem + '.')
                elif res == FAIL:
                    sysMessage.set(useItem + ' failed.')
                    self.equipStats.set(self.parent.m_inventory.m_equip[self.m_selectedEquipIdx].showEquip())
                    equipStatsContent.config(state=Tkinter.NORMAL)
                    equipStatsContent.delete('1.0', Tkinter.END)
                    equipStatsContent.insert('insert', self.equipStats.get())
                    equipStatsContent.config(state=Tkinter.DISABLED)
                    self.equipStatsContent.config(state=Tkinter.NORMAL)
                    self.equipStatsContent.delete('1.0', Tkinter.END)
                    self.equipStatsContent.insert('insert', self.equipStats.get())
                    self.equipStatsContent.config(state=Tkinter.DISABLED)
                elif res == SUCCESS:
                    sysMessage.set('Used ' + useItem + ' successfully.')
                    self.equipStats.set(self.parent.m_inventory.m_equip[self.m_selectedEquipIdx].showEquip())
                    equipStatsContent.config(state=Tkinter.NORMAL)
                    equipStatsContent.delete('1.0', Tkinter.END)
                    equipStatsContent.insert('insert', self.equipStats.get())
                    equipStatsContent.config(state=Tkinter.DISABLED)
                    self.equipStatsContent.config(state=Tkinter.NORMAL)
                    self.equipStatsContent.delete('1.0', Tkinter.END)
                    self.equipStatsContent.insert('insert', self.equipStats.get())
                    self.equipStatsContent.config(state=Tkinter.DISABLED)
                elif res == BOOM:
                    self.parent.m_sysMessage.set(equipName + ' is destroyed by ' + useItem)
                    self.equipListbox.delete(self.m_selectedEquipIdx)
                    self.equipStats.set('')
                    self.equipStatsContent.config(state=Tkinter.NORMAL)
                    self.equipStatsContent.delete('1.0', Tkinter.END)
                    self.equipStatsContent.insert('insert', self.equipStats.get())
                    self.equipStatsContent.config(state=Tkinter.DISABLED)
                    self.m_selectedEquipIdx = -1
                    toplevel.destroy()
                    tkMessageBox.showwarning('Item Destroyed', message=equipName + ' is destroyed by ' + useItem)
                else: # Cubes
                    pass

        toplevel = Tkinter.Toplevel(self)
        toplevel.grab_set()
        toplevel.title('Modify Equipment')
        toplevel.geometry('600x400+300+300')

        toplevel.columnconfigure(0, weight=1)
        toplevel.columnconfigure(1, weight=1)
        
        toplevel.Frameleft = Tkinter.Frame(toplevel, padx=5, pady=10)
        toplevel.Frameright = Tkinter.Frame(toplevel, padx=5, pady=5)

        toplevel.Frameleft.rowconfigure(2, weight=1)
        toplevel.Frameright.rowconfigure(2, weight=1)
        


        uses = ['']
        chosenUse = Tkinter.StringVar()
        chosenUse.set('- Choose Use Item -')
        
        types = ['Special', 'Hammer', 'Cube', 'Scroll', 'Trace']
        chosenType = Tkinter.StringVar()
        chosenType.set('- Choose Type -')
        typeOptionMenu = Tkinter.OptionMenu(toplevel.Frameleft, chosenType, *types, command=update)
        useOptionMenu = Tkinter.OptionMenu(toplevel.Frameleft, chosenUse, *uses)
        useOptionMenu['menu'].delete(0, 'end')

        useDescription = Tkinter.StringVar()
        useDescriptionContent = Tkinter.Label(toplevel.Frameleft,
                                              textvariable=useDescription,
                                              anchor=Tkinter.N,
                                              justify=Tkinter.LEFT)
        useDescription.set('')
        useButton = Tkinter.Button(toplevel.Frameleft, text='Use', command=use)
        cancelButton = Tkinter.Button(toplevel.Frameleft, text='Cancel', command=toplevel.destroy)

        equipStatsContent = ScrolledText.ScrolledText(toplevel.Frameright,
                                                      wrap=Tkinter.WORD,
                                                      width=35)
        equipStatsContent.config(font=('San Francisco', 13, 'normal'))
        equipStatsContent.insert('insert', self.equipStats.get())
        equipStatsContent.config(state=Tkinter.DISABLED)
        
        sysMessage = Tkinter.StringVar()
        sysMessageLabel = Tkinter.Label(toplevel.Frameright,
                                   textvariable=sysMessage,
                                   justify=Tkinter.LEFT)
        sysMessage.set('')

        typeOptionMenu.grid(row=0, column=0, rowspan=1, columnspan=2,
                            padx=5)
        useOptionMenu.grid(row=1, column=0, rowspan=1, columnspan=2,
                            padx=5)
        useDescriptionContent.grid(row=2, column=0,
                                  rowspan=3, columnspan=2,
                                  padx=10, pady=5,
                                  sticky=Tkinter.N+Tkinter.S+Tkinter.W,
                                  )
        useButton.grid(row=5, column=0, padx=5, pady=5)
        cancelButton.grid(row=5, column=1, padx=5, pady=5)
        equipStatsContent.grid(row=0, column=0, rowspan=3, columnspan=5,
                               padx=5, pady=5,
                               sticky=Tkinter.N+Tkinter.S+Tkinter.W)
        sysMessageLabel.grid(row=5, column=1, rowspan=3, columnspan=1, padx=5, pady=10,
                             sticky=Tkinter.W)
        toplevel.Frameleft.pack(fill=Tkinter.BOTH, expand=1, side=Tkinter.LEFT)
        toplevel.Frameright.pack(fill=Tkinter.BOTH, expand=1, side=Tkinter.RIGHT)

    def equipDeleteButtonClicked(self):
        if self.m_selectedEquipIdx != -1:
            message = 'Are You Sure?\n\n' + 'Deleting: ' + self.parent.m_inventory.m_equip[self.m_selectedEquipIdx].showEquip()
            result = tkMessageBox.askquestion("Delete", message, icon='warning', type='yesno')
            if result == 'yes':
                self.parent.m_sysMessage.set(self.parent.m_inventory.m_equip[self.m_selectedEquipIdx].m_name + ' deleted.')
                self.equipListbox.delete(self.m_selectedEquipIdx)
                self.parent.m_inventory.deleteEquip(self.m_selectedEquipIdx)
                self.equipStats.set('')
                self.equipStatsContent.config(state=Tkinter.NORMAL)
                self.equipStatsContent.delete('1.0', Tkinter.END)
                self.equipStatsContent.insert('insert', self.equipStats.get())
                self.equipStatsContent.config(state=Tkinter.DISABLED)
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
            self.equipStatsContent.config(state=Tkinter.NORMAL)
            self.equipStatsContent.delete('1.0', Tkinter.END)
            self.equipStatsContent.insert('insert', self.equipStats.get())
            self.equipStatsContent.config(state=Tkinter.DISABLED)
        else:
            self.m_selectedEquipIdx = -1

    def initUI(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        
        self.Frameleft = Tkinter.Frame(self, padx=5, pady=5)
        self.Frameright = Tkinter.Frame(self, padx=5, pady=5)

        self.Frameleft.rowconfigure(1, weight=1)
        self.Frameright.rowconfigure(1, weight=1)
        
        self.equipListbox = Tkinter.Listbox(self.Frameleft, selectmode='single')
        self.equipListbox.bind('<<ListboxSelect>>', self.equipListboxSelect)

        self.equipCreateButton = Tkinter.Button(self.Frameleft, text='Create', command=self.equipCreateButtonClicked)
        self.equipModifyButton = Tkinter.Button(self.Frameleft, text='Modify', command=self.equipModifyButtonClicked)
        self.equipDeleteButton = Tkinter.Button(self.Frameleft, text='Delete', command=self.equipDeleteButtonClicked)
 
        self.equipStats = Tkinter.StringVar()
        self.equipStatsContent = ScrolledText.ScrolledText(self.Frameright,
                                                           wrap=Tkinter.WORD,
                                                           width=35)
        self.equipStats.set('')
        self.equipStatsContent.config(font=('San Francisco', 13, 'normal'))
        self.equipStatsContent.insert('insert', self.equipStats.get())
        self.equipStatsContent.config(state=Tkinter.DISABLED)
        

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

    def quitButtonClicked(self):
        message = 'Are You Sure?\n\nQuitting'
        result = tkMessageBox.askquestion("Quit", message, icon='warning', type='yesno')
        if result == 'yes':
            self.destroy()
            self.parent.destroy()

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
        self.quitButton = Tkinter.Button(self, text='Quit', command=self.quitButtonClicked)
        
        self.tabs.pack(fill=Tkinter.BOTH, expand=1)
        self.sysMessage.pack(padx=5, pady=5, side=Tkinter.LEFT)
        self.quitButton.pack(padx=5, pady=5, side=Tkinter.RIGHT)
        
if __name__ == '__main__':

    root = Tkinter.Tk()
    root.geometry('680x600+200+200')
    app = MainWidget(root)
    root.mainloop()
    
