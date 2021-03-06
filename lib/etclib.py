import random, locale

class EtcLib:

    m_lib = {
        'Spell Trace': {
            'type': 'Trace',
            'description': 'Required to purchase most enhancing scrolls that use up upgrade counts.\n',
            'cost': ['Meso', 'Black Cube Coin'],
            'value': [1, 5],
            'stock': [5, -1],
            'max': [10, -1],
            'supply': [5, -1],
            'etc': 'Trace',
            'quantity': 1,
            },
        'Free Meso (dev only)': {
            'type': 'Meso',
            'description': 'Receive arbitraty amount of Mesos.\nMeso is the in-game currency.\n',
            'cost': ['Meso'],
            'value': [0],
            'stock': [-1],
            'max': [-1],
            'supply': [-1],
            'etc': 'Meso',
            'quantity': 1,
            },
        'Unique Meso Sack': {
            'type': 'Meso',
            'description': 'Randomly receive large amount of Mesos.\nMeso is the in-game currency.\n',
            'cost': ['NX'],
            'value': [5000],
            'stock': [-1],
            'max': [-1],
            'supply': [-1],
            'etc': 'Meso',
            'quantity': 0.2,
            },
        'Epic Meso Sack': {
            'type': 'Meso',
            'description': 'Randomly receive good amount of Mesos.\nMeso is the in-game currency.\n',
            'cost': ['NX'],
            'value': [3000],
            'stock': [-1],
            'max': [-1],
            'supply': [-1],
            'etc': 'Meso',
            'quantity': 0.5,
            },
        'Rare Meso Sack': {
            'type': 'Meso',
            'description': 'Randomly receive small amount of Mesos.\nMeso is the in-game currency.\n',
            'cost': ['NX'],
            'value': [2000],
            'stock': [-1],
            'max': [-1],
            'supply': [-1],
            'etc': 'Meso',
            'quantity': 1,
            },
        'NX 10,000': {
            'type': 'NX',
            'description': 'Receive 10,000 NX.\nNX is used to purchase cash items.\n',
            'cost': ['Meso'],
            'value': [1100000000],
            'stock': [10],
            'max': [10],
            'supply': [10],
            'etc': 'NX',
            'quantity': 10000,
            },
        'NX 25,000': {
            'type': 'NX',
            'description': 'Receive 25,000 NX.\nNX is used to purchase cash items.\n',
            'cost': ['Meso'],
            'value': [2600000000],
            'stock': [5],
            'max': [5],
            'supply': [5],
            'etc': 'NX',
            'quantity': 25000,
            },
        'NX 50,000': {
            'type': 'NX',
            'description': 'Receive 50,000 NX.\nNX is used to purchase cash items.\n',
            'cost': ['Meso'],
            'value': [5000000000],
            'stock': [2],
            'max': [2],
            'supply': [2],
            'etc': 'NX',
            'quantity': 50000,
            },
        
        'Elite Coin': {
            'type': 'Coin',
            'description': 'Coins awarded for defeating Elite Bosses.\n',
            'cost': [],
            'value': [],
            'stock': [],
            'max': [],
            'supply': [],
            'etc': 'Elite Coin',
            'quantity': 1,
            },
        'Boss Coin': {
            'type': 'Coin',
            'description': 'Coins awarded for defeating Bosses.\n',
            'cost': [],
            'value': [],
            'stock': [],
            'max': [],
            'supply': [],
            'etc': 'Boss Coin',
            'quantity': 1,
            },
        'Event Coin': {
            'type': 'Coin',
            'description': 'Coins awarded for participating in events.\n',
            'cost': [],
            'value': [],
            'stock': [],
            'max': [],
            'supply': [],
            'etc': 'Event Coin',
            'quantity': 1,
            },
        'Red Cube Coin': {
            'type': 'Coin',
            'description': 'Coins awarded for using a Red Cube.\n',
            'cost': [],
            'value': [],
            'stock': [],
            'max': [],
            'supply': [],
            'etc': 'Red Cube Coin',
            'quantity': 1,
            },
        'Black Cube Coin': {
            'type': 'Coin',
            'description': 'Coins awarded for using a Black Cube.\n',
            'cost': [],
            'value': [],
            'stock': [],
            'max': [],
            'supply': [],
            'etc': 'Black Cube Coin',
            'quantity': 1,
            },
        'Queen Coin': {
            'type': 'Coin',
            'description': 'Coins awarded for defeating Chaos Crimson Queen.\n',
            'cost': [],
            'value': [],
            'stock': [],
            'max': [],
            'supply': [],
            'etc': 'Queen Coin',
            'quantity': 1,
            },
        'Pierre Coin': {
            'type': 'Coin',
            'description': 'Coins awarded for defeating Chaos Pierre.\n',
            'cost': [],
            'value': [],
            'stock': [],
            'max': [],
            'supply': [],
            'etc': 'Pierre Coin',
            'quantity': 1,
            },
        'VonBon Coin': {
            'type': 'Coin',
            'description': 'Coins awarded for defeating Chaos VonBon.\n',
            'cost': [],
            'value': [],
            'stock': [],
            'max': [],
            'supply': [],
            'etc': 'VonBon Coin',
            'quantity': 1,
            },
        'Vellum Coin': {
            'type': 'Coin',
            'description': 'Coins awarded for defeating Chaos Vellum.\n',
            'cost': [],
            'value': [],
            'stock': [],
            'max': [],
            'supply': [],
            'etc': 'Vellum Coin',
            'quantity': 1,
            },
        'Magnus Coin': {
            'type': 'Coin',
            'description': 'Coins awarded for defeating Hard Magnus.\nCan be used to exchange for Tyrant Boots/Belt.\n',
            'cost': [],
            'value': [],
            'stock': [],
            'max': [],
            'supply': [],
            'etc': 'Magnus Coin',
            'quantity': 1,
            },
        'Magnus Coin B': {
            'type': 'Coin',
            'description': 'Coins awarded for defeating Hard Magnus.\nCan be used to exchange for Tyrant Capes.\n',
            'cost': [],
            'value': [],
            'stock': [],
            'max': [],
            'supply': [],
            'etc': 'Magnus Coin B',
            'quantity': 1,
            },
        'Cygnus Coin': {
            'type': 'Coin',
            'description': 'Coins awarded for defeating Empress Cygnus.\n',
            'cost': [],
            'value': [],
            'stock': [],
            'max': [],
            'supply': [],
            'etc': 'Cygnus Coin',
            'quantity': 1,
            },
        'Shadow Coin': {
            'type': 'Coin',
            'description': 'Coins awarded for finishing Kritias daily quests.\n',
            'cost': [],
            'value': [],
            'stock': [],
            'max': [],
            'supply': [],
            'etc': 'Shadow Coin',
            'quantity': 1,
            },
        'Denaro': {
            'type': 'Coin',
            'description': 'Coins awarded for completing Commerci voyage.\n',
            'cost': [],
            'value': [],
            'stock': [],
            'max': [],
            'supply': [],
            'etc': 'Denaro',
            'quantity': 1,
            },
        'Gollux Coin': {
            'type': 'Coin',
            'description': 'Coins awarded for defeating Gollux.\n',
            'cost': [],
            'value': [],
            'stock': [],
            'max': [],
            'supply': [],
            'etc': 'Gollux Coin',
            'quantity': 1,
            },
        'Gollux Penny': {
            'type': 'Coin',
            'description': 'Coins dropped by Gollux parts.\n',
            'cost': [],
            'value': [],
            'stock': [],
            'max': [],
            'supply': [],
            'etc': 'Gollux Penny',
            'quantity': 1,
            },
        'Gollux Coin B': {
            'type': 'Coin',
            'description': 'Coins awarded for defeating Gollux under difficulty level 1.\n',
            'cost': [],
            'value': [],
            'stock': [],
            'max': [],
            'supply': [],
            'etc': 'Gollux Coin B',
            'quantity': 1,
            },
        'Gollux Coin A': {
            'type': 'Coin',
            'description': 'Coins awarded for defeating Gollux under difficulty level 2.\n',
            'cost': [],
            'value': [],
            'stock': [],
            'max': [],
            'supply': [],
            'etc': 'Gollux Coin A',
            'quantity': 1,
            },
        'Gollux Coin S': {
            'type': 'Coin',
            'description': 'Coins awarded for defeating Gollux under difficulty level 3.\n',
            'cost': [],
            'value': [],
            'stock': [],
            'max': [],
            'supply': [],
            'etc': 'Gollux Coin S',
            'quantity': 1,
            },
        'Gollux Coin SS': {
            'type': 'Coin',
            'description': 'Coins awarded for defeating Gollux under difficulty level MAX.\n',
            'cost': [],
            'value': [],
            'stock': [],
            'max': [],
            'supply': [],
            'etc': 'Gollux Coin SS',
            'quantity': 1,
            },
        }

    
    @staticmethod
    def dispLongNum(num):
        locale.setlocale(locale.LC_ALL, 'en_US')
        return locale.format("%d", num, grouping=True)
        

if __name__ == '__main__':

    print EtcLib.dispLongNum(EtcLib.m_lib['Rare Meso Sack']['quantity'])
    print EtcLib.dispLongNum(EtcLib.m_lib['Epic Meso Sack']['quantity'])
    print EtcLib.dispLongNum(EtcLib.m_lib['Unique Meso Sack']['quantity'])
            
