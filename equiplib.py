class EquipLib:
    'Equipment library'

    m_libHat = {
        'Royal Dunwitch Hat': {
            'name': 'Royal Dunwitch Hat',
            'type': 'Hat',
            'class': 'Magician',
            'level': 150,
            'str': 0,
            'dex': 0,
            'int': 40,
            'luk': 40,
            'hp': 360,
            'mp': 360,
            'watt': 0,
            'matt': 2,
            'wdef': 180,
            'mdef': 240,
            'accuracy': 240,
            'avoid': 120,
            'boss': 0,
            'pdr': 0.1,
            'slot': 11,
            'setId': 1,
            },
        'Royal Assassin Hood': {
            'name': 'Royal Assassin Hood',
            'type': 'Hat',
            'class': 'Thief',
            'level': 150,
            'str': 0,
            'dex': 40,
            'int': 0,
            'luk': 40,
            'hp': 360,
            'mp': 360,
            'watt': 2,
            'matt': 0,
            'wdef': 300,
            'mdef': 0,
            'accuracy': 240,
            'avoid': 120,
            'boss': 0,
            'pdr': 0.1,
            'slot': 11,
            'setId': 2,
            },
        }
    
    m_libTop = {
        'Royal Dunwitch Top': {
            'name': 'Royal Dunwitch Top',
            'type': 'Hat',
            'level': 150,
            'str': 0,
            'dex': 0,
            'int': 40,
            'luk': 40,
            'hp': 360,
            'mp': 360,
            'watt': 0,
            'matt': 2,
            'wdef': 180,
            'mdef': 240,
            'accuracy': 240,
            'avoid': 120,
            'boss': 0,
            'pdr': 0.1,
            'slot': 11,
            'setId': 1,
            },
        'Royal Dunwitch Top 2': {
            'name': 'Royal Dunwitch Top 2',
            'type': 'Hat',
            'level': 150,
            'str': 0,
            'dex': 0,
            'int': 40,
            'luk': 40,
            'hp': 360,
            'mp': 360,
            'watt': 0,
            'matt': 2,
            'wdef': 180,
            'mdef': 240,
            'accuracy': 240,
            'avoid': 120,
            'boss': 0,
            'pdr': 0.1,
            'slot': 11,
            'setId': 1,
            },
        }

    m_lib = {
        'Hat': m_libHat,
        'Top': m_libTop,
    }

    def __getitem__(self, typeName):
        return self.m_lib[typeName]
    
    def getType(self, typeName):
        return self.__getitem__(typeName)

    def getEquip(self, equipName):
        for equipType in self.m_lib.values():
            if equipName in equipType.keys():
                return equipType[equipName]
        return None
                
