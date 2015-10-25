import pickle, random, os.path, math
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
        message = 'Action Point: ' + str(int(round(self.parent.m_charInfo.actionPoint)))
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
##                print key, lib
                for entry in lib.keys():
                    self.listboxList.append(key + ': ' + entry)
                    self.actionListbox.insert(Tkinter.END, key + ': ' + entry)
        elif self.curChosenType == 'Boss':
            for boss in BossLib.m_bosses:
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
                description += 'Next level progress: ' + str(float(characterStats[1]*100)) + '%\n\n'
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
                    description += '+ ' + info['effect'][i] + ' (Up to ' + (str(maxstat) if maxstat > 1 else (str(float(maxstat*100)) + '%')) + ')\n'
                description += '\n'
                characterStats = self.parent.m_charInfo.oneTimeAcquire[minorType][minorEntry]
                level = characterStats[0]
                description += 'Current Effect:\n'
                for i in range(len(info['effect'])):
                    stat = info['table'][i][int(level / 5)]
                    if stat == 0:
                        stat = '0'
                    elif stat < 1:
                        stat = str(float(stat*100)) + '%'
                    else:
                        stat = str(stat)
                    description += '+ ' + info['effect'][i] + ': ' + stat + '\n'
                description += '\n'
                description += 'Current level: ' + str(level) + '\n'
                description += 'EXP for next level: ' + str(UpgradeLib.m_traitsEXP[level+1]-UpgradeLib.m_traitsEXP[level]) + '\n'
                description += 'Next level progress: ' + '%.1f' % float(characterStats[1]*100) + '%\n'
                description += 'Upgrade cost: 1 Action Point per 5 EXP\n'
        elif self.curChosenType == 'Boss':
            entry = self.listboxList[self.curSelectIdx]
            info = BossLib.m_lib[entry]
            description += entry + '\n\n'
            description += info['description'] + '\n\n'
            description += 'DPS requirement: ' + str(info['dps']) + '\n'
            description += 'Defense: ' + str(int(round(info['defense']*100))) + '%\n'
            description += 'Resistance: ' + str(int(round(info['resistance']*100))) + '%\n'
            description += 'Reward: ' + ', '.join(sorted(info['reward'].keys())) + '\n'
            counter = self.parent.m_charInfo.bossCounter[info['counter']]
            description += 'Attempt: ' + str(counter[0]) + '/' + (str(BossLib.m_counter[info['counter']][1]) if BossLib.m_counter[info['counter']][1] != -1 else 'Unlimited') + ' time(s) per ' + BossLib.m_counter[info['counter']][0] + '\n'
            description += 'Defeat: ' + str(counter[1]) + '/' + str(BossLib.m_counter[info['counter']][3]) + ' time(s) per ' + BossLib.m_counter[info['counter']][2] + '\n'
            description += 'Attempt cost: ' + str(info['AP cost']) + ' Action Points\n'
        elif self.curChosenType == 'Farming':
            entry = self.listboxList[self.curSelectIdx]
            info = FarmingLib.m_lib[entry]
            description += entry + '\n\n'
            description += 'Reward: ' + ', '.join(sorted(info['reward'].keys())) + '\n'
            description += 'Limit: ' + (str(self.parent.m_charInfo.farmCounter[entry]) + '/' + str(info['limit']) + ' time(s) per day' if info['limit'] >= 0 else 'Unlimited') + '\n'
            description += 'Cost: ' + str(info['AP cost']) + ' Action Points' + '\n'
                
        self.descriptionContent.config(state=Tkinter.NORMAL)
        self.descriptionContent.delete('1.0', Tkinter.END)
        self.descriptionContent.insert('insert', description)
        self.descriptionContent.config(state=Tkinter.DISABLED)
            
    def chooseButtonClicked(self):
        def upgradeLinkSkill():
            def updateDescription():
                description = ''
                description += 'Link skill can give your character extra boost, which is acquired by leveling up a new character to a certain level. Most link skills have 2 or 3 levels, acquired at Lv. 70, 120 and 210.\n\n'
                description += 'Link Skill: ' + minorEntry + '\n\n'
                info = UpgradeLib.m_lib['Link Skill'][minorEntry]
                for i in info.keys():
                    description += 'Level ' + str(i) + ':\nEffect: ' + PotentialLib.showPotList(info[i]['effect'], ', ') + 'Upgrade cost: ' + str(info[i]['AP cost']) + ' Action Points\n'
                description += '\n'
                characterStats = self.parent.m_charInfo.oneTimeAcquire['Link Skill'][minorEntry]
                description += 'Current level: ' + str(characterStats[0]) + '\n'
                description += 'Next level progress: ' + str(float(characterStats[1]*100)) + '%\n\n'
                self.descriptionContent.config(state=Tkinter.NORMAL)
                self.descriptionContent.delete('1.0', Tkinter.END)
                self.descriptionContent.insert('insert', description)
                self.descriptionContent.config(state=Tkinter.DISABLED)
                message = 'Action Point: ' + str(self.parent.m_charInfo.actionPoint)
                self.APContent.set(message)
                return
            
            value = quantityEntry.get()
            try: 
                quantity = int(value)
                assert quantity > 0
            except Exception:
                tkMessageBox.showwarning('Invalid', 'Invalid input!')
                return
            if quantity > self.parent.m_charInfo.actionPoint:
                tkMessageBox.showwarning('Invalid', 'You don\'t have enough Action Point.')
                return
            progress = curProgress
            level = curLevel
            q = quantity
            while q > 0.5 and level < max(info.keys()):
                levelCost = int(round((1 - progress) * info[level + 1]['AP cost']))
                if levelCost > q:
                    progress += float(q) / info[level + 1]['AP cost']
                    message = 'Are You Sure?\nYou will reach Level ' + str(level) + ', with ' + str(float(progress*100)) + '% progress towards next level.'
                    res = tkMessageBox.askquestion('Upgrade', message, type='yesno')
                    if res == 'yes':
                        self.parent.m_charInfo.actionPoint -= quantity
                        self.parent.m_charInfo.oneTimeAcquire['Link Skill'][minorEntry] = (level, progress)
                        updateDescription()
                        self.parent.tabEquip.reset()
                        toplevel.destroy()
                    return
                else:
                    q -= int(round(levelCost))
                    level += 1
                    progress = 0
                    if q == 0:
                        message = 'Are You Sure?\nYou will reach Level ' + str(level) + ', with ' + str(float(progress*100)) + '% progress towards next level.'
                        res = tkMessageBox.askquestion('Upgrade', message, type='yesno')
                        if res == 'yes':
                            self.parent.m_charInfo.actionPoint -= quantity
                            self.parent.m_charInfo.oneTimeAcquire['Link Skill'][minorEntry] = (level, progress)
                            updateDescription()
                            self.parent.tabEquip.reset()
                            toplevel.destroy()
                        return
            if q > 0.5:
                message = 'Are You Sure?\nYou will reach Level ' + str(level) + ', with ' + str(float(progress*100)) + '% progress towards next level.\n'
                message += 'You only need ' + str(quantity - q) + ' Action Points to level up to max level. ' + str(q) + ' Action Points will be saved.\n'
                res = tkMessageBox.askquestion('Upgrade', message, type='yesno')
                if res == 'yes':
                    self.parent.m_charInfo.actionPoint -= (quantity - q)
                    self.parent.m_charInfo.oneTimeAcquire['Link Skill'][minorEntry] = (level, progress)
                    updateDescription()
                    self.parent.tabEquip.reset()
                    toplevel.destroy()
                return
                
            
        def upgradeTraits():
            def updateDescription():
                description = ''
                info = UpgradeLib.m_lib['Traits'][minorEntry]
                description += 'Traits give your character extra benefit or stats boost.\n\n'
                description += entry + '\n\n'
                description += 'Effect:\n'
                for i in range(len(info['effect'])):
                    maxstat = max(info['table'][i])
                    print maxstat
                    description += '+ ' + info['effect'][i] + ' (Up to ' + (str(maxstat) if maxstat > 1 else (str(float(maxstat*100)) + '%')) + ')\n'
                description += '\n'
                characterStats = self.parent.m_charInfo.oneTimeAcquire['Traits'][minorEntry]
                level = characterStats[0]
                description += 'Current Effect:\n'
                for i in range(len(info['effect'])):
                    stat = info['table'][i][int(level / 5)]
                    if stat == 0:
                        stat = '0'
                    elif stat < 1:
                        stat = str(float(stat*100)) + '%'
                    else:
                        stat = str(stat)
                    description += '+ ' + info['effect'][i] + ': ' + stat + '\n'
                description += '\n'
                description += 'Current level: ' + str(level) + '\n'
                description += 'EXP for next level: ' + str(UpgradeLib.m_traitsEXP[level+1]-UpgradeLib.m_traitsEXP[level]) + '\n'
                description += 'Next level progress: ' + '%.1f' % float(characterStats[1]*100) + '%\n'
                description += 'Upgrade cost: 1 Action Point per 5 EXP\n'
                self.descriptionContent.config(state=Tkinter.NORMAL)
                self.descriptionContent.delete('1.0', Tkinter.END)
                self.descriptionContent.insert('insert', description)
                self.descriptionContent.config(state=Tkinter.DISABLED)
                message = 'Action Point: ' + str(self.parent.m_charInfo.actionPoint)
                self.APContent.set(message)
                return
            
            value = quantityEntry.get()
            try: 
                quantity = int(value)
                assert quantity > 0
            except Exception:
                tkMessageBox.showwarning('Invalid', 'Invalid input!')
                return
            if quantity > self.parent.m_charInfo.actionPoint:
                tkMessageBox.showwarning('Invalid', 'You don\'t have enough Action Point.')
                return

            table = UpgradeLib.m_traitsEXP
            curEXP = self.parent.m_charInfo.oneTimeAcquire['Traits'][minorEntry][2]
 
            if math.ceil(float(table[100] - curEXP)/5) < quantity:
                q = int(round(math.ceil(float(table[100] - curEXP)/5)))
                message = 'Are You Sure?\nYou will reach Level 100 with 0.0% progress towards next level.\n'
                message += 'You only need ' + str(q) + ' Action Points to level up to max level. ' + str(quantity - q) + ' Action Points will be saved.\n'
                res = tkMessageBox.askquestion('Upgrade', message, type='yesno')
                if res == 'yes':
                    self.parent.m_charInfo.actionPoint -= q
                    self.parent.m_charInfo.oneTimeAcquire['Traits'][minorEntry] = (100, 0, table[100])
                    updateDescription()
                    self.parent.tabEquip.reset()
                    toplevel.destroy()
                return
            else:
                curEXP += quantity * 5
                curLevel = -1
                for i in range(1, 101):
                    if table[i] > curEXP:
                        curLevel = i - 1
                        break
                if curLevel == -1:
                    curLevel = 100
                    curProgress = 0
                else:
                    curProgress = float(curEXP - table[curLevel]) / (table[curLevel + 1] - table[curLevel])
                message = 'Are You Sure?\nYou will reach Level ' + str(curLevel) + ' with ' + '%.1f' % float(curProgress*100) + '% progress towards next level.\n'
                res = tkMessageBox.askquestion('Upgrade', message, type='yesno')
                if res == 'yes':
                    self.parent.m_charInfo.actionPoint -= quantity
                    self.parent.m_charInfo.oneTimeAcquire['Traits'][minorEntry] = (curLevel, curProgress, curEXP)
                    updateDescription()
                    self.parent.tabEquip.reset()
                    toplevel.destroy()
                return
            
        if self.curChosenType == '- Choose Type -':
            tkMessageBox.showwarning('Invalid', 'Please choose a type.')
            return
        if self.curSelectIdx == -1:
            tkMessageBox.showwarning('Invalid', 'Please select an action.')
            return
        entry = self.listboxList[self.curSelectIdx]
        if self.curChosenType == 'Upgrade':
            minorType, minorEntry = entry.split(': ')
            if minorType == 'Link Skill':
                curLevel = self.parent.m_charInfo.oneTimeAcquire['Link Skill'][minorEntry][0]
                curProgress = self.parent.m_charInfo.oneTimeAcquire['Link Skill'][minorEntry][1]
                info = UpgradeLib.m_linklib[minorEntry]
                if curLevel == max(info.keys()):
                    tkMessageBox.showwarning('Invalid', 'You have reached max level!')
                    return
                toplevel = Tkinter.Toplevel(self)
                toplevel.title('Upgrade Link Skill')
                toplevel.geometry('350x120+300+300')
                toplevel.grab_set()
                quantityLabel = Tkinter.Label(toplevel, text='Spend Action Point:')
                quantityEntry = Tkinter.Entry(toplevel)
                startButton = Tkinter.Button(toplevel, text='Start', command=upgradeLinkSkill)
                cancelButton = Tkinter.Button(toplevel, text='Cancel', command=toplevel.destroy)
                quantityLabel.grid(row=0, column=0, padx=5, pady=5)
                quantityEntry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
                startButton.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
                cancelButton.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
            elif minorType == 'Traits':
                curLevel = self.parent.m_charInfo.oneTimeAcquire['Traits'][minorEntry][0]
                curProgress = self.parent.m_charInfo.oneTimeAcquire['Traits'][minorEntry][1]
                
                if curLevel == 100:
                    tkMessageBox.showwarning('Invalid', 'You have reached max level!')
                    return
                toplevel = Tkinter.Toplevel(self)
                toplevel.title('Upgrade Traits')
                toplevel.geometry('350x120+300+300')
                toplevel.grab_set()
                quantityLabel = Tkinter.Label(toplevel, text='Spend Action Point:')
                quantityEntry = Tkinter.Entry(toplevel)
                startButton = Tkinter.Button(toplevel, text='Start', command=upgradeTraits)
                cancelButton = Tkinter.Button(toplevel, text='Cancel', command=toplevel.destroy)
                quantityLabel.grid(row=0, column=0, padx=5, pady=5)
                quantityEntry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
                startButton.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
                cancelButton.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
            elif minorType == 'Crusader Codex':
                info = UpgradeLib.m_lib['Crusader Codex'][minorEntry]
                if self.parent.m_charInfo.oneTimeAcquire['Crusader Codex']['chosen'] == minorEntry:
                    tkMessageBox.showwarning('Invalid', 'You have chosen this set!')
                    return
                if self.parent.m_charInfo.oneTimeAcquire['Crusader Codex'][minorEntry][0] == 1:
                    message = 'Are You Sure?\n\n'
                    message += 'Choosing Crusader Codex: ' + minorEntry + ' Set'
                    res = tkMessageBox.askquestion('Choose Crusader Codex', message, type='yesno')
                    if res == 'yes':
                        self.parent.m_charInfo.oneTimeAcquire['Crusader Codex']['chosen'] = minorEntry
                        description = ''
                        description += 'The Crusader Codex is a collection of Monster Book Cards, which gives your character extra boost when a certain set is chosen.\n\n'
                        description += 'Crusader Codex: ' + minorEntry + '\n\n'
                        description += 'Effect: ' + PotentialLib.showPotList(info['effect'], ', ') + 'Upgrade cost: ' + str(info['AP cost']) + ' Action Points\n\n'
                        description += 'Status: ' + ('Acquired' if self.parent.m_charInfo.oneTimeAcquire['Crusader Codex'][minorEntry][0] == 1 else 'Not acquired') + '\n'
                        description += 'Current Codex set: ' + self.parent.m_charInfo.oneTimeAcquire['Crusader Codex']['chosen'] + '\n'
                        self.descriptionContent.config(state=Tkinter.NORMAL)
                        self.descriptionContent.delete('1.0', Tkinter.END)
                        self.descriptionContent.insert('insert', description)
                        self.descriptionContent.config(state=Tkinter.DISABLED)
                    return
                else:
                    if self.parent.m_charInfo.actionPoint < info['AP cost']:
                        tkMessageBox.showwarning('Invalid', 'You don\'t have enough Action Points.')
                        return
                    else:
                        message = 'Are You Sure?\n\n'
                        message += 'Acquiring Crusader Codex: ' + minorEntry + ' Set'
                        res = tkMessageBox.askquestion('Acquiring Crusader Codex', message, type='yesno')
                        if res == 'yes':
                            self.parent.m_charInfo.oneTimeAcquire['Crusader Codex'][minorEntry] = (1, 0)
                            self.parent.m_charInfo.actionPoint -= info['AP cost']
                            description = ''
                            description += 'The Crusader Codex is a collection of Monster Book Cards, which gives your character extra boost when a certain set is chosen.\n\n'
                            description += 'Crusader Codex: ' + minorEntry + '\n\n'
                            description += 'Effect: ' + PotentialLib.showPotList(info['effect'], ', ') + 'Upgrade cost: ' + str(info['AP cost']) + ' Action Points\n\n'
                            description += 'Status: ' + ('Acquired' if self.parent.m_charInfo.oneTimeAcquire['Crusader Codex'][minorEntry][0] == 1 else 'Not acquired') + '\n'
                            description += 'Current Codex set: ' + self.parent.m_charInfo.oneTimeAcquire['Crusader Codex']['chosen'] + '\n'
                            self.descriptionContent.config(state=Tkinter.NORMAL)
                            self.descriptionContent.delete('1.0', Tkinter.END)
                            self.descriptionContent.insert('insert', description)
                            self.descriptionContent.config(state=Tkinter.DISABLED)
                            message = 'Action Point: ' + str(self.parent.m_charInfo.actionPoint)
                            self.APContent.set(message)
                            message = 'You have acquired Crusader Codex: ' + minorEntry + ' Set.\n'
                            message += 'Click "Choose" Button again to enable this set.'
                            tkMessageBox.showinfo('Success', message)
                        return
                    
        elif self.curChosenType == 'Boss':
            info = BossLib.m_lib[entry]
            if self.parent.m_charInfo.actionPoint < info['AP cost']:
                tkMessageBox.showwarning('Invalid', 'You don\'t have enough Action Points.')
                return
            curAttempt = self.parent.m_charInfo.bossCounter[info['counter']][0]
            curDefeat = self.parent.m_charInfo.bossCounter[info['counter']][1]
            if BossLib.m_counter[info['counter']][1] != -1 and curAttempt >= BossLib.m_counter[info['counter']][1]:
                tkMessageBox.showwarning('Invalid', 'You have reached attempt limit.')
                return
            if curDefeat >= BossLib.m_counter[info['counter']][3]:
                tkMessageBox.showwarning('Invalid', 'You have reached defeat limit.')
                return
            stat = self.parent.m_charInfo.m_stat
            multiplier = 1
            multiplier *= (1 + stat['Critical Rate'] * (stat['Minimum Critical Damage'] + stat['Maximum Critical Damage']) / 2)
            multiplier *= (1 + stat['Boss Damage'] + stat['Total Damage']) * (1 + stat['Final Damage'])
            multiplier *= max(0, (1-info['defense']*(1-stat['Ignore Enemy Defense'])))
            multiplier *= max(0, (1-info['resistance']*(1-stat['Ignore Enemy Resistance'])))
            lowdps = int(round(stat['DPS'][0] * multiplier))
            highdps = int(round(stat['DPS'][1] * multiplier))
            message = 'Are You Sure?\n\n'
            message += 'DPS requirement for defeat: ' + str(info['dps']) + '\n'
            message += 'Your DPS on ' + entry + ': ' + str(lowdps) + ' ~ ' + str(highdps) + '\n'
            res = tkMessageBox.askquestion('Attempt Boss', message, type='yesno')
            if res == 'yes':
                self.parent.m_charInfo.actionPoint -= info['AP cost']
                self.parent.m_charInfo.bossCounter[info['counter']][0] += 1
                dps = random.random() * (highdps - lowdps) + lowdps
                if dps >= info['dps']:
                    self.parent.m_charInfo.bossCounter[info['counter']][1] += 1
                    message = 'You defeated ' + entry + '!\n\n'
                    message += 'Rewards:\n'
                    for key in sorted(info['reward'].keys()):
                        if key == 'Meso':
                            mu = info['reward'][key][0] * info['reward'][key][1]
                            sigma = math.sqrt(info['reward'][key][0] * info['reward'][key][1] * (1 - info['reward'][key][1]))
                            amount = int(round(random.normalvariate(mu, sigma)))
                            if amount > 0:
                                self.parent.m_inventory.m_etc[key] += amount
                                message += key + ': ' + str(amount) + '\n'
                        else:
                            n = info['reward'][key][0]
                            p = info['reward'][key][1]
                            amount = 0
                            for i in range(n):
                                if random.random() < p:
                                    amount += 1
                            if amount > 0:
                                self.parent.m_inventory.m_etc[key] += amount
                                message += key + ': ' + str(amount) + '\n'
                    self.parent.tabPurchase.reset()
                    tkMessageBox.showinfo('Success', message)
                else:
                    tkMessageBox.showinfo('Fail', 'You didn\'t defeat ' + entry + '.')
                description = entry + '\n\n'
                description += info['description'] + '\n\n'
                description += 'DPS requirement: ' + str(info['dps']) + '\n'
                description += 'Defense: ' + str(int(round(info['defense']*100))) + '%\n'
                description += 'Resistance: ' + str(int(round(info['resistance']*100))) + '%\n'
                description += 'Reward: ' + ', '.join(sorted(info['reward'].keys())) + '\n'
                counter = self.parent.m_charInfo.bossCounter[info['counter']]
                description += 'Attempt: ' + str(counter[0]) + '/' + (str(BossLib.m_counter[info['counter']][1]) if BossLib.m_counter[info['counter']][1] != -1 else 'Unlimited') + ' time(s) per ' + BossLib.m_counter[info['counter']][0] + '\n'
                description += 'Defeat: ' + str(counter[1]) + '/' + str(BossLib.m_counter[info['counter']][3]) + ' time(s) per ' + BossLib.m_counter[info['counter']][2] + '\n'
                description += 'Attempt cost: ' + str(info['AP cost']) + ' Action Points\n'
                self.descriptionContent.config(state=Tkinter.NORMAL)
                self.descriptionContent.delete('1.0', Tkinter.END)
                self.descriptionContent.insert('insert', description)
                self.descriptionContent.config(state=Tkinter.DISABLED)
                message = 'Action Point: ' + str(self.parent.m_charInfo.actionPoint)
                self.APContent.set(message)
                
            return
        elif self.curChosenType == 'Farming':
            if FarmingLib.m_lib[entry]['limit'] != -1:
                if self.parent.m_charInfo.farmCounter[entry] >= FarmingLib.m_lib[entry]['limit']:
                    tkMessageBox.showwarning('Invalid', 'You have reached daily limit.')
                    return
            if self.parent.m_charInfo.actionPoint < FarmingLib.m_lib[entry]['AP cost']:
                tkMessageBox.showwarning('Invalid', 'You don\'t have enough Action Points.')
                return
            message = 'Are You Sure?\n'
            res = tkMessageBox.askquestion('Farm', message, type='yesno')
            info = FarmingLib.m_lib[entry]
            if res == 'yes':
                self.parent.m_charInfo.actionPoint -= info['AP cost']
                self.parent.m_charInfo.farmCounter[entry] += 1
                message = 'You completed Farming: ' + entry + '\n\n'
                message += 'Rewards:\n'
                for key in sorted(info['reward'].keys()):
                    if key == 'Meso':
                        mu = info['reward'][key][0] * info['reward'][key][1]
                        sigma = math.sqrt(info['reward'][key][0] * info['reward'][key][1] * (1 - info['reward'][key][1]))
                        amount = int(round(random.normalvariate(mu, sigma)))
                        if amount > 0:
                            self.parent.m_inventory.m_etc[key] += amount
                            message += key + ': ' + str(amount) + '\n'
                    else:
                        n = info['reward'][key][0]
                        p = info['reward'][key][1]
                        amount = 0
                        for i in range(n):
                            if random.random() < p:
                                amount += 1
                        if amount > 0:
                            self.parent.m_inventory.m_etc[key] += amount
                            message += key + ': ' + str(amount) + '\n'
                self.parent.tabPurchase.reset()
                tkMessageBox.showinfo('Success', message)
                description = ''
                description += entry + '\n\n'
                description += 'Reward: ' + ', '.join(sorted(info['reward'].keys())) + '\n'
                description += 'Limit: ' + (str(self.parent.m_charInfo.farmCounter[entry]) + '/' + str(info['limit']) + ' time(s) per day' if info['limit'] >= 0 else 'Unlimited') + '\n'
                description += 'Cost: ' + str(info['AP cost']) + ' Action Points' + '\n'
                self.descriptionContent.config(state=Tkinter.NORMAL)
                self.descriptionContent.delete('1.0', Tkinter.END)
                self.descriptionContent.insert('insert', description)
                self.descriptionContent.config(state=Tkinter.DISABLED)
                message = 'Action Point: ' + str(self.parent.m_charInfo.actionPoint)
                self.APContent.set(message)               
            return

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
        message = 'Action Point: ' + str(int(round(self.parent.m_charInfo.actionPoint)))
        self.APContent.set(message)

        self.descriptionLabel = Tkinter.Label(self.Frameright, text='Description')
        self.descriptionContent = ScrolledText.ScrolledText(self.Frameright,
                                                           wrap=Tkinter.WORD,
                                                           width=39, height=10)
        self.descriptionContent.config(font=('San Francisco', 13, 'normal'))
        self.descriptionContent.insert('insert', '')
        self.descriptionContent.config(state=Tkinter.DISABLED)
        
        self.chooseButton = Tkinter.Button(self.Frameright, text='Choose', command=self.chooseButtonClicked)

        self.typeOptionMenu.grid(row=0, column=0, columnspan=3, padx=5, sticky=Tkinter.W)
        self.actionListbox.grid(row=1, column=0, rowspan=7, columnspan=3, padx=5, pady=5, sticky=Tkinter.W+Tkinter.E+Tkinter.S+Tkinter.N)
        self.APLabel.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky=Tkinter.W)

        self.descriptionLabel.grid(row=0, column=0, padx=5, pady=5, sticky=Tkinter.W)
        self.descriptionContent.grid(row=1, column=0,
                                    rowspan=7, columnspan=3,
                                    padx=5, pady=5,
                                    sticky=Tkinter.N+Tkinter.S+Tkinter.W)
        self.chooseButton.grid(row=8, column=2, padx=5, pady=5, sticky=Tkinter.E)
        
        self.Frameleft.pack(fill=Tkinter.BOTH, expand=1, side=Tkinter.LEFT)
        self.Frameright.pack(fill=Tkinter.BOTH, expand=1, side=Tkinter.RIGHT)

