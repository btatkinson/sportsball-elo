import numpy as np
import pandas as pd

class Elo(object):
    """docstring for Elo."""
    def __init__(self, elo_1, elo_2, score_1, score_2, k, beta):
        super(Elo, self).__init__()
        self.elo_1 = elo_1
        self.elo_2 = elo_2
        self.score_1 = score_1
        self.score_2 = score_2
        self.k = k
        self.beta = beta
        self.result = self.find_result()
        self.p1_expected = self.expect(elo_1,elo_2)
        self.p2_expected = self.expect(elo_2,elo_1)

    def find_result(self):
        if self.score_1 > self.score_2:
            self.p1_r = 1
            self.p2_r = 0
        elif self.score_2 > self.score_1:
            self.p1_r = 0
            self.p2_r = 1
        else:
            self.p1_r = 0.5
            self.p2_r = 0.5
        return

    def expect(self, elo_1, elo_2):
        diff = float(self.elo_2) - float(self.elo_1)
        f_factor = self.beta
        return 1 / (1 + 10 ** (diff / f_factor))

    def p1_adjust(self):
        return self.elo_1 + (self.k * (self.p1_r - self.p1_expected))

    def p2_adjust(self):
        return self.elo_2 + (self.k * (self.p2_r - self.p2_expected))



# end
