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
from lib.potentiallib import PotentialLib

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
                    self.listboxList.append(key + ': ' + entry)
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
        description = ''
        if self.curChosenType == 'Upgrade':
            entry = self.listboxList[self.curSelectIdx]
            minorType, minorEntry = entry.split(': ')
            info = UpgradeLib.m_lib[minorType][minorEntry]
            if minorType == 'Link Skill':
                description += 'Link skill can give your character extra boost, which is acquired by leveling up a new character to a certain level. Most link skills have 2 or 3 levels, acquired at Lv. 70, 120 and 210.\n\n'
                description += entry + '\n\n'
                for i in info.keys():
                    description += 'Level ' + str(i) + ':\nEffect: ' + PotentialLib.showPotList(info[i]['effect'], ', ') + 'Upgrade cost: ' + str(info[i]['AP cost']) + ' Action Points\n'
                description += '\n'
                characterStats = self.parent.m_charInfo.oneTimeAcquire[minorType][minorEntry]
                description += 'Current level: ' + str(characterStats[0]) + '\n'
                description += 'Next level progress: ' + str(int(round(characterStats[1]*100))) + '%\n\n'
            elif minorType == 'Crusader Codex':
                description += 'The Crusader Codex is a collection of Monster Book Cards, which gives your character extra boost when a certain set is chosen.\n\n'
                description += entry + '\n\n'
                description += 'Effect: ' + PotentialLib.showPotList(info['effect'], ', ') + 'Upgrade cost: ' + str(info['AP cost']) + ' Action Points\n\n'
                description += 'Status: ' + ('Acquired' if self.parent.m_charInfo.oneTimeAcquire['Crusader Codex'][minorEntry][0] == 1 else 'Not acquired') + '\n'
                description += 'Current Codex set: ' + self.parent.m_charInfo.oneTimeAcquire['Crusader Codex']['chosen'] + '\n'
            elif minorType == 'Traits':
                description += 'Traits give your character extra benefit or stats boost.\n\n'
                description += entry + '\n\n'
                description += 'Effect:\n'
                for i in range(len(info['effect'])):
                    maxstat = max(info['table'][i])
                    description += '+ ' + info['effect'][i] + ' (Up to ' + (str(maxstat) if maxstat > 1 else (str(int(round(maxstat*100))) + '%')) + ')\n'
                description += '\n'
                characterStats = self.parent.m_charInfo.oneTimeAcquire[minorType][minorEntry]
                level = characterStats[0]
                description += 'Current level: ' + str(level) + '\n'
                description += 'Current Effect:\n'
                for i in range(len(info['effect'])):
                    stat = info['table'][i][int(level / 5)]
                    if stat == 0:
                        stat = '0'
                    elif stat < 1:
                        stat = str(int(round(stat*100))) + '%'
                    else:
                        stat = str(stat)
                    description += '+ ' + info['effect'][i] + ': ' + stat + '\n'
                description += '\n'
                description += 'EXP for next level: ' + str(UpgradeLib.m_traitsEXP[level+1]) + '\n'
                description += 'Next level progress: ' + str(int(round(characterStats[1]*100))) + '%\n'
                description += 'Upgrade cost: 1 Action Point per 10 EXP\n'
        elif self.curChosenType == 'Boss':
            entry = self.listboxList[self.curSelectIdx]
            info = BossLib.m_lib[entry]
            description += entry + '\n\n'
            description += info['description'] + '\n\n'
            description += 'DPS requirement: ' + str(info['dps']) + '\n'
            description += 'Reward: ' + ', '.join(info['reward'].keys()) + '\n'
            description += 'Attempt: ' + str(BossLib.m_counter[info['counter']][1]) + ' time(s) per ' + BossLib.m_counter[info['counter']][0] + '\n'
            description += 'Defeat: ' + str(BossLib.m_counter[info['counter']][3]) + ' time(s) per ' + BossLib.m_counter[info['counter']][2] + '\n'
            description += 'Attempt cost: ' + str(info['AP cost']) + ' Action Points\n'
        elif self.curChosenType == 'Farming':
            entry = self.listboxList[self.curSelectIdx]
            info = FarmingLib.m_lib[entry]
            description += entry + '\n\n'
            description += 'Reward: ' + ', '.join(info['reward'].keys()) + '\n'
            description += 'Limit: ' + (str(info['limit']) + ' time(s) per day' if info['limit'] >= 0 else 'Unlimited') + '\n'
            description += 'Cost: ' + str(info['AP cost']) + ' Action Points' + '\n'
                
                
                
        self.descriptionContent.config(state=Tkinter.NORMAL)
        self.descriptionContent.delete('1.0', Tkinter.END)
        self.descriptionContent.insert('insert', description)
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

