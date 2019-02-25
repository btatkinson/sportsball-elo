# Sportsball Elo

### A season simulator that compares performance of the Elo ratings system to Win-Loss record prediction

##### This post is a compliment to [my medium post](https://medium.com/p/d46ee57c1314/edit)

To simulate a season, simply run `python3 season.py` in the terminal (assuming appropriate libraries are installed).

To adjust parameters, adjust the settings dictionaries in settings.py.

To experiment with different elo ratings, adjust the settings in experiment.py and then run `python3 experiment.py`.

To create more skill disparity between players, increase the 'std_dev' parameter.

To create more game-to-game volatility, increase the 'game_var' parameter.

To create more skill mobility for the players over the course of the season, increase the 'rtg_nudge' parameter.

This is a simple repo and future repos will have more complicated forms of Elo and customization. Stay tuned!




<!-- end -->
