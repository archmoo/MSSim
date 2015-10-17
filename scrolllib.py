class ScrollLib:
    'Scroll library'

    '''scrolls'''
    m_lib = {
        'Prime Scroll for Weapon': {
            'type': 'Scroll',
            'success rate': 0.4,
            'boom rate': 0.3,
            'effect': 'Prime Scroll for Weapon',
            'description': 'Improves Weapon ATT and Magic ATT for weapons.\n',
            },
        'Prime Scroll for Armor': {
            'type': 'Scroll',
            'success rate': 0.4,
            'boom rate': 0.3,
            'effect': 'Prime Scroll for Armor',
            'description': 'Improves armor stats.\n'
            },
        'Chaos Scroll 60%': {
            'type' : 'Scroll',
            'success rate': 0.6,
            'boom rate': 0,
            'effect': 'Chaos Scroll',
            'description': 'Reconfigures equipment stats.\n'
            },
        'Chaos Scroll of Goodness 30%': {
            'type' : 'Scroll',
            'success rate': 0.3,
            'boom rate': 0,
            'effect': 'Chaos Scroll of Goodness',
            'description': 'Reconfigures equipment stats. Equipment stats will not decrease.\n'
            },
        'Incredible Chaos Scroll of Goodness 50%': {
            'type' : 'Scroll',
            'success rate': 0.5,
            'boom rate': 0,
            'effect': 'Incredible Chaos Scroll of Goodness',
            'description': 'Reconfigures equipment stats. Equipment stats will not decrease. Offers more improvement than Chaos Scroll of Goodness.\n'
            },
        'Miraculous Chaos Scroll 60%': {
            'type' : 'Scroll',
            'success rate': 0.6,
            'boom rate': 0,
            'effect': 'Miraculous Chaos Scroll',
            'description': 'Reconfigures equipment stats. Offers options better or worse than Chaos Scroll.\n'
            },
        
        'STR for Weapon 15%': {
            'type': 'Trace',
            'success rate': 0.15,
            'boom rate': 0,
            'effect': 'STR for Weapon',
            'description': 'Improves Weapon ATT and STR for weapons.\n'
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
        'STR for Weapon': {
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
    @staticmethod
    def showScrollStat(name):
        keyDisp = {
            'str':'STR',
            'dex':'DEX',
            'int':'INT',
            'luk':'LUK',
            'watt':'Weapon ATT',
            'matt':'Magic ATT',
            'hp':'MaxHP',
            'mp':'MaxHP',
            'accuracy':'Accuracy',
            'avoid':'Avoidability',
            }
        def sortFunc(key):
            return {
                'str':0,
                'dex':1,
                'int':2,
                'luk':3,
                'watt':4,
                'matt':5,
                'hp':6,
                'mp':7,
                'accuracy':8,
                'avoid':9
                }[key]
        
        effect = ScrollLib.m_lib[name]['effect']
        description = ScrollLib.m_lib[name]['description']
        description += 'Success Rate: ' + str(int(100*ScrollLib.m_lib[name]['success rate'])) + '%\n'
        if ScrollLib.m_lib[name]['boom rate'] != 0:
            description += 'If it fails, the item has a ' + str(int(ScrollLib.m_lib[name]['boom rate']*100)) + '% chance of it being destroyed.\n'
        if effect in ScrollLib.m_decisive.keys():
            options = ScrollLib.m_decisive[effect]
            for lvlRange, stat in options.items():
                low = lvlRange[0]
                high = lvlRange[1]
                if not (low == 0 and high == 250):
                    description += '\nFor equipment level from ' + str(low) + ' to ' + str(high) + ' :\n'
                else:
                    description += '\n'
                for key, value in sorted(stat.items(),key=lambda t: sortFunc(t[0])):
                    description += keyDisp[key] + ': +' + str(value) + '\n'
        return description
                        
                    
        
        

        
