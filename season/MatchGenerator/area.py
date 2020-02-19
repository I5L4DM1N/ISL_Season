import random
# import os 
# dir_path = os.path.dirname(os.path.realpath(__file__))
# folder = os.path.basename(dir_path)

# if folder == 'MatchGenerator':
#     from status import *
# else:
#     from season.MatchGenerator.status import *


#from status import *
from season.MatchGenerator.status import *

class Area():
    list_of_areas = []

    def __init__(self,name):
        self.name = name
        Area.list_of_areas.append(self)

    def __str__(self):
        return "{}".format(self.name)


    @classmethod
    def current_area(cls):
        current_area = random.choice(cls.list_of_areas)
        return current_area


A1 = Area("A1")
A2 = Area("A2")
A3 = Area("A3")
B1 = Area("B1")
B2 = Area("B2")
B3 = Area("B3")
C1 = Area("C1")
C2 = Area("C2")
C3 = Area("C3")
