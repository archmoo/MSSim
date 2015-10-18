from joblib import JobLib

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
            'Critical Rate': 0,
            'Minimum Critical Damage': 0,
            'Maximum Critical Damage': 0,
            'Boss Damage': 0,
            'Ignore Enemy Defense': 0,
            'Status Resistance': 0,
            'Speed': 0,
            'Jump': 0,
            }

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

        for equip in equips:
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

        # TODO: set effect
        
        self['Weapon ATT'] = int(self['# watt'] * (1 + self['% watt']))
        self['Magic ATT'] = int(self['# matt'] * (1 + self['% matt']))
        self['STR'] = int((self['# str'] + self['# all stats']) * (1 + self['% str'] + self['% all stats']))
        self['DEX'] = int((self['# dex'] + self['# all stats']) * (1 + self['% dex'] + self['% all stats']))
        self['INT'] = int((self['# int'] + self['# all stats']) * (1 + self['% int'] + self['% all stats']))
        self['LUK'] = int((self['# luk'] + self['# all stats']) * (1 + self['% luk'] + self['% all stats']))
        self['Max HP'] = min(50000000, int(self['# hp'] * (1 + self['% hp'])))
        self['Max MP'] = min(50000000, int(self['# mp'] * (1 + self['% mp'])))
        maxDefense = 9999
        if self.m_job == 'Paladin':
            maxDefense = 19999
        self['Weapon Defense'] = min(maxDefense,
                                     int((self['STR'] * 1.2 + (self['DEX'] + self['LUK']) * 0.5 + self['INT'] * 0.4 + self['# wdef']) * (1 + self['% wdef'])))
        self['Magic Defense'] = min(maxDefense,
                                     int((self['STR'] * 0.4 + (self['DEX'] + self['LUK']) * 0.5 + self['INT'] * 1.2 + self['# mdef']) * (1 + self['% mdef'])))
        maxAccuracy = int(9999 * (1 + jobStats['% accuracy']))
        self['Weapon Accuracy'] = min(maxAccuracy,
                                      int((self['DEX'] * 1.2 + self['LUK'] + self['# accuracy']) * (1 + self['% accuracy'])))
        self['Magic Accuracy'] = min(maxAccuracy,
                                      int((self['INT'] + self['LUK'] * 1.2 + self['# accuracy']) * (1 + self['% accuracy'])))
        self['Weapon Avoidability'] = min(9999,
                                      int((self['DEX'] + self['LUK'] * 2 + self['# avoid']) * (1 + self['% avoid'])))
        self['Magic Avoidability'] = min(9999,
                                      int((self['INT'] + self['LUK'] * 2 + self['# avoid']) * (1 + self['% avoid'])))
        self['Critical Rate'] = self['% Crit Rate']
        self['Minimum Critical Damage'] = min(self['% Min Crit'], self['% Max Crit'])
        self['Maximum Critical Damage'] = max(self['% Min Crit'], self['% Max Crit'])
        self['Boss Damage'] = self['% Boss Damage']
        self['Ignore Enemy Defense'] = self['% Ignore Defense']
        self['Status Resistance'] = self['% Status Resistance']
        self['Speed'] = self['# speed']
        self['Jump'] = self['# jump']

        
        multiplier = JobLib.m_weaponMultiplier[weaponCategory]
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
            statValue = self['Max HP'] / 9 + self['STR'] # TODO: really?

        if jobStats['class'] == 'Magician':
            highRange = int(0.01 * multiplier * statValue * self['Magic ATT'] * (1 + self['% Total Damage']))
        else:
            highRange = int(0.01 * multiplier * statValue * self['Weapon ATT'] * (1 + self['% Total Damage']))
        lowRange = int(highRange * jobStats['% mastery'])
        self['ATT Stats'] = [lowRange, highRange]

    def showCharacterStats(self):
        output = ''
        output += 'Class: ' + self.m_job + ' (' + JobLib.m_job[self.m_job]['class'] + ')\n\n'
        output += 'STR: ' + str(self['STR']) + '\nDEX: ' + str(self['DEX']) + '\nINT: ' + str(self['INT']) + '\nLUK: ' + str(self['LUK']) + '\n\n'
        output += 'ATT Stats: ' + str(self['ATT Stats'][0]) + ' ~ ' + str(self['ATT Stats'][1]) + '\n\n'
        output += 'Critical Chance: ' + str(int(self['Critical Rate']*100)) + '%\n'
        output += 'Minimum Critical: ' + str(int(self['Minimum Critical Damage']*100+100)) + '%\nMaximum Critical: ' + str(int(self['Maximum Critical Damage']*100+100)) + '%\n\n'
        output += 'Boss ATT: ' + str(int(self['Boss Damage']*100)) + '%\nIgnore DEF: ' + str(int(self['Ignore Enemy Defense']*100)) + '%\n'
        output += 'Status Resistance: ' + str(int(self['Status Resistance']*100)) + '%\n\n'
        output += 'Weapon DEF: ' + str(self['Weapon Defense']) + '\n'
        output += 'Magic DEF: ' + str(self['Magic Defense']) + '\n'
        output += 'Weapon ACC: ' + str(self['Weapon Accuracy']) + '\n'
        output += 'Magic ACC: ' + str(self['Magic Accuracy']) + '\n'
        output += 'Weapon Avoid: ' + str(self['Weapon Avoidability']) + '\n'
        output += 'Magic Avoid: ' + str(self['Magic Avoidability']) + '\n\n'
        output += 'Speed: ' + str(self['Speed']) + '%\nJump: ' + str(self['Jump']) + '%\n'
        return output
        
        
if __name__ == '__main__':

    a = Character('Bow Master')
    a.updateStats([])
    print a.showCharacterStats()
        
            
            
            