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
        'Diligence': {None},
##        'Diligence': (5, 0.01),
##        'Insight':
##        'Empathy': (0, 0),
##        'Charm': (0, 0),
##        'Ambition': (0, 0),
##        'Willpower': (0, 0),
        }

    m_lib = {
        'Link Skill': m_linklib,
        'Codex': m_codexlib,
        'Traits': m_traitslib,
        }
