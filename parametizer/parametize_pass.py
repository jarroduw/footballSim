## Script reads in a csv file containing per-game statistics for passing
##  and calculates average and sd for passing stats

import numpy as np
import pandas as pd

team_of_interest = "sea"

passing = pd.read_csv("instance/stats/pass_stats.csv")
passing_of_interest = passing[passing['team']==team_of_interest]

mean_pass_play = sum(passing_of_interest['yds']) / sum(passing_of_interest['att'])
sd_pass_play = (passing_of_interest['yds'].std()*len(passing_of_interest['yds']))/sum(passing_of_interest['att'])

pass_stats = {
    "yds": mean_pass_play,
    "sd": sd_pass_play
}

print(pass_stats)