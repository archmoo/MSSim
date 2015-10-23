import pickle, random, os.path
import Tkinter, ttk, tkMessageBox
import ScrolledText

from equip import Equip
from lib.equipslotlib import EquipSlotLib
from lib.equiplib import EquipLib
from lib.scrolllib import ScrollLib
from lib.speciallib import SpecialLib
from lib.etclib import EtcLib
from lib.joblib import JobLib

from marketinfo import MarketInfo
from character import Character
from potential import rank_label
from inventory import Inventory, SUCCESS, FAIL, BOOM, INVALID, NOITEM

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
        self.parent.m_charInfo.updateStats([self.parent.m_inventory.m_equip[i] for i in self.parent.m_inventory.m_equipped.values() if i != -1])
        self.charStatsContent.insert('insert', self.parent.m_charInfo.showCharacterStats())
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
        if self.curEquipIdx != -1:
            tkMessageBox.showwarning('Invalid', 'Please unequip the equipped item.')
            return INVALID

        if self.selectEquipIdx == -1:
            tkMessageBox.showwarning('Invalid', 'Please select a piece of equipment to equip.')
            return INVALID

        equip = self.parent.m_inventory.m_equip[self.equipIdxList[self.selectEquipIdx]]
        try:
            if equip.m_class != 'All':
                charClass = JobLib.m_job[self.parent.m_charInfo.m_job]['class']
                if charClass == 'Thief, Pirate':
                    if equip.m_class not in ['Thief', 'Pirate']:
                        message = 'You can only equip Thief or Pirate equipments.'
                        raise AssertionError(message)
                else:
                    if equip.m_class != charClass:
                        message = 'You can only equip ' + charClass + ' equipments.'
                        raise AssertionError(message)
            if equip.m_type in ['Weapon', 'Secondary', 'Emblem']:
                if equip.m_category not in JobLib.m_job[self.parent.m_charInfo.m_job][equip.m_type]:
                    message = 'You can only equip certain types of equipment as your ' + equip.m_type + ':\n\n'
                    for s in JobLib.m_job[self.parent.m_charInfo.m_job][equip.m_type]:
                        message += s + '\n'
                    raise AssertionError(message)
            if equip.m_type == 'Overall' and self.parent.m_inventory.m_equipped['Bottom'] != -1:
                message = 'You can not equip an Overall item and a Bottom item at the same time.'
                raise AssertionError(message)
            if equip.m_type == 'Bottom' and self.parent.m_inventory.m_equipped['Top'] != -1:
                if self.parent.m_inventory.m_equip[self.parent.m_inventory.m_equipped['Top']].m_type == 'Overall':
                    message = 'You can not equip an Overall item and a Bottom item at the same time.'
                    raise AssertionError(message)
        except AssertionError as e:
            tkMessageBox.showwarning('Invalid', 'Can not equip.\n\n' + message)
            return INVALID

        self.curEquipIdx = self.equipIdxList[self.selectEquipIdx]
        
        self.parent.m_inventory.onEquip(self.chosenType.get(), self.equipIdxList[self.selectEquipIdx])
        self.currentEquipListbox.insert(Tkinter.END, self.parent.m_inventory.m_equip[self.curEquipIdx].m_name)
        self.charStatsContent.config(state=Tkinter.NORMAL)
        self.charStatsContent.delete('1.0', Tkinter.END)
        self.parent.m_charInfo.updateStats([self.parent.m_inventory.m_equip[i] for i in self.parent.m_inventory.m_equipped.values() if i != -1])
        self.charStatsContent.insert('insert', self.parent.m_charInfo.showCharacterStats())
        self.charStatsContent.config(state=Tkinter.DISABLED)

    def offEquip(self):
        if self.curEquipIdx == -1:
            return INVALID
        self.parent.m_inventory.offEquip(self.chosenType.get())
        self.currentEquipListbox.delete(0)
        self.curEquipIdx = -1
        self.charStatsContent.config(state=Tkinter.NORMAL)
        self.charStatsContent.delete('1.0', Tkinter.END)
        self.parent.m_charInfo.updateStats([self.parent.m_inventory.m_equip[i] for i in self.parent.m_inventory.m_equipped.values() if i != -1])
        self.charStatsContent.insert('insert', self.parent.m_charInfo.showCharacterStats())
        self.charStatsContent.config(state=Tkinter.DISABLED)

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
        
        self.types = sorted(EquipSlotLib.m_lib.keys())
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
        self.parent.m_charInfo.updateStats([self.parent.m_inventory.m_equip[i] for i in self.parent.m_inventory.m_equipped.values() if i != -1])
        self.charStatsContent.insert('insert', self.parent.m_charInfo.showCharacterStats())
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

