class UpgradeLib:
    m_linklib = {
        'Demon Avenger': {
            1: {
                'effect': [('% Total Damage', 0.05)],
                'AP cost': 500,
                },
            2: {
                'effect': [('% Total Damage', 0.1)],
                'AP cost': 1000,
                },
            3: {
                'effect': [('% Total Damage', 0.15)],
                'AP cost': 5000,
                },
            },
        'Kanna': {
            1: {
                'effect': [('% Total Damage', 0.05)],
                'AP cost': 500,
                },
            2: {
                'effect': [('% Total Damage', 0.1)],
                'AP cost': 1000,
                },
            },
        'Demon Slayer': {
            1: {
                'effect': [('% Boss Damage', 0.1)],
                'AP cost': 500,
                },
            2: {
                'effect': [('% Boss Damage', 0.15)],
                'AP cost': 1000,
                },
            3: {
                'effect': [('% Boss Damage', 0.2)],
                'AP cost': 5000,
                },
            },
        'Luminous': {
            1: {
                'effect': [('% Ignore Defense', 0.1)],
                'AP cost': 500,
                },
            2: {
                'effect': [('% Ignore Defense', 0.15)],
                'AP cost': 1000,
                },
            3: {
                'effect': [('% Ignore Defense', 0.2)],
                'AP cost': 5000,
                },
            },
        'Xenon': {
            1: {
                'effect': [('% All Stats', 0.05)],
                'AP cost': 500,
                },
            2: {
                'effect': [('% All Stats', 0.1)],
                'AP cost': 1000,
                },
            },
        'Phantom': {
            1: {
                'effect': [('% Crit Rate', 0.1)],
                'AP cost': 500,
                },
            2: {
                'effect': [('% Crit Rate', 0.15)],
                'AP cost': 1000,
                },
            3: {
                'effect': [('% Crit Rate', 0.2)],
                'AP cost': 5000,
                },
            },
        'Zero': {
            1: {
                'effect': [('% Ignore Defense', 0.02), ('% Chance to ignore monster damage', (1, 0.03))],
                'AP cost': 1000,
                },
            2: {
                'effect': [('% Ignore Defense', 0.04), ('% Chance to ignore monster damage', (1, 0.06))],
                'AP cost': 1500,
                },
            3: {
                'effect': [('% Ignore Defense', 0.06), ('% Chance to ignore monster damage', (1, 0.09))],
                'AP cost': 2000,
                },
            4: {
                'effect': [('% Ignore Defense', 0.08), ('% Chance to ignore monster damage', (1, 0.12))],
                'AP cost': 2500,
                },
            5: {
                'effect': [('% Ignore Defense', 0.1), ('% Chance to ignore monster damage', (1, 0.15))],
                'AP cost': 3000,
                },
            },
        'Kaiser': {
            1: {
                'effect': [('% Max HP', 0.1)],
                'AP cost': 500,
                },
            2: {
                'effect': [('% Max HP', 0.15)],
                'AP cost': 1000,
                },
            3: {
                'effect': [('% Max HP', 0.2)],
                'AP cost': 5000,
                },
            },
        'Beast Tamer': {
            1: {
                'effect': [('% Boss Damage', 0.04), ('% Crit Rate', 0.04), ('% Max HP', 0.03), ('% Max MP', 0.03)],
                'AP cost': 500,
                },
            2: {
                'effect': [('% Boss Damage', 0.07), ('% Crit Rate', 0.07), ('% Max HP', 0.04), ('% Max MP', 0.04)],
                'AP cost': 1000,
                },
            3: {
                'effect': [('% Boss Damage', 0.1), ('% Crit Rate', 0.1), ('% Max HP', 0.05), ('% Max MP', 0.05)],
                'AP cost': 5000,
                },
            },
        'Hayato': {
            1: {
                'effect': [('# All Stats', 10), ('# Weapon ATT', 5)],
                'AP cost': 500,
                },
            },
        'Cannoneer': {
            1: {
                'effect': [('# All Stats', 15), ('% Max HP', 0.05), ('% Max MP', 0.05)],
                'AP cost': 500,
                },
            2: {
                'effect': [('# All Stats', 25), ('% Max HP', 0.1), ('% Max MP', 0.1)],
                'AP cost': 1000,
                },
            3: {
                'effect': [('# All Stats', 35), ('% Max HP', 0.15), ('% Max MP', 0.15)],
                'AP cost': 5000,
                },
            },
        'Cygnus Knights': {
            1: {
                'effect': [('% Abnormal Status Resistance', 0.02)],
                'AP cost': 500,
                },
            2: {
                'effect': [('% Abnormal Status Resistance', 0.05)],
                'AP cost': 1000,
                },
            3: {
                'effect': [('% Abnormal Status Resistance', 0.07)],
                'AP cost': 500,
                },
            4: {
                'effect': [('% Abnormal Status Resistance', 0.10)],
                'AP cost': 1000,
                },
            5: {
                'effect': [('% Abnormal Status Resistance', 0.12)],
                'AP cost': 500,
                },
            6: {
                'effect': [('% Abnormal Status Resistance', 0.15)],
                'AP cost': 1000,
                },
            7: {
                'effect': [('% Abnormal Status Resistance', 0.17)],
                'AP cost': 500,
                },
            8: {
                'effect': [('% Abnormal Status Resistance', 0.20)],
                'AP cost': 1000,
                },
            9: {
                'effect': [('% Abnormal Status Resistance', 0.22)],
                'AP cost': 500,
                },
            10: {
                'effect': [('% Abnormal Status Resistance', 0.25)],
                'AP cost': 1000,
                },
            },
        }
    m_codexlib = {
        'Leafre': {
            'effect': [('% Ignore Defense', 0.3), ('# Skill Level Increase', 1)],
            'AP cost': 300,
            },
        'Henesys Ruins': {
            'effect': [('% Weapon ATT', 0.03), ('% Magic ATT', 0.03)],
            'AP cost': 300,
            },
        }
    m_traitslib = {
        # exp(k): to reach level k, the minimum EXP.
        'Diligence': {
            'effect': ['Scroll success rate (excluding special scrolls)'],
            'table': [[0, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05,
                      0.055, 0.06, 0.065, 0.07, 0.075, 0.08, 0.085, 0.09, 0.095, 0.1]],
            },
        'Ambition': {
            'effect': ['Ignore Enemy Defense'],
            'table': [[0, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05,
                      0.055, 0.06, 0.065, 0.07, 0.075, 0.08, 0.085, 0.09, 0.095, 0.1]],
            },
        'Empathy': {
            'effect': ['Max MP'],
            'table': [[0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000,
                       1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000]],
            },
        'Insight': {
            'effect': ['Accuracy', 'Avoid'],
            'table': [[0, 10, 15, 25, 40, 60, 85, 115, 150, 190, 235,
                       285, 340, 400, 465, 535, 610, 690, 775, 865, 960],
                      [0, 10, 15, 25, 40, 60, 85, 115, 150, 190, 235,
                       285, 340, 400, 465, 535, 610, 690, 775, 865, 960]],
            },
        'Willpower': {
            'effect': ['Max HP', 'Weapon DEF', 'Magic DEF', 'Abnormal Status Resistance'],
            'table': [[0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000,
                       1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000],
                      [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50,
                       55, 60, 65, 70, 75, 80, 85, 90, 95, 100],
                      [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50,
                       55, 60, 65, 70, 75, 80, 85, 90, 95, 100],
                      [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1,
                       0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2]],
            },
        }

    m_lib = {
        'Link Skill': m_linklib,
        'Crusader Codex': m_codexlib,
        'Traits': m_traitslib,
        }

    m_traitsEXP = [0,20,46,80,124,181,255,351,476,639,851,1084,1340,1622,1932,2273,2648,3061,3515,4014,4563,5128,5710,6309,6945,7581,8236,8911,9506,10222,10959,11707,12477,13259,14053,14859,15677,16507,17349,18204,19072,19953,20847,21754,22675,23610,24559,25522,26499,27491,28498,29520,30557,31610,32679,33764,34865,35983,37118,38270,39439,40626,41831,43054,44295,45555,46834,48132,49449,50786,52127,53472,54821,56174,57531,58892,60257,61626,62999,64376,65757,67142,68531,69924,71321,72722,74127,75536,76949,78366,79787,81212,82641,84074,85511,86952,88397,89846,91299,92756,93596, 93596]

if __name__ == '__main__':
    print len(UpgradeLib.m_traitslib['EXP'])
