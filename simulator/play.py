import logging
import inspect

logger = logging.getLogger(__name__)

class Play(object):

    def __init__(self, game):

        self.offense_name = game.teams[game.offense].get_name()
        self.defense_name = game.teams[game.defense].get_name()
        self.down = game.down
        self.distance = game.distance
        self.time_in_quarter = game.time
        self.quarter = game.quarter
        self.play_call = None
        self.distance = None
        self.distance_to_td = game.distance_to_td
        self.turnover = None
        self.time_run_off = 0

    def deserialize(self):
        """deserializes the object as a json object"""

        temp = {}
        for k in dir(self):
            if not k.startswith("__"):
                attr = getattr(self, k)
                if 'function' not in str(type(attr)) and 'method' not in str(type(attr)):
                    temp[k] = attr
        return temp
