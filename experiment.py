import numpy as np
import pandas as pd
import random

experiment_settings = {
    'team_1_elo':1970,
    'team_2_elo':991,
    'team_1_true_skill':110,
    'team_2_true_skill':92,
    'game_var':7.5
}

def exp_play_game(p1, p2, game_var):

    # add random variation
    p1_game_score = int(np.round(random.gauss(p1,game_var),0))
    p2_game_score = int(np.round(random.gauss(p2,game_var),0))
    return p1_game_score, p2_game_score

def expect(elo_1, elo_2):
    diff = float(elo_2) - float(elo_1)
    f_factor = 2 * 400
    return 1 / (1 + 10 ** (diff / f_factor))

print("Team 1 is expected to win " + str(np.round(expect(experiment_settings['team_1_elo'],experiment_settings['team_2_elo']),3)*100) + " pct of their games")
num_tries = 1000
game_log = []
for x in range(num_tries):
    p1, p2 = exp_play_game(experiment_settings['team_1_true_skill'],experiment_settings['team_2_true_skill'],experiment_settings['game_var'])
    if p1 > p2:
        game_log.append(1)
    elif p2 > p1:
        game_log.append(0)
    else:
        game_log.append(0.5)
print("Team 1 actually won " + str(np.round(np.sum(game_log)/(num_tries),3)*100) + " pct of their games")
