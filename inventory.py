from speciallib import SpecialLib
from scrolllib import ScrollLib
from equip import Equip
from potential import Potential
import random

SUCCESS = 0
FAIL = 1
BOOM = 2
INVALID = -1

class Inventory:
    m_equip = []
    m_use = {}

    def __init__(self):
        for key in SpecialLib.m_lib.keys():
            self.m_use[key] = 0
        for key in ScrollLib.m_lib.keys():
            if ScrollLib.m_lib[key]['type'] != 'trace':
                self.m_use[key] = 0

    def createItem(self, item, num):
        if item in self.m_use.keys():
            self.m_use[item] += num

    def useItem(self, item, equipIdx):
        
        if equipIdx >= len(self.m_equip):
            return INVALID
        if item not in self.m_use.keys():
            return INVALID
        if self.m_use[item] == 0:
            return INVALID
        
        if item in ScrollLib.m_lib.keys():
            stat = ScrollLib.m_lib[item]
        elif item in SpecialLib.m_lib.keys():
            stat = SpecialLib.m_lib[item]

        if stat['type'] == 'special':
            #TODO: condition check
            if (stat['effect'] == 'Clean Slate' and self.m_equip[equipIdx].m_total_slot == self.m_equip[equipIdx].m_remain_slot + self.m_equip[equipIdx].m_success) or\
               (stat['effect'] == 'Potential' and self.m_equip[equipIdx].m_pot.m_rank > 0) or\
               (stat['effect'] == 'Epic Potential' and self.m_equip[equipIdx].m_pot.m_rank > 0) or\
               (stat['effect'] == 'Unique Potential' and self.m_equip[equipIdx].m_pot.m_rank > 0) or\
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
                    
        elif stat['type'] == 'hammer':
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

        elif stat['type'] == 'scroll':
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
            
                
        elif stat['type'] == 'trace':
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

        elif stat['type'] == 'cube':
            rank = self.m_equip[equipIdx].m_pot.m_rank
            if rank < 1:
                return INVALID
            if not stat['availability'][rank - 1]:
                return INVALID
            newPot = Potential(self.m_equip[equipIdx])
            if random.random() < stat['tierup rate'][rank - 1]:
                newPot.m_rank += 1
            if stat['effect'] == 'Pick Potential Lines':
                newPot.m_lines = [()] * len(self.m_equip[equipIdx].m_pot.m_lines) * 2
            newPot.roll()
            if stat['effect'] == 'Reset Potential':
                self.m_equip[equipIdx].m_pot = newPot
            elif stat['effect'] == 'Choose Potential':
                print '---Compare---'
                print '1. (Original)', self.m_equip[equipIdx].m_pot.m_rank
                for line in self.m_equip[equipIdx].m_pot.m_lines:
                    print line
                print
                print '2. (New)', newPot.m_rank
                for line in newPot.m_lines:
                    print line
                print 
                choice = int(raw_input('Choose 1 or 2:'))
                if choice == 2:
                    self.m_equip[equipIdx].m_pot = newPot
            elif stat['effect'] == 'Pick Potential Lines':
                numLines = len(self.m_equip[equipIdx].m_pot.m_lines)
                print '---Pick '+str(numLines)+'---'
                print 'Rank:', newPot.m_rank
                for i in range(len(newPot.m_lines)):
                    print str(i)+'.', newPot.m_lines[i]
                print
                choices = []
                for i in range(numLines):
                    choice = int(raw_input('Choice '+str(i)+':'))
                    while(choice in choices or choice >= len(newPot.m_lines)):
                        choice = int(raw_input('Choice '+str(i)+':'))
                    choices.append(choice)
                pot = []
                for i in range(numLines):
                    pot.append(newPot.m_lines[choices[i]])
                self.m_equip[equipIdx].m_pot.m_lines = pot
                    
        
    def createEquip(self, equipName):
        equip = Equip(equipName)
        equip.setClean()
        self.m_equip.append(equip)

    def deleteEquip(self, idx):
        self.m_equip.pop(idx)

if __name__ == '__main__':
    a = Inventory()
    a.createItem('Prime Scroll for Armor', 100)
    a.createItem('Protect Scroll', 100)
    a.createItem('Guardian Scroll', 100)
    a.createItem('Safety Scroll', 100)
    a.createItem('10% Clean Slate Scroll', 1000)
    a.createItem('100% Golden Hammer', 2)
    a.createEquip('Royal Dunwitch Hat')
    a.useItem('100% Golden Hammer', 0)
    a.useItem('100% Golden Hammer', 0)
    while a.m_equip[0].m_remain_slot and a.m_use['10% Clean Slate Scroll']:
        for i in range(100):
            if not a.m_equip[0].m_remain_slot:
                break
            a.useItem('Protect Scroll', 0)
            a.useItem('Guardian Scroll', 0)
            a.useItem('Safety Scroll', 0)
            res = a.useItem('Prime Scroll for Armor', 0)
            if res == BOOM:
                print 'BOOM'
                break
            if res == INVALID:
                print 'stop', a.m_equip[0].m_remain_slot, a.m_equip[0].m_total_slot, a.m_equip[0].m_success
                print res, a.m_equip[0]['int'], a.m_use['Prime Scroll for Armor']
                break
            print res, a.m_equip[0]['int'], a.m_use['Prime Scroll for Armor']
        
        for i in range(1000):
            res = a.useItem('10% Clean Slate Scroll', 0)
            if res == SUCCESS:
                print 'css pass', a.m_equip[0].m_remain_slot, a.m_equip[0].m_total_slot, a.m_equip[0].m_success
            elif res == INVALID:
                break
    print a.m_use['10% Clean Slate Scroll'], a.m_equip[0].m_remain_slot, a.m_equip[0].m_total_slot, a.m_equip[0].m_success, a.m_equip[0]['int']
##    a.createItem('60% Unique Potential Scroll', 1)
##    a.createItem('Perfect Potential Stamp', 1)
##    a.createItem('Black Cube', 100)
##    a.createItem('Violet Cube', 100)
##    while a.m_equip[0].m_pot.m_rank < 3:
##        a.useItem('Guardian Scroll', 0)
##        res = a.useItem('60% Unique Potential Scroll', 0)
##        if res == SUCCESS:
##            a.useItem('Perfect Potential Stamp', 0)
##            print 'uniq pot pass'
##            print a.m_equip[0].m_pot.m_rank, a.m_equip[0].m_pot.m_lines
##
##    for i in range(30):
##        if a.m_equip[0].m_pot.m_rank < 4:
##            a.useItem('Black Cube', 0)
##            print a.m_equip[0].m_pot.m_rank
##            for line in a.m_equip[0].m_pot.m_lines:
##                print line[0][2:], str(line[1]*100)+'%'
##
##    for i in range(30):
##        a.useItem('Violet Cube', 0)
##        print a.m_equip[0].m_pot.m_rank
##        for line in a.m_equip[0].m_pot.m_lines:
##            print line[0][2:], str(line[1]*100)+'%'
        
