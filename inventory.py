from speciallib import SpecialLib
from scrolllib import ScrollLib

class Inventory:
    m_equip = []
    m_use = {}

    def __init__(self):
        for key in SpecialLib.m_lib.keys():
            self.m_use[key] = 0
        for key in ScrollLib.m_lib.keys():
            self.m_use[key] = 0

    def useItem(self, item, equip):
        if item in ScrollLib.m_lib.keys():
            stat = ScrollLib.m_lib[item]
        elif item in SpecialLib.m_lib.keys():
            stat = SpecialLib.m_lib.keys()

        if stat['type'] == 'special':
            pass
        elif stat['type'] == 'hammer':
            pass
        elif stat['type'] == 'scroll':
            pass
        elif stat['type'] == 'trace':
            pass
        
    def createEquip(self, equip):
        pass

    def deleteEquip(self, idx):
        pass

if __name__ == '__main__':
    a = Inventory()
    print a.m_use
    a.useItem('Prime Scroll for Armor', 0)
        
