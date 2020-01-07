from season.MatchGenerator.player import *
#from player import *
import random

class Team():
    list_of_teams = []
    def __init__(self,home_or_away,name,tactics_value,motivation,favorite_status,players=None):
        self.home_or_away = home_or_away
        self.name = name
        self.tactics_value = tactics_value
        self.motivation = motivation
        self.favorite_status = favorite_status
        self.previous_score = 0 
        self.score = 0
        self.after_penalties_score = 0
        self.motivation_change = 0
        self.total_motivation_change = 0
        self.current_status = Equal
        self.status_change = None
        self.general_intensity = 1 #change to be imported based on prestige of game etc
        
        self.total_ability = 0
        self.average_ability = 0


        #Setting Favorite staus
        if favorite_status == "Normal":
            self.favorite_status = Normal
        elif favorite_status == "Favorite":
            self.favorite_status = Favorite
        elif favorite_status == "Underdog":
            self.favorite_status = Underdog
        elif favorite_status == "Big favorite":
            self.favorite_status = Big_favorite
        elif favorite_status == "Big underdog":
            self.favorite_status = Big_underdog
        
        if players is None:
            self.players = []
        else:
            self.players = players

        if self.tactics_value > 70:
            self.tactics = "push_up"
        elif self.tactics_value < 30:
            self.tactics = "drop_back"
        else:
            self.tactics = "balanced"

        if self.tactics == "balanced":
            self.offensive_intensity = 1
            self.defensive_intensity = 1
        elif self.tactics == "push_up":
            self.offensive_intensity = 1.15
            self.defensive_intensity = 0.85
        elif self.tactics == "drop_back":
            self.offensive_intensity = 0.85
            self.defensive_intensity = 1.15
     
        #temporary attributes
        self.attack_value = 0
        self.defense_value = 0
        self.tactics_change_value = 0
        self.attack_result = ""
        self.player_score = None
        self.player_save = None
        #self.GK = None
        #self.LM = None
        #self.RM = None
        #self.ST = None
        Team.list_of_teams.append(self)

    def __str__(self):
        return "{}".format(self.name)

    def add_player(self,player):
        if player not in self.players:
            self.players.append(player)

    def remove_player(self,player):
        if player not in self.players:
            self.players.remove(player)

    def print_players(self):
        for player in self.players:
            print("-->",player.player_name)
            
    def print_players_on_pitch(self):
        for player in self.players:
            if player.on_pitch == True and player.sent_off == False:
                print(player.current_position,"-",player.player_name, \
                    "team motivation:", round(player.team_motivation,2), \
                    "motivation update:", round(player.personal_motivation_change,2),\
                    "personal motivation", round(player.personal_motivation,2),\
                    "motivation", round(player.motivation,2))

    def print_players_on_bench(self):
        for player in self.players:
            if player.on_bench == True:
                print(player.player_name)

    def print_players_sent_off(self):
        for player in self.players:
            if player.sent_off == True:
                print(player.player_name)
        

    def initial_selection(self):
        playercombo =[]
        highest_value = 0
        #print('---Team - initial selction---')
        #print(self.players)
        for pos_GK in self.players:
            pos_GK.current_position = GK
            #team = pos_GK.home_away
            GK.tactics_factors(self.tactics)
            pos_GK.calculate_def_ability()
            pos_GK.calculate_off_ability()
            pos_GK.temp_ability = (pos_GK.attack_ability + pos_GK.defend_ability)/2
            for pos_LM in self.players:
                if pos_LM != pos_GK:
                    pos_LM.current_position = LM
                    #team = pos_LM.home_away
                    LM.tactics_factors(self.tactics)
                    pos_LM.calculate_def_ability()
                    pos_LM.calculate_off_ability()
                    pos_LM.temp_ability = (pos_LM.attack_ability + pos_LM.defend_ability)/2
                    for pos_RM in self.players:
                        if pos_RM != pos_GK and pos_RM != pos_LM:
                            pos_RM.current_position = RM
                            #team = pos_RM.home_away
                            RM.tactics_factors(self.tactics)
                            pos_RM.calculate_def_ability()
                            pos_RM.calculate_off_ability()
                            pos_RM.temp_ability = (pos_RM.attack_ability + pos_RM.defend_ability)/2
                            for pos_ST in self.players:
                                if pos_ST != pos_GK and pos_ST != pos_LM and pos_ST != pos_RM:
                                    pos_ST.current_position = ST
                                    #team = pos_ST.home_away
                                    ST.tactics_factors(self.tactics)
                                    pos_ST.calculate_def_ability()
                                    pos_ST.calculate_off_ability()
                                    pos_ST.temp_ability = (pos_ST.attack_ability + pos_ST.defend_ability)/2
                                    combovalue = pos_GK.temp_ability + pos_LM.temp_ability + pos_RM.temp_ability + pos_ST.temp_ability
                                    if combovalue > highest_value:
                                        highest_value = combovalue
                                        playercombo = pos_GK,pos_LM,pos_RM,pos_ST
                                    Position.reset()
                                        
        pos_GK = playercombo[0]
        pos_LM = playercombo[1]
        pos_RM = playercombo[2]
        pos_ST = playercombo[3]
        #self.GK = pos_GK
        #self.LM = pos_LM
        #self.RM = pos_RM
        #self.ST = pos_ST
        pos_GK.current_position = GK
        pos_LM.current_position = LM
        pos_RM.current_position = RM
        pos_ST.current_position = ST
        pos_GK.on_pitch = True
        pos_LM.on_pitch = True
        pos_RM.on_pitch = True
        pos_ST.on_pitch = True
        for player in self.players:
            if player.on_pitch == False:
                player.on_bench = True

    def player_calculate_off_ability(self):
        for player in self.players:
            player.team_tactics = self.tactics
            if player.on_pitch == True and player.sent_off == False:
                Position = player.current_position
                Position.tactics_factors(self.tactics)
                player.calculate_off_ability()
                
    def player_attack(self, general):
        intensity = self.offensive_intensity * self.general_intensity
        for player in self.players:
            if player.on_pitch == True and player.sent_off == False:
                #print(player.player_name)
                player.attack_intensity = intensity
                player.attack(intensity, general) 
                player.attack_rating()
                #print("")
                player.increase_decrease_attack()
            #print("\n")
            elif player.sent_off == True:
                player.sent_off_attack_ability_change()

    def player_calculate_def_ability(self):
        for player in self.players:
            if player.on_pitch == True and player.sent_off == False:
                Position = player.current_position
                Position.tactics_factors(self.tactics)
                player.calculate_def_ability()


    def player_defense(self, general):
        intensity = self.defensive_intensity * self.general_intensity
        for player in self.players:
            if player.on_pitch == True and player.sent_off == False:
                #print(player.player_name)
                player.defence_intensity = intensity
                player.defense(intensity, general)
                player.defense_rating()
                #print("")
                player.increase_decrease_defense()
            #print("\n")
            elif player.sent_off == True:
                player.sent_off_defend_ability_change()

    def team_attack(self):
        self.attack_value = 0
        for player in self.players:
            if player.on_pitch == True and player.sent_off == False:
                self.attack_value = self.attack_value + player.offensive_value

    def team_defense(self):
        self.defense_value = 0
        for player in self.players:
            if player.on_pitch == True and player.sent_off == False:
                self.defense_value = self.defense_value + player.defensive_value

    def goal(self):
        highest_off_value = None
        for player in self.players:
            if player.on_pitch == True and player.sent_off == False:
                if highest_off_value == None:
                    highest_off_value = player
                elif player.offensive_value > highest_off_value.offensive_value:
                    highest_off_value = player
        highest_off_value.goals_scored += 1
        highest_off_value.goal_off_ability_change()
        highest_off_value.personal_motivation_change += 0.01
        highest_off_value.match_rating += 0.02
        self.player_score = highest_off_value.player_id

        #print("Goal by:",highest_off_value.player_name)

    def save(self):
        highest_def_value = None
        for player in self.players:
            if player.on_pitch == True and player.sent_off == False:
                if highest_def_value == None:
                    highest_def_value = player
                elif player.defensive_value > highest_def_value.defensive_value:
                    highest_def_value = player
        highest_def_value.saves_made += 1
        highest_def_value.save_def_ability_change()
        highest_def_value.match_rating += 0.02
        highest_def_value.personal_motivation_change += 0.01
        self.player_save = highest_def_value.player_id
        #print("Save by:",highest_def_value.player_name)
    
    def no_of_subs(self):
        no_of_subs = 0
        for Player in self.players:
            if Player.on_bench == True:
                no_of_subs += 1
        return no_of_subs

    def no_of_sent_off(self):
        no_of_sent_off = 0
        for player in self.players:
            if player.sent_off == True:
                no_of_sent_off += 1
        return no_of_sent_off

    def substitution(self):
        if self.no_of_subs()<1 or self.no_of_sent_off()>0:
            return
        else:
            lowest_fitness = None
            for player in self.players:
                if player.on_pitch == True:
                    if lowest_fitness == None:
                        lowest_fitness = player
                    if player.fitness * 100 < lowest_fitness.fitness * 100:
                        lowest_fitness = player
            if lowest_fitness.fitness * 100 > 49:
                return
            else:
                sub_pos = lowest_fitness.current_position
                lowest_fitness.current_position = ""
                lowest_fitness.on_pitch = False
                for player in self.players:
                    if player.on_bench == True: #lägg till något för att hitta först Sub inte vilken sub som helst
                        player.current_position = sub_pos
                        player.on_pitch = True
                        player.sub_in = True
                        player.on_bench = False
                        break
                    
    def special_event(self):
        for player in self.players:
            if player.on_pitch == True:
                player.special_event()

    def fitness_update(self):
        intensity = self.general_intensity
        for player in self.players:
            if player.on_pitch ==True:
                player.fitness_update(intensity)

    def team_motivation_update(self):
        #print("motivation:"+str(self.motivation) + " motivation_change:"+str(self.motivation_change))
        self.motivation = self.motivation + self.motivation_change

        for player in self.players:
            if player.on_pitch ==True:
                player.team_motivation = self.motivation_change
                player.team_motivation_change = self.motivation_change

        #acumulated motivational change
        self.total_motivation_change = self.total_motivation_change + self.motivation_change

    def player_motivation_update(self):
        team_motivation = self.motivation
        for player in self.players:
            player.motivation_update(team_motivation)

    def reset_values(self):
        for player in self.players:
            player.reset_values()

    def tactics_change(self):
        if self.current_status == Losing_big:
            min_change = -10
            max_change = 40
        elif self.current_status == Losing:
            min_change = -5
            max_change = 25
        elif self.current_status == Equal:
            min_change = -15
            max_change = 15
        elif self.current_status == Lead:
            min_change = -25
            max_change = 5
        elif self.current_status == Big_lead:
            min_change = -40
            max_change = 10
        
        self.tactics_change_value = random.uniform(min_change,max_change)
        new_tactics_value = self.tactics_value + self.tactics_change_value
        self.tactics_value = min(max(new_tactics_value,0),100)

        if self.tactics_value > 70:
            self.tactics = "push_up"
        elif self.tactics_value < 30:
            self.tactics = "drop_back"
        else:
            self.tactics = "balanced"

    def intensity(self):
        #fixa så att det blir någon form av kombination av favorit status och nuvarande match status dvs leder, ligger under etc
        if self.current_status == Losing_big:
            self.general_intensity = 1.1
        elif self.current_status == Losing:
            self.general_intensity = 1.05
        elif self.current_status == Equal:
            self.general_intensity = 1
        elif self.current_status == Lead:
            self.general_intensity = 0.95
        elif self.current_status == Big_lead:
            self.general_intensity = 0.9

            
        if self.tactics == "balanced":
            self.offensive_intensity = 1
            self.defensive_intensity = 1
        elif self.tactics == "push_up":
            self.offensive_intensity = 1.15
            self.defensive_intensity = 0.85
        elif self.tactics == "drop_back":
            self.offensive_intensity = 0.85
            self.defensive_intensity = 1.15

    def remove_sentoff(self):
        for player in self.players:
            player.remove_sentoff()

            