import pickle, random, os.path
import Tkinter, ttk, tkMessageBox
import ScrolledText

from equip import Equip
from lib.equiplib import EquipLib
from lib.scrolllib import ScrollLib
from lib.speciallib import SpecialLib
from lib.etclib import EtcLib
from lib.joblib import JobLib

from marketinfo import MarketInfo
from character import Character
from potential import rank_label
from inventory import Inventory, SUCCESS, FAIL, BOOM, INVALID, NOITEM

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

