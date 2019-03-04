season_settings = {
    # must be even number of players
    'num_players':32,
    'num_games':2000,
    # average ratings for the teams
    'avg_rtg':100,
    # standard deviation of ratings (higher -> more difference in player skill)
    'std_dev': 5,
    # game by game variation amount:
    'game_var':10,
    # after each game, how much does the true rating change?
    # basically a random walk, so we will expect sqrt(num_games) deviation
    # if num_games == 1000, average end of season deviation will be sqrt(1000) * nudge value,
    # so about 8 in the default example
    'rtg_nudge':0.2
}
elo_settings = {
    'init_elo': 1500,
    'K': 0.5,
    'beta':400
}
