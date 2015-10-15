from potentiallib import PotentialLib
import random
import rng

rank_label = ['','RARE', 'EPIC', 'UNIQUE', 'LEGENDARY']

class Potential:
    'Potential class'
    potLib = PotentialLib()

    m_rank = 0
    m_type = ''
    m_level = 0
    m_lines = [(),()]

    def __init__(self, parent):
        self.m_rank = 0
        self.m_type = parent.m_type
        self.m_level = parent.m_level
        self.m_lines = []
        if parent.m_pot:
            self.m_rank = parent.m_pot.m_rank
            self.m_lines = [()] * len(parent.m_pot.m_lines)

    def showPot(self):
        output = ''
        if self.m_rank > 0:
            output = '('+ rank_label[self.m_rank] + ')\n'
        for line in self.m_lines:
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
            
    def setRank(self, rank):
        self.m_rank = rank

    def roll(self, numLines = -1):
        if numLines == -1:
            numLines = len(self.m_lines)
        primeChance = 0.02 * numLines
        ranks = []
        for i in range(numLines):
            if i == 0:
                ranks.append(self.m_rank)
            else:
                if ranks[i - 1] == self.m_rank and random.random() < primeChance:
                    ranks.append(self.m_rank)
                else:
                    ranks.append(max(0, self.m_rank - 1))
        self.m_lines = []
        for i in range(numLines):
            line = rng.weighted_choice(Potential.potLib.roll(self, ranks[i]))
            self.m_lines.append(line)
            

    def expand(self):
        self.m_lines.append(rng.weighted_choice(Potential.potLib.roll(self, max(0, self.m_rank - 1))))
        
        
        
