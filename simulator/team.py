import logging
import yaml
import numpy as np

logger = logging.getLogger(__name__)

class Team(object):

    def __init__(self, path_to_config):
        """Initializes team object and runs configurations."""

        self.path_to_config = path_to_config
        self.config()
        self.score = 0

    def config(self):
        """Sets attributes for team object based on configuration file."""
        ##TODO: Need to set this up
        with open(self.path_to_config) as fi:
            self.config = yaml.load(fi, Loader=yaml.FullLoader)

        for k in self.config.keys():
            setattr(self, k, self.config[k])

    def deserialize(self):
        """deserializes the object as a json object"""

        temp = {}
        for k in dir(self):
            if not k.startswith("__"):
                attr = getattr(self, k)
                if 'function' not in str(type(attr)) and 'method' not in str(type(attr)):
                    temp[k] = attr
        return temp

    def get_name(self):

        return self.team_name

    def call_play(self, play):
        """Logic for which type of play to run."""

        if self.decide_punt(play):
            play.play_call = 'punt'
        else:
            if self.decide_pass(play):
                play.play_call = 'pass'
            else:
                play.play_call = 'run'

        return play

    def run_play(self, play):
        """Logic for result of play."""

        if play.play_call == 'punt':
            play = self.punt(play)
        elif play.play_call == 'run':
            play = self.run(play)
        elif play.play_call == 'pass':
            play = self.make_pass(play)
        return play

    def decide_punt(self, play):
        """Make punt decision"""

        punt_it = False
        if play.down == 4:
            ##TODO: Should probably make this depend on field position and distance
            punt_it = bool(np.random.binomial(1, 0.9))
        return punt_it

    def decide_pass(self, play):
        """Make decision to pass or run"""

        ##TODO: Should be based on down and distance...

        pass_play = bool(np.random.binomial(1, self.pass_pct))

        return pass_play

    def punt(self, play):
        """Punts ball"""

        ##TODO: Make distance and time_run_off parameterizable
        play.play_call = 'punt'
        play.distance = np.random.normal(self.punt_stats['yds'], self.punt_stats['sd'])
        play.time_run_off = np.random.poisson(25)

        return play

    def make_pass(self, play):
        """Passes ball"""

        ##TODO: Need to get distance and time_run_off parameterizable
        play.play_call = 'pass'
        play.distance = np.random.normal(self.pass_stats['yds'], self.pass_stats['sd'])
        play.time_run_off = np.random.poisson(20)

        return play

    def run(self, play):
        """Runs ball"""

        ##TODO: Need to get distance as parameter
        ##TODO: Need to get time_run_off as parameter
        play.play_call = 'run'
        play.distance = np.random.normal(self.run_stats['yds'], self.run_stats['sd'])
        play.time_run_off = np.random.poisson(25)

        return play
