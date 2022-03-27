import logging
from simulator.team import Team
from simulator.game import Game

logging.basicConfig(level=logging.WARNING)

home_win = []
for i in range(0, 1000):

    home_team = Team('instance/config/home_team.yaml')
    away_team = Team('instance/config/away_team.yaml')

    game = Game(home_team, away_team)
    results = game.play_game()

    print(
        "Score: %s: %s, %s:%s" % (
            results['home_team']['team_name'],
            results['home_team']['score'],
            results['away_team']['team_name'],
            results['away_team']['score']
            )
        )
    if results['home_team']['score'] > results['away_team']['score']:
        home_win.append(True)
    else:
        home_win.append(False)

print("Home win likelihood: %s" % (sum(home_win)/len(home_win),))