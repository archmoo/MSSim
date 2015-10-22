class EquipSetLib:
    m_lib = {
        1: {
            'name': 'Root Abyss Set (Warrior)',
            'effect': {
                2: [('# STR', 20),('# DEX', 20), ('# Max HP', 1000), ('# Max MP', 1000)],
                3: [('% Max HP', 0.1), ('% Max MP', 0.1), ('# Weapon ATT', 50)],
                4: [('% Boss Damage', 0.3)],
                }
            },
        2: {
            'name': 'Root Abyss Set (Bowman)',
            'effect': {
                2: [('# STR', 20),('# DEX', 20), ('# Max HP', 1000), ('# Max MP', 1000)],
                3: [('% Max HP', 0.1), ('% Max MP', 0.1), ('# Weapon ATT', 50)],
                4: [('% Boss Damage', 0.3)],
                }
            },
        3: {
            'name': 'Root Abyss Set (Magician)',
            'effect': {
                2: [('# INT', 20),('# LUK', 20), ('# Max HP', 1000), ('# Max MP', 1000)],
                3: [('% Max HP', 0.1), ('% Max MP', 0.1), ('# Magic ATT', 50)],
                4: [('% Boss Damage', 0.3)],
                }
            },
        4: {
            'name': 'Root Abyss Set (Thief)',
            'effect': {
                2: [('# DEX', 20),('# LUK', 20), ('# Max HP', 1000), ('# Max MP', 1000)],
                3: [('% Max HP', 0.1), ('% Max MP', 0.1), ('# Weapon ATT', 50)],
                4: [('% Boss Damage', 0.3)],
                }
            },
        5: {
            'name': 'Root Abyss Set (Pirate)',
            'effect': {
                2: [('# STR', 20),('# DEX', 20), ('# Max HP', 1000), ('# Max MP', 1000)],
                3: [('% Max HP', 0.1), ('% Max MP', 0.1), ('# Weapon ATT', 50)],
                4: [('% Boss Damage', 0.3)],
                }
            },
        6: {
            'name': 'Lionheart Set',
            'effect': {
                2: [('# Weapon DEF', 300), ('# Magic DEF', 300), ('# Accuracy', 200), ('# Avoid', 200)],
                3: [('% Max HP', 0.15), ('% Max MP', 0.15)],
                4: [('# Weapon ATT', 15), ('# Abnormal Status Duration Reduction', '2 sec')],
                5: [('# All Stats', 20), ('# Skill Level Increase', 2)],
                6: [('# Weapon ATT', 30), ('% Boss Damage', 0.3)],
                7: [('% Max HP', 0.15), ('% Max MP', 0.15), ('# Weapon ATT', 10)],
                }
            },
        7: {
            'name': 'Falcon Wing Set',
            'effect': {
                2: [('# Weapon DEF', 300), ('# Magic DEF', 300), ('# Accuracy', 200), ('# Avoid', 200)],
                3: [('% Max HP', 0.15), ('% Max MP', 0.15)],
                4: [('# Weapon ATT', 15), ('# Abnormal Status Duration Reduction', '2 sec')],
                5: [('# All Stats', 20), ('# Skill Level Increase', 2)],
                6: [('# Weapon ATT', 30), ('% Boss Damage', 0.3)],
                7: [('% Max HP', 0.15), ('% Max MP', 0.15), ('# Weapon ATT', 10)],
                }
            },
        8: {
            'name': 'Dragon Tail Set',
            'effect': {
                2: [('# Weapon DEF', 300), ('# Magic DEF', 300), ('# Accuracy', 200), ('# Avoid', 200)],
                3: [('% Max HP', 0.15), ('% Max MP', 0.15)],
                4: [('# Magic ATT', 15), ('# Abnormal Status Duration Reduction', '2 sec')],
                5: [('# All Stats', 20), ('# Skill Level Increase', 2)],
                6: [('# Magic ATT', 30), ('% Boss Damage', 0.3)],
                7: [('% Max HP', 0.15), ('% Max MP', 0.15), ('# Magic ATT', 10)],
                }
            },
        9: {
            'name': 'Raven Horn Set',
            'effect': {
                2: [('# Weapon DEF', 300), ('# Magic DEF', 300), ('# Accuracy', 200), ('# Avoid', 200)],
                3: [('% Max HP', 0.15), ('% Max MP', 0.15)],
                4: [('# Weapon ATT', 15), ('# Abnormal Status Duration Reduction', '2 sec')],
                5: [('# All Stats', 20), ('# Skill Level Increase', 2)],
                6: [('# Weapon ATT', 30), ('% Boss Damage', 0.3)],
                7: [('% Max HP', 0.15), ('% Max MP', 0.15), ('# Weapon ATT', 10)],
                }
            },
        10: {
            'name': 'Shark Tooth Set',
            'effect': {
                2: [('# Weapon DEF', 300), ('# Magic DEF', 300), ('# Accuracy', 200), ('# Avoid', 200)],
                3: [('% Max HP', 0.15), ('% Max MP', 0.15)],
                4: [('# Weapon ATT', 15), ('# Abnormal Status Duration Reduction', '2 sec')],
                5: [('# All Stats', 20), ('# Skill Level Increase', 2)],
                6: [('# Weapon ATT', 30), ('% Boss Damage', 0.3)],
                7: [('% Max HP', 0.15), ('% Max MP', 0.15), ('# Weapon ATT', 10)],
                }
            },
        11: {
            'name': '8th Warrior Set',
            'effect': {
                2: [('# Weapon DEF', 140), ('# Magic DEF', 140), ('# Accuracy', 140), ('# Avoid', 140)],
                3: [('% Max HP', 0.09), ('% Max MP', 0.09)],
                4: [('# STR', 9), ('# Weapon ATT', 9)],
                5: [('# All Stats', 15), ('# Weapon DEF', 250), ('# Magic DEF', 250), ('% Ignore Defense', 0.1)],
                6: [('# Weapon ATT', 10), ('# Magic ATT', 10), ('% Ignore Defense', 0.1)],
                }
            },
        12: {
            'name': '8th Bowman Set',
            'effect': {
                2: [('# Weapon DEF', 140), ('# Magic DEF', 140), ('# Accuracy', 140), ('# Avoid', 140)],
                3: [('% Max HP', 0.09), ('% Max MP', 0.09)],
                4: [('# DEX', 9), ('# Weapon ATT', 9)],
                5: [('# All Stats', 15), ('# Weapon DEF', 250), ('# Magic DEF', 250), ('% Ignore Defense', 0.1)],
                6: [('# Weapon ATT', 10), ('# Magic ATT', 10), ('% Ignore Defense', 0.1)],
                }
            },
        13: {
            'name': '8th Magician Set',
            'effect': {
                2: [('# Weapon DEF', 140), ('# Magic DEF', 140), ('# Accuracy', 140), ('# Avoid', 140)],
                3: [('% Max HP', 0.09), ('% Max MP', 0.09)],
                4: [('# INT', 9), ('# Magic ATT', 9)],
                5: [('# All Stats', 15), ('# Weapon DEF', 250), ('# Magic DEF', 250), ('% Ignore Defense', 0.1)],
                6: [('# Weapon ATT', 10), ('# Magic ATT', 10), ('% Ignore Defense', 0.1)],
                }
            },
        14: {
            'name': '8th Thief Set',
            'effect': {
                2: [('# Weapon DEF', 140), ('# Magic DEF', 140), ('# Accuracy', 140), ('# Avoid', 140)],
                3: [('% Max HP', 0.09), ('% Max MP', 0.09)],
                4: [('# LUK', 9), ('# Weapon ATT', 9)],
                5: [('# All Stats', 15), ('# Weapon DEF', 250), ('# Magic DEF', 250), ('% Ignore Defense', 0.1)],
                6: [('# Weapon ATT', 10), ('# Magic ATT', 10), ('% Ignore Defense', 0.1)],
                }
            },
        15: {
            'name': '8th Pirate Set',
            'effect': {
                2: [('# Weapon DEF', 140), ('# Magic DEF', 140), ('# Accuracy', 140), ('# Avoid', 140)],
                3: [('% Max HP', 0.09), ('% Max MP', 0.09)],
                4: [('# STR', 9), ('# DEX', 9), ('# Weapon ATT', 9)],
                5: [('# All Stats', 15), ('# Weapon DEF', 250), ('# Magic DEF', 250), ('% Ignore Defense', 0.1)],
                6: [('# Weapon ATT', 10), ('# Magic ATT', 10), ('% Ignore Defense', 0.1)],
                }
            },
        16: {
            'name': 'Superior Gollux Set',
            'effect': {
                2: [('# All Stats', 20), ('# Max HP', 1500), ('# Max MP', 1500)],
                3: [('% Max HP', 0.13), ('% Max MP', 0.13), ('# Weapon ATT', 35), ('# Magic ATT', 35)],
                4: [('% Boss Damage', 0.3), ('% Ignore Defense', 0.3)],
                }
            },
        17: {
            'name': 'Reinforced Gollux Set',
            'effect': {
                2: [('# All Stats', 15), ('# Max HP', 1200), ('# Max MP', 1200)],
                3: [('% Max HP', 0.1), ('% Max MP', 0.1), ('# Weapon ATT', 30), ('# Magic ATT', 30)],
                4: [('% Boss Damage', 0.3), ('% Ignore Defense', 0.15)],
                }
            },
        18: {
            'name': 'Solid Gollux Set',
            'effect': {
                2: [('# All Stats', 12), ('# Max HP', 800), ('# Max MP', 800)],
                3: [('% Max HP', 0.08), ('% Max MP', 0.08), ('# Weapon ATT', 20), ('# Magic ATT', 20)],
                4: [('% Ignore Defense', 0.15), ('# Chance to inflict status when attacking', (0.05, 'Freeze Level 2'))],
                }
            },
        19: {
            'name': 'Cracked Gollux Set',
            'effect': {
                2: [('# All Stats', 10), ('# Max HP', 500), ('# Max MP', 500)],
                3: [('% Max HP', 0.05), ('% Max MP', 0.05), ('# Weapon ATT', 12), ('# Magic ATT', 12)],
                4: [('# Chance to inflict status when attacking', (0.05, 'Freeze Level 2'))],
                }
            },
        20: {
            'name': 'Boss Accessory Set',
            'effect': {
                3: [('# All Stats', 10), ('# Weapon ATT', 5), ('# Magic ATT', 5), ('# Weapon DEF', 60), ('# Magic DEF', 60), ('% Max HP', 0.05), ('% Max MP', 0.05)],
                5: [('# All Stats', 10), ('# Weapon ATT', 5), ('# Magic ATT', 5), ('# Weapon DEF', 60), ('# Magic DEF', 60), ('% Max HP', 0.05), ('% Max MP', 0.05)],
                7: [('# All Stats', 10), ('# Weapon ATT', 10), ('# Magic ATT', 10), ('# Weapon DEF', 80), ('# Magic DEF', 80), ('% Ignore Defense', 0.1)],
                9: [('# All Stats', 15), ('# Weapon ATT', 10), ('# Magic ATT', 10), ('# Weapon DEF', 100), ('# Magic DEF', 100), ('% Boss Damage', 0.1)],
                }
            },
        }

    @staticmethod
    def getShowEffectList(effectLines):
        output = ''
        for line in effectLines:
            if type(line[1]) is not tuple:
                if line[1] >= 0:
                    sign = '+'
                else:
                    sign = '-'
                if line[0][0] == '%':
                    output += line[0][2:] + ': ' + sign + str(int(line[1]*100)) + '%'
                elif type(line[1]) is str:
                    output += line[0][2:] + ': ' + line[1]
                else:
                    output += line[0][2:] + ': ' + sign + str(line[1])
            else:
                if line[0][0] == '%':
                    output += str(int(line[1][0]*100)) + '% ' + line[0][2:] + ': ' + str(int(line[1][1]*100)) + '%'
                elif type(line[1]) is str:
                    output += str(int(line[1][0]*100)) + '% ' + line[0][2:] + ': ' + line[1][1]
                else:
                    output += str(int(line[1][0]*100)) + '% ' + line[0][2:] + ': ' + str(line[1][1])
            output += '\n'
        return output

    @staticmethod
    def showSetEffect(idx):
        output = '\nThis item belongs to: '
        equipSet = EquipSetLib.m_lib[idx]
        name = equipSet['name']
        output += name + '\n\n'
        for num in sorted(equipSet['effect'].keys()):
            output += str(num) + ' Set Effect:\n'
            output += EquipSetLib.getShowEffectList(equipSet['effect'][num])
            output += '\n'
        return output
        
