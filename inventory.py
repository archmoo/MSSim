from lib.speciallib import SpecialLib
from lib.scrolllib import ScrollLib
from lib.equipslotlib import EquipSlotLib
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
            self.m_use[key] = 0
        for key in EquipSlotLib.m_lib.keys():
            self.m_equipped[key] = -1
        self.m_etc = {
            'Meso': 1000000000,
            'NX': 10000,
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
            'Magnus Coin B': 0,
            'Cygnus Coin': 0,
            'Shadow Coin': 0,
            'Denaro': 0,
            'Gollux Coin': 0,
            'Gollux Penny': 0,
            'Gollux Coin B': 0,
            'Gollux Coin A': 0,
            'Gollux Coin S': 0,
            'Gollux Coin SS': 0,
            }

    def initBasicEquips(self, jobName, className):
        hat = {
            'Warrior': 'Pensalir Battle Helm',
            'Bowman': 'Pensalir Sentinel Cap',
            'Magician': 'Pensalir Mage Sallet',
            'Thief': 'Pensalir Chaser Hat',
            'Pirate': 'Pensalir Skipper Hat',
            }
        overall = {
            'Warrior': 'Pensalir Battle Mail',
            'Bowman': 'Pensalir Sentinel Suit',
            'Magician': 'Pensalir Mage Robe',
            'Thief': 'Pensalir Chaser Armor',
            'Pirate': 'Pensalir Skipper Coat',
            }
        shoe = {
            'Warrior': 'Pensalir Battle Boots',
            'Bowman': 'Pensalir Sentinel Boots',
            'Magician': 'Pensalir Mage Boots',
            'Thief': 'Pensalir Chaser Boots',
            'Pirate': 'Pensalir Skipper Boots',
            }
        cape = {
            'Warrior': 'Pensalir Battle Cape',
            'Bowman': 'Pensalir Sentinel Cape',
            'Magician': 'Pensalir Mage Cape',
            'Thief': 'Pensalir Chaser Cape',
            'Pirate': 'Pensalir Skipper Cape',
            }
        glove = {
            'Warrior': 'Pensalir Battle Gloves',
            'Bowman': 'Pensalir Sentinel Gloves',
            'Magician': 'Pensalir Mage Gloves',
            'Thief': 'Pensalir Chaser Gloves',
            'Pirate': 'Pensalir Skipper Gloves',
            }
        weapon = {
            'Bow Master': 'Utgard Bow',
            'Wind Archer': 'Utgard Bow',
            'Phantom': 'Utgard Cane',
            'Buccaneer': 'Utgard Claw',
            'Shade': 'Utgard Claw',
            'Thunder Breaker': 'Utgard Claw',
            'Marksman': 'Utgard Crossbow',
            'Wild Hunter': 'Utgard Crossbow',
            'Blade Master': 'Utgard Dagger',
            'Shadower': 'Utgard Dagger',
            'Demon Avenger': 'Utgard Desperado',
            'Angelic Buster': 'Utgard Dragon Soul',
            'Mercedes': 'Utgard Dual Bowguns',
            'Xenon': {
                'Thief': 'Utgard Energy Chain (Thief)',
                'Pirate': 'Utgard Energy Chain (Pirate)',
                },
            'Kanna': 'Utgard Fan',
            'Night Lord': 'Utgard Guards',
            'Night Walker': 'Utgard Guards',
            'Aran': 'Utgard Hellslayer',
            'Hayato': 'Utgard Katana',
            'Mechanic': 'Utgard Pistol',
            'Corsair': 'Utgard Pistol',
            'Mihile': 'Utgard Saber',
            'Paladin': 'Utgard Saber',
            'Luminous': 'Utgard Shining Rod',
            'Beast Tamer': 'Utgard Shining Stick',
            'Cannoneer': 'Utgard Siege Gun',
            'Dark Knight': 'Utgard Spear',
            'Battle Mage': 'Utgard Staff',
            'Blaze Wizard': 'Utgard Staff',
            'Evan': 'Utgard Staff',
            'Arch Mage (Fire, Poison)': 'Utgard Staff',
            'Arch Mage (Ice, Lightning)': 'Utgard Staff',
            'Bishop': 'Utgard Staff',
            'Dawn Warrior': 'Utgard Two-handed Sword',
            'Kaiser': 'Utgard Two-handed Sword',
            'Hero': 'Utgard Two-handed Sword',
            'Demon Slayer': 'Utgard Hair',
            }
        self.createEquip(hat[className])
        self.createEquip(overall[className])
        self.createEquip(cape[className])
        self.createEquip(glove[className])
        self.createEquip(shoe[className])
        if jobName != 'Xenon':
            self.createEquip(weapon[jobName])
        else:
            self.createEquip(weapon[jobName][className])

        self.m_equipped['Hat'] = 0
        self.m_equipped['Top'] = 1
        self.m_equipped['Cape'] = 2
        self.m_equipped['Glove'] = 3
        self.m_equipped['Shoe'] = 4
        self.m_equipped['Weapon'] = 5
        
    
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
            #TODO: non-potable
            if (stat['effect'] == 'Clean Slate' and self.m_equip[equipIdx].m_total_slot == self.m_equip[equipIdx].m_remain_slot + self.m_equip[equipIdx].m_success) or\
               (stat['effect'] == 'Potential' and self.m_equip[equipIdx].m_pot.m_rank > 0) or\
               (stat['effect'] == 'Epic Potential' and self.m_equip[equipIdx].m_pot.m_rank > 1) or\
               (stat['effect'] == 'Unique Potential' and self.m_equip[equipIdx].m_pot.m_rank > 2) or\
               (stat['effect'] == 'Hammer' and self.m_equip[equipIdx].m_remain_hammer == 0) or\
               (stat['effect'] == 'Potential Stamp' and (self.m_equip[equipIdx].m_pot.m_rank == 0 or len(self.m_equip[equipIdx].m_pot.m_lines) == 3)) or\
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
            if 'restriction' in stat.keys():
                if self.m_equip[equipIdx].m_type not in stat['restriction']:
                    return INVALID
                if self.m_equip[equipIdx].m_type == 'Secondary':
                    if self.m_equip[equipIdx].m_category not in stat['secondary']:
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
            if 'restriction' in stat.keys():
                if self.m_equip[equipIdx].m_type not in stat['restriction']:
                    return INVALID
                if self.m_equip[equipIdx].m_type == 'Secondary':
                    if self.m_equip[equipIdx].m_category not in stat['secondary']:
                        return INVALID
            
            if random.random() < stat['success rate']:
                if not self.m_equip[equipIdx].m_guardian:
                    self.m_use[item] -= 1
                self.m_equip[equipIdx].applyScroll(stat['effect'])
                self.m_equip[equipIdx].m_safety = False
                self.m_equip[equipIdx].m_guardian = False
                return SUCCESS
            else:
                if not self.m_equip[equipIdx].m_guardian:
                    self.m_use[item] -= 1
                if not self.m_equip[equipIdx].m_safety:
                    self.m_equip[equipIdx].m_remain_slot -= 1
                self.m_equip[equipIdx].m_safety = False
                self.m_equip[equipIdx].m_guardian = False
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
        if equipType not in EquipSlotLib.m_lib[slot]:
            return INVALID
        self.m_equipped[slot] = idx
        return SUCCESS

    def offEquip(self, slot):
        self.m_equipped[slot] = -1

    def getEquipIdxListbySlot(self, slot):
        res = []
        for i in range(len(self.m_equip)):
            if self.m_equip[i].m_type in EquipSlotLib.m_lib[slot]:
                res.append(i)
        return res
            

if __name__ == '__main__':
    a = Inventory()
##    a.createItem('Prime Scroll for Armor', 100)
    a.createItem('Protect Scroll', 100)
    a.createItem('Guardian Scroll', 100)
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
    a.createItem('Advanced Potential Scroll', 1)
    a.createItem('Perfect Potential Stamp', 1)
    a.createItem('Meister Cube', 1000)
    while a.m_equip[0].m_pot.m_rank < 1:
        a.useItem('Protect Scroll', 0)
        a.useItem('Guardian Scroll', 0)
        res = a.useItem('Advanced Potential Scroll', 0)
        if res == SUCCESS:
            a.useItem('Perfect Potential Stamp', 0)
            print 'pot pass'
            print a.m_equip[0].m_pot.m_rank, a.m_equip[0].m_pot.m_lines
    for i in range(300):
        if a.m_equip[0].m_pot.m_rank < 5:
            a.useItem('Meister Cube', 0)
            print a.m_equip[0].m_pot.m_lines
            raw_input('Continue ?')

