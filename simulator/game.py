import logging
import numpy

from simulator.play import Play

logger = logging.getLogger(__name__)

class Game(object):

    def __init__(self, home, visitor):
        logger.info("Initializing a game!")
        self.time = 15*60
        self.quarter = 1
        self.offense = None ## This will be an index to self.teams
        self.defense = None ## This will be an index to self.teams
        self.teams = [home, visitor]
        self.down = None
        self.distance = None
        self.distance_to_td = None
        self.game_is_over = False
        self.plays = []

    def first_down(self):
        """Sets down and distance"""

        logger.info("First down!")
        self.down = 1
        self.distance = 10

    def increment_play(self, distance):
        """Updates down and distance"""

        logger.info("Updating down and distance with distance = %s", distance)

        self.distance_to_td -= distance
        self.distance -= distance
        if self.distance <= 0:
            self.first_down()
        else:
            self.down += 1

        logger.info("New down = %s and distance = %s", self.down, self.distance)

    def increment_clock(self, time_runoff):
        """Updates game clock."""

        self.time -= time_runoff
        if self.time <= 0:
            logger.info("Time expired for quarter %s", self.quarter)
            if self.quarter < 4 or self.teams[self.offense].score == self.teams[self.defense].score:
                self.quarter += 1
            else:
                self.end_game()

    def end_game(self):
        """Cleans up game and saves data."""

        self.game_is_over = True
        logger.info("Game over!")

    def coin_toss(self):
        """Randomly selects a team with even odds."""

        self.offense = numpy.random.randint(0, 2)
        if self.offense == 0:
            self.defense = 1
        else:
            self.defense = 0
        logger.info("%s wins coin toss", self.teams[self.offense].get_name())

    def run_play(self):
        """Logic for running a play. Returns play object."""

        logger.info("Running play!")
        play = Play(self)
        play = self.teams[self.offense].call_play(play)
        play = self.teams[self.offense].run_play(play)
        
        if play.turnover or play.play_call == 'punt':
            if self.offense == 0:
                self.offense = 1
                self.defense = 0
            else:
                self.offense = 0
                self.defense = 1
            self.first_down()
            self.distance_to_td = 100 - self.distance_to_td
        else:
            self.increment_play(play.distance)
            if self.distance_to_td <= 0:
                logger.info("TOUCHDOWN")
                self.teams[self.offense].score += 7
                if self.offense == 0:
                    self.offense = 1
                    self.defense = 0
                else:
                    self.offense = 0
                    self.defense = 1
                self.distance_to_td = 80
            elif self.distance_to_td >= 100:
                logger.info("SAFETY")
                self.teams[self.defense].score += 2
                self.distance_to_td = 80

        self.increment_clock(play.time_run_off)

        return play

    def play_game(self):
        """Logic for playing a game."""

        logger.info("Starting game!")
        self.coin_toss()

        self.first_down()
        self.distance_to_td = 80
        while not self.game_is_over:
            self.plays.append(self.run_play())

        results = [x.deserialize() for x in self.plays]
        end_data = {'home_team': self.teams[0].deserialize(), 'away_team': self.teams[1].deserialize(), 'results': results}
        return end_data
