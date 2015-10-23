import pickle, random, os.path
import Tkinter, ttk, tkMessageBox
import ScrolledText

from equip import Equip
from lib.equiplib import EquipLib
from lib.scrolllib import ScrollLib
from lib.speciallib import SpecialLib
from lib.etclib import EtcLib
from lib.joblib import JobLib
from lib.upgradelib import UpgradeLib
from lib.bosslib import BossLib
from lib.farminglib import FarmingLib

from marketinfo import MarketInfo
from character import Character
from potential import rank_label
from inventory import Inventory, SUCCESS, FAIL, BOOM, INVALID, NOITEM

class ActivityWidget(Tkinter.Frame):

    def __init__(self, parent):
        Tkinter.Frame.__init__(self, parent)
        self.parent = parent
        self.curChosenType = '- Choose Type -'
        self.listboxList = []
        self.curSelectIdx = -1
        self.initUI()

    def reset(self):
        self.curChosenType = '- Choose Type -'
        self.chosenType.set('- Choose Type -')
        self.listboxList = []
        self.curSelectIdx = -1
        size = self.actionListbox.size()
        if size:
            self.actionListbox.delete(0, size-1)
        self.descriptionContent.config(state=Tkinter.NORMAL)
        self.descriptionContent.delete('1.0', Tkinter.END)
        self.descriptionContent.config(state=Tkinter.DISABLED)
        message = 'Action Point: '
        self.APContent.set(message)

    def updateType(self, event):          
        chosenType = self.chosenType.get()
        if self.curChosenType == chosenType:
            return
        self.curChosenType = chosenType
        self.descriptionContent.config(state=Tkinter.NORMAL)
        self.descriptionContent.delete('1.0', Tkinter.END)
        self.descriptionContent.config(state=Tkinter.DISABLED)
        size = self.actionListbox.size()
        if size:
            self.actionListbox.delete(0, size-1)
        self.listboxList = []
        self.curSelectIdx = -1

        if self.curChosenType == 'Upgrade':
            for key, lib in UpgradeLib.m_lib.items():
                print key, lib
                for entry in lib.keys():
                    self.listboxList.append((key, entry))
                    self.actionListbox.insert(Tkinter.END, key + ': ' + entry)
        elif self.curChosenType == 'Boss':
            for boss in BossLib.m_lib.keys():
                self.listboxList.append(boss)
                self.actionListbox.insert(Tkinter.END, boss)
        elif self.curChosenType == 'Farming':
            for entry in FarmingLib.m_lib.keys():
                self.listboxList.append(entry)
                self.actionListbox.insert(Tkinter.END, entry)
            

    def actionListboxSelect(self, event):
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
        if self.curChosenType == '':
            self.descriptionContent.config(state=Tkinter.NORMAL)
            self.descriptionContent.delete('1.0', Tkinter.END)
            self.descriptionContent.insert('insert', '')
            self.descriptionContent.config(state=Tkinter.DISABLED)
            
    def startButtonClicked(self):
        pass
    
    def initUI(self):

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        
        self.Frameleft = Tkinter.Frame(self, padx=5, pady=10)
        self.Frameleft.rowconfigure(2, weight=1)
        self.Frameright = Tkinter.Frame(self, padx=5, pady=5)
        self.Frameright.rowconfigure(1, weight=1)
        self.Frameright.rowconfigure(5, weight=1)

        
        self.types = ['Upgrade', 'Boss', 'Farming']
        self.chosenType = Tkinter.StringVar()
        self.chosenType.set('- Choose Type -')

        self.typeOptionMenu = Tkinter.OptionMenu(self.Frameleft, self.chosenType, *self.types, command=self.updateType)

        self.actionListbox = Tkinter.Listbox(self.Frameleft, selectmode='single')
        self.actionListbox.bind('<<ListboxSelect>>', self.actionListboxSelect)

        self.APContent = Tkinter.StringVar()
        self.APLabel = Tkinter.Label(self.Frameleft, textvariable=self.APContent, justify=Tkinter.LEFT)
        message = 'Action Point: '
        self.APContent.set(message)

        self.descriptionLabel = Tkinter.Label(self.Frameright, text='Description')
        self.descriptionContent = ScrolledText.ScrolledText(self.Frameright,
                                                           wrap=Tkinter.WORD,
                                                           width=39, height=10)
        self.descriptionContent.config(font=('San Francisco', 13, 'normal'))
        self.descriptionContent.insert('insert', '')
        self.descriptionContent.config(state=Tkinter.DISABLED)
        
        self.startButton = Tkinter.Button(self.Frameright, text='Start', command=self.startButtonClicked)

        self.typeOptionMenu.grid(row=0, column=0, columnspan=3, padx=5, sticky=Tkinter.W)
        self.actionListbox.grid(row=1, column=0, rowspan=7, columnspan=3, padx=5, pady=5, sticky=Tkinter.W+Tkinter.E+Tkinter.S+Tkinter.N)
        self.APLabel.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky=Tkinter.W)

        self.descriptionLabel.grid(row=0, column=0, padx=5, pady=5, sticky=Tkinter.W)
        self.descriptionContent.grid(row=1, column=0,
                                    rowspan=7, columnspan=3,
                                    padx=5, pady=5,
                                    sticky=Tkinter.N+Tkinter.S+Tkinter.W)
        self.startButton.grid(row=8, column=2, padx=5, pady=5, sticky=Tkinter.E)
        
        self.Frameleft.pack(fill=Tkinter.BOTH, expand=1, side=Tkinter.LEFT)
        self.Frameright.pack(fill=Tkinter.BOTH, expand=1, side=Tkinter.RIGHT)

