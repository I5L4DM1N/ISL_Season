# import os 
# dir_path = os.path.dirname(os.path.realpath(__file__))
# folder = os.path.basename(dir_path)

# if folder == 'MatchGenerator':
#     from general import *
# else:
#     from season.MatchGenerator.general import *


#from general import *
from season.MatchGenerator.general import *



class Position():
    all_positions = []

    def __init__(self,name, offensive_factor):
        self.name = name
        self.offensive_factor = offensive_factor
        self.defensive_factor = 1 - self.offensive_factor
        Position.all_positions.append(self)

    def __str__(self):
        return "{}".format(self.name)

    def tactics_factors(self,tactics):
        if tactics == "balanced":
            self.offensive_factor = self.offensive_factor
            self.defensive_factor = 1 - self.offensive_factor
        elif tactics == "push_up":
            self.offensive_factor = self.offensive_factor + 0.1
            self.defensive_factor = 1 - self.offensive_factor
        elif tactics == "drop_back":
            self.offensive_factor = self.offensive_factor - 0.1
            self.defensive_factor = 1 - self.offensive_factor

    def attack(self):
        self.offensive_factor = self.offensive_factor + 0.1
        self.defensive_factor = 1 - self.offensive_factor

    def defense(self):
        self.offensive_factor = self.offensive_factor - 0.1
        self.defensive_factor = 1 - self.offensive_factor

    def area_influence(self,home_away,area):
        if area == A1:
            if home_away =="home":
                if self.name =="GK":
                    return 0.2
                if self.name =="LM":
                    return 0.3
                if self.name =="RM":
                    return 0.2
                if self.name =="ST":
                    return 0.3
            if home_away =="away":
                if self.name =="GK":
                    return 0.3
                if self.name =="LM":
                    return 0.2
                if self.name =="RM":
                    return 0.3
                if self.name =="ST":
                    return 0.2
        if area == A2:
            if home_away =="home":
                if self.name =="GK":
                    return 0.23
                if self.name =="LM":
                    return 0.32
                if self.name =="RM":
                    return 0.23
                if self.name =="ST":
                    return 0.23
            if home_away =="away":
                if self.name =="GK":
                    return 0.23
                if self.name =="LM":
                    return 0.23
                if self.name =="RM":
                    return 0.32
                if self.name =="ST":
                    return 0.23
        if area == A3:
            if home_away =="home":
                if self.name =="GK":
                    return 0.3
                if self.name =="LM":
                    return 0.3
                if self.name =="RM":
                    return 0.2
                if self.name =="ST":
                    return 0.2
            if home_away =="away":
                if self.name =="GK":
                    return 0.2
                if self.name =="LM":
                    return 0.2
                if self.name =="RM":
                    return 0.3
                if self.name =="ST":
                    return 0.3
        if area == B1:
            if home_away =="home":
                if self.name =="GK":
                    return 0.23
                if self.name =="LM":
                    return 0.23
                if self.name =="RM":
                    return 0.23
                if self.name =="ST":
                    return 0.32
            if home_away =="away":
                if self.name =="GK":
                    return 0.32
                if self.name =="LM":
                    return 0.23
                if self.name =="RM":
                    return 0.23
                if self.name =="ST":
                    return 0.23
        if area == B2:
            if home_away =="home":
                if self.name =="GK":
                    return 0.25
                if self.name =="LM":
                    return 0.25
                if self.name =="RM":
                    return 0.25
                if self.name =="ST":
                    return 0.25
            if home_away =="away":
                if self.name =="GK":
                    return 0.25
                if self.name =="LM":
                    return 0.25
                if self.name =="RM":
                    return 0.25
                if self.name =="ST":
                    return 0.25
        if area == B3:
            if home_away =="home":
                if self.name =="GK":
                    return 0.32
                if self.name =="LM":
                    return 0.23
                if self.name =="RM":
                    return 0.23
                if self.name =="ST":
                    return 0.23
            if home_away =="away":
                if self.name =="GK":
                    return 0.23
                if self.name =="LM":
                    return 0.23
                if self.name =="RM":
                    return 0.23
                if self.name =="ST":
                    return 0.32
        if area == C1:
            if home_away =="home":
                if self.name =="GK":
                    return 0.2
                if self.name =="LM":
                    return 0.2
                if self.name =="RM":
                    return 0.3
                if self.name =="ST":
                    return 0.3
            if home_away =="away":
                if self.name =="GK":
                    return 0.3
                if self.name =="LM":
                    return 0.3
                if self.name =="RM":
                    return 0.2
                if self.name =="ST":
                    return 0.2
        if area == C2:
            if home_away =="home":
                if self.name =="GK":
                    return 0.23
                if self.name =="LM":
                    return 0.23
                if self.name =="RM":
                    return 0.32
                if self.name =="ST":
                    return 0.23
            if home_away =="away":
                if self.name =="GK":
                    return 0.23
                if self.name =="LM":
                    return 0.32
                if self.name =="RM":
                    return 0.23
                if self.name =="ST":
                    return 0.23
        if area == C3:
            if home_away =="home":
                if self.name =="GK":
                    return 0.3
                if self.name =="LM":
                    return 0.2
                if self.name =="RM":
                    return 0.3
                if self.name =="ST":
                    return 0.2
            if home_away =="away":
                if self.name =="GK":
                    return 0.2
                if self.name =="LM":
                    return 0.3
                if self.name =="RM":
                    return 0.2
                if self.name =="ST":
                    return 0.3

    @classmethod
    def reset(cls):
        for position in cls.all_positions:
            if position == GK:
                position.offensive_factor = 0.4
            if position == LM:
                position.offensive_factor = 0.5
            if position == RM:
                position.offensive_factor = 0.5
            if position == ST:
                position.offensive_factor = 0.6   
            position.defensive_factor = 1 - position.offensive_factor

GK = Position("GK",0.4)
LM = Position("LM",0.5)
RM = Position("RM",0.5)
ST = Position("ST",0.6)

#print (GK.area_influence("home",A1))

 