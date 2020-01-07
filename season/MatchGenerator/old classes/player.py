#from season.MatchGenerator.position import *
from position import *


import random

class Player():
    no_of_players = 0
    list_of_players = []
    max_performance_home_attack = 0
    max_performance_away_attack = 0
    rating_max = 5.99
    rating_min = 1.00

    def __init__(self):
        pass 

    def Attributes(self,Player_name, Nation, Team, Home_Away, Position, Division_Rank, \
                 Ability, Offensive_Ability, Defensive_Ability, Routine,  \
                 Routine_Rank, Fitness, GK_pos_experience, LM_pos_experience, \
                 RM_pos_experience, ST_pos_experience, Personal_chemistry, Personal_motivation,player_id):
        self.player_name = Player_name
        self.player_id = player_id
        self.nation = Nation
        self.team = Team
        self.home_away = Home_Away
        self.position = Position
        self.current_position = None
        self.division_rank = Division_Rank
        self.ability = Ability
        self.offensive_ability = Offensive_Ability * 100
        self.defensive_ability = Defensive_Ability * 100
        self.routine = Routine
        self.routine_rank = Routine_Rank
        self.fitness = Fitness
        self.GK_pos_experience = GK_pos_experience
        self.LM_pos_experience = LM_pos_experience
        self.RM_pos_experience = RM_pos_experience
        self.ST_pos_experience = ST_pos_experience
        self.personal_chemistry = Personal_chemistry
        self.personal_motivation = Personal_motivation
        self.original_motivation = Personal_motivation 
        self.adjusted_personal_motivation = 0
        self.motivation = 1 # team_motivation + personal_motivation /2
        self.attack_ability = 0
        self.defend_ability = 0

        if self.position =="GK":
            self.ability = (self.offensive_ability * 0.4) + (self.defensive_ability * 0.6)
        elif self.position == "LM":
            self.ability = (self.offensive_ability * 0.5) + (self.defensive_ability * 0.5)
        elif self.position == "RM":
            self.ability = (self.offensive_ability * 0.5) + (self.defensive_ability * 0.5)
        elif self.position == "ST":
            self.ability = (self.offensive_ability * 0.6) + (self.defensive_ability * 0.4)


        ##Temporary attributes
        self.att_pos_off_factor = 0
        self.att_pos_def_factor = 0
        self.def_pos_off_factor = 0
        self.def_pos_def_factor = 0
        self.current_pos_exp = 0
        self.team_tactics = None
        self.attack_intensity = 0
        self.defence_intensity = 0
        self.routine_bonus = 0
        self.nervosity = 0
        self.team_motivation = 1 #fixa så at motivation uppdateras från laget
        self.team_motivation_change = 0
        self.adjusted_personal_motivation_change = 0
        self.max_attack_performance = 0
        self.max_defence_performance = 0
        self.attack_area_influence = 0
        self.defence_area_influence = 0
        self.sent_off_off_abi_change = 0
        self.sent_off_def_abi_change = 0
        self.attack_ability_change_performance = 0
        self.defence_ability_change_performance = 0
        self.attack_ability_change_effect = 0
        self.defence_ability_change_effect = 0
        

        self.temp_ability = 0
        self.offensive_value = 0
        self.defensive_value = 0
        self.offensive_performance = 0
        self.defensive_performance = 0
        self.motivation_adjusted_off_performance = 0
        self.motivation_adjusted_def_performance = 0
        self.fitness_change = 0
        self.total_fitness_change = 0
        self.personal_motivation_change = 0
        self.motivation_change = 0
        self.total_motivation_change = 0
        self.sent_off = False
        self.on_pitch = False
        self.on_bench = False
        self.off_perf_abi_change = 0 #ablity change based on performance
        self.total_off_change = 0
        self.def_perf_abi_change = 0 #ablity change based on performance
        self.total_def_change = 0
        self.goal_off_abi_change = 0
        self.save_def_abi_change = 0
        self.offensive_rating = 0
        self.defensive_rating = 0
        self.match_rating = 5  #aggregated rating for the whole game
        self.sub_in = False

        #stats
        self.goals_scored = 0
        self.saves_made = 0

        #class updates
        Player.no_of_players += 1
        Player.list_of_players.append(self)

    def __str__(self):
        return "{}".format("Player: ",self.player_name)

    def calculate_off_ability(self):
        #Ability calculation
        #print(self.home_away, "-", self.player_name)
        Position = self.current_position
        #print("position off, def factor",Position.offensive_factor, Position.defensive_factor)
        Position.attack()
        #print("position off, def factor",Position.offensive_factor, Position.defensive_factor)
        #print("off abi, def abi", self.offensive_ability, self.defensive_ability)
        self.attack_ability = (self.offensive_ability * Position.offensive_factor) + (self.defensive_ability * Position.defensive_factor)
        #print ("self.attack_ability",self.attack_ability)





        if Position == GK:
            Positional_experience = self.GK_pos_experience
        elif Position == LM:
            Positional_experience = self.LM_pos_experience
        elif Position == RM:
            Positional_experience = self.RM_pos_experience
        elif Position == ST:
            Positional_experience = self.ST_pos_experience
        #print ("Positional_experience",Positional_experience)
        #print ("self.personal_chemistry",self.personal_chemistry)
        #print ("self.fitness",self.fitness)
        self.attack_ability = self.attack_ability * Positional_experience * self.personal_chemistry * self.fitness
        #print ("self.attack_ability",self.attack_ability)
        #print("\n")

        #adding these attributes for logging purpostes
        self.att_pos_off_factor = Position.offensive_factor
        self.att_pos_def_factor = Position.defensive_factor
        self.current_pos_exp = Positional_experience


    def attack(self,intensity):

        #Performance calculation
        self.adjusted_personal_motivation = self.personal_motivation + self.routine_bonus + self.nervosity
        self.motivation = (self.adjusted_personal_motivation + self.team_motivation) /2   
        
        max_performance = 0
        if self.home_away == "home":
            max_performance = Player.max_performance_home_attack

        elif self.home_away == "away":
            max_performance = Player.max_performance_away_attack

        if max_performance == 0:
            max_performance = 1

        self.max_attack_performance = max_performance
        self.offensive_performance = random.randint(1,max_performance)
        #print("offensive performance",self.offensive_performance)

        #performance vs ability
        #-->performance ska UNDERstiga ability för att lyckas<--#
        self.motivation_adjusted_off_performance = self.offensive_performance + ((1-self.motivation)*(1-intensity)*self.offensive_performance)
        #print("motivation",self.motivation)
        #print("motivation adjusted performance",self.motivation_adjusted_off_performance)
        Position = self.current_position
        if self.home_away == "home":
            Area_influence = Position.area_influence(self.home_away,general.home_attack_area)
        elif self.home_away == "away":
            Area_influence = Position.area_influence(self.home_away,general.away_attack_area)
        
        self.attack_area_influence = Area_influence
        #temp_full_off_val =  self.offensive_value = self.attack_ability - self.motivation_adjusted_off_performance
        #print("full off value",temp_full_off_val)
        self.offensive_value = (self.attack_ability - self.motivation_adjusted_off_performance) * Area_influence
        #print("offensive_value",self.offensive_value)

    def attack_rating(self):
        max_performance = 0
        if self.home_away == "home":
            max_performance = Player.max_performance_home_attack
        elif self.home_away == "away":
            max_performance = Player.max_performance_away_attack

        if max_performance == 0:
            max_performance = 1

        if self.offensive_value > 0 :
            bonus = random.randint (1,5)/10
            self.match_rating += 0.2
        else:
            bonus = 0
            self.match_rating -= 0.2

        # temp = self.motivation_adjusted_off_performance/max_performance
        # temp2 = 1+(5*(1-self.motivation_adjusted_off_performance/max_performance))
        #print(self.player_name,"match rating",self.match_rating)
        
        self.offensive_rating = min(max(1+(5*(1-self.motivation_adjusted_off_performance/max_performance)) + bonus,Player.rating_min),Player.rating_max)
        #match_rating_change = (self.offensive_rating - Player.match_rate_hurdle)/10
        #self.match_rating += match_rating_change
        
        #print(self.player_name,"off rating",self.offensive_rating," match rating",self.match_rating, "max perfomance", max_performance, "change", match_rating_change )
        # print("motivation_adjusted_off_performance",round(self.motivation_adjusted_off_performance,2))
        # print("perf/max", round(temp,2),"before bonus", round(temp2,2))
        # print("bonus", round(bonus,2))
        # print("offensive rating", round(self.offensive_rating,2))
        # print("\n")


    def increase_decrease_attack(self):
        #performance skall ÖVERstiga abilty för att höja
        self.attack_ability_change_performance = random.randint(1,600)
        #print("increase performance",increase_performance)
        self.attack_ability_change_effect = self.attack_ability_change_performance - self.offensive_ability
        #print("increase effect", incr_decr_effect)
        if self.attack_ability_change_effect > 0 and self.offensive_value > 0:
            self.off_perf_abi_change = random.randint(1,5)/100
            self.offensive_ability = self.offensive_ability + (self.off_perf_abi_change * 100)
            #print("increase/decrease", increase_decrease)
            self.total_off_change = self.total_off_change + (self.off_perf_abi_change * 100)

        elif self.attack_ability_change_effect < 0 and self.offensive_value < 0:
            self.off_perf_abi_change = (0 - random.randint(1,5))/100
            self.offensive_ability = self.offensive_ability + (self.off_perf_abi_change * 100)
            #print("increase/decrease", increase_decrease)
            self.total_off_change = self.total_off_change + (self.off_perf_abi_change * 100)

        else:
            self.off_perf_abi_change = 0


    def calculate_def_ability(self):       
        #Ability calculation
        #print(self.home_away, "-", self.player_name)
        Position = self.current_position
        #print("position off, def factor",Position.offensive_factor, Position.defensive_factor)
        Position.defense() 
        #print("position off, def factor",Position.offensive_factor, Position.defensive_factor)
        #print("off abi, def abi", self.offensive_ability, self.defensive_ability)
        self.defend_ability = (self.offensive_ability * Position.offensive_factor) + (self.defensive_ability * Position.defensive_factor)
        #print ("self.defend_ability",self.attack_ability)

        if Position == GK:
            Positional_experience = self.GK_pos_experience
        elif Position == LM:
            Positional_experience = self.LM_pos_experience
        elif Position == RM:
            Positional_experience = self.RM_pos_experience
        elif Position == ST:
            Positional_experience = self.ST_pos_experience
        #print ("Positional_experience",Positional_experience)
        #print ("self.personal_chemistry",self.personal_chemistry)
        #print ("self.fitness",self.fitness)
        self.defend_ability = self.defend_ability * Positional_experience * self.personal_chemistry * self.fitness
        #print ("self.defend_ability",self.defend_ability)
        #print("\n")

        #adding these attributes for logging purpostes
        self.def_pos_off_factor = Position.offensive_factor
        self.def_pos_def_factor = Position.defensive_factor


        
    def defense(self,intensity):
        #Performance calculationdf
        self.adjusted_personal_motivation = self.personal_motivation + self.routine_bonus + self.nervosity
        self.motivation = (self.adjusted_personal_motivation + self.team_motivation) /2   
        
        max_performance = 0
        if self.home_away == "away":
            max_performance = Player.max_performance_home_attack
        elif self.home_away == "home":
            max_performance = Player.max_performance_away_attack

        if max_performance == 0:
            max_performance = 1
        
        self.max_defence_performance = max_performance  
        #-->performance ska UNDERstiga ability för att lyckas<--#    
        self.defensive_performance = random.randint(1,max_performance)
        #print("defensive performance",self.defensive_performance)
        self.motivation_adjusted_def_performance = self.defensive_performance + ((1-self.motivation)*(1-intensity)*self.defensive_performance)
        #print("motivation",self.motivation)
        #print("motivation adjusted performance",self.motivation_adjusted_def_performance)
        Position = self.current_position
        if self.home_away == "home":
            Area_influence = Position.area_influence(self.home_away,general.away_attack_area)
        elif self.home_away == "away":
            Area_influence = Position.area_influence(self.home_away,general.home_attack_area)
        
        self.defence_area_influence = Area_influence

        self.defensive_value = (self.defend_ability - self.motivation_adjusted_def_performance) * Area_influence

        #print("fitness",self.fitness)
        #print("defensive value",self.defensive_value)

    def defense_rating(self):
        max_performance = 0
        if self.home_away == "away":
            max_performance = Player.max_performance_home_attack
        elif self.home_away == "home":
            max_performance = Player.max_performance_away_attack
        
        if max_performance == 0:
            max_performance = 1

        if self.defensive_value > 0 :
            bonus = random.randint (1,5)/10
            self.match_rating += 0.2
        else:
            bonus = 0
            self.match_rating -= 0.2

        # temp = self.motivation_adjusted_def_performance/max_performance
        # temp2 = 1+(5*(1-self.motivation_adjusted_def_performance/max_performance))

        self.defensive_rating = min(max(1+(5*(1-self.motivation_adjusted_def_performance/max_performance)) + bonus,Player.rating_min),Player.rating_max)
        
        #self.match_rating += (self.defensive_rating - Player.match_rate_hurdle)/10
        #print(self.player_name,"max performance",max_performance)
        #print("motivation_adjusted_off_performance",round(self.motivation_adjusted_def_performance,2))
        #print("perf/max", round(temp,2),"before bonus", round(temp2,2))
        #print("bonus", round(bonus,2))
        #print("offensive rating", round(self.defensive_rating,2))
        #print("\n")
    
        
    def increase_decrease_defense(self):
        #performance skall ÖVERstiga abilty för att höja
        self.defence_ability_change_performance = random.randint(1,600)
        #print("increase performance",increase_performance)
        self.defence_ability_change_effect = self.defence_ability_change_performance - self.defensive_ability
        #print("increase effect", incr_deself.defence_ability_change_performancecr_effect)
        if self.defence_ability_change_effect > 0 and self.defensive_value > 0:
            self.def_perf_abi_change = random.randint(1,5)/ 100
            self.defensive_ability = self.defensive_ability + (self.def_perf_abi_change *100)
            #print("increase/decrease", increase_decrease)
            self.total_def_change = self.total_def_change + (self.def_perf_abi_change *100)
        elif self.defence_ability_change_effect < 0 and self.defensive_value < 0:
            self.def_perf_abi_change = (0 - random.randint(1,5))/ 100
            self.defensive_ability = self.defensive_ability + (self.def_perf_abi_change *100)
            #print("increase/decrease", increase_decrease)
            self.total_def_change = self.total_def_change + (self.def_perf_abi_change *100)
        else:
            self.def_perf_abi_change = 0

    def goal_off_ability_change(self):
        self.goal_off_abi_change = random.randint(1,3)/100
        self.total_off_change = self.total_off_change + (self.goal_off_abi_change * 100)
        self.offensive_ability = self.offensive_ability + (self.goal_off_abi_change * 100)

    def save_def_ability_change(self):
        self.save_def_abi_change = random.randint(1,3)/100
        self.total_def_change = self.total_def_change + (self.save_def_abi_change * 100)
        self.defensive_ability = self.defensive_ability + (self.save_def_abi_change * 100)

    def sent_off_attack_ability_change(self):
        self.sent_off_off_abi_change = -5/100
        self.total_off_change = self.total_off_change + (self.sent_off_off_abi_change * 100)
        self.offensive_ability = self.offensive_ability + (self.sent_off_off_abi_change * 100)

    def sent_off_defend_ability_change(self):
        self.sent_off_def_abi_change = -5/100
        self.total_def_change = self.total_def_change + (self.sent_off_def_abi_change * 100)
        self.defensive_ability = self.defensive_ability + (self.sent_off_def_abi_change * 100)

    def fitness_update(self,intensity):
        self.fitness_change = (random.normalvariate(4,0.9)/100) * intensity #random via tabell, avvikelser upp till -50 inkl 0 effekt
        self.fitness = max(self.fitness - self.fitness_change,0)

        #updates acumulated fitness change
        self.total_fitness_change = self.total_fitness_change + self.fitness_change

    def motivation_update(self,team_motivation):
        self.team_motivation = team_motivation

        if self.defensive_value > 0:
            self.personal_motivation_change += 0.01
        if self.offensive_value > 0:
            self.personal_motivation_change += 0.01
        if self.defensive_value < 0:
            self.personal_motivation_change += -0.01
        if self.offensive_value < 0:
            self.personal_motivation_change += -0.01

        #updating acumulated motivation change
        self.total_motivation_change = self.total_motivation_change + self.personal_motivation

        #update personal motivation
        self.personal_motivation = self.personal_motivation + self.personal_motivation_change

        #update general motivation (team and personal motivation combined)
        self.motivation = (self.personal_motivation + self.team_motivation)/2

    def special_event(self):
        if self.sent_off == True:
            self.sent_off = False
        else:
            sent_off_value = random.randint(1,25)
            if sent_off_value == 25:
               self.sent_off = True
               self.match_rating -= -0.6
            else:
                self.sent_off = False

    def reset_values(self):
        self.personal_motivation_change = 0 
        self.goal_off_abi_change = 0
        self.save_def_abi_change = 0
        self.sent_off_off_abi_change = 0
        self.sent_off_def_abi_change = 0
            
    @classmethod
    def calculate_max_performance_home_attack(cls):
        cls.max_performance_home_attack = 0
        for player in cls.list_of_players:
            if player.on_pitch == True:
                if player.home_away == "home":
                    if player.attack_ability > cls.max_performance_home_attack:
                        cls.max_performance_home_attack = int(player.attack_ability)
                elif player.home_away == "away":
                    if player.defend_ability > cls.max_performance_home_attack:
                        cls.max_performance_home_attack = int(player.defend_ability)
        cls.max_performance_home_attack = int(cls.max_performance_home_attack * general.max_performance_factor)
                        
    @classmethod
    def calculate_max_performance_away_attack(cls):
        cls.max_performance_away_attack = 0
        for player in cls.list_of_players:
            if player.on_pitch == True:
                if player.home_away == "away":
                    if player.attack_ability > cls.max_performance_away_attack:
                        cls.max_performance_away_attack = int(player.attack_ability)
                elif player.home_away == "home":
                    if player.defend_ability > cls.max_performance_away_attack: 
                        cls.max_performance_away_attack = int(player.defend_ability)
        #print(cls.max_performance_away_attack, "before factor")                
        cls.max_performance_away_attack = int(cls.max_performance_away_attack * general.max_performance_factor)
        #print(cls.max_performance_away_attack, "after factor")

    def penaltyshot(self):
        penaltyshotperformance = random.randint(1,600)
        shotattempt = self.offensive_ability - penaltyshotperformance 
        return shotattempt


    def penaltysave(self):
        penaltysaveperformance = random.randint(1,600)
        saveattempt = self.defensive_ability - penaltysaveperformance 
        return saveattempt

    def remove_sentoff(self):
        if self.sent_off ==True:
            self.sent_off = False

Home_team_Player01 = Player()
Home_team_Player02 = Player()
Home_team_Player03 = Player()
Home_team_Player04 = Player()
Home_team_Player05 = Player()
Home_team_Player06 = Player()
Home_team_Player07 = Player()
Home_team_Player08 = Player()


Away_team_Player01 = Player()
Away_team_Player02 = Player()
Away_team_Player03 = Player()
Away_team_Player04 = Player()
Away_team_Player05 = Player()
Away_team_Player06 = Player()
Away_team_Player07 = Player()
Away_team_Player08 = Player() 