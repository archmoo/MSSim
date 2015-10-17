from speciallib import SpecialLib
from scrolllib import ScrollLib
from equipslot import EquipSlot
from equip import Equip
from potential import Potential
import random

SUCCESS = 0
FAIL = 1
BOOM = 2
INVALID = -1
NOITEM = -2

class Inventory:
    m_equip = []
    m_equipped = {}
    m_use = {}
    m_etc = {}

    def __init__(self):
        self.m_equip = []
        self.m_use = {}
        self.m_equipped = {}
        
        for key in SpecialLib.m_lib.keys():
            self.m_use[key] = 0
        for key in ScrollLib.m_lib.keys():
            if ScrollLib.m_lib[key]['type'] != 'trace':
                self.m_use[key] = 0
        for key in EquipSlot.m_lib.keys():
            self.m_equipped[key] = -1
        self.m_etc = {
            'Meso': 100000,
            'NX': 0,
            'Trace': 0,
            'Elite Coin': 0,
            'Boss Coin': 0,
            'Event Coin': 0,
            'Red Cube Coin': 0,
            'Black Cube Coin': 0,
            'Queen Coin': 0,
            'Pierre Coin': 0,
            'VonBon Coin': 0,
            'Vellum Coin': 0,
            'Magnus Coin': 0,
            'Magnus Coin 2': 0,
            'Cygnus Coin': 0,
            'Shadow Coin': 0,
            'Denaro': 0,
            'Gollux Coin': 0,
            'Gollux Coin 1': 0,
            'Gollux Coin 2': 0,
            'Gollux Coin 3': 0,
            'Gollux Coin 4': 0,
            }

    def createItem(self, item, num):
        if item in self.m_use.keys():
            self.m_use[item] += num

    def useItem(self, item, equipIdx):
        
        if equipIdx >= len(self.m_equip):
            return INVALID
        if item not in self.m_use.keys():
            return INVALID
        if self.m_use[item] <= 0:
            return NOITEM
        
        if item in ScrollLib.m_lib.keys():
            stat = ScrollLib.m_lib[item]
        elif item in SpecialLib.m_lib.keys():
            stat = SpecialLib.m_lib[item]

        if stat['type'] == 'Special':
            #TODO: condition check
            if (stat['effect'] == 'Clean Slate' and self.m_equip[equipIdx].m_total_slot == self.m_equip[equipIdx].m_remain_slot + self.m_equip[equipIdx].m_success) or\
               (stat['effect'] == 'Potential' and self.m_equip[equipIdx].m_pot.m_rank > 0) or\
               (stat['effect'] == 'Epic Potential' and self.m_equip[equipIdx].m_pot.m_rank > 1) or\
               (stat['effect'] == 'Unique Potential' and self.m_equip[equipIdx].m_pot.m_rank > 2) or\
               (stat['effect'] == 'Hammer' and self.m_equip[equipIdx].m_remain_hammer == 0) or\
               (stat['effect'] == 'Potential Stamp' and len(self.m_equip[equipIdx].m_pot.m_lines) == 3) or\
               (stat['effect'] == 'Protect' and self.m_equip[equipIdx].m_protect) or\
               (stat['effect'] == 'Guardian' and self.m_equip[equipIdx].m_guardian) or\
               (stat['effect'] == 'Safety' and self.m_equip[equipIdx].m_safety):
                   return INVALID
                
            if random.random() < stat['success rate']: # success
                self.m_equip[equipIdx].applySpecial(stat['effect'])
                self.m_use[item] -= 1
                return SUCCESS
            elif random.random() < stat['boom rate']: # boom
                if not self.m_equip[equipIdx].m_guardian:
                    self.m_use[item] -= 1
                if self.m_equip[equipIdx].m_protect:
                    self.m_protect = False
                    self.m_guardian = False
                    return FAIL
                else:
                    self.deleteEquip(equipIdx)
                    return BOOM
                
            else: # fail
                if not self.m_equip[equipIdx].m_guardian:
                    self.m_use[item] -= 1
                self.m_protect = False
                self.m_guardian = False
                return FAIL
                    
        elif stat['type'] == 'Hammer':
            if self.m_equip[equipIdx].m_remain_hammer == 0:
                return INVALID
            if random.random() < stat['success rate']: # success
                self.m_equip[equipIdx].applySpecial(stat['effect'])
                self.m_use[item] -= 1
                return SUCCESS
            elif random.random() < stat['boom rate']: # boom
                self.m_use[item] -= 1
                if self.m_equip[equipIdx].m_protect:
                    if not self.m_equip[equipIdx].m_safety:
                        self.m_equip[equipIdx].m_remain_slot -= 1
                    self.m_equip[equipIdx].applySpecial(stat['effect'])
                    return FAIL
                else:
                    self.deleteEquip(equipIdx)
                    return BOOM
            else:
                self.m_use[item] -= 1
                if not self.m_equip[equipIdx].m_safety:
                        self.m_equip[equipIdx].m_remain_slot -= 1
                self.m_equip[equipIdx].applySpecial(stat['effect'])
                return FAIL

        elif stat['type'] == 'Scroll':
            if self.m_equip[equipIdx].m_remain_slot <= 0:
                return INVALID
            if random.random() < stat['success rate']: # success
                self.m_equip[equipIdx].applyScroll(stat['effect'])
                self.m_use[item] -= 1
                self.m_equip[equipIdx].m_protect = False
                self.m_equip[equipIdx].m_guardian = False
                self.m_equip[equipIdx].m_safety = False
                return SUCCESS
            elif random.random() < stat['boom rate']: # boom
                if not self.m_equip[equipIdx].m_guardian:
                    self.m_use[item] -= 1
                if self.m_equip[equipIdx].m_protect:
                    if not self.m_equip[equipIdx].m_safety:
                        self.m_equip[equipIdx].m_remain_slot -= 1
                    self.m_equip[equipIdx].m_protect = False
                    self.m_equip[equipIdx].m_guardian = False
                    self.m_equip[equipIdx].m_safety = False
                    return FAIL
                else:
                    self.deleteEquip(equipIdx)
                    return BOOM
            else: # fail
                if not self.m_equip[equipIdx].m_guardian:
                    self.m_use[item] -= 1
                if not self.m_equip[equipIdx].m_safety:
                    self.m_equip[equipIdx].m_remain_slot -= 1
                self.m_equip[equipIdx].m_protect = False
                self.m_equip[equipIdx].m_guardian = False
                self.m_equip[equipIdx].m_safety = False
                return FAIL
            
                
        elif stat['type'] == 'Trace':
            if self.m_equip[equipIdx].m_remain_slot <= 0:
                return INVALID
            #TODO: spell trace etc logic
            if random.random() < stat['success rate']:
                self.m_equip[equipIdx].applyScroll(stat['effect'])
                self.m_equip[equipIdx].m_safety = False
                return SUCCESS
            else:
                if not self.m_equip[equipIdx].m_safety:
                    self.m_equip[equipIdx].m_remain_slot -= 1
                self.m_equip[equipIdx].m_safety = False
                return FAIL

        elif stat['type'] == 'Cube':
            rank = self.m_equip[equipIdx].m_pot.m_rank
            if rank < 1:
                return INVALID
            if not stat['availability'][rank - 1]:
                return INVALID
            self.m_use[item] -= 1
            newPot = Potential(self.m_equip[equipIdx])
            if random.random() < stat['tierup rate'][rank - 1]:
                newPot.m_rank += 1
            if stat['effect'] == 'Pick Potential Lines':
                newPot.m_lines = [()] * len(self.m_equip[equipIdx].m_pot.m_lines) * 2
            newPot.roll()
            return (stat['effect'], newPot)
##            if stat['effect'] == 'Reset Potential':
##                self.m_equip[equipIdx].m_pot = newPot
##            elif stat['effect'] == 'Choose Potential':
##                print '---Compare---'
##                print '1. (Original)', self.m_equip[equipIdx].m_pot.m_rank
##                for line in self.m_equip[equipIdx].m_pot.m_lines:
##                    print line
##                print
##                print '2. (New)', newPot.m_rank
##                for line in newPot.m_lines:
##                    print line
##                print 
##                choice = int(raw_input('Choose 1 or 2:'))
##                if choice == 2:
##                    self.m_equip[equipIdx].m_pot = newPot
##            elif stat['effect'] == 'Pick Potential Lines':
##                numLines = len(self.m_equip[equipIdx].m_pot.m_lines)
##                print '---Pick '+str(numLines)+'---'
##                print 'Rank:', newPot.m_rank
##                for i in range(len(newPot.m_lines)):
##                    print str(i)+'.', newPot.m_lines[i]
##                print
##                choices = []
##                for i in range(numLines):
##                    choice = int(raw_input('Choice '+str(i)+':'))
##                    while(choice in choices or choice >= len(newPot.m_lines)):
##                        choice = int(raw_input('Choice '+str(i)+':'))
##                    choices.append(choice)
##                pot = []
##                for i in range(numLines):
##                    pot.append(newPot.m_lines[choices[i]])
##                self.m_equip[equipIdx].m_pot.m_lines = pot

    def setEquipPot(self, pot, equipIdx):
        self.m_equip[equipIdx].m_pot = pot
        
    def createEquip(self, equipName):
        equip = Equip(equipName)
        equip.setClean()
        self.m_equip.append(equip)

    def deleteEquip(self, idx):
        self.m_equip.pop(idx)
        for key in self.m_equipped.keys():
            if self.m_equipped[key] > idx:
                self.m_equipped[key] = self.m_equipped[key] - 1

    def onEquip(self, slot, idx):
        equipType = self.m_equip[idx].m_type
        if equipType not in EquipSlot.m_lib[slot]:
            return INVALID
        self.m_equipped[slot] = idx
        return SUCCESS

    def offEquip(self, slot):
        self.m_equipped[slot] = -1

    def getEquipIdxListbySlot(self, slot):
        res = []
        for i in range(len(self.m_equip)):
            if self.m_equip[i].m_type in EquipSlot.m_lib[slot]:
                res.append(i)
        return res
            

if __name__ == '__main__':
    a = Inventory()
##    a.createItem('Prime Scroll for Armor', 100)
##    a.createItem('Protect Scroll', 100)
##    a.createItem('Guardian Scroll', 100)
##    a.createItem('Safety Scroll', 100)
##    a.createItem('10% Clean Slate Scroll', 1000)
##    a.createItem('100% Golden Hammer', 2)
    a.createEquip('Royal Dunwitch Hat')
##    a.useItem('100% Golden Hammer', 0)
##    a.useItem('100% Golden Hammer', 0)
##    while a.m_equip[0].m_remain_slot and a.m_use['10% Clean Slate Scroll']:
##        for i in range(100):
##            if not a.m_equip[0].m_remain_slot:
##                break
##            a.useItem('Protect Scroll', 0)
##            a.useItem('Guardian Scroll', 0)
##            a.useItem('Safety Scroll', 0)
##            res = a.useItem('Prime Scroll for Armor', 0)
##            if res == BOOM:
##                print 'BOOM'
##                break
##            if res == INVALID:
##                print 'stop', a.m_equip[0].m_remain_slot, a.m_equip[0].m_total_slot, a.m_equip[0].m_success
##                print res, a.m_equip[0]['int'], a.m_use['Prime Scroll for Armor']
##                break
##            print res, a.m_equip[0]['int'], a.m_use['Prime Scroll for Armor']
##        
##        for i in range(1000):
##            res = a.useItem('10% Clean Slate Scroll', 0)
##            if res == SUCCESS:
##                print 'css pass', a.m_equip[0].m_remain_slot, a.m_equip[0].m_total_slot, a.m_equip[0].m_success
##            elif res == INVALID:
##                break
##    print a.m_use['10% Clean Slate Scroll'], a.m_equip[0].m_remain_slot, a.m_equip[0].m_total_slot, a.m_equip[0].m_success, a.m_equip[0]['int']
##    a.createItem('Advanced Potential Scroll', 1)
##    a.createItem('Perfect Potential Stamp', 1)
##    a.createItem('Meister Cube', 1000)
##    while a.m_equip[0].m_pot.m_rank < 1:
##        a.useItem('Protect Scroll', 0)
##        a.useItem('Guardian Scroll', 0)
##        res = a.useItem('Advanced Potential Scroll', 0)
##        if res == SUCCESS:
##            a.useItem('Perfect Potential Stamp', 0)
##            print 'pot pass'
##            print a.m_equip[0].m_pot.m_rank, a.m_equip[0].m_pot.m_lines
##    for i in range(300):
##        if a.m_equip[0].m_pot.m_rank < 5:
##            a.useItem('Meister Cube', 0)
##            print a.m_equip[0].m_pot.showPot()
##            raw_input('Continue ?')
    a.onEquip('Hat', 0)
    print a.m_equipped['Face']
    print ScrollLib.showScrollStat('STR for Weapon 15%')
