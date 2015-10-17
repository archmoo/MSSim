class SpecialLib:
    'Special items library'

    m_lib = {
        'Innocent Scroll 50%' : {
            'type': 'Special',
            'success rate': 0.5,
            'boom rate': 0,
            'effect': 'Innocent',
            'description': 'Resets all stats from an item except for its Potentials.\nSuccess Rate: 50%\n',
            # market info
            'cost': ['Meso','Elite Coin'],
            'value': [1, 3],
            'stock': [-1, 5],
            'max': [-1, 5],
            'supply': [-1, 5],
            },
        'Innocent Scroll 100%' : {
            'type': 'Special',
            'success rate': 1,
            'boom rate': 0,
            'effect': 'Innocent',
            'description': 'Resets all stats from an item except for its Potentials.\nSuccess Rate: 100%\n',
            # market info
            'cost': ['NX'],
            'value': [1],
            'stock': [-1],
            'max': [-1],
            'supply': [-1],
            },
        'Potential Scroll' : {
            'type': 'Special',
            'success rate': 0.7,
            'boom rate': 1,
            'effect': 'Potential',
            'description': 'Provides potentials for regular equip items.\nSuccess Rate: 70%\nIf it fails, the item will be destroyed.\n',
            # market info
            'cost': ['Meso','Elite Coin'],
            'value': [1, 3],
            'stock': [5, 5],
            'max': [10, 5],
            'supply': [5, 5],
            },
        'Advanced Potential Scroll' : {
            'type': 'Special',
            'success rate': 0.9,
            'boom rate': 1,
            'effect': 'Potential',
            'description': 'Provides potentials for regular equip items.\nSuccess Rate: 90%\nIf it fails, the item will be destroyed.\n',
            # market info
            'cost': ['Meso','Red Cube Coin'],
            'value': [1, 10],
            'stock': [5, -1],
            'max': [10, -1],
            'supply': [5, -1],
            },
        'Special Potential Scroll' : {
            'type': 'Special',
            'success rate': 1,
            'boom rate': 0,
            'effect': 'Potential',
            'description': 'Provides potentials for regular equip items.\nSuccess Rate: 100%\n',
            # market info
            'cost': ['NX'],
            'value': [1],
            'stock': [-1],
            'max': [-1],
            'supply': [-1],
            },
        'Epic Potential Scroll 50%' : {
            'type': 'Special',
            'success rate': 0.5,
            'boom rate': 0,
            'effect': 'Epic Potential',
            'description': 'Gives Epic Potential to items that are ranked Rare or below.\nSuccess Rate: 50%\n',
            # market info
            'cost': ['Meso','Elite Coin'],
            'value': [1, 3],
            'stock': [5, 5],
            'max': [10, 5],
            'supply': [5, 5],
            },
        'Epic Potential Scroll 80%' : {
            'type': 'Special',
            'success rate': 0.8,
            'boom rate': 0.2,
            'effect': 'Epic Potential',
            'description': 'Gives Epic Potential to items that are ranked Rare or below.\nSuccess Rate: 80%\nIf it fails, the item has a 20% chance of being destroyed.\n',
            # market info
            'cost': ['Event Coin'],
            'value': [1],
            'stock': [0],
            'max': [1],
            'supply': [0],
            },
        'Epic Potential Scroll 100%' : {
            'type': 'Special',
            'success rate': 1,
            'boom rate': 0,
            'effect': 'Epic Potential',
            'description': 'Gives Epic Potential to items that are ranked Rare or below.\nSuccess Rate: 100%\n',
            # market info
            'cost': ['Event Coin'],
            'value': [1],
            'stock': [0],
            'max': [1],
            'supply': [0],
            },
        'Unique Potential Scroll 60%' : {
            'type': 'Special',
            'success rate': 0.6,
            'boom rate': 0,
            'effect': 'Unique Potential',
            'description': 'Gives Unique Potential to items that are ranked Epic or below.\nSuccess Rate: 60%\n',
            # market info
            'cost': ['Event Coin'],
            'value': [1],
            'stock': [0],
            'max': [1],
            'supply': [0],
            },
        'Unique Potential Scroll 80%' : {
            'type': 'Special',
            'success rate': 0.8,
            'boom rate': 0,
            'effect': 'Unique Potential',
            'description': 'Gives Unique Potential to items that are ranked Epic or below.\nSuccess Rate: 80%\n',
            # market info
            'cost': ['Event Coin'],
            'value': [1],
            'stock': [0],
            'max': [1],
            'supply': [0],
            },
        'Clean Slate Scroll 10%' : {
            'type': 'Special',
            'success rate': 0.1,
            'boom rate': 0,
            'effect': 'Clean Slate',
            'description': 'Recovers the lost number of upgrades due to failed scroll by 1.\nSuccess Rate: 10%\n',
            # market info
            'cost': ['Meso','Elite Coin'],
            'value': [1, 3],
            'stock': [5, 5],
            'max': [10, 5],
            'supply': [5, 5],
            },
        'Clean Slate Scroll 1%' : {
            'type': 'Special',
            'success rate': 0.01,
            'boom rate': 0.02,
            'effect': 'Clean Slate',
            'description': 'Recovers the lost number of upgrades due to failed scroll by 1.\nSuccess Rate: 1%\nIf failed, the item has a 2% chance of being destroyed.\n',
            # market info
            'cost': ['Meso','Boss Coin'],
            'value': [1, 3],
            'stock': [5, 5],
            'max': [10, 5],
            'supply': [5, 5],
            },
        'Clean Slate Scroll 20%' : {
            'type': 'Special',
            'success rate': 0.2,
            'boom rate': 0,
            'effect': 'Clean Slate',
            'description': 'Recovers the lost number of upgrades due to failed scroll by 1.\nSuccess Rate: 20%\n',
            # market info
            'cost': ['Event Coin'],
            'value': [1],
            'stock': [0],
            'max': [1],
            'supply': [0],
            },
        'Golden Hammer 50%' : {
            'type': 'Hammer',
            'success rate': 0.5,
            'boom rate': 0,
            'effect': 'Hammer',
            'description': 'Provides one additional chance to apply a scroll to your equipment.\nSuccess Rate: 50%\n',
            # market info
            'cost': ['Meso','Elite Coin'],
            'value': [1, 3],
            'stock': [5, 5],
            'max': [10, 5],
            'supply': [5, 5],
            },
        'Golden Hammer 100%' : {
            'type': 'Hammer',
            'success rate': 1,
            'boom rate': 0,
            'effect': 'Hammer',
            'description': 'Provides one additional chance to apply a scroll to your equipment.\nSuccess Rate: 100%\n',
            # market info
            'cost': ['NX','Event Coin'],
            'value': [1, 1],
            'stock': [5, 0],
            'max': [10, 1],
            'supply': [5, 0],
            },
        'Perfect Potential Stamp' : {
            'type': 'Special',
            'success rate': 1,
            'boom rate': 0,
            'effect': 'Potential Stamp',
            'description': 'Add 1 additional line of Potential to a piece of equipment with less than 3 Potential lines.\nSuccess Rate: 100%\n',
            # market info
            'cost': ['Meso','Red Cube Coin', 'Black Cube Coin'],
            'value': [1, 20, 15],
            'stock': [5, -1, -1],
            'max': [10, -1, -1],
            'supply': [5, -1, -1],
            },
        'Gold Potential Stamp' : {
            'type': 'Special',
            'success rate': 0.8,
            'boom rate': 0,
            'effect': 'Potential Stamp',
            'description': 'Adds 1 additional line of Potential to a piece of equipment with less than 3 Potential lines.\nSuccess Rate: 80%\n',
            # market info
            'cost': ['Meso','Elite Coin'],
            'value': [1, 3],
            'stock': [5, 5],
            'max': [10, 5],
            'supply': [5, 5],
            },
        'Silver Potential Stamp' : {
            'type': 'Special',
            'success rate': 0.5,
            'boom rate': 0,
            'effect': 'Potential Stamp',
            'description': 'Adds 1 additional line of Potential to a piece of equipment with less than 3 Potential lines.\nSuccess Rate: 50%\n',
            # market info
            'cost': ['Meso','Elite Coin'],
            'value': [1, 3],
            'stock': [5, 5],
            'max': [10, 5],
            'supply': [5, 5],
            },
        'Protection Scroll' : {
            'type': 'Special',
            'success rate': 1,
            'boom rate': 0,
            'effect': 'Protect',
            'description': 'Protects a piece of equipment from being destroyed by a failed scroll 1 time. Effect disappears after a successful scroll use.\n',
            # market info
            'cost': ['Meso','NX', 'Elite Coin', 'Event Coin'],
            'value': [1, 3, 3, 1],
            'stock': [5, -1, 5, 0],
            'max': [10, -1, 5, 1],
            'supply': [5, -1, 5, 0],
            },
        #TODO: 12+ enhancement not available
        'Guardian Scroll' : {
            'type': 'Special',
            'success rate': 1,
            'boom rate': 0,
            'effect': 'Guardian',
            'description': 'Keeps a scroll from being destroyed if a scrolling attempt fails. Effect disappears after a successful scroll use.\n',
            # market info
            'cost': ['NX'],
            'value': [1],
            'stock': [-1],
            'max': [-1],
            'supply': [-1],
            },
        'Shield Scroll' : {
            'type': 'Special',
            'success rate': 1,
            'boom rate': 0,
            'effect': 'Safety',
            'description': 'Protects a piece of equipment from having its upgrade count reduced by a failed scroll 1 time. Effect disappears after a successful scroll use.\n',
            # market info
            'cost': ['NX','Event Coin'],
            'value': [1, 1],
            'stock': [-1, 0],
            'max': [-1, 1],
            'supply': [-1, 0],
            },
        'Red Cube' : {
            'type': 'Cube',
            'availability': (True, True, True, True),
            'tierup rate': (0.2, 0.1, 0.04, 0),
            'effect': 'Reset Potential',
            'description': 'Randomly reconfigures the Potential on a piece of equipment. Only usable on items from Rare to Legendary.\nMax Result: Legendary\nHas a chance to raise Potential rank.\n',
            # market info
            'cost': ['NX'],
            'value': [1],
            'stock': [-1],
            'max': [-1],
            'supply': [-1],
            },
        'Black Cube' : {
            'type': 'Cube',
            'availability': (True, True, True, True),
            'tierup rate': (0.45, 0.25, 0.1, 0),
            'effect': 'Choose Potential',
            'description': 'Randomly reconfigures the Potential on a piece of equipment. Offers the chance to decide whether or not to apply the new Potential to the item. Only usable on items from Rare to Legendary.\nMax Result: Legendary\nHas a higher chance to raise Potential rank.\n',
            # market info
            'cost': ['NX'],
            'value': [1],
            'stock': [-1],
            'max': [-1],
            'supply': [-1],
            },
        'Violet Cube' : {
            'type': 'Cube',
            'availability': (True, True, True, True),
            'tierup rate': (0.45, 0.25, 0.1, 0),
            'effect': 'Pick Potential Lines',
            'description': 'Randomly reconfigures the Potential on a piece of equipment. Gives twice the lines of its current number of Potential lines to choose from. Only usable on items from Rare to Legendary.\nMax Result: Legendary\nHas a higher chance to raise Potential rank.\n',
            # market info
            'cost': ['NX'],
            'value': [1],
            'stock': [0],
            'max': [1],
            'supply': [0],
            },
        'Master Craftsman Cube' : {
            'type': 'Cube',
            'availability': (True, True, True, False),
            'tierup rate': (0.055, 0.01, 0, 0),
            'effect': 'Reset Potential',
            'description': 'Randomly reconfigures the Potential on a piece of equipment. Only usable on items from Rare to Unique.\nMax Result: Unique\nHas a chance to raise Potential rank.\n',
            # market info
            'cost': ['Meso','Boss Coin'],
            'value': [1, 3],
            'stock': [5, 5],
            'max': [10, 5],
            'supply': [5, 5],
            },
        'Meister Cube' : {
            'type': 'Cube',
            'availability': (True, True, True, True),
            'tierup rate': (0.1, 0.05, 0.01, 0),
            'effect': 'Reset Potential',
            'description': 'Randomly reconfigures the Potential on a piece of equipment. Only usable on items from Rare to Legendary.\nMax Result: Legendary\nHas a chance to raise Potential rank.\n',
            # market info
            'cost': ['Meso','Boss Coin'],
            'value': [1, 3],
            'stock': [5, 5],
            'max': [10, 5],
            'supply': [5, 5],
            },
        
        }
