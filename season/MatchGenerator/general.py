# import os 
# dir_path = os.path.dirname(os.path.realpath(__file__))
# folder = os.path.basename(dir_path)

# if folder == 'MatchGenerator':
#     from area import *
# else:
#     from season.MatchGenerator.area import *

#from area import *
from season.MatchGenerator.area import *


class General ():

    def __init__(self, match_ID, tournament, day, TypeOfGame):
        #match specific configurations
        self.match_ID = match_ID
        self.tournament = tournament
        self.day = day
        self.TypeOfGame = TypeOfGame

        #general configuration
        self.max_performance_factor = 1.1
        self.min_adjustment = 0.5
        self.max_adjustment = 1.5
        self.margin_to_score = 0.3
        self.current_round = 0
        self.home_attack_area = None
        self.away_attack_area = None

    # def re_set():
    #     general.max_performance_factor = 1.1
    #     general.min_adjustment = 0.5
    #     general.max_adjustment = 1.5
    #     general.margin_to_score = 0.3
    #     general.current_round = 0

 
#general = General()

# general.max_performance_factor = 1.1
# general.min_adjustment = 0.5
# general.max_adjustment = 1.5
# general.margin_to_score = 0.3
# general.current_round = 0


#print(general.margin_to_score)
