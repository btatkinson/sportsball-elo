import numpy as np
import pandas as pd
import random
import statistics

from player import Player
from settings import *
from elo import Elo
from tqdm import tqdm
# for fake player names
from faker import Faker
fake = Faker()

# array to store players
league = []
# table to track wins/losses
table_array = []

# create league
for p in range(season_settings['num_players']):
    # initialize players
    player_name = fake.name()

    # assign random initial true ratings
    player_rtg = random.gauss(season_settings['avg_rtg'], season_settings['std_dev'])
    player_elo = elo_settings['init_elo']

    nudge = season_settings['rtg_nudge']

    player_entry = [player_name, player_rtg, 0, 0, 0, player_elo]
    table_array.append(player_entry)

    new_player = Player(player_name, player_rtg, player_elo, nudge)
    league.append(new_player)

league_table = pd.DataFrame(table_array, columns=['Name', 'True Rating', 'Wins', 'Losses', 'Ties', 'Elo'])
league_table = league_table.sort_values(by='True Rating', ascending=False)

print(league_table)

def create_matchups(league):
    pairs = []
    random.shuffle(league)
    for x in range(int(len(league)/2)):
        p1 = league.pop()
        p2 = league.pop()
        pair = [p1, p2]
        pairs.append(pair)
    return pairs

def error_calc(epred, wlpred, outcome):
    elo_error = (epred-outcome) ** 2
    wl_error = (wlpred-outcome) ** 2
    return elo_error, wl_error

def play_game(p1, p2, game_var):

    # add random variation
    p1_game_score = int(np.round(random.gauss(p1.rtg,game_var),0))
    p2_game_score = int(np.round(random.gauss(p2.rtg,game_var),0))
    return p1_game_score, p2_game_score

def update_players(p1, p2, p1_score, p2_score):

    p1.played_game()
    p2.played_game()

    p1_elo = p1.elo
    p2_elo = p2.elo

    elo_obj = Elo(p1_elo, p2_elo, p1_score, p2_score, elo_settings['K'], elo_settings['beta'])

    # elo predictions
    p1_elo_pred = elo_obj.p1_expected
    p2_elo_pred = elo_obj.p2_expected

    #win-loss predictions
    p1_wl_pred = (p1.wins + 0.5 * p1.losses)/p1.games_played
    p2_wl_pred = (p2.wins + 0.5 * p2.losses)/p2.games_played

    # adjust player ratings
    p1.elo = elo_obj.p1_adjust()
    p2.elo = elo_obj.p2_adjust()

    if p1_score > p2_score:
        # player 1 wins
        p1.add_win()
        p2.add_loss()
        p1_outcome = 1
    elif p2_score > p1_score:
        # player 2 wins
        p2.add_win()
        p1.add_loss()
        p1_outcome = 0
    else:
        # tie
        p1.add_tie()
        p2.add_tie()
        p1_outcome = 0.5

    # compare outcome to predictions
    p2_outcome = 1 - p1_outcome
    p1_elo_error,p1_wl_error = error_calc(p1_elo_pred, p1_wl_pred, p1_outcome)
    p2_elo_error,p2_wl_error = error_calc(p2_elo_pred, p2_wl_pred, p2_outcome)

    # record errors
    p1.elo_error += p1_elo_error
    p1.wl_error += p1_wl_error
    p2.elo_error += p2_elo_error
    p2.wl_error += p2_wl_error

    # nudge true ratings
    p1.nudge_rating()
    p2.nudge_rating()

    return p1, p2

# look up once so that it doesn't have to look it up each game
game_var = season_settings['game_var']

for i in tqdm(range(season_settings['num_games'])):

    # create random matchups
    matchups = create_matchups(league)

    # reset league
    league = []

    # play games
    for matchup in matchups:
        p1 = matchup[0]
        p2 = matchup[1]
        p1_score, p2_score = play_game(p1, p2, game_var)
        p1, p2 = update_players(p1, p2, p1_score, p2_score)
        league.append(p1)
        league.append(p2)

# end of season table
table_array = []
for player in league:
    name = player.name
    rtg = player.rtg
    wins = player.wins
    losses = player.losses
    ties = player.ties
    gp = player.games_played
    elo = player.elo
    elo_error = player.elo_error
    wl_error = player.wl_error
    entry = [name, rtg, wins, losses, ties, gp, elo, elo_error, wl_error]
    table_array.append(entry)

columns = ['Name', 'True Rating', 'Wins', 'Losses', 'Ties', 'Games Played', 'Elo', 'Elo error', 'WL error']
league_table = pd.DataFrame(table_array, columns=columns)
league_table = league_table.sort_values(by='True Rating', ascending=False)

print(league_table)
total_elo_error = league_table['Elo error'].sum()
total_wl_error = league_table['WL error'].sum()

average_elo_error = np.round(total_elo_error/season_settings['num_games']/season_settings['num_players']/2,3)
average_wl_error = np.round(total_wl_error/season_settings['num_games']/season_settings['num_players']/2,3)
print("The error for your custom Elo system: " + str(average_elo_error))
print("The error for Win-Loss predictions: " + str(average_wl_error))



#end
