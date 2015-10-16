class ScrollLib:
    'Scroll library'

    '''scrolls'''
    m_lib = {
        'Prime Scroll for Weapon': {
            'type': 'Scroll',
            'success rate': 0.4,
            'boom rate': 0.3,
            'effect': 'Prime Scroll for Weapon',
            },
        'Prime Scroll for Armor': {
            'type': 'Scroll',
            'success rate': 0.4,
            'boom rate': 0.3,
            'effect': 'Prime Scroll for Armor',
            },
        '15% str for Weapon': {
            'type': 'Trace',
            'success rate': 0.15,
            'boom rate': 0,
            'effect': '15% str for Weapon'
            },
        }

    '''effects'''
    m_decisive = {
        'Prime Scroll for Weapon': {
            (0, 250): {
                'str': 3,
                'dex': 3,
                'int': 3,
                'luk': 3,
                'watt': 10,
                'matt': 10,
                },
            },
        'Prime Scroll for Armor': {
            (0, 250): {
                'str': 10,
                'dex': 10,
                'int': 10,
                'luk': 10,
                },
            },
        '15% str for Weapon': {
            (150, 250): {
                'str': 4,
                'watt': 9
                },
            },
        }

    m_chaos = {
        'Chaos Scroll' : {
            (0, 250): {
                -5: 0.04,
                -4: 0.09,
                -3: 0.15,
                -2: 0.24,
                -1: 0.34,
                0: 0.66,
                1: 0.76,
                2: 0.85,
                3: 0.91,
                4: 0.96,
                5: 1,
                },
            },
        'Chaos Scroll of Goodness' : {
            (0, 250) : {
                0: 0.32,
                1: 0.52,
                2: 0.7,
                3: 0.82,
                4: 0.92,
                5: 1,
                }
            },
        'Miraculous Chaos Scroll' : {
            (0, 250) : {
                -10: 0.001,
                -9: 0.003,
                -8: 0.008,
                -7: 0.017,
                -6: 0.036,
                -5: 0.073,
                -4: 0.119,
                -3: 0.175,
                -2: 0.259,
                -1: 0.352,
                0: 0.648,
                1: 0.741,
                2: 0.825,
                3: 0.881,
                4: 0.927,
                5: 0.964,
                6: 0.983,
                7: 0.992,
                8: 0.997,
                9: 0.999,
                10: 1,
                }
            },
        'Incredible Chaos Scroll of Goodness' : {
            (0, 250) : {
                0: 0.297,
                1: 0.483,
                2: 0.650,
                3: 0.761,
                4: 0.854,
                5: 0.928,
                6: 0.965,
                7: 0.984,
                8: 0.993,
                9: 0.998,
                10: 1,
                }
            },

        }

    def getScrollStat(self, effect, equip):
        if effect in self.m_decisive.keys():
            options = self.m_decisive[effect]
            for lvlRange, stat in options.items():
                low = lvlRange[0]
                high = lvlRange[1]
                if low <= equip.m_level and high >= equip.m_level:
                    return ('decisive', stat)
        elif effect in self.m_chaos.keys():
            options = self.m_chaos[effect]
            for lvlRange, cdf in options.items():
                low = lvlRange[0]
                high = lvlRange[1]
                if low <= equip.m_level and high >= equip.m_level:
                    return ('chaos', cdf)

        
