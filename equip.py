from equiplib import EquipLib
from potential import Potential
from potentiallib import PotentialLib
from scrolllib import ScrollLib
import random

class Equip:
    'Equipment class'

    #static
    equipLib = EquipLib()
    potLib = PotentialLib()
    scrollLib = ScrollLib()
    
    m_name = ''
    m_type = ''
    m_level = 0
    m_class = ''
    
    m_str = 0
    m_dex = 0
    m_int = 0
    m_luk = 0
    m_hp = 0
    m_mp = 0
    m_watt = 0
    m_matt = 0
    m_wdef = 0
    m_mdef = 0
    m_accuracy = 0
    m_avoid = 0
    
    m_boss = 0
    m_pdr = 0

    m_total_slot = 0
    m_remain_slot = 0
    m_remain_hammer = 0
    m_success = 0

    m_stars = 0

    m_pot = None
    m_bpot = None
    m_neb = None

    m_protect = False
    m_guardian = False
    m_safety = False

    m_setId = 0

    def __init__(self, name):
        self.m_name = name
        self.m_type = 'generic'
        self.m_class = 'all'

    def __getitem__(self, string):
        return {
            'str': self.m_str,
            'dex': self.m_dex,
            'int': self.m_int,
            'luk': self.m_luk,
            'hp': self.m_hp,
            'mp': self.m_mp,
            'watt': self.m_watt,
            'matt': self.m_matt,
            'wdef': self.m_wdef,
            'mdef': self.m_mdef,
            'accuracy': self.m_accuracy,
            'avoid': self.m_avoid,
            }[string]

    def __setitem__(self, string, value):
        if string == 'str':
            self.m_str = value
        elif string == 'dex':
            self.m_dex = value
        elif string == 'int':
            self.m_int = value
        elif string == 'luk':
            self.m_luk = value
        elif string == 'hp':
            self.m_hp = value
        elif string == 'mp':
            self.m_mp = value
        elif string == 'watt':
            self.m_watt = value
        elif string == 'matt':
            self.m_matt = value
        elif string == 'wdef':
            self.m_wdef = value
        elif string == 'mdef':
            self.m_mdef = value
        elif string == 'accuracy':
            self.m_accuracy = value
        elif string == 'avoid':
            self.m_avoid = value

    def showEquip(self):
        output = ''
        output += self.m_name + '\n'
        output += 'Category: ' + self.m_type + '\n'
        output += 'REQ LVL: ' + str(self.m_level) + '\n'
        output += 'Class: ' + self.m_class + '\n'
        if self.m_str:
            output += 'STR: +' + str(self.m_str) + '\n'
        if self.m_dex:
            output += 'DEX: +' + str(self.m_dex) + '\n'
        if self.m_int:
            output += 'INT: +' + str(self.m_int) + '\n'
        if self.m_luk:
            output += 'LUK: +' + str(self.m_luk) + '\n'
        if self.m_hp:
            output += 'MaxHP: +' + str(self.m_hp) + '\n'
        if self.m_mp:
            output += 'MaxMP: +' + str(self.m_mp) + '\n'
        if self.m_watt:
            output += 'WEAPON ATT: ' + str(self.m_watt) + '\n'
        if self.m_matt:
            output += 'MAGIC ATT: ' + str(self.m_matt) + '\n'
        if self.m_wdef:
            output += 'WEAPON DEF: ' + str(self.m_wdef) + '\n'
        if self.m_mdef:
            output += 'MAGIC DEF: ' + str(self.m_mdef) + '\n'
        if self.m_accuracy:
            output += 'ACCURACY: +' + str(self.m_accuracy) + '\n'
        if self.m_avoid:
            output += 'AVOIDABILITY: +' + str(self.m_avoid) + '\n'
        if self.m_pot:
            output += self.m_pot.showPot()
        return output

        
    def setClean(self):
        equip = Equip.equipLib.getEquip(self.m_name)
        if equip is None:
            return False
        self.m_type = equip['type']
        self.m_level = equip['level']
        self.m_class = equip['class']
        self.m_str = equip['str']
        self.m_dex = equip['dex']
        self.m_int = equip['int']
        self.m_luk = equip['luk']
        self.m_hp = equip['hp']
        self.m_mp = equip['mp']
        self.m_watt = equip['watt']
        self.m_matt = equip['matt']
        self.m_wdef = equip['wdef']
        self.m_mdef = equip['mdef']
        self.m_accuracy = equip['accuracy']
        self.m_avoid = equip['avoid']
        self.m_boss = equip['boss']
        self.m_pdr = equip['pdr']
        self.m_total_slot = equip['slot']
        self.m_remain_slot = equip['slot']
        self.m_remain_hammer = 2
        self.m_success = 0
        self.m_stars = 0
        self.m_setId = equip['setId']
        self.m_pot = Potential(self)
        self.m_bpot = None
        self.m_neb = None
        self.m_protect = False
        self.m_guardian = False
        self.m_safety = False
        return True

    def applySpecial(self, effect):
        if effect == 'Innocent':
            equip = Equip.equipLib.getEquip(self.m_name)
            if equip is None:
                return False
            self.m_str = equip['str']
            self.m_dex = equip['dex']
            self.m_int = equip['int']
            self.m_luk = equip['luk']
            self.m_hp = equip['hp']
            self.m_mp = equip['mp']
            self.m_watt = equip['watt']
            self.m_matt = equip['matt']
            self.m_wdef = equip['wdef']
            self.m_mdef = equip['mdef']
            self.m_accuracy = equip['accuracy']
            self.m_avoid = equip['avoid']
            self.m_total_slot = equip['slot']
            self.m_remain_slot = equip['slot']
            self.m_remain_hammer = 2
            self.m_success = 0
            self.m_stars = 0
            self.m_protect = False
            self.m_guardian = False
        elif effect == 'Potential':
            if random.random() < 0.8:
                numLines = 2
            else:
                numLines = 3
            r = random.random()
            if r < 0.99:
                rank = 1
            elif r < 0.9999:
                rank = 2
            else:
                rank = 3
            self.m_pot.m_rank = rank
            self.m_pot.roll(numLines)
            self.m_protect = False
            self.m_guardian = False
        elif effect == 'Epic Potential':
            if random.random() < 0.8:
                numLines = 2
            else:
                numLines = 3
            self.m_pot.m_rank = 2
            self.m_pot.roll(numLines)
            self.m_protect = False
            self.m_guardian = False
        elif effect == 'Unique Potential':
            if random.random() < 0.8:
                numLines = 2
            else:
                numLines = 3
            self.m_pot.m_rank = 3
            self.m_pot.roll(numLines)
            self.m_protect = False
            self.m_guardian = False
        elif effect == 'Clean Slate':
            if self.m_success + self.m_remain_slot < self.m_total_slot:
                self.m_remain_slot += 1
            self.m_protect = False
            self.m_guardian = False
        elif effect == 'Hammer':
            if self.m_remain_hammer > 0:
                self.m_remain_hammer -= 1
                self.m_total_slot += 1
                self.m_remain_slot += 1
                self.m_protect = False
                self.m_safety = False
        elif effect == 'Potential Stamp':
            if len(self.m_pot.m_lines) == 2:
                self.m_pot.expand()
        elif effect == 'Protect':
            self.m_protect = True
        elif effect == 'Guardian':
            self.m_guardian = True
        elif effect == 'Safety':
            self.m_safety = True
        return True

    def applyScroll(self, effect):
        scrollType, stat = Equip.scrollLib.getScrollStat(effect, self)
        if scrollType == 'decisive':
            for key, value in stat.items():
                self[key] = self[key] + value
        elif scrollType == 'chaos':
            mutable = ['str', 'dex', 'int', 'luk', 'hp', 'mp', 'watt', 'matt',
                       'wdef', 'mdef', 'accuracy', 'avoid']
            for option in mutable:
                if self[option] != 0:
                    r = random.random()
                    for i in range(min(stat.keys()), max(stat.keys())):
                        if r > stat[i]:
                            continue
                        else:
                            val = i
                            if option == 'hp' or option == 'mp':
                                val *= 10
                            self[option] = max(0, self[option] + val)
                            break
        self.m_remain_slot -= 1
        self.m_success += 1                        
            

if __name__ == '__main__':
    equipLib = EquipLib()
    potLib = PotentialLib()
    scrollLib = ScrollLib()
    a = Equip("Royal Dunwitch Hat")
    a.setClean()
    print a.m_name, a.m_type, a.m_pdr, a.m_pot.m_level
    print a['matt']
    
    
    
        
        
        
        

    
    
