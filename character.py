from lib.joblib import JobLib
from lib.equipsetlib import EquipSetLib
from lib.bosslib import BossLib
from lib.farminglib import FarmingLib

class Character:

    def __init__(self, job='dummy'):
        self.m_job = job
        self.m_interStat = {
            '# str': 0, '% str': 0,
            '# dex': 0, '% dex': 0,
            '# int': 0, '% int': 0,
            '# luk': 0, '% luk': 0,
            '# watt': 0, '% watt': 0,
            '# matt': 0, '% matt': 0,
            '# wdef': 0, '% wdef': 0,
            '# mdef': 0, '% mdef': 0,
            '# accuracy': 0, '% accuracy': 0,
            '# avoid': 0, '% avoid': 0,
            '# hp': 0, '% hp': 0,
            '# mp': 0, '% mp': 0,
            '# all stats': 0, '% all stats': 0,
            '# speed': 0, '# max speed': 140, '# jump': 0,
            '% Boss Damage': 0,
            '% Ignore Defense': 0,
            '% Total Damage': 0,
            '% Crit Rate': 0,
            '% Min Crit': 0,
            '% Max Crit': 0,
            '% Status Resistance': 0,
            '# Skill Delay': 1,
            }
        self.m_stat = {
            'STR': 0,
            'DEX': 0,
            'INT': 0,
            'LUK': 0,
            'Max HP': 0,
            'Max MP': 0,
            'Weapon ATT': 0,
            'Magic ATT': 0,
            'Weapon Defense': 0,
            'Magic Defense': 0,
            'Weapon Accuracy': 0,
            'Magic Accuracy': 0,
            'Weapon Avoidability': 0,
            'Magic Avoidability': 0,
            'ATT Stats': [0, 0],
            'ATT Stats Reinforce': [0, 0],
            'Critical Rate': 0,
            'Minimum Critical Damage': 0,
            'Maximum Critical Damage': 0,
            'Boss Damage': 0,
            'Total Damage': 0,
            'Final Damage': 0,
            'Ignore Enemy Defense': 0,
            'Ignore Enemy Resistance': 0,
            'Status Resistance': 0,
            'Speed': 0,
            'Jump': 0,
            'DPS': [90, 100],
            }
        self.oneTimeAcquire = {
            'Crusader Codex': {
                'chosen': 'None',
                'Leafre': (0, 0),
                'Henesys Ruins': (0, 0),
                },
            'Link Skill': {                               
                'Demon Avenger': (0, 0),
                'Kanna': (0, 0),
                'Demon Slayer': (0, 0),
                'Luminous': (0, 0),
                'Xenon': (0, 0),
                'Phantom': (0, 0),
                'Zero': (0, 0),
                'Kaiser': (0, 0),
                'Beast Tamer': (0, 0),
                'Hayato': (0, 0),
                'Cannoneer': (0, 0),
                'Cygnus Knights': (0, 0),
                },
            'Traits': {
                'Diligence': (0, 0, 0),
                'Insight': (0, 0, 0),
                'Empathy': (0, 0, 0),
                'Ambition': (0, 0, 0),
                'Willpower': (0, 0, 0),
                },
            
            }
        self.bossCounter = {}
        self.farmCounter = {}
        self.actionPoint = 500
        for boss in BossLib.m_counter.keys():
            self.bossCounter[boss] = [0, 0]
        for farmOption in FarmingLib.m_lib.keys():
            self.farmCounter[farmOption] = 0
        
        self.equipSet = {}
            

    def __getitem__(self, key):
        if key[0] == '%' or key[0] == '#':
            return self.m_interStat[key]
        else:
            return self.m_stat[key]

    def __setitem__(self, key, value):
        if key[0] == '%' or key[0] == '#':
            self.m_interStat[key] = value
        else:
            self.m_stat[key] = value

    def setJob(self, job):
        self.m_job = job
        
    def updateStats(self, equips):
        jobStats = JobLib.m_job[self.m_job]
        weaponCategory = 'None'
        for key in jobStats.keys():
            if key in self.m_interStat.keys():
               self[key] = jobStats[key]

        self.equipSet = {}

        for equip in equips:

            if equip.m_setId:
                if equip.m_setId in self.equipSet.keys():
                    self.equipSet[equip.m_setId] += 1
                else:
                    self.equipSet[equip.m_setId] = 1
            
            self['# str'] += equip['str']
            self['# dex'] += equip['dex']
            self['# int'] += equip['int']
            self['# luk'] += equip['luk']
            self['# hp'] += equip['hp']
            self['# mp'] += equip['mp']
            self['# watt'] += equip['watt']
            self['# matt'] += equip['matt']
            self['# wdef'] += equip['wdef']
            self['# mdef'] += equip['mdef']
            self['# accuracy'] += equip['accuracy']
            self['# avoid'] += equip['avoid']
            self['% Boss Damage'] += equip['boss']
            self['% Ignore Defense'] = self['% Ignore Defense'] + (1 - self['% Ignore Defense']) * equip['pdr']
            # TODO: speed, jump

            if equip.m_type == 'Weapon':
                weaponCategory = equip.m_category
            
            pots = equip.m_pot.m_lines

            for pot in pots:
                stat, val = pot

                mapping = {
                    '% STR': '% str',
                    '% DEX': '% dex',
                    '% INT': '% int',
                    '% LUK': '% luk',
                    '% All Stats': '% all stats',
                    '% Avoid': '% avoid',
                    '% Accuracy': '% accuracy',
                    '% Max HP': '% hp',
                    '% Max MP': '% mp',
                    '% Weapon DEF': '% wdef',
                    '% Magic DEF': '% mdef',
                    '% Min Crit Damage': '% Min Crit',
                    '% Max Crit Damage': '% Max Crit',
                    '% Abnormal Status Resistance': '% Status Resistance',
                    '% Boss Damage': '% Boss Damage',
                    '% Weapon ATT': '% watt',
                    '% Magic ATT': '% matt',
                    '% Total Damage': '% Total Damage',
                    '% Crit Rate': '% Crit Rate',
                    '# STR': '# str',
                    '# DEX': '# dex',
                    '# INT': '# int',
                    '# LUK': '# luk',
                    '# All Stats': '# all stats',
                    '# Avoid': '# avoid',
                    '# Accuracy': '# accuracy',
                    '# Max HP': '# hp',
                    '# Max MP': '# mp',
                    '# Weapon ATT': '# watt',
                    '# Magic ATT': '# matt',
                    '# Weapon DEF': '# wdef',
                    '# Magic DEF': '# mdef',
                    '# Speed': '# speed',
                    '# Jump': '# jump',
                    }
                if stat in mapping.keys():
                    self[mapping[stat]] += val
                elif stat == '% Ignore Defense':
                    self['% Ignore Defense'] = self['% Ignore Defense'] + (1 - self['% Ignore Defense']) * val
                elif stat == '# Weapon ATT per 10 levels':
                    self['# watt'] += 21
                elif stat == '# Magic ATT per 10 levels':
                    self['# matt'] += 21
                else:
                    pass # TODO: decent skills, drop rate

        #set effect
        for key, value in self.equipSet.items():
            equipSet = EquipSetLib.m_lib[key]
##            print equipSet['name'], value
            effect = equipSet['effect']
            for num, pots in effect.items():
                if num <= value:
                    for pot in pots:
                        stat, val = pot

                        mapping = {
                            '% STR': '% str',
                            '% DEX': '% dex',
                            '% INT': '% int',
                            '% LUK': '% luk',
                            '% All Stats': '% all stats',
                            '% Avoid': '% avoid',
                            '% Accuracy': '% accuracy',
                            '% Max HP': '% hp',
                            '% Max MP': '% mp',
                            '% Weapon DEF': '% wdef',
                            '% Magic DEF': '% mdef',
                            '% Min Crit Damage': '% Min Crit',
                            '% Max Crit Damage': '% Max Crit',
                            '% Abnormal Status Resistance': '% Status Resistance',
                            '% Boss Damage': '% Boss Damage',
                            '% Weapon ATT': '% watt',
                            '% Magic ATT': '% matt',
                            '% Total Damage': '% Total Damage',
                            '% Crit Rate': '% Crit Rate',
                            '# STR': '# str',
                            '# DEX': '# dex',
                            '# INT': '# int',
                            '# LUK': '# luk',
                            '# All Stats': '# all stats',
                            '# Avoid': '# avoid',
                            '# Accuracy': '# accuracy',
                            '# Max HP': '# hp',
                            '# Max MP': '# mp',
                            '# Weapon ATT': '# watt',
                            '# Magic ATT': '# matt',
                            '# Weapon DEF': '# wdef',
                            '# Magic DEF': '# mdef',
                            '# Speed': '# speed',
                            '# Jump': '# jump',
                            }
                        if stat in mapping.keys():
                            self[mapping[stat]] += val
                        elif stat == '% Ignore Defense':
                            self['% Ignore Defense'] = self['% Ignore Defense'] + (1 - self['% Ignore Defense']) * val
                        elif stat == '# Weapon ATT per 10 levels':
                            self['# watt'] += 21
                        elif stat == '# Magic ATT per 10 levels':
                            self['# matt'] += 21
                        else:
                            pass # TODO: decent skills, drop rate

        self['Weapon ATT'] = int(round(self['# watt'] * (1 + self['% watt'])))
        self['Magic ATT'] = int(round(self['# matt'] * (1 + self['% matt'])))
        self['STR'] = int(round((self['# str'] + self['# all stats']) * (1 + self['% str'] + self['% all stats'])))
        self['DEX'] = int(round((self['# dex'] + self['# all stats']) * (1 + self['% dex'] + self['% all stats'])))
        self['INT'] = int(round((self['# int'] + self['# all stats']) * (1 + self['% int'] + self['% all stats'])))
        self['LUK'] = int(round((self['# luk'] + self['# all stats']) * (1 + self['% luk'] + self['% all stats'])))
        self['Max HP'] = min(500000, int(round(self['# hp'] * (1 + self['% hp']))))
        self['Max MP'] = min(500000, int(round(self['# mp'] * (1 + self['% mp']))))
        maxDefense = 9999
        if self.m_job == 'Paladin':
            maxDefense = 19999
        self['Weapon Defense'] = min(maxDefense,
                                     int(round((self['STR'] * 1.2 + (self['DEX'] + self['LUK']) * 0.5 + self['INT'] * 0.4 + self['# wdef']) * (1 + self['% wdef']))))
        self['Magic Defense'] = min(maxDefense,
                                     int(round((self['STR'] * 0.4 + (self['DEX'] + self['LUK']) * 0.5 + self['INT'] * 1.2 + self['# mdef']) * (1 + self['% mdef']))))
        maxAccuracy = int(round(9999 * (1 + jobStats['% accuracy'])))
        self['Weapon Accuracy'] = min(maxAccuracy,
                                      int(round((self['DEX'] * 1.2 + self['LUK'] + self['# accuracy']) * (1 + self['% accuracy']))))
        self['Magic Accuracy'] = min(maxAccuracy,
                                      int(round((self['INT'] + self['LUK'] * 1.2 + self['# accuracy']) * (1 + self['% accuracy']))))
        self['Weapon Avoidability'] = min(9999,
                                      int(round((self['DEX'] + self['LUK'] * 2 + self['# avoid']) * (1 + self['% avoid']))))
        self['Magic Avoidability'] = min(9999,
                                      int(round((self['INT'] + self['LUK'] * 2 + self['# avoid']) * (1 + self['% avoid']))))
        self['Critical Rate'] = min(1, self['% Crit Rate'] + jobStats['% Hyper Critical'])
        self['Minimum Critical Damage'] = min(self['% Min Crit'], self['% Max Crit'])
        self['Maximum Critical Damage'] = max(self['% Min Crit'], self['% Max Crit'])
        self['Boss Damage'] = self['% Boss Damage'] + jobStats['% Hyper Boss Rush']
        self['Total Damage'] = self['% Total Damage'] + jobStats['% Hyper Reinforce']
        self['Final Damage'] = jobStats['% Final Damage']
        self['Ignore Enemy Defense'] = self['% Ignore Defense'] + (1 - self['% Ignore Defense']) * jobStats['% Hyper Guard Break']
        self['Ignore Enemy Resistance'] = jobStats['% Ignore Resistance']
        self['Status Resistance'] = self['% Status Resistance']
        self['Speed'] = min(self['# speed']+100, jobStats['# max speed'])
        self['Jump'] = min(self['# jump']+100, 123)

        
        multiplier = JobLib.m_weaponMultiplier[weaponCategory]
        if weaponCategory in ['Wand', 'Staff']:
            if jobStats['category'] == 0: # Explorer
                multiplier = 1.2
            else:
                multiplier = 1
        statValue = 0
        if jobStats['class'] == 'Magician':
            statValue = self['INT'] * 4 + self['LUK']
        elif jobStats['class'] == 'Bowman':
            statValue = self['DEX'] * 4 + self['STR']
        elif jobStats['class'] == 'Thief':
            statValue = self['LUK'] * 4 + self['DEX'] + self['STR']
        elif jobStats['class'] == 'Warrior' and self.m_job != 'Demon Avenger':
            statValue = self['STR'] * 4 + self['DEX']
        elif jobStats['class'] == 'Pirate':
            if self.m_job in ['Corsair', 'Angelic Buster', 'Jett', 'Mechanic']:
                statValue = self['DEX'] * 4 + self['STR']
            elif self.m_job in ['Cannoneer', 'Buccaneer',  'Thunder Breaker', 'Shade']:
                statValue = self['STR'] * 4 + self['DEX']
        elif self.m_job == 'Xenon':
            statValue = 3.5 * (self['STR'] + self['DEX'] + self['LUK'])
        elif self.m_job == 'Demon Avenger':
            statValue = self['Max HP'] / 9 + self['STR']
        if jobStats['% Hyper Reinforce'] == 0:
            if jobStats['class'] == 'Magician':
                highRange = int(round(0.01 * multiplier * statValue * self['Magic ATT'] * (1 + self['% Total Damage']) * (1 + jobStats['% Final Damage'])))
            else:
                highRange = int(round(0.01 * multiplier * statValue * self['Weapon ATT'] * (1 + self['% Total Damage']) * (1 + jobStats['% Final Damage'])))
            lowRange = int(round(highRange * jobStats['% mastery']))
            self['ATT Stats'] = [lowRange, highRange]
        else:
            if jobStats['class'] == 'Magician':
                highRange = int(round(0.01 * multiplier * statValue * self['Magic ATT'] * (1 + self['% Total Damage']) * (1 + jobStats['% Final Damage'])))
            else:
                highRange = int(round(0.01 * multiplier * statValue * self['Weapon ATT'] * (1 + self['% Total Damage']) * (1 + jobStats['% Final Damage'])))
            lowRange = int(round(highRange * jobStats['% mastery']))
            self['ATT Stats'] = [lowRange, highRange]
            if jobStats['class'] == 'Magician':
                highRange = int(round(0.01 * multiplier * statValue * self['Magic ATT'] * (1 + self['% Total Damage'] + jobStats['% Hyper Reinforce']) * (1 + jobStats['% Final Damage'])))
            else:
                highRange = int(round(0.01 * multiplier * statValue * self['Weapon ATT'] * (1 + self['% Total Damage'] + jobStats['% Hyper Reinforce']) * (1 + jobStats['% Final Damage'])))
            lowRange = int(round(highRange * jobStats['% mastery']))
            self['ATT Stats Reinforce'] = [lowRange, highRange]
##        print self['ATT Stats'],
        
        if jobStats['class'] == 'Magician':
            highRange = 0.01 * multiplier * statValue * self['Magic ATT']
        else:
            highRange = 0.01 * multiplier * statValue * self['Weapon ATT']

#### Code for calculating class modifiers
##        highRange = 0.01 * multiplier * 60000
##        if jobStats['class'] == 'Magician':
##            highRange *= 1000 * (1 + self['% matt'] + 0.6)
##        else:
##            highRange *= 1000 * (1 + self['% watt'] + 0.6)
##        highRange *= (self['Minimum Critical Damage'] + self['Maximum Critical Damage'])/ 2 + 1
##        highRange *= (1 + self['Boss Damage'] + 2.3 + self['Total Damage'] + 0.3)
##        highRange *= (1 + self['Final Damage'])
##        highRange *= (1 - 0.5*(1-self['Ignore Enemy Resistance']))
##        highRange = int(round(highRange))
        lowRange = highRange * jobStats['% mastery']
        modifier = JobLib.m_classModifier[self.m_job]
        lowRange *= modifier
        highRange *= modifier
        self['DPS'] = [lowRange, highRange]
#### Code for calculating DPS on each boss with certain stats
##        classMulti = multiplier
##        statValue = [4 * 5000, 4 * 10000, 4 * 15000, 4 * 20000, 4 * 25000]
##        baseAtt = [700, 900, 1100, 1300, 1500]
##        percAtt = [0.1, 0.3, 0.5, 0.7, 0.9]
##        bossDmg = [1.1, 1.4, 1.8, 2.2, 2.6]
##        totDmg = [0.15, 0.15, 0.2, 0.2, 0.25]
##        pdr = 0.93
##        crit = 1
##        
##        for i in range(5):
##            if jobStats['class'] == 'Magician':
##                att = baseAtt[i] * (1 + percAtt[i] + self['% matt'])
##            else:
##                att = baseAtt[i] * (1 + percAtt[i] + self['% watt'])
##            highRange = 0.01 * classMulti * statValue[i] * att * modifier
##
##            for boss, info in BossLib.m_lib.items():
##                if boss == 'Chaos Zakum':
##                    multiplier = 1
##                    multiplier *= (1 + 1 * (self['Minimum Critical Damage'] + self['Maximum Critical Damage']) / 2)
##                    multiplier *= (1 + self['Boss Damage'] + bossDmg[i] + self['Total Damage'] + totDmg[i]) * (1 + self['Final Damage'])
##                    multiplier *= max(0, (1-info['defense']*(1-pdr)))
##                    multiplier *= max(0, (1-info['resistance']*(1-self['Ignore Enemy Resistance'])))
##                    highdps = highRange * multiplier
##                    lowdps = highdps * jobStats['% mastery']
##                    print str('%.1f' % ((lowdps+highdps)/2)) + ',',

#### Code for calculating current equip
##        for boss, info in BossLib.m_lib.items():
##            if boss == 'Easy Magnus':
##                multiplier = 1
##                multiplier *= (1 + self['Critical Rate'] * (self['Minimum Critical Damage'] + self['Maximum Critical Damage']) / 2)
##                multiplier *= (1 + self['Boss Damage'] + self['Total Damage']) * (1 + self['Final Damage'])
##                multiplier *= max(0, (1-info['defense']*(1-self['Ignore Enemy Defense'])))
##                multiplier *= max(0, (1-info['resistance']*(1-self['Ignore Enemy Resistance'])))
##                highdps = self['DPS'][1] * multiplier
##                lowdps = int(round(self['DPS'][0] * multiplier))
##                highdps = int(round(highdps))
##                print str('%.1f %.1f' % (lowdps, highdps)) + ',',

        

    def showCharacterStats(self):
        jobStats = JobLib.m_job[self.m_job]
        output = ''
        output += 'Job: ' + self.m_job + ' (' + JobLib.m_job[self.m_job]['class'] + ')\nLevel: 210\n\n'
        output += 'STR: ' + str(self['STR']) + '\nDEX: ' + str(self['DEX']) + '\nINT: ' + str(self['INT']) + '\nLUK: ' + str(self['LUK']) + '\n\n'
        
        output += 'ATT Stats:\n' + str(self['ATT Stats'][0]) + ' ~ ' + str(self['ATT Stats'][1])
        if jobStats['% Hyper Reinforce'] != 0:
            output += ' (' + str(self['ATT Stats Reinforce'][0]) + ' ~ ' + str(self['ATT Stats Reinforce'][1]) + ')'
        output += '\n\n'
        if jobStats['% Hyper Critical'] != 0:
            output += 'Critical Chance: ' + str(int(self['% Crit Rate']*100)) + '% (' + str(int(self['Critical Rate']*100)) + '%)\n'
        else:
            output += 'Critical Chance: ' + str(int(self['Critical Rate']*100)) + '%\n'

        output += 'Minimum Critical: ' + str(int(self['Minimum Critical Damage']*100+100)) + '%\nMaximum Critical: ' + str(int(self['Maximum Critical Damage']*100+100)) + '%\n\n'

        if jobStats['% Hyper Boss Rush'] != 0:
            output += 'Boss ATT: ' + str(int(self['% Boss Damage']*100)) + '% (' + str(int(self['Boss Damage']*100)) + '%)\n'
        else:
            output += 'Boss ATT: ' + str(int(self['Boss Damage']*100)) + '%\n'
        if jobStats['% Hyper Guard Break'] != 0:
            output += 'Ignore DEF: ' + str(int(round(self['% Ignore Defense']*100))) + '% (' + str(int(round(self['Ignore Enemy Defense']*100))) + '%)\n'
        else:
            output += 'Ignore DEF: ' + str(int(round(self['Ignore Enemy Defense']*100))) + '%\n'

        output += 'Ignore Elemental Resistance: ' + str(int(100*jobStats['% Ignore Resistance'])) + '%\n'        
        output += 'Status Resistance: ' + str(int(self['Status Resistance']*100)) + '%\n\n'
        output += 'Weapon DEF: ' + str(self['Weapon Defense']) + '\n'
        output += 'Magic DEF: ' + str(self['Magic Defense']) + '\n'
        output += 'Weapon ACC: ' + str(self['Weapon Accuracy']) + '\n'
        output += 'Magic ACC: ' + str(self['Magic Accuracy']) + '\n'
        output += 'Weapon Avoid: ' + str(self['Weapon Avoidability']) + '\n'
        output += 'Magic Avoid: ' + str(self['Magic Avoidability']) + '\n\n'
        output += 'Speed: ' + str(self['Speed']) + '%\nJump: ' + str(self['Jump']) + '%\n\n'
        output += '--------\nWhen in combat, characters may gain additional stats due to certain skills. Final stats are shown in parentheses. Some temporary boosts are not included in calculation.'
        if 'Hyper related' in jobStats.keys():
            output += '\n\nRelative skills:\n\n'
            for skill in sorted(jobStats['Hyper related']):
                output += skill + '\n'
        return output
        
        
if __name__ == '__main__':

    a = Character('Bow Master')
    a.updateStats([])
    print a.showCharacterStats()
        
            
            
            
