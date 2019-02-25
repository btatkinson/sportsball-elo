import numpy as np
import pandas as pd
import random


class Player(object):
    """Player Object"""
    def __init__(self, name, rtg, elo, nudge):
        super(Player, self).__init__()
        self.name = name

        # true rating
        self.rtg = rtg

        # elo rating
        self.elo = elo

        # wins, losses, ties
        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.games_played = 0

        # how much to nudge ratings
        self.nudge = nudge

        # error trackers
        self.elo_error = 0
        self.wl_error = 0

    def nudge_rating(self):
        # decide to nudge up or down
        direction = random.randint(0,1)
        if direction == 0:
            self.rtg += self.nudge
        else:
            self.rtg -= self.nudge

    def add_win(self):
        self.wins += 1

    def add_loss(self):
        self.losses += 1

    def add_tie(self):
        self.ties += 1

    def played_game(self):
        self.games_played += 1

















#end
