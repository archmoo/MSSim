class UpgradeLib:
    m_linklib = {
        'Demon Avenger': {
            1: {
                'effect': [('% Total Damage', 0.05)],
                'AP cost': 100,
                },
            2: {
                'effect': [('% Total Damage', 0.1)],
                'AP cost': 500,
                },
            3: {'effect': [('% Total Damage', 0.15)],
                'AP cost': 2500,
                },
            },
##        'Kanna': -1,
##        'Demon Slayer': -1,
##        'Luminous': -1,
##        'Xenon': -1,
##        'Phantom': -1,
##        'Zero': -1,
##        'Kaiser': -1,
##        'Beast Tamer': -1,
##        'Hayato': -1,
##        'Cannoneer': -1,
##        'Cygnus Knight': -1,
        }
    m_codexlib = {
        'Leafre': {
            'effect': [('% Ignore Defense', 0.3), ('# Skill Level Increase', 1)],
            'AP cost': 50,
            },
        }
    m_traitslib = {
        # exp(k): to reach level k, the minimum EXP.
        'Diligence': {
            'effect': ['Scroll success rate (excluding special scrolls)'],
            'table': [[0, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05,
                      0.055, 0.06, 0.065, 0.07, 0.075, 0.08, 0.085, 0.09, 0.095, 0.01]],
            },
##        'Diligence': (5, 0.01),
##        'Insight':
##        'Empathy': (0, 0),
##        'Charm': (0, 0),
##        'Ambition': (0, 0),
##        'Willpower': (0, 0),
        }

    m_lib = {
        'Link Skill': m_linklib,
        'Crusader Codex': m_codexlib,
        'Traits': m_traitslib,
        }

    m_traitsEXP = [0,20,46,80,124,181,255,351,476,639,851,1084,1340,1622,1932,2273,2648,3061,3515,4014,4563,5128,5710,6309,6945,7581,8236,8911,9506,10222,10959,11707,12477,13259,14053,14859,15677,16507,17349,18204,19072,19953,20847,21754,22675,23610,24559,25522,26499,27491,28498,29520,30557,31610,32679,33764,34865,35983,37118,38270,39439,40626,41831,43054,44295,45555,46834,48132,49449,50786,52127,53472,54821,56174,57531,58892,60257,61626,62999,64376,65757,67142,68531,69924,71321,72722,74127,75536,76949,78366,79787,81212,82641,84074,85511,86952,88397,89846,91299,92756,93596, 0]

if __name__ == '__main__':
    print len(UpgradeLib.m_traitslib['EXP'])
