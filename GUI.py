import Tkinter, ttk, tkMessageBox
import ScrolledText
from equip import Equip
from equiplib import EquipLib
from scrolllib import ScrollLib
from speciallib import SpecialLib
from etclib import EtcLib
from equipslot import EquipSlot
from inventory import Inventory, SUCCESS, FAIL, BOOM, INVALID, NOITEM
from potential import rank_label
from marketinfo import MarketInfo
import pickle

class InventoryWidget(Tkinter.Frame):

    m_selectedEquipIdx = -1
    
    def __init__(self, parent):
        Tkinter.Frame.__init__(self, parent)
        self.parent = parent
        self.m_selectedEquipIdx = -1
        self.initUI()

    def reset(self):
        self.m_selectedEquipIdx = -1
        self.equipListbox.delete(0, Tkinter.END)
        for i in range(len(self.parent.m_inventory.m_equip)):
            self.equipListbox.insert(Tkinter.END, self.parent.m_inventory.m_equip[i].m_name)
        self.equipStatsContent.config(state=Tkinter.NORMAL)
        self.equipStatsContent.delete('1.0', Tkinter.END)
        self.equipStatsContent.config(state=Tkinter.DISABLED)
        
        
##    def equipCreateButtonClicked(self):
##        def update(self):
##            equips = EquipLib.m_lib[chosenType.get()].keys()
##            equipOptionMenu['menu'].delete(0, 'end')
##            for equip in equips:
##                equipOptionMenu['menu'].add_command(label=equip,
##                                                    command=Tkinter._setit(chosenEquip, equip))
##            chosenEquip.set('- Choose Equip -')
##
##        def select():
##            equip = chosenEquip.get()
##            if equip != '- Choose Equip -':
##                self.equipListbox.insert(Tkinter.END, equip)
##                self.parent.m_inventory.createEquip(equip)
##                self.parent.m_sysMessage.set(equip + ' created.')
##
##        self.parent.tabEquip.reset()
##        
##        toplevel = Tkinter.Toplevel(self)
##        toplevel.grab_set()
##        toplevel.title('Create Equipment')
##        toplevel.geometry('200x150+300+300')
##
##        equips = ['']
##        chosenEquip = Tkinter.StringVar()
##        chosenEquip.set('- Choose Equip -')
##
##        types = EquipLib.m_lib.keys()
##        chosenType = Tkinter.StringVar()
##        chosenType.set('- Choose Type -')
##        typeOptionMenu = Tkinter.OptionMenu(toplevel, chosenType, *types, command=update)
##        equipOptionMenu = Tkinter.OptionMenu(toplevel, chosenEquip, *equips)
##        equipOptionMenu['menu'].delete(0, 'end')        
##
##        selectButton = Tkinter.Button(toplevel, text='Select', command=select)
##        quitButton = Tkinter.Button(toplevel, text='Cancel', command=toplevel.destroy)
##
##        toplevel.columnconfigure(0, weight=1)
##        toplevel.rowconfigure(2, weight=1)
##        
##        typeOptionMenu.grid(row=0, pady=5)
##        equipOptionMenu.grid(row=1)
##        selectButton.grid(row=3)
##        quitButton.grid(row=4, pady=5)

    def equipModifyButtonClicked(self):
        if self.m_selectedEquipIdx == -1:
            return
        if self.m_selectedEquipIdx in self.parent.m_inventory.m_equipped.values():
            message = 'Can\'t. ' + self.parent.m_inventory.m_equip[self.m_selectedEquipIdx].m_name + ' is equipped.'
            tkMessageBox.showwarning('Invalid', message)
            return

        self.parent.tabEquip.reset()
        
        def update():
            def setUpUseOptionMenu(self, use):
                chosenUse.set(use)
                description = 'Quantity in inventory: ' + str(self.parent.m_inventory.m_use[use]) + '\n\n'
                if chosenType.get() in ['Special', 'Hammer', 'Cube']:
                    description += SpecialLib.m_lib[use]['description']
                else:
                    description += ScrollLib.showScrollStat(use)
                useDescriptionContent.config(state=Tkinter.NORMAL)
                useDescriptionContent.delete('1.0', Tkinter.END)
                useDescriptionContent.insert('insert', description)
                useDescriptionContent.config(state=Tkinter.DISABLED)
                
            usesLib = {}
            usesLib.update(ScrollLib.m_lib)
            usesLib.update(SpecialLib.m_lib)
            uses = sorted([key for key in usesLib.keys() if usesLib[key]['type'] == chosenType.get()])
            useOptionMenu['menu'].delete(0, 'end')
            for use in uses:
                useOptionMenu['menu'].add_command(label=use,
                                                    command=lambda use=use: setUpUseOptionMenu(self, use))
            chosenUse.set('- Choose Use Item -')

        def use():
            useItem = chosenUse.get()
            equipName = self.parent.m_inventory.m_equip[self.m_selectedEquipIdx].m_name
            if useItem != '- Choose Use Item -':
                message = 'Use ' + useItem + ' on ' + equipName + '?'
                if tkMessageBox.askquestion("Use Item", message, type='yesno') != 'yes':
                    return
                res = self.parent.m_inventory.useItem(useItem, self.m_selectedEquipIdx)
                if res == NOITEM:
                    sysMessage.set('No ' + useItem + ' available.')
                    tkMessageBox.showwarning('Invalid', 'No ' + useItem + ' available.')
                elif res == INVALID:
                    sysMessage.set('Can not use ' + useItem + '.')
                    tkMessageBox.showwarning('Invalid', 'Can not use ' + useItem + '.')
                else:
                    description = 'Quantity in inventory: ' + str(self.parent.m_inventory.m_use[useItem]) + '\n\n'
                    if chosenType.get() in ['Special', 'Hammer', 'Cube']:
                        description += SpecialLib.m_lib[useItem]['description']
                    else:
                        description += ScrollLib.showScrollStat(useItem)
                    useDescriptionContent.config(state=Tkinter.NORMAL)
                    useDescriptionContent.delete('1.0', Tkinter.END)
                    useDescriptionContent.insert('insert', description)
                    useDescriptionContent.config(state=Tkinter.DISABLED)
                    try:
                        if useItem == self.parent.tabPurchase.listboxList[self.parent.tabPurchase.curSelectIdx]:
                            description = useItem + '\n\n' + description
                            self.parent.tabPurchase.descriptionContent.config(state=Tkinter.NORMAL)
                            self.parent.tabPurchase.descriptionContent.delete('1.0', Tkinter.END)
                            self.parent.tabPurchase.descriptionContent.insert('insert', description)
                            self.parent.tabPurchase.descriptionContent.config(state=Tkinter.DISABLED)
                    except:
                        pass
                    if res == FAIL:
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
                        effect = res[0]
                        newPot = res[1]
                        if effect == 'Reset Potential':
                            message = 'New Potential:\n-------------\n'
                            if newPot.m_rank > self.parent.m_inventory.m_equip[self.m_selectedEquipIdx].m_pot.m_rank:
                                message += '***TIER UP!***\n\n'
                            self.parent.m_inventory.setEquipPot(newPot, self.m_selectedEquipIdx)
                            message += self.parent.m_inventory.m_equip[self.m_selectedEquipIdx].m_pot.showPot()
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
                            tkMessageBox.showinfo('Potential Reset', message)
                        elif effect == 'Choose Potential':
                            def select():
                                if choice.get() == 1:
                                    self.parent.m_inventory.setEquipPot(newPot, self.m_selectedEquipIdx)
                                    self.equipStats.set(self.parent.m_inventory.m_equip[self.m_selectedEquipIdx].showEquip())
                                    equipStatsContent.config(state=Tkinter.NORMAL)
                                    equipStatsContent.delete('1.0', Tkinter.END)
                                    equipStatsContent.insert('insert', self.equipStats.get())
                                    equipStatsContent.config(state=Tkinter.DISABLED)
                                    self.equipStatsContent.config(state=Tkinter.NORMAL)
                                    self.equipStatsContent.delete('1.0', Tkinter.END)
                                    self.equipStatsContent.insert('insert', self.equipStats.get())
                                    self.equipStatsContent.config(state=Tkinter.DISABLED)
                                    sysMessage.set('New potential is chosen.')
                                else:
                                    sysMessage.set('Original potential is kept.')
                                selectPotPopup.destroy()
                            choice = Tkinter.IntVar()
                            choice.set(0)
                            selectPotPopup = Tkinter.Toplevel(toplevel)
                            selectPotPopup.grab_set()
                            selectPotPopup.title('Choose Potential')
                            selectPotPopup.geometry('500x200+350+350')
                            oldPotMessage = self.parent.m_inventory.m_equip[self.m_selectedEquipIdx].m_pot.showPot()
                            newPotMessage = ''
                            if newPot.m_rank > self.parent.m_inventory.m_equip[self.m_selectedEquipIdx].m_pot.m_rank:
                                newPotMessage += '***TIER UP!***\n\n'
                            newPotMessage += newPot.showPot()
                            oldPotLabel = Tkinter.Label(selectPotPopup, text='Original\n-----------------')
                            newPotLabel = Tkinter.Label(selectPotPopup, text='New\n-----------------')
                            oldPotContent = Tkinter.Label(selectPotPopup, text=oldPotMessage)
                            newPotContent = Tkinter.Label(selectPotPopup, text=newPotMessage)
                            oldPotRadio = Tkinter.Radiobutton(selectPotPopup, text='', variable=choice, value=0)
                            newPotRadio = Tkinter.Radiobutton(selectPotPopup, text='', variable=choice, value=1)
                            selectButton = Tkinter.Button(selectPotPopup, text='Select', command=select, pady=5)

                            selectPotPopup.rowconfigure(1, weight=1)
                            selectPotPopup.columnconfigure(0, weight=1)
                            selectPotPopup.columnconfigure(1, weight=1)
                            oldPotLabel.grid(row=0, column=0, sticky=Tkinter.N)
                            newPotLabel.grid(row=0, column=1, sticky=Tkinter.N)
                            oldPotContent.grid(row=1, column=0, sticky=Tkinter.N)
                            newPotContent.grid(row=1, column=1, sticky=Tkinter.N)
                            oldPotRadio.grid(row=2, column=0)
                            newPotRadio.grid(row=2, column=1)
                            selectButton.grid(row=3, column=0, columnspan=2)
                        elif effect == 'Pick Potential Lines':
                            def select():
                                selectedNum = 0
                                for i in range(linesNum*2):
                                    selectedNum += checkboxVars[i].get()
                                if selectedNum != linesNum:
                                    tkMessageBox.showwarning('Wrong Selections', 'Please choose exactly ' + str(linesNum) + ' lines.')
                                else:
                                    self.parent.m_inventory.m_equip[self.m_selectedEquipIdx].m_pot.m_rank = newPot.m_rank
                                    self.parent.m_inventory.m_equip[self.m_selectedEquipIdx].m_pot.m_lines = []
                                    for i in range(linesNum*2):
                                        if checkboxVars[i].get():
                                            self.parent.m_inventory.m_equip[self.m_selectedEquipIdx].m_pot.m_lines.append(newPot.m_lines[i])
                                    self.equipStats.set(self.parent.m_inventory.m_equip[self.m_selectedEquipIdx].showEquip())
                                    equipStatsContent.config(state=Tkinter.NORMAL)
                                    equipStatsContent.delete('1.0', Tkinter.END)
                                    equipStatsContent.insert('insert', self.equipStats.get())
                                    equipStatsContent.config(state=Tkinter.DISABLED)
                                    self.equipStatsContent.config(state=Tkinter.NORMAL)
                                    self.equipStatsContent.delete('1.0', Tkinter.END)
                                    self.equipStatsContent.insert('insert', self.equipStats.get())
                                    self.equipStatsContent.config(state=Tkinter.DISABLED)
                                    sysMessage.set('New potential is chosen.')
                                    selectPotPopup.destroy()

                            # default: 0, 1, (2)
                            linesNum = len(self.parent.m_inventory.m_equip[self.m_selectedEquipIdx].m_pot.m_lines)
                            origRank = self.parent.m_inventory.m_equip[self.m_selectedEquipIdx].m_pot.m_rank
                            self.parent.m_inventory.m_equip[self.m_selectedEquipIdx].m_pot.m_rank = newPot.m_rank
                            self.parent.m_inventory.m_equip[self.m_selectedEquipIdx].m_pot.m_lines = []
                            for i in range(linesNum):
                                self.parent.m_inventory.m_equip[self.m_selectedEquipIdx].m_pot.m_lines.append(newPot.m_lines[i])
                            self.equipStats.set(self.parent.m_inventory.m_equip[self.m_selectedEquipIdx].showEquip())
                            equipStatsContent.config(state=Tkinter.NORMAL)
                            equipStatsContent.delete('1.0', Tkinter.END)
                            equipStatsContent.insert('insert', self.equipStats.get())
                            equipStatsContent.config(state=Tkinter.DISABLED)
                            self.equipStatsContent.config(state=Tkinter.NORMAL)
                            self.equipStatsContent.delete('1.0', Tkinter.END)
                            self.equipStatsContent.insert('insert', self.equipStats.get())
                            self.equipStatsContent.config(state=Tkinter.DISABLED)
                            
                            selectPotPopup = Tkinter.Toplevel(toplevel)
                            selectPotPopup.grab_set()
                            selectPotPopup.title('Select Potential Lines')
                            selectPotPopup.geometry('320x280+350+350')
                            message = 'Select ' + str(linesNum) + ' lines:\n-------------------\n'
                            if newPot.m_rank > origRank:
                                message += '***TIER UP!***\n'
                            message += '\n('+ rank_label[newPot.m_rank] + ')'
                            messageLabel = Tkinter.Label(selectPotPopup, text=message)
                            showPotList = newPot.getShowPotList()
                            checkboxVars = []
                            for i in range(linesNum*2):
                                checkboxVars.append(Tkinter.IntVar())
                            checkboxes = [None]*(linesNum*2)
                            for i in range(linesNum*2):
                                checkboxes[i] = Tkinter.Checkbutton(selectPotPopup, text=showPotList[i], variable=checkboxVars[i])
                            selectButton = Tkinter.Button(selectPotPopup, text='Select', command=select, pady=5)

                            for col in range(11):
                                selectPotPopup.columnconfigure(col, weight=1)
                            selectPotPopup.rowconfigure(linesNum*2+1, weight=1)
                            messageLabel.grid(row=0, column=0, columnspan=11)
                            for i in range(linesNum*2):
                                checkboxes[i].grid(row=i+1, column=5, sticky=Tkinter.W)
                            selectButton.grid(row=linesNum*2+1, column=0, columnspan=11)

                                            

        toplevel = Tkinter.Toplevel(self)
        toplevel.grab_set()
        toplevel.title('Upgrade Equipment')
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
        typeOptionMenu = Tkinter.OptionMenu(toplevel.Frameleft, chosenType, *types, command=lambda x:update())
        useOptionMenu = Tkinter.OptionMenu(toplevel.Frameleft, chosenUse, *uses)
        useOptionMenu['menu'].delete(0, 'end')

        useDescriptionContent = ScrolledText.ScrolledText(toplevel.Frameleft,
                                                      wrap=Tkinter.WORD,
                                                      width=20)
        useDescriptionContent.config(font=('San Francisco', 13, 'normal'))
        useDescriptionContent.insert('insert', '')
        useDescriptionContent.config(state=Tkinter.DISABLED)

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
                            padx=5, sticky=Tkinter.W)
        useOptionMenu.grid(row=1, column=0, rowspan=1, columnspan=2,
                            padx=5, sticky=Tkinter.W)
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
            if self.m_selectedEquipIdx in self.parent.m_inventory.m_equipped.values():
                message = 'Can\'t. ' + self.parent.m_inventory.m_equip[self.m_selectedEquipIdx].m_name + ' is equipped.'
                tkMessageBox.showwarning('Invalid', message)
                return
            
            self.parent.tabEquip.reset()
            
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

##        self.equipCreateButton = Tkinter.Button(self.Frameleft, text='Create', command=self.equipCreateButtonClicked)
        self.equipModifyButton = Tkinter.Button(self.Frameleft, text='Upgrade', command=self.equipModifyButtonClicked)
        self.equipDeleteButton = Tkinter.Button(self.Frameleft, text='Delete', command=self.equipDeleteButtonClicked)
 
        self.equipStats = Tkinter.StringVar()
        self.equipStatsContent = ScrolledText.ScrolledText(self.Frameright,
                                                           wrap=Tkinter.WORD,
                                                           width=40)
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
##        self.equipCreateButton.grid(row=6, column=0, padx=5, pady=5, sticky=Tkinter.W)
        self.equipModifyButton.grid(row=6, column=0, padx=5, pady=5, sticky=Tkinter.W)
        self.equipDeleteButton.grid(row=6, column=2, padx=5, pady=5, sticky=Tkinter.E)
        self.equipStatsLabel.grid(row=0, column=0, rowspan=1, columnspan=3, padx=5, pady=5)
        self.equipStatsContent.grid(row=1, column=0,
                                  rowspan=5, columnspan=3,
                                  padx=5, pady=5,
                                  sticky=Tkinter.N+Tkinter.S+Tkinter.W,
                                  )
        
        self.Frameleft.pack(fill=Tkinter.BOTH, expand=1, side=Tkinter.LEFT)
        self.Frameright.pack(fill=Tkinter.BOTH, expand=1, side=Tkinter.RIGHT)

class EquipWidget(Tkinter.Frame):
    
    def __init__(self, parent):
        Tkinter.Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
        self.curEquipIdx = -1
        self.selectEquipIdx = -1
        self.equipIdxList = []

    def reset(self):
        self.equipStatsContent.config(state=Tkinter.NORMAL)
        self.equipStatsContent.delete('1.0', Tkinter.END)
        self.equipStatsContent.config(state=Tkinter.DISABLED)
        self.charStatsContent.config(state=Tkinter.NORMAL)
        self.charStatsContent.delete('1.0', Tkinter.END)
        self.charStatsContent.config(state=Tkinter.DISABLED)
        self.chosenType.set('- Choose Slot -')
        size = self.currentEquipListbox.size()
        if size:
            self.currentEquipListbox.delete(0, size-1)
        size = self.equipListbox.size()
        if size:
            self.equipListbox.delete(0, size-1)
        self.curEquipIdx = -1
        self.selectEquipIdx = -1
        self.equipIdxList = []

    def currentEquipListboxSelect(self, event):
        if self.curEquipIdx != -1:
            curEquipStats = self.parent.m_inventory.m_equip[self.curEquipIdx].showEquip()
            self.equipStatsContent.config(state=Tkinter.NORMAL)
            self.equipStatsContent.delete('1.0', Tkinter.END)
            self.equipStatsContent.insert('insert', curEquipStats)
            self.equipStatsContent.config(state=Tkinter.DISABLED)
    
    def equipListboxSelect(self, event):
        listbox = event.widget
        choice = listbox.curselection()
        if len(choice) != 0:
            idx = choice[0]
            value = listbox.get(choice[0])
            self.selectEquipIdx = idx
            equip = self.parent.m_inventory.m_equip[self.equipIdxList[idx]]
            self.equipStatsContent.config(state=Tkinter.NORMAL)
            self.equipStatsContent.delete('1.0', Tkinter.END)
            self.equipStatsContent.insert('insert', equip.showEquip())
            self.equipStatsContent.config(state=Tkinter.DISABLED)
        else:
            self.selectEquipIdx = -1

    def updateEquipListbox(self, event):
            size = self.currentEquipListbox.size()
            if size:
                self.currentEquipListbox.delete(0, size-1)
            size = self.equipListbox.size()
            if size:
                self.equipListbox.delete(0, size-1)
            self.curEquipIdx = self.parent.m_inventory.m_equipped[self.chosenType.get()]
            if self.curEquipIdx != -1:
                self.currentEquipListbox.insert(Tkinter.END, self.parent.m_inventory.m_equip[self.curEquipIdx].m_name)
            self.equipIdxList = self.parent.m_inventory.getEquipIdxListbySlot(self.chosenType.get())
            for idx in self.equipIdxList:
                self.equipListbox.insert(Tkinter.END, self.parent.m_inventory.m_equip[idx].m_name)
            self.equipStatsContent.config(state=Tkinter.NORMAL)
            self.equipStatsContent.delete('1.0', Tkinter.END)
            if self.curEquipIdx != -1:
                self.equipStatsContent.insert('insert', self.parent.m_inventory.m_equip[self.curEquipIdx].showEquip())
                self.currentEquipListbox.selection_set(0)
            self.equipStatsContent.config(state=Tkinter.DISABLED)
            self.selectEquipIdx = -1

    def onEquip(self):
        if self.curEquipIdx != -1 or self.selectEquipIdx == -1:
            return INVALID
        self.parent.m_inventory.onEquip(self.chosenType.get(), self.equipIdxList[self.selectEquipIdx])
        self.curEquipIdx = self.equipIdxList[self.selectEquipIdx]
        self.currentEquipListbox.insert(Tkinter.END, self.parent.m_inventory.m_equip[self.curEquipIdx].m_name)

    def offEquip(self):
        if self.curEquipIdx == -1:
            return INVALID
        self.parent.m_inventory.offEquip(self.chosenType.get())
        self.currentEquipListbox.delete(0)
        self.curEquipIdx = -1

    def offEquipAll(self):
        for t in self.types:
            self.parent.m_inventory.offEquip(t)
            self.reset()
    
    def initUI(self):

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        
        self.Frameleft = Tkinter.Frame(self, padx=5, pady=5)
        self.Frameleft.rowconfigure(4, weight=1)
        self.Frameright = Tkinter.Frame(self, padx=5, pady=5)
        self.Frameright.rowconfigure(1, weight=1)
        self.Frameright.rowconfigure(5, weight=1)
        
        self.types = sorted(EquipSlot.m_lib.keys())
        self.chosenType = Tkinter.StringVar()
        self.chosenType.set('- Choose Slot -')
        self.typeOptionMenu = Tkinter.OptionMenu(self.Frameleft, self.chosenType, *self.types, command=self.updateEquipListbox)

        self.currentEquipListbox = Tkinter.Listbox(self.Frameleft, selectmode='single', height=1)
        self.equipListbox = Tkinter.Listbox(self.Frameleft, selectmode='single')
        self.currentEquipListbox.bind('<<ListboxSelect>>', self.currentEquipListboxSelect)
        self.equipListbox.bind('<<ListboxSelect>>', self.equipListboxSelect)
        self.equipButton = Tkinter.Button(self.Frameleft, text='Equip', command=self.onEquip)
        self.unequipButton = Tkinter.Button(self.Frameleft, text='Unequip', command=self.offEquip)
        self.unequipAllButton = Tkinter.Button(self.Frameright, text='Unequip All', command=self.offEquipAll)

        self.equipStatsContent = ScrolledText.ScrolledText(self.Frameright,
                                                           wrap=Tkinter.WORD,
                                                           width=35, height=10)
        self.equipStatsContent.config(font=('San Francisco', 13, 'normal'))
        self.equipStatsContent.insert('insert', '')
        self.equipStatsContent.config(state=Tkinter.DISABLED)

        self.charStatsContent = ScrolledText.ScrolledText(self.Frameright,
                                                           wrap=Tkinter.WORD,
                                                           width=35, height=10)
        self.charStatsContent.config(font=('San Francisco', 13, 'normal'))
        self.charStatsContent.insert('insert', '')
        self.charStatsContent.config(state=Tkinter.DISABLED)

        self.currentEquipLabel = Tkinter.Label(self.Frameleft, text='Currently Equipped:')
        self.inventoryEquipLabel = Tkinter.Label(self.Frameleft, text='Inventory:')
        self.equipStatsLabel = Tkinter.Label(self.Frameright, text='Selected Equip Stats')
        self.charStatsLabel = Tkinter.Label(self.Frameright, text='Character Stats')

        self.typeOptionMenu.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky=Tkinter.W)
        self.currentEquipLabel.grid(row=1, column=0, padx=5, pady=5, sticky=Tkinter.W)
        self.currentEquipListbox.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky=Tkinter.W+Tkinter.E)
        self.inventoryEquipLabel.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky=Tkinter.W)
        self.equipListbox.grid(row=4, column=0, rowspan=3, columnspan=3, padx=5, pady=5, sticky=Tkinter.W+Tkinter.E+Tkinter.N+Tkinter.S)
        self.equipButton.grid(row=7, column=0, padx=5, pady=5, sticky=Tkinter.W)
        self.unequipButton.grid(row=7, column=2, padx=5, pady=5, sticky=Tkinter.E)

        self.equipStatsLabel.grid(row=0, column=0, padx=5, pady=5, sticky=Tkinter.W)
        self.equipStatsContent.grid(row=1, column=0,
                                    rowspan=3, columnspan=3,
                                    padx=5, pady=5,
                                    sticky=Tkinter.N+Tkinter.S+Tkinter.W)
        self.charStatsLabel.grid(row=4, column=0, padx=5, pady=5, sticky=Tkinter.W)
        self.charStatsContent.grid(row=5, column=0,
                                    rowspan=2, columnspan=3,
                                    padx=5, pady=5,
                                    sticky=Tkinter.N+Tkinter.S+Tkinter.W)
        self.unequipAllButton.grid(row=8, column=2, padx=5, pady=5, sticky=Tkinter.E)
        
        self.Frameleft.pack(fill=Tkinter.BOTH, expand=1, side=Tkinter.LEFT)
        self.Frameright.pack(fill=Tkinter.BOTH, expand=1, side=Tkinter.RIGHT)

class PurchaseWidget(Tkinter.Frame):

    def __init__(self, parent):
        Tkinter.Frame.__init__(self, parent)
        self.parent = parent
        self.curChosenType = '- Choose Type -'
        self.curChosenCategory = '- Choose Category -'
        self.listboxList = []
        self.curSelectIdx = -1
        self.initUI()

    def reset(self):
        self.curChosenType = '- Choose Type -'
        self.chosenType.set('- Choose Type -')
        self.curChosenCategory = '- Choose Category -'
        self.chosenCategory.set('- Choose Category -')
        self.listboxList = []
        self.curSelectIdx = -1
        size = self.itemListbox.size()
        if size:
            self.itemListbox.delete(0, size-1)
        self.descriptionContent.config(state=Tkinter.NORMAL)
        self.descriptionContent.delete('1.0', Tkinter.END)
        self.descriptionContent.config(state=Tkinter.DISABLED)
        self.marketInfoContent.config(state=Tkinter.NORMAL)
        self.marketInfoContent.delete('1.0', Tkinter.END)
        self.marketInfoContent.config(state=Tkinter.DISABLED)
        message = 'Meso: ' + EtcLib.dispLongNum(self.parent.m_inventory.m_etc['Meso']) + '\n'
        message += 'NX: ' + EtcLib.dispLongNum(self.parent.m_inventory.m_etc['NX'])
        self.resourceContent.set(message)

    def updateType(self, event):
        def setUpCategory(option):
            self.chosenCategory.set(option)
            self.updateCategory()
            
        chosenType = self.chosenType.get()
        if self.curChosenType == chosenType:
            return
        self.curChosenType = chosenType
        self.chosenCategory.set('- Choose Category -')
        self.curChosenCategory = '- Choose Category -'
        self.descriptionContent.config(state=Tkinter.NORMAL)
        self.descriptionContent.delete('1.0', Tkinter.END)
        self.descriptionContent.config(state=Tkinter.DISABLED)
        self.marketInfoContent.config(state=Tkinter.NORMAL)
        self.marketInfoContent.delete('1.0', Tkinter.END)
        self.marketInfoContent.config(state=Tkinter.DISABLED)
        size = self.itemListbox.size()
        if size:
            self.itemListbox.delete(0, size-1)
        self.listboxList = []
        self.curSelectIdx = -1

        if chosenType == 'Equip':
            equipTypes = sorted(EquipLib.m_lib.keys())
            self.categoryOptionMenu['menu'].delete(0, 'end')
            for equipType in equipTypes:
                self.categoryOptionMenu['menu'].add_command(label=equipType,
                                                    command=lambda name=equipType: setUpCategory(name))
        elif chosenType == 'Use':
            useTypes = ['Special', 'Hammer', 'Cube', 'Scroll', 'Trace']
            self.categoryOptionMenu['menu'].delete(0, 'end')
            for useType in useTypes:
                self.categoryOptionMenu['menu'].add_command(label=useType,
                                                    command=lambda name=useType: setUpCategory(name))
        elif chosenType == 'Etc':
            etcTypes = ['Trace', 'Meso', 'NX', 'Coin']
            self.categoryOptionMenu['menu'].delete(0, 'end')
            for etcType in etcTypes:
                self.categoryOptionMenu['menu'].add_command(label=etcType,
                                                    command=lambda name=etcType: setUpCategory(name))

    def updateCategory(self):
            chosenCategory = self.chosenCategory.get()
            if self.curChosenCategory == chosenCategory:
                return
            self.curChosenCategory = chosenCategory
            self.descriptionContent.config(state=Tkinter.NORMAL)
            self.descriptionContent.delete('1.0', Tkinter.END)
            self.descriptionContent.config(state=Tkinter.DISABLED)
            self.marketInfoContent.config(state=Tkinter.NORMAL)
            self.marketInfoContent.delete('1.0', Tkinter.END)
            self.marketInfoContent.config(state=Tkinter.DISABLED)
            size = self.itemListbox.size()
            if size:
                self.itemListbox.delete(0, size-1)
            self.listboxList = []
            self.curSelectIdx = -1

            if self.curChosenType == 'Equip':
                self.listboxList = sorted(EquipLib.m_lib[chosenCategory].keys())
                print self.listboxList
                for equipName in self.listboxList:
                    self.itemListbox.insert(Tkinter.END, equipName)
            elif self.curChosenType == 'Use':
                usesLib = {}
                usesLib.update(ScrollLib.m_lib)
                usesLib.update(SpecialLib.m_lib)
                self.listboxList = sorted([key for key in usesLib.keys() if usesLib[key]['type'] == chosenCategory])
                for useName in self.listboxList:
                    self.itemListbox.insert(Tkinter.END, useName)
            elif self.curChosenType == 'Etc':
                etcLib = EtcLib.m_lib
                self.listboxList = sorted([key for key in etcLib.keys() if etcLib[key]['type'] == chosenCategory])
                for etcName in self.listboxList:
                    self.itemListbox.insert(Tkinter.END, etcName)
                
                

    def itemListboxSelect(self, event):
        listbox = event.widget
        choice = listbox.curselection()
        if len(choice) != 0:
            idx = choice[0]
            value = listbox.get(choice[0])
            self.curSelectIdx = idx
        else:
            self.curSelectIdx = -1
        if self.curSelectIdx == -1:
            return
        if self.curChosenType == 'Equip':
            equip = Equip(self.listboxList[self.curSelectIdx])
            equip.setClean()
            self.descriptionContent.config(state=Tkinter.NORMAL)
            self.descriptionContent.delete('1.0', Tkinter.END)
            self.descriptionContent.insert('insert', equip.showEquip())
            self.descriptionContent.config(state=Tkinter.DISABLED)
            self.marketInfoContent.config(state=Tkinter.NORMAL)
            self.marketInfoContent.delete('1.0', Tkinter.END)
            self.marketInfoContent.insert('insert', self.parent.m_marketInfo.showMarketInfo(equip.m_name, self.parent.m_inventory.m_etc))
            self.marketInfoContent.config(state=Tkinter.DISABLED)
        elif self.curChosenType == 'Use':
            scrollName = self.listboxList[self.curSelectIdx]
            description = scrollName + '\n\n'
            description += 'Quantity in inventory: ' + EtcLib.dispLongNum(self.parent.m_inventory.m_use[scrollName]) + '\n\n'
            if self.curChosenCategory in ['Special', 'Hammer', 'Cube']:
                description += SpecialLib.m_lib[scrollName]['description']
                self.descriptionContent.config(state=Tkinter.NORMAL)
                self.descriptionContent.delete('1.0', Tkinter.END)
                self.descriptionContent.insert('insert', description)
                self.descriptionContent.config(state=Tkinter.DISABLED)
            else:
                description += ScrollLib.showScrollStat(scrollName)
                self.descriptionContent.config(state=Tkinter.NORMAL)
                self.descriptionContent.delete('1.0', Tkinter.END)
                self.descriptionContent.insert('insert', description)
                self.descriptionContent.config(state=Tkinter.DISABLED)
            self.marketInfoContent.config(state=Tkinter.NORMAL)
            self.marketInfoContent.delete('1.0', Tkinter.END)
            self.marketInfoContent.insert('insert', self.parent.m_marketInfo.showMarketInfo(scrollName, self.parent.m_inventory.m_etc))
            self.marketInfoContent.config(state=Tkinter.DISABLED)
                
        elif self.curChosenType == 'Etc':
            etcName = self.listboxList[self.curSelectIdx]
            description = etcName + '\n\n'
            description += EtcLib.m_lib[etcName]['description']
            self.descriptionContent.config(state=Tkinter.NORMAL)
            self.descriptionContent.delete('1.0', Tkinter.END)
            self.descriptionContent.insert('insert', description)
            self.descriptionContent.config(state=Tkinter.DISABLED)
            self.marketInfoContent.config(state=Tkinter.NORMAL)
            self.marketInfoContent.delete('1.0', Tkinter.END)
            self.marketInfoContent.insert('insert', self.parent.m_marketInfo.showMarketInfo(etcName, self.parent.m_inventory.m_etc))
            self.marketInfoContent.config(state=Tkinter.DISABLED)
            
        
    def purchaseButtonClicked(self):
        def purchaseEquip():
            choiceIdx = radioButtonVar.get()
            if choiceIdx == -1:
                tkMessageBox.showwarning('Invalid', 'Please select payment type.')
                return
            marketInfo = self.parent.m_marketInfo.m_info[equipName]
            availPay = self.parent.m_inventory.m_etc[marketInfo['cost'][choiceIdx]]
            if marketInfo['stock'][choiceIdx] == 0:
                tkMessageBox.showwarning('Invalid', 'Out of stock.')
                return
            elif marketInfo['value'][choiceIdx] > availPay:
                message = 'Can not afford.\n\n'
                message += 'Price: ' + EtcLib.dispLongNum(marketInfo['value'][choiceIdx]) + ' ' + marketInfo['cost'][choiceIdx] + '.\n'
                message += 'You only have ' + EtcLib.dispLongNum(availPay) + ' ' + marketInfo['cost'][choiceIdx] + '.'
                tkMessageBox.showwarning('Invalid', message)
                return
            else:
                message = 'Are You Sure?\n\n'
                message += 'Price: ' + EtcLib.dispLongNum(marketInfo['value'][choiceIdx]) + ' ' + marketInfo['cost'][choiceIdx] + '.\n'
                message += 'You have ' + EtcLib.dispLongNum(availPay) + ' ' + marketInfo['cost'][choiceIdx] + '.'
                res = tkMessageBox.askquestion('Purchase', message, type='yesno')
                if res == 'yes':
                    self.parent.m_inventory.m_etc[marketInfo['cost'][choiceIdx]] -= marketInfo['value'][choiceIdx]
                    if marketInfo['stock'][choiceIdx] != -1:
                        self.parent.m_marketInfo.m_info[equipName]['stock'][choiceIdx] -= 1
                    self.parent.m_inventory.createEquip(self.listboxList[self.curSelectIdx])

                    message = 'Meso: ' + EtcLib.dispLongNum(self.parent.m_inventory.m_etc['Meso']) + '\n'
                    message += 'NX: ' + EtcLib.dispLongNum(self.parent.m_inventory.m_etc['NX'])
                    self.resourceContent.set(message)
                    self.marketInfoContent.config(state=Tkinter.NORMAL)
                    self.marketInfoContent.delete('1.0', Tkinter.END)
                    self.marketInfoContent.insert('insert', self.parent.m_marketInfo.showMarketInfo(equipName, self.parent.m_inventory.m_etc))
                    self.marketInfoContent.config(state=Tkinter.DISABLED)
                    self.parent.tabInventory.reset()
                    self.parent.tabEquip.reset()
                    toplevel.destroy()

            
        def purchaseUse():
            choiceIdx = radioButtonVar.get()
            if choiceIdx == -1:
                tkMessageBox.showwarning('Invalid', 'Please select payment type.')
                return
            value = quantityEntry.get()
            try: 
                quantity = int(value)
                assert quantity > 0
            except Exception:
                tkMessageBox.showwarning('Invalid', 'Invalid input!')
                return
            marketInfo = self.parent.m_marketInfo.m_info[scrollName]
            availPay = self.parent.m_inventory.m_etc[marketInfo['cost'][choiceIdx]]
            if marketInfo['stock'][choiceIdx] == 0:
                tkMessageBox.showwarning('Invalid', 'Out of stock.')
                return
            elif marketInfo['stock'][choiceIdx] != -1 and marketInfo['stock'][choiceIdx] < quantity:
                message = 'Only ' + EtcLib.dispLongNum(marketInfo['stock'][choiceIdx]) + ' in stock.\n'
                tkMessageBox.showwarning('Invalid', message)
                return
            elif marketInfo['value'][choiceIdx] * quantity > availPay:
                message = 'Can not afford.\n\n'
                message += 'Price: ' + EtcLib.dispLongNum(marketInfo['value'][choiceIdx] * quantity) + ' ' + marketInfo['cost'][choiceIdx] + '.\n'
                message += 'You only have ' + EtcLib.dispLongNum(availPay) + ' ' + marketInfo['cost'][choiceIdx] + '.'
                tkMessageBox.showwarning('Invalid', message)
                return
            else:
                message = 'Are You Sure?\n\n'
                message += 'Purchasing ' + EtcLib.dispLongNum(quantity) + ' ' + self.listboxList[self.curSelectIdx] + '.\n'
                message += 'Price: ' + EtcLib.dispLongNum(marketInfo['value'][choiceIdx] * quantity) + ' ' + marketInfo['cost'][choiceIdx] + '.\n'
                message += 'You have ' + EtcLib.dispLongNum(availPay) + ' ' + marketInfo['cost'][choiceIdx] + '.'
                res = tkMessageBox.askquestion('Purchase', message, type='yesno')
                if res == 'yes':
                    self.parent.m_inventory.m_etc[marketInfo['cost'][choiceIdx]] -= (marketInfo['value'][choiceIdx] * quantity)
                    if marketInfo['stock'][choiceIdx] != -1:
                        self.parent.m_marketInfo.m_info[scrollName]['stock'][choiceIdx] -= quantity
                    self.parent.m_inventory.m_use[self.listboxList[self.curSelectIdx]] += quantity

                    message = 'Meso: ' + EtcLib.dispLongNum(self.parent.m_inventory.m_etc['Meso']) + '\n'
                    message += 'NX: ' + EtcLib.dispLongNum(self.parent.m_inventory.m_etc['NX'])
                    self.resourceContent.set(message)
                    self.marketInfoContent.config(state=Tkinter.NORMAL)
                    self.marketInfoContent.delete('1.0', Tkinter.END)
                    self.marketInfoContent.insert('insert', self.parent.m_marketInfo.showMarketInfo(scrollName, self.parent.m_inventory.m_etc))
                    self.marketInfoContent.config(state=Tkinter.DISABLED)
                    self.parent.tabInventory.reset()
                    description = scrollName + '\n\n'
                    description += 'Quantity in inventory: ' + EtcLib.dispLongNum(self.parent.m_inventory.m_use[scrollName]) + '\n\n'
                    if self.curChosenCategory in ['Special', 'Hammer', 'Cube']:
                        description += SpecialLib.m_lib[scrollName]['description']
                        self.descriptionContent.config(state=Tkinter.NORMAL)
                        self.descriptionContent.delete('1.0', Tkinter.END)
                        self.descriptionContent.insert('insert', description)
                        self.descriptionContent.config(state=Tkinter.DISABLED)
                    else:
                        description += ScrollLib.showScrollStat(scrollName)
                        self.descriptionContent.config(state=Tkinter.NORMAL)
                        self.descriptionContent.delete('1.0', Tkinter.END)
                        self.descriptionContent.insert('insert', description)
                        self.descriptionContent.config(state=Tkinter.DISABLED)
##                    self.parent.tabEquip.reset()
                    toplevel.destroy()
                
        if self.curSelectIdx == -1:
            return
        if self.curChosenType == 'Equip':
            equipName = self.listboxList[self.curSelectIdx]
            choiceNum = self.parent.m_marketInfo.getPaymentTypeNum(equipName)
            if choiceNum == 0:
                tkMessageBox.showwarning('Not available', 'Not available for purchase.')
                return
            toplevel = Tkinter.Toplevel(self)
            toplevel.title('Purchase')
            height = choiceNum * 80 + 150
            toplevel.geometry('300x'+str(height)+'+300+300')
            toplevel.grab_set()
            choiceLabel = Tkinter.Label(toplevel, text='Choose Payment\n-------------------')
            
            radioButtons = []
            radioButtonVar = Tkinter.IntVar()
            radioButtonVar.set(-1)
            for i in range(choiceNum):
                choiceInfo = self.parent.m_marketInfo.showPurchaseChoice(equipName, i)
                radioButton = Tkinter.Radiobutton(toplevel, text=choiceInfo, variable=radioButtonVar, value=i, justify=Tkinter.LEFT)
                radioButtons.append(radioButton)
                
            purchaseButton = Tkinter.Button(toplevel, text='Purchase', command=purchaseEquip)
            cancelButton = Tkinter.Button(toplevel, text='Cancel', command=toplevel.destroy)

            toplevel.columnconfigure(0, weight=1)
            toplevel.columnconfigure(1, weight=1)
            toplevel.columnconfigure(2, weight=1)
            choiceLabel.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
            for i in range(choiceNum):
                toplevel.rowconfigure(i+1, weight=1)
                radioButtons[i].grid(row=i+1, column=1, columnspan=2, padx=5, pady=5, sticky=Tkinter.W)
            purchaseButton.grid(row=choiceNum+1, column=0, columnspan=3, padx=5, pady=5)
            cancelButton.grid(row=choiceNum+2, column=0, columnspan=3, padx=5, pady=5)
                            
        elif self.curChosenType == 'Use':
            scrollName = self.listboxList[self.curSelectIdx]
            choiceNum = self.parent.m_marketInfo.getPaymentTypeNum(scrollName)
            toplevel = Tkinter.Toplevel(self)
            toplevel.title('Purchase')
            height = choiceNum * 80 + 150
            toplevel.geometry('300x'+str(height)+'+300+300')
            toplevel.grab_set()
            toplevel.columnconfigure(0, weight=1)
            toplevel.columnconfigure(1, weight=1)
            toplevel.columnconfigure(2, weight=1)
            quantityLabel = Tkinter.Label(toplevel, text='Quantity:')
            quantityEntry = Tkinter.Entry(toplevel)

            choiceLabel = Tkinter.Label(toplevel, text='Choose Payment\n-------------------')
            
            radioButtons = []
            radioButtonVar = Tkinter.IntVar()
            radioButtonVar.set(-1)
            for i in range(choiceNum):
                choiceInfo = self.parent.m_marketInfo.showPurchaseChoice(scrollName, i)
                radioButton = Tkinter.Radiobutton(toplevel, text=choiceInfo, variable=radioButtonVar, value=i, justify=Tkinter.LEFT)
                radioButtons.append(radioButton)
            
            
            purchaseButton = Tkinter.Button(toplevel, text='Purchase', command=purchaseUse)
            cancelButton = Tkinter.Button(toplevel, text='Cancel', command=toplevel.destroy)

            quantityLabel.grid(row=0, column=0, padx=5, pady=5)
            quantityEntry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
            choiceLabel.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
            for i in range(choiceNum):
                toplevel.rowconfigure(i+2, weight=1)
                radioButtons[i].grid(row=i+2, column=1, columnspan=2, padx=5, pady=5, sticky=Tkinter.W)
            purchaseButton.grid(row=choiceNum+2, column=1, padx=5, pady=5)
            cancelButton.grid(row=choiceNum+3, column=1, padx=5, pady=5)
            
        elif self.curChosenType == 'Etc':
            pass
    
    def initUI(self):

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        
        self.Frameleft = Tkinter.Frame(self, padx=5, pady=10)
        self.Frameleft.rowconfigure(2, weight=1)
        self.Frameright = Tkinter.Frame(self, padx=5, pady=5)
        self.Frameright.rowconfigure(1, weight=1)
        self.Frameright.rowconfigure(5, weight=1)


        self.categories = ['']
        self.chosenCategory = Tkinter.StringVar()
        self.chosenCategory.set('- Choose Category -')
        
        self.types = ['Equip', 'Use', 'Etc']
        self.chosenType = Tkinter.StringVar()
        self.chosenType.set('- Choose Type -')

        self.typeOptionMenu = Tkinter.OptionMenu(self.Frameleft, self.chosenType, *self.types, command=self.updateType)
        self.categoryOptionMenu = Tkinter.OptionMenu(self.Frameleft, self.chosenCategory, *self.categories)
        self.categoryOptionMenu['menu'].delete(0)

        self.itemListbox = Tkinter.Listbox(self.Frameleft, selectmode='single')
        self.itemListbox.bind('<<ListboxSelect>>', self.itemListboxSelect)

        self.resourceContent = Tkinter.StringVar()
        self.resourceLabel = Tkinter.Label(self.Frameleft, textvariable=self.resourceContent, justify=Tkinter.LEFT)
        message = 'Meso: ' + EtcLib.dispLongNum(self.parent.m_inventory.m_etc['Meso']) + '\n'
        message += 'NX: ' + EtcLib.dispLongNum(self.parent.m_inventory.m_etc['NX'])
        self.resourceContent.set(message)

        self.descriptionLabel = Tkinter.Label(self.Frameright, text='Description')
        self.descriptionContent = ScrolledText.ScrolledText(self.Frameright,
                                                           wrap=Tkinter.WORD,
                                                           width=39, height=10)
        self.descriptionContent.config(font=('San Francisco', 13, 'normal'))
        self.descriptionContent.insert('insert', '')
        self.descriptionContent.config(state=Tkinter.DISABLED)
        self.marketInfoLabel = Tkinter.Label(self.Frameright, text='Market Info')
        self.marketInfoContent = ScrolledText.ScrolledText(self.Frameright,
                                                           wrap=Tkinter.WORD,
                                                           width=39, height=10)
        self.marketInfoContent.config(font=('San Francisco', 13, 'normal'))
        self.marketInfoContent.insert('insert', '')
        self.marketInfoContent.config(state=Tkinter.DISABLED)
        self.purchaseButton = Tkinter.Button(self.Frameright, text='Purchase', command=self.purchaseButtonClicked)

        self.typeOptionMenu.grid(row=0, column=0, columnspan=3, padx=5, sticky=Tkinter.W)
        self.categoryOptionMenu.grid(row=1, column=0, columnspan=3, padx=5, sticky=Tkinter.W)
        self.itemListbox.grid(row=2, column=0, rowspan=6, columnspan=3, padx=5, pady=5, sticky=Tkinter.W+Tkinter.E+Tkinter.S+Tkinter.N)
        self.resourceLabel.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky=Tkinter.W)

        self.descriptionLabel.grid(row=0, column=0, padx=5, pady=5, sticky=Tkinter.W)
        self.descriptionContent.grid(row=1, column=0,
                                    rowspan=3, columnspan=3,
                                    padx=5, pady=5,
                                    sticky=Tkinter.N+Tkinter.S+Tkinter.W)
        self.marketInfoLabel.grid(row=4, column=0, padx=5, pady=5, sticky=Tkinter.W)
        self.marketInfoContent.grid(row=5, column=0,
                                    rowspan=3, columnspan=3,
                                    padx=5, pady=5,
                                    sticky=Tkinter.N+Tkinter.S+Tkinter.W)
        self.purchaseButton.grid(row=8, column=2, padx=5, pady=5, sticky=Tkinter.E)
        
        self.Frameleft.pack(fill=Tkinter.BOTH, expand=1, side=Tkinter.LEFT)
        self.Frameright.pack(fill=Tkinter.BOTH, expand=1, side=Tkinter.RIGHT)


class MainWidget(Tkinter.Frame):

    m_inventory = None
    m_marketInfo = None
    m_sysMessage = None
    
    def __init__(self, parent):

        self.m_inventory = Inventory()
        self.m_marketInfo = MarketInfo()
        self.m_sysMessage = Tkinter.StringVar()
        self.m_sysMessage.set('Welcome!')
        Tkinter.Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def saveButtonClicked(self):
        message = 'Save Progress?\n(Old savefiles will be overwritten.)'
        result = tkMessageBox.askquestion("Save", message, icon='warning', type='yesno')
        if result == 'yes':
            with open('savedata', 'wb') as output:
                pickle.dump([self.m_inventory, self.m_marketInfo], output, -1)
            tkMessageBox.showinfo('Save', 'Progress saved.')
            self.m_sysMessage.set('Progress saved.')

    def loadButtonClicked(self):
        message = 'Load Savedata?\n(Current progress will be overwritten.)'
        result = tkMessageBox.askquestion("Load", message, icon='warning', type='yesno')
        if result == 'yes':
            with open('savedata', 'rb') as save:
                oldapp = pickle.load(save)
            self.m_inventory = oldapp[0]
            self.m_marketInfo = oldapp[1]
            tkMessageBox.showinfo('Load', 'Progress loaded.')
            self.m_sysMessage.set('Progress loaded.')
            self.tabInventory.reset()
            self.tabEquip.reset()
            self.tabPurchase.reset()
    
    def quitButtonClicked(self):
        message = 'Are You Sure?'
        result = tkMessageBox.askquestion("Quit", message, icon='warning', type='yesno')
        if result == 'yes':
            self.destroy()
            self.parent.destroy()

    def initUI(self):
        self.parent.title('MS Sim')
        self.pack(fill=Tkinter.BOTH, expand=1)
        self.tabs = ttk.Notebook(self)
        self.tabInventory = InventoryWidget(self)
        self.tabEquip = EquipWidget(self)
        self.tabPurchase = PurchaseWidget(self)
        self.tabs.add(self.tabInventory, text='Inventory')
        self.tabs.add(self.tabEquip, text='Equip')
        self.tabs.add(self.tabPurchase, text='Purchase')

        self.sysMessage = Tkinter.Label(self,
                                        textvariable=self.m_sysMessage,
                                        justify=Tkinter.LEFT)
        self.saveButton = Tkinter.Button(self, text='Save', command=self.saveButtonClicked)
        self.loadButton = Tkinter.Button(self, text='Load', command=self.loadButtonClicked)
        self.quitButton = Tkinter.Button(self, text='Quit', command=self.quitButtonClicked)
        
        self.tabs.pack(fill=Tkinter.BOTH, expand=1)
        self.sysMessage.pack(padx=5, pady=5, side=Tkinter.LEFT)
        self.quitButton.pack(padx=5, pady=5, side=Tkinter.RIGHT)
        self.loadButton.pack(padx=5, pady=5, side=Tkinter.RIGHT)
        self.saveButton.pack(padx=5, pady=5, side=Tkinter.RIGHT)
        
        
        
if __name__ == '__main__':

    root = Tkinter.Tk()
    root.geometry('680x600+200+200')
    app = MainWidget(root)
    root.mainloop()
    
