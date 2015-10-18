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
            # market info
            'cost': ['Meso','Queen Coin'],
            'value': [1, 5],
            'stock': [-1, -1],
            'max': [-1, -1],
            'supply': [-1, -1],
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
            # market info
            'cost': ['Meso','Queen Coin'],
            'value': [1, 5],
            'stock': [5, -1],
            'max': [10, -1],
            'supply': [5, -1],
            },
        }
    
    m_libTop = {
        'Eagle Eye Dunwitch Robe': {
            'name': 'Eagle Eye Dunwitch Robe',
            'type': 'Top',
            'class': 'Magician',
            'level': 150,
            'str': 0,
            'dex': 0,
            'int': 30,
            'luk': 30,
            'hp': 0,
            'mp': 0,
            'watt': 0,
            'matt': 2,
            'wdef': 120,
            'mdef': 150,
            'accuracy': 30,
            'avoid': 30,
            'boss': 0,
            'pdr': 0.05,
            'slot': 7,
            'setId': 1,
            # market info
            'cost': ['Meso','VonBon Coin'],
            'value': [1, 5],
            'stock': [5, -1],
            'max': [10, -1],
            'supply': [5, -1],
            },
        }
    m_libBottom = {
        'Trixter Dunwitch Pants' : {
            'name': 'Trixter Dunwitch Pants',
            'type': 'Bottom',
            'class': 'Magician',
            'level': 150,
            'str': 0,
            'dex': 0,
            'int': 30,
            'luk': 30,
            'hp': 0,
            'mp': 0,
            'watt': 0,
            'matt': 2,
            'wdef': 120,
            'mdef': 150,
            'accuracy': 30,
            'avoid': 30,
            'boss': 0,
            'pdr': 0.05,
            'slot': 7,
            'setId': 1,
            # market info
            'cost': ['Meso','Pierre Coin'],
            'value': [1, 5],
            'stock': [5, -1],
            'max': [10, -1],
            'supply': [5, -1],
            },
        }
    m_libShoe = {
        'Tyrant Hermes Boots' : {
            'name': 'Tyrant Hermes Boots',
            'type': 'Shoe',
            'class': 'Magician',
            'level': 150,
            'str': 50,
            'dex': 50,
            'int': 50,
            'luk': 50,
            'hp': 0,
            'mp': 0,
            'watt': 30,
            'matt': 30,
            'wdef': 130,
            'mdef': 130,
            'accuracy': 0,
            'avoid': 0,
            'boss': 0,
            'pdr': 0,
            'slot': 2,
            'setId': 0,
            # market info
            'cost': ['Meso','Magnus Coin'],
            'value': [1, 70],
            'stock': [5, -1],
            'max': [10, -1],
            'supply': [5, -1],
            },
        }
    m_libCape = {
        'Tyrant Hermes Cloak' : {
            'name': 'Tyrant Hermes Cloak',
            'type': 'Cape',
            'class': 'Magician',
            'level': 150,
            'str': 50,
            'dex': 50,
            'int': 50,
            'luk': 50,
            'hp': 0,
            'mp': 0,
            'watt': 30,
            'matt': 30,
            'wdef': 150,
            'mdef': 150,
            'accuracy': 0,
            'avoid': 0,
            'boss': 0,
            'pdr': 0,
            'slot': 2,
            'setId': 0,
            # market info
            'cost': ['Meso','Magnus Coin B'],
            'value': [1, 1],
            'stock': [5, -1],
            'max': [10, -1],
            'supply': [5, -1],
            },
        }
    m_libBelt = {
        'Tyrant Hermes Belt' : {
            'name': 'Tyrant Hermes Belt',
            'type': 'Belt',
            'class': 'Magician',
            'level': 150,
            'str': 50,
            'dex': 50,
            'int': 50,
            'luk': 50,
            'hp': 0,
            'mp': 0,
            'watt': 25,
            'matt': 25,
            'wdef': 105,
            'mdef': 105,
            'accuracy': 0,
            'avoid': 0,
            'boss': 0,
            'pdr': 0,
            'slot': 1,
            'setId': 0,
            # market info
            'cost': ['Meso','Magnus Coin'],
            'value': [1, 100],
            'stock': [5, -1],
            'max': [10, -1],
            'supply': [5, -1],
            },
        }
    m_libGlove = {
        'Tyrant Hermes Gloves' : {
            'name': 'Tyrant Hermes Gloves',
            'type': 'Glove',
            'class': 'Magician',
            'level': 150,
            'str': 0,
            'dex': 0,
            'int': 12,
            'luk': 12,
            'hp': 0,
            'mp': 300,
            'watt': 0,
            'matt': 15,
            'wdef': 0,
            'mdef': 160,
            'accuracy': 35,
            'avoid': 0,
            'boss': 0,
            'pdr': 0,
            'slot': 1,
            'setId': 0,
            # market info
            'cost': ['Meso','Shadow Coin'],
            'value': [1, 400],
            'stock': [5, -1],
            'max': [10, -1],
            'supply': [5, -1],
            },
        }
    m_libEye = {
        'Sweetwater Glasses' : {
            'name': 'Sweetwater Glasses',
            'type': 'Eye',
            'class': 'All',
            'level': 160,
            'str': 10,
            'dex': 10,
            'int': 10,
            'luk': 10,
            'hp': 240,
            'mp': 240,
            'watt': 0,
            'matt': 0,
            'wdef': 0,
            'mdef': 0,
            'accuracy': 0,
            'avoid': 0,
            'boss': 0,
            'pdr': 0,
            'slot': 5,
            'setId': 0,
            # market info
            'cost': ['Meso','Denaro'],
            'value': [1, 250],
            'stock': [5, -1],
            'max': [10, -1],
            'supply': [5, -1],
            },
        }
    m_libFace = {
        'Sweetwater Tattoo' : {
            'name': 'Sweetwater Tattoo',
            'type': 'Face',
            'class': 'All',
            'level': 160,
            'str': 5,
            'dex': 5,
            'int': 5,
            'luk': 5,
            'hp': 120,
            'mp': 120,
            'watt': 0,
            'matt': 0,
            'wdef': 0,
            'mdef': 0,
            'accuracy': 0,
            'avoid': 0,
            'boss': 0,
            'pdr': 0,
            'slot': 5,
            'setId': 0,
            # market info
            'cost': ['Meso','Denaro'],
            'value': [1, 250],
            'stock': [5, -1],
            'max': [10, -1],
            'supply': [5, -1],
            },
        }
    m_libRing = {
        'Superior Gollux Ring' : {
            'name': 'Superior Gollux Ring',
            'type': 'Ring',
            'class': 'All',
            'level': 150,
            'str': 10,
            'dex': 10,
            'int': 10,
            'luk': 10,
            'hp': 250,
            'mp': 250,
            'watt': 8,
            'matt': 8,
            'wdef': 150,
            'mdef': 150,
            'accuracy': 100,
            'avoid': 100,
            #TODO: speed
            'boss': 0,
            'pdr': 0,
            'slot': 6,
            'setId': 5,
            # market info
            'cost': ['Meso','Gollux Coin'],
            'value': [1, 160],
            'stock': [5, 1],
            'max': [10, 1],
            'supply': [5, 0],
            },
        }
    m_libPendant = {
        'Superior Engraved Gollux Pendant' : {
            'name': 'Superior Engraved Gollux Pendant',
            'type': 'Pendant',
            'class': 'All',
            'level': 150,
            'str': 28,
            'dex': 28,
            'int': 28,
            'luk': 28,
            'hp': 300,
            'mp': 300,
            'watt': 5,
            'matt': 5,
            'wdef': 100,
            'mdef': 100,
            'accuracy': 50,
            'avoid': 50,
            'boss': 0,
            'pdr': 0,
            'slot': 6,
            'setId': 5,
            # market info
            'cost': ['Meso','Gollux Coin SS'],
            'value': [1, 1],
            'stock': [5, 1],
            'max': [10, 1],
            'supply': [5, 1],
            },
        }
    m_libEarring = {
        'Superior Gollux Earrings' : {
            'name': 'Superior Gollux Earrings',
            'type': 'Earring',
            'class': 'All',
            'level': 150,
            'str': 15,
            'dex': 15,
            'int': 15,
            'luk': 15,
            'hp': 150,
            'mp': 150,
            'watt': 10,
            'matt': 10,
            'wdef': 100,
            'mdef': 100,
            'accuracy': 100,
            'avoid': 100,
            'boss': 0,
            'pdr': 0,
            'slot': 7,
            'setId': 5,
            # market info
            'cost': ['Meso','Gollux Coin'],
            'value': [1, 170],
            'stock': [5, 1],
            'max': [10, 1],
            'supply': [5, 0],
            },
        }
    m_libBadge = {
        'Ghost Ship Exorcist' : {
            'name': 'Ghost Ship Exorcist',
            'type': 'Badge',
            'class': 'All',
            'level': 150,
            'str': 3,
            'dex': 3,
            'int': 3,
            'luk': 3,
            'hp': 0,
            'mp': 0,
            'watt': 2,
            'matt': 2,
            'wdef': 70,
            'mdef': 70,
            'accuracy': 0,
            'avoid': 0,
            'boss': 0,
            'pdr': 0,
            'slot': 1,
            'setId': 0,
            # market info
            'cost': ['Meso'],
            'value': [0],
            'stock': [1],
            'max': [1],
            'supply': [0],
            },
        }
    m_libWeapon = {
        'Fafnir Mana Crown' : {
            'name': 'Fafnir Mana Crown',
            'type': 'Weapon',
            'category': 'Staff',
            'class': 'Magician',
            'level': 150,
            'str': 0,
            'dex': 0,
            'int': 40,
            'luk': 40,
            'hp': 0,
            'mp': 0,
            'watt': 126,
            'matt': 204,
            'wdef': 0,
            'mdef': 0,
            'accuracy': 120,
            'avoid': 0,
            'boss': 0.3,
            'pdr': 0.1,
            'slot': 8,
            'setId': 1,
            # market info
            'cost': ['Meso','Vellum Coin'],
            'value': [1, 5],
            'stock': [5, 1],
            'max': [10, 1],
            'supply': [5, 0],
            },
        'Fafnir Wind Chaser' : {
            'name': 'Fafnir Wind Chaser',
            'type': 'Weapon',
            'category': 'Bow',
            'class': 'Bowman',
            'level': 150,
            'str': 40,
            'dex': 40,
            'int': 0,
            'luk': 0,
            'hp': 0,
            'mp': 0,
            'watt': 160,
            'matt': 0,
            'wdef': 0,
            'mdef': 0,
            'accuracy': 120,
            'avoid': 0,
            'boss': 0.3,
            'pdr': 0.1,
            'slot': 8,
            'setId': 2,
            # market info
            'cost': ['Meso','Vellum Coin'],
            'value': [1, 5],
            'stock': [5, 1],
            'max': [10, 1],
            'supply': [5, 0],
            },
        }
    m_libSecondary = {
        'VIP Magician Shield' : {
            'name': 'VIP Magician Shield',
            'type': 'Secondary',
            'category': 'Shield',
            'class': 'Magician',
            'level': 127,
            'str': 0,
            'dex': 0,
            'int': 10,
            'luk': 4,
            'hp': 0,
            'mp': 0,
            'watt': 0,
            'matt': 0,
            'wdef': 110,
            'mdef': 160,
            'accuracy': 0,
            'avoid': 0,
            'boss': 0,
            'pdr': 0,
            'slot': 7,
            'setId': 0,
            # market info
            'cost': ['Meso'],
            'value': [1],
            'stock': [5],
            'max': [10],
            'supply': [5],
            },
        'Blasted Feather': {
            'name': 'Blasted Feather',
            'type': 'Secondary',
            'category': 'Arrow Fletching',
            'class': 'Bowman',
            'level': 100,
            'str': 10,
            'dex': 10,
            'int': 0,
            'luk': 0,
            'hp': 0,
            'mp': 0,
            'watt': 3,
            'matt': 0,
            'wdef': 0,
            'mdef': 0,
            'accuracy': 0,
            'avoid': 0,
            'boss': 0,
            'pdr': 0,
            'slot': 0,
            'setId': 0,
            # market info
            'cost': ['Meso'],
            'value': [1],
            'stock': [5],
            'max': [10],
            'supply': [5],
            },
        }
    m_libEmblem = {
        'Gold Maple Leaf Emblem' : {
            'name': 'Gold Maple Leaf Emblem',
            'type': 'Emblem',
            'category': 'Explorer',
            'class': 'All',
            'level': 100,
            'str': 10,
            'dex': 10,
            'int': 10,
            'luk': 10,
            'hp': 0,
            'mp': 0,
            'watt': 2,
            'matt': 2,
            'wdef': 0,
            'mdef': 0,
            'accuracy': 0,
            'avoid': 0,
            'boss': 0,
            'pdr': 0,
            'slot': 0,
            'setId': 0,
            # market info
            'cost': ['Meso'],
            'value': [0],
            'stock': [-1],
            'max': [-1],
            'supply': [-1],
            },
        }
    m_lib = {
        'Hat': m_libHat,
        'Top': m_libTop,
        'Bottom': m_libBottom,
        'Shoe': m_libShoe,
        'Cape': m_libCape,
        'Belt': m_libBelt,
        'Glove': m_libGlove,
        'Eye': m_libEye,
        'Face': m_libFace,
        'Ring': m_libRing,
        'Pendant': m_libPendant,
        'Earring': m_libEarring,
        'Badge': m_libBadge,
        'Weapon': m_libWeapon,
        'Secondary': m_libSecondary,
        'Emblem': m_libEmblem,
        
    }


    @staticmethod
    def getEquip(equipName):
        for equipType in EquipLib.m_lib.values():
            if equipName in equipType.keys():
                return equipType[equipName]
        return None
                
