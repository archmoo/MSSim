from potentiallib import PotentialLib
import random

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

    def setRank(self, rank):
        self.m_rank = rank

    def roll(self, numLines = -1):
        if numLines == -1:
            numLines = len(self.m_lines)
        primeChance = 0.05
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
            line = random.choice(Potential.potLib.roll(self, ranks[i]))
            self.m_lines.append(line)
            

    def expand(self):
        self.m_lines.append(random.choice(Potential.potLib.roll(self, max(0, self.m_rank - 1))))
        
        
        
