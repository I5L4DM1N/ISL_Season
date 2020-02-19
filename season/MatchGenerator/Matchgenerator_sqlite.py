import random

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
folder = os.path.basename(dir_path)

if folder == 'MatchGenerator':
  from team import *
else:
    from season.MatchGenerator.team import *
DatabasePath = "C:\\Users\\ASV11691\\OneDrive\\ISL_Season\\db.sqlite3"




# def Set_general_values():
#   general = General()
#   general.max_performance_factor = 1.1
#   general.min_adjustment = 0.5
#   general.max_adjustment = 1.5
#   general.margin_to_score = 0.3
#   general.current_round = 0

def Set_match_ID():
    conn = sqlite3.connect(DatabasePath)
    c = conn.cursor()
    #importing from Season_GeneralSchedule
    c.execute('SELECT id,TournamentName,Day,TypeOfGame FROM Season_GeneralSchedule WHERE Played = (?)',(False,))
    Season_GeneralSchedule = c.fetchone()
    #print(Season_GeneralSchedule)
    general.max_performance_factor = 1.1
    general.min_adjustment = 0.5
    general.max_adjustment = 1.5
    general.margin_to_score = 0.3
    general.current_round = 0
    general.match_ID = Season_GeneralSchedule[0]
    general.tournament = Season_GeneralSchedule[1]
    general.day = Season_GeneralSchedule[2]
    general.TypeOfGame = Season_GeneralSchedule[3]

    #test data
    # general.match_ID = 69
    # general.tournament = "Cup"
    # general.day = 11
    # general.TypeOfGame = "Playoff"
    c.close()


def Set_teams():
  conn = sqlite3.connect(DatabasePath)
  c = conn.cursor()
  MatchID = general.match_ID
  #MatchID = 1
  #print(MatchID)
  c.execute('SELECT Home,TeamTacticsValueHome,TeamMotivationHome,FavouriteStatusHome,\
    Away,TeamTacticsValueAway,TeamMotivationAway,FavouriteStatusAway FROM Season_GeneralSchedule WHERE id = (?)',(MatchID,))
  Season_GeneralSchedule = c.fetchone()
  #print(Season_GeneralSchedule)

  home_team.Attributes(Season_GeneralSchedule[0],Season_GeneralSchedule[1],Season_GeneralSchedule[2],Season_GeneralSchedule[3],)
  away_team.Attributes(Season_GeneralSchedule[4],Season_GeneralSchedule[5],Season_GeneralSchedule[6],Season_GeneralSchedule[7],)
  c.close()

def Set_players():
  #Home_team
  conn = sqlite3.connect(DatabasePath)
  c = conn.cursor()
  c.execute('SELECT Name,Nation_id,Team,Position,DivisionRank,Ability,OffensiveAbility,DefensiveAbility,\
    Routine,RoutineRank,Fitness, GKPosExperience, LMPosExperience, RMPosExperience, STPosExperience, \
    PlayerChemistry, PlayerMotivation,id FROM Season_Player WHERE Team = ?',(home_team.name,))
  Home_team_players = c.fetchall()
  HTPL_no = len(Home_team_players)
  HTPL01 = Home_team_players[0]
  Home_team_Player01.Attributes(HTPL01[0],HTPL01[1],HTPL01[2],"home",HTPL01[3],HTPL01[4],\
                HTPL01[5],HTPL01[6],HTPL01[7],HTPL01[8],HTPL01[9],\
                HTPL01[10],HTPL01[11],HTPL01[12],HTPL01[13],HTPL01[14],\
                HTPL01[15],HTPL01[16],HTPL01[17])
  home_team.add_player(Home_team_Player01)


  HTPL02 = Home_team_players[1]
  Home_team_Player02.Attributes(HTPL02[0],HTPL02[1],HTPL02[2],"home",HTPL02[3],HTPL02[4],\
                HTPL02[5],HTPL02[6],HTPL02[7],HTPL02[8],HTPL02[9],\
                HTPL02[10],HTPL02[11],HTPL02[12],HTPL02[13],HTPL02[14],\
                HTPL02[15],HTPL02[16],HTPL02[17])
  home_team.add_player(Home_team_Player02)

      
  HTPL03 = Home_team_players[2]
  Home_team_Player03.Attributes(HTPL03[0],HTPL03[1],HTPL03[2],"home",HTPL03[3],HTPL03[4],\
                HTPL03[5],HTPL03[6],HTPL03[7],HTPL03[8],HTPL03[9],\
                HTPL03[10],HTPL03[11],HTPL03[12],HTPL03[13],HTPL03[14],\
                HTPL03[15],HTPL03[16],HTPL03[17])
  home_team.add_player(Home_team_Player03)

      
  HTPL04 = Home_team_players[3]
  Home_team_Player04.Attributes(HTPL04[0],HTPL04[1],HTPL04[2],"home",HTPL04[3],HTPL04[4],\
                HTPL04[5],HTPL04[6],HTPL04[7],HTPL04[8],HTPL04[9],\
                HTPL04[10],HTPL04[11],HTPL04[12],HTPL04[13],HTPL04[14],\
                HTPL04[15],HTPL04[16],HTPL04[17])
  home_team.add_player(Home_team_Player04)

  HTPL05 = Home_team_players[4]
  Home_team_Player05.Attributes(HTPL05[0],HTPL05[1],HTPL05[2],"home",HTPL05[3],HTPL05[4],\
                HTPL05[5],HTPL05[6],HTPL05[7],HTPL05[8],HTPL05[9],\
                HTPL05[10],HTPL05[11],HTPL05[12],HTPL05[13],HTPL05[14],\
                HTPL05[15],HTPL05[16],HTPL05[17])
  home_team.add_player(Home_team_Player05)

  HTPL06 = Home_team_players[5]
  Home_team_Player06.Attributes(HTPL06[0],HTPL06[1],HTPL06[2],"home",HTPL06[3],HTPL06[4],\
                HTPL06[5],HTPL06[6],HTPL06[7],HTPL06[8],HTPL06[9],\
                HTPL06[10],HTPL06[11],HTPL06[12],HTPL06[13],HTPL06[14],\
                HTPL06[15],HTPL06[16],HTPL06[17])
  home_team.add_player(Home_team_Player06)

  if len(Home_team_players)> 6:
      HTPL07 = Home_team_players[6]
      Home_team_Player07.Attributes(HTPL07[0],HTPL07[1],HTPL07[2],"home",HTPL07[3],HTPL07[4],\
                HTPL07[5],HTPL07[6],HTPL07[7],HTPL07[8],HTPL07[9],\
                HTPL07[10],HTPL07[11],HTPL07[12],HTPL07[13],HTPL07[14],\
                HTPL07[15],HTPL07[16],HTPL07[17])
      home_team.add_player(Home_team_Player07)

      if len(Home_team_players)> 7:
          HTPL08 = Home_team_players[7]
          Home_team_Player08.Attributes(HTPL08[0],HTPL08[1],HTPL08[2],"home",HTPL08[3],HTPL08[4],\
                HTPL08[5],HTPL08[6],HTPL08[7],HTPL08[8],HTPL08[9],\
                HTPL08[10],HTPL08[11],HTPL08[12],HTPL08[13],HTPL08[14],\
                HTPL08[15],HTPL08[16],HTPL08[17])
          home_team.add_player(Home_team_Player08)



  #Away_team
  c.execute('SELECT Name,Nation_id,Team,Position,DivisionRank,Ability,OffensiveAbility,DefensiveAbility,\
    Routine,RoutineRank,Fitness, GKPosExperience, LMPosExperience, RMPosExperience, STPosExperience, \
    PlayerChemistry, PlayerMotivation,id FROM Season_Player WHERE Team = ?',(away_team.name,))
  Away_team_players = c.fetchall()

  ATPL_no = len(Away_team_players)
  ATPL01 = Away_team_players[0]    
  Away_team_Player01.Attributes(ATPL01[0],ATPL01[1],ATPL01[2],"away",ATPL01[3],ATPL01[4],\
                ATPL01[5],ATPL01[6],ATPL01[7],ATPL01[8],ATPL01[9],\
                ATPL01[10],ATPL01[11],ATPL01[12],ATPL01[13],ATPL01[14],\
                ATPL01[15],ATPL01[16],ATPL01[17])
  away_team.add_player(Away_team_Player01)

  ATPL02 = Away_team_players[1]
  Away_team_Player02.Attributes(ATPL02[0],ATPL02[1],ATPL02[2],"away",ATPL02[3],ATPL02[4],\
                ATPL02[5],ATPL02[6],ATPL02[7],ATPL02[8],ATPL02[9],\
                ATPL02[10],ATPL02[11],ATPL02[12],ATPL02[13],ATPL02[14],\
                ATPL02[15],ATPL02[16],ATPL02[17])
  away_team.add_player(Away_team_Player02)
      
  ATPL03 = Away_team_players[2]
  Away_team_Player03.Attributes(ATPL03[0],ATPL03[1],ATPL03[2],"away",ATPL03[3],ATPL03[4],\
                ATPL03[5],ATPL03[6],ATPL03[7],ATPL03[8],ATPL03[9],\
                ATPL03[10],ATPL03[11],ATPL03[12],ATPL03[13],ATPL03[14],\
                ATPL03[15],ATPL03[16],ATPL03[17])
  away_team.add_player(Away_team_Player03)
      
  ATPL04 = Away_team_players[3]
  Away_team_Player04.Attributes(ATPL04[0],ATPL04[1],ATPL04[2],"away",ATPL04[3],ATPL04[4],\
                ATPL04[5],ATPL04[6],ATPL04[7],ATPL04[8],ATPL04[9],\
                ATPL04[10],ATPL04[11],ATPL04[12],ATPL04[13],ATPL04[14],\
                ATPL04[15],ATPL04[16],ATPL04[17])
  away_team.add_player(Away_team_Player04)

  ATPL05 = Away_team_players[4]
  Away_team_Player05.Attributes(ATPL05[0],ATPL05[1],ATPL05[2],"away",ATPL05[3],ATPL05[4],\
                ATPL05[5],ATPL05[6],ATPL05[7],ATPL05[8],ATPL05[9],\
                ATPL05[10],ATPL05[11],ATPL05[12],ATPL05[13],ATPL05[14],\
                ATPL05[15],ATPL05[16],ATPL05[17])
  away_team.add_player(Away_team_Player05)

  ATPL06 = Away_team_players[5]
  Away_team_Player06.Attributes(ATPL06[0],ATPL06[1],ATPL06[2],"away",ATPL06[3],ATPL06[4],\
                ATPL06[5],ATPL06[6],ATPL06[7],ATPL06[8],ATPL06[9],\
                ATPL06[10],ATPL06[11],ATPL06[12],ATPL06[13],ATPL06[14],\
                ATPL06[15],ATPL06[16],ATPL06[17])
  away_team.add_player(Away_team_Player06)


  if len(Away_team_players)> 6:
      ATPL07 = Away_team_players[6]
      Away_team_Player07.Attributes(ATPL07[0],ATPL07[1],ATPL07[2],"away",ATPL07[3],ATPL07[4],\
                ATPL07[5],ATPL07[6],ATPL07[7],ATPL07[8],ATPL07[9],\
                ATPL07[10],ATPL07[11],ATPL07[12],ATPL07[13],ATPL07[14],\
                ATPL07[15],ATPL07[16],ATPL07[17])
      away_team.add_player(Away_team_Player07)

      if len(Away_team_players)> 7:
          ATPL08 = Away_team_players[7]
          Away_team_Player08.Attributes(ATPL08[0],ATPL08[1],ATPL08[2],"away",ATPL08[3],ATPL08[4],\
                ATPL08[5],ATPL08[6],ATPL08[7],ATPL08[8],ATPL08[9],\
                ATPL08[10],ATPL08[11],ATPL08[12],ATPL08[13],ATPL08[14],\
                ATPL08[15],ATPL08[16],ATPL08[17])
          away_team.add_player(Away_team_Player08)
  c.close()

def round_attack(attacking_team,defending_team):
  attacking_team.attack_result = ""
  attacking_team.player_score = None
  defending_team.player_save = None
  attacking_team.previous_score = attacking_team.score
  if attacking_team.attack_value < 0:
    attacking_team.attack_result = "Miss"
  elif attacking_team.attack_value > (defending_team.defense_value + \
    (general.margin_to_score*defending_team.defense_value)):
    attacking_team.score += 1
    attacking_team.attack_result = "Goal"
    attacking_team.goal()
  else:
    attacking_team.attack_result = "Save"
    defending_team.save()

def round_status_update(team_1, team_2):
  #team 1
  #print("\n")
  #print("team",team_1.name)
  team1_score = team_1.score
  team2_score = team_2.score
  status = Status_determination(team1_score,team2_score)
  team_1.current_status = status
  #print("status",status)

  score_difference = team_1.score - team_2.score
  #print("score difference",score_difference)
  previous_score_difference = team_1.previous_score - team_2.previous_score
  #print("previous score difference",previous_score_difference)
  change = Change_determination(score_difference,previous_score_difference)
  team_1.status_change = change
  #print("change",change)

  status_n_change = Status_and_change_determination(status,change)
  #print(status_n_change)
  value_determination = status_n_change.value_determination(team_1.favorite_status)
  # print(team_1.favorite_status)
  #print(team_1.motivation_change)
  # print(status_n_change.Big_underdog)
  #print(value_determination)
  team_1.motivation_change = value_determination
  #print("mot change",value_determination)

  #team 2
  #print("\n")
  #print("team",team_2.name)
  status = Status_determination(team2_score,team1_score)
  team_2.current_status = status
  #print("status",status)

  score_difference = team_2.score - team_1.score
  #print("score difference",score_difference)
  previous_score_difference = team_2.previous_score - team_1.previous_score
  #print("previous score difference",previous_score_difference)
  change = Change_determination(score_difference,previous_score_difference)
  team_2.status_change = change
  #print("change",change)

  status_n_change = Status_and_change_determination(status,change)
  #print(status_n_change)
  #print(team_2.favorite_status)
  value_determination = status_n_change.value_determination(team_2.favorite_status)
  #print(value_determination)
  team_2.motivation_change = value_determination
  #print("mot change",value_determination)
  
def Initial_set_up():
  #Set_general_values()
  Set_match_ID()
  Set_teams()
  Set_players()

  home_team.initial_selection()
  away_team.initial_selection()

def Finshed_values ():
    conn = sqlite3.connect(DatabasePath)
    c = conn.cursor()
    #updating Season_GeneralSchedule

    #defining result symbols
    if general.TypeOfGame == "Playoff" and home_team.score == away_team.score:
      if home_team.after_penalties_score > away_team.after_penalties_score:
        home_team_result_symbol = "W"
        away_team_result_symbol = "L"
        Winner = home_team.name
      else:
        home_team_result_symbol = "L"
        away_team_result_symbol = "W"
        Winner = away_team.name
    else:
      home_team_result_symbol = "D"
      away_team_result_symbol = "D"
      Winner = "Draw"
      if home_team.score > away_team.score:
        home_team_result_symbol = "W"
        away_team_result_symbol = "L"
        Winner = home_team.name
      elif home_team.score < away_team.score:
        home_team_result_symbol = "L"
        away_team_result_symbol = "W"
        Winner = away_team.name

    c.execute('UPDATE Season_GeneralSchedule SET Played = (?), GoalsHome = (?), GoalsAway = (?), \
      SignHome = (?), SignAway = (?),Winner = (?), AfterPenaltyHome = (?),AfterPenaltyAway = (?) WHERE GameID = (?)',\
      (True,home_team.score, away_team.score, home_team_result_symbol, away_team_result_symbol, \
        Winner,home_team.after_penalties_score,away_team.after_penalties_score, general.match_ID))
    conn.commit()

    #updating logs
    #Player motivation

    for player in Player.list_of_players:

      c.execute('INSERT INTO Season_PlayerMotivationLog (Player_id,MotivationChange,NewMotivation,Day,TypeOfUpdate,GameID) \
      VALUES (?,?,?,?,?,?)',
             (player.player_id, player.total_motivation_change, player.personal_motivation,general.day,"Game",general.match_ID))

      c.execute('INSERT INTO Season_PlayerFitnessLog (Player_id,FitnessChange,NewFitness,Day,TypeOfUpdate,GameID) \
      VALUES (?,?,?,?,?,?)',
             (player.player_id, player.total_fitness_change, player.fitness,general.day,"Game",general.match_ID))

      c.execute('INSERT INTO Season_PlayerAbilityLog (Name,OffensiveAbilityChange,OffensiveAbility, DefensiveAbilityChange,DefensiveAbility, Day,TypeOfUpdate,GameID) \
      VALUES (?,?,?,?,?,?,?,?)',
             (player.player_name, player.total_off_change, player.offensive_ability,player.total_def_change, player.defensive_ability,general.day,"Game",general.match_ID))

      if player.position =="GK":
        player.ability = (player.offensive_ability * 0.4) + (player.defensive_ability * 0.6)
      elif player.position == "LM":
        player.ability = (player.offensive_ability * 0.5) + (player.defensive_ability * 0.5)
      elif player.position == "RM":
        player.ability = (player.offensive_ability * 0.5) + (player.defensive_ability * 0.5)
      elif player.position == "ST":
        player.ability = (player.offensive_ability * 0.6) + (player.defensive_ability * 0.4)

      #print("Org mot:" + str(round(player.original_motivation,2)) + " New pers mot:" + str(round(player.personal_motivation,2)) +  " Total mot:" + str(round(player.motivation,2)) + " Mot change:" + str(round(player.total_motivation_change,2))) 
      
      motivation = player.original_motivation + (player.total_motivation_change/500)

      c.execute('UPDATE Season_Player SET Ability = (?), DefensiveAbility = (?), Fitness = (?), GKPosExperience = (?), LMPosExperience = (?), OffensiveAbility = (?), RMPosExperience = (?), Routine = (?), STPosExperience = (?),PlayerMotivation = (?) WHERE Name = (?)',\
             ((player.ability/100), (player.defensive_ability/100), player.fitness, player.GK_pos_experience, player.LM_pos_experience, (player.offensive_ability/100), player.RM_pos_experience, player.routine, player.ST_pos_experience,motivation,player.player_name))



    c.execute('INSERT INTO Season_TeamMotivationLog (Name,MotivationChange,Motivation,Day,TypeOfUpdate,GameID) \
    VALUES (?,?,?,?,?,?)',
             (home_team.name, home_team.total_motivation_change, home_team.motivation,general.day,"Game",general.match_ID))

    c.execute('INSERT INTO Season_TeamMotivationLog (Name,MotivationChange,Motivation,Day,TypeOfUpdate,GameID) \
    VALUES (?,?,?,?,?,?)',
             (away_team.name, away_team.total_motivation_change, away_team.motivation,general.day,"Game",general.match_ID))

    no_of_players = 0
    for player in home_team.players:
      home_team.total_ability = home_team.total_ability + (player.ability/100)
      no_of_players += 1

    home_team.average_ability = (home_team.total_ability/no_of_players)
    
    

    #Home team update
    c.execute('UPDATE Season_Team SET AverageAbility = (?), TotalAbility = (?) WHERE Name = (?)',\
             (home_team.average_ability,home_team.total_ability,home_team.name))

    no_of_players = 0
    for player in away_team.players:
      away_team.total_ability = away_team.total_ability + player.ability
      no_of_players += 1

    away_team.average_ability = (away_team.total_ability/no_of_players)

    #Away team update
    c.execute('UPDATE Season_Team SET AverageAbility = (?), TotalAbility = (?) WHERE Name = (?)',\
             (away_team.average_ability,away_team.total_ability,away_team.name))
    conn.commit()
    c.close()

def Round_to_db ():
  conn = sqlite3.connect(DatabasePath)
  c = conn.cursor()

  #inserting Hometeam data into Season_GameTeamLog
  c.execute('INSERT INTO Season_GameTeamLog (GameID, GameRound, TeamName, HomeOrAway, AttckingArea, DefendingArea, \
  AttackResult, DefenceResult, GoalsForwardAfterRound, GoalsAgainstAfterRound, \
  TacticsValueChange, TacticsValue, Tactics, \
  Motivation, MotivationChange, Intensity,\
  AttackValue,DefenseValue,Status,StatusChange, EventPlayerAttack_id, EventPlayerDefence_id) \
  VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
  (general.match_ID,general.current_round,home_team.name,str("Home"),str(general.home_attack_area.name),str(general.away_attack_area.name),\
    home_team.attack_result, away_team.attack_result,home_team.score,away_team.score,\
    float(home_team.tactics_change_value), float(home_team.tactics_value), str(home_team.tactics),\
    float(home_team.motivation),float(home_team.motivation_change),float(home_team.general_intensity),\
    float(home_team.attack_value),float(home_team.defense_value),str(home_team.current_status),str(home_team.status_change),home_team.player_score, home_team.player_save))

  #inserting Awayteam data into Season_GameTeamLog
  c.execute('INSERT INTO Season_GameTeamLog (GameID, GameRound, TeamName, HomeOrAway, AttckingArea, DefendingArea, \
  AttackResult, DefenceResult, GoalsForwardAfterRound, GoalsAgainstAfterRound, \
  TacticsValueChange, TacticsValue, Tactics, Motivation, MotivationChange, Intensity, AttackValue,DefenseValue,Status,StatusChange,EventPlayerAttack_id, EventPlayerDefence_id) \
  VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
  (general.match_ID,general.current_round,away_team.name,str("Away"),str(general.away_attack_area.name),str(general.home_attack_area.name),\
    away_team.attack_result, home_team.attack_result,away_team.score,home_team.score,\
    float(away_team.tactics_change_value), float(away_team.tactics_value), str(away_team.tactics),\
    float(away_team.motivation),float(away_team.motivation_change),float(away_team.general_intensity),\
    float(away_team.attack_value),float(away_team.defense_value),str(away_team.current_status),str(away_team.status_change),away_team.player_score, away_team.player_save))

  for player in Player.list_of_players:
    #print(str(player.player_name) + " Round: " + str(general.current_round))
    if player.on_pitch == True:
      #print(str(player.player_name) + " Round: " + str(general.current_round))
      if player.home_away == "home":
        AreaAttack = general.home_attack_area.name
        AreaDefence = general.away_attack_area.name
      elif player.home_away == "away":
        AreaAttack = general.away_attack_area.name
        AreaDefence = general.home_attack_area.name
      c.execute('INSERT INTO Season_GamePlayerLog (Player_id,Chemestry, DefensivePerformance, MotivationAdjustedDefensivePerformance, \
        FitnessChange, GameID, GameRound, AreaAttack, AreaDefence, GoalPlayer, PersonalMotivationChange, MotivationChange, TotalMotivationChange, \
        NewFitness, NewMotivation, PersonalMotivation, AdjustedPersonalMotivation, OffensivePerformance, MotivationAdjustedOffensivePerformance, \
        Name, Position, SavePlayer, SentOff, Team, OffensiveValue, DefensiveValue, Ability, OffensiveAbility, DefensiveAbility, AttackAbility, \
        DefendAbility, OffensiveAbilityChange, DefensiveAbilityChange, GoalOffAbilityChange, SaveDefAbilityChange, DefensiveRating, OffensiveRating, \
        Substitute, MatchRating, AttackingPostionalOffensiveFactor, AttackingPostionalDefensiveFactor, DefendingPostionalOffensiveFactor, \
        DefendingPostionalDefensiveFactor, PositionalExperience, TeamTactics, AttackIntensity, DefenceIntensity, RoutineBonus, Nervosity, \
        TeamMotivation,TeamMotivationChange, MaxAttackPerformance, MaxDefencePerformance, AttackAreaInfluence, DefenceAreaInfluence, \
        SentOffOffAbilityChange, SentOffDefAbilityChange, AttackAbilityChangePerformance, DefeneceAbilityChangePerformance, \
        AttackAbilityChangeEffect, DefenceAbilityChangeEffect)\
      VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
      (player.player_id ,
      round(player.personal_chemistry,2), 
      round(player.defensive_performance/100,2),
      round(player.motivation_adjusted_def_performance/100,2),
      round(player.fitness_change,2), 
      general.match_ID, 
      general.current_round, 
      AreaAttack, 
      AreaDefence, 
      player.goals_scored,
      round(player.personal_motivation_change,2), 
      round(player.motivation_change,2), 
      round(player.total_motivation_change,2),
      round(player.fitness,2), 
      round(player.motivation,2),
      round(player.personal_motivation,2),
      round(player.adjusted_personal_motivation,2),   
      round(player.offensive_performance/100,2),
      round(player.motivation_adjusted_off_performance/100,2),  
      player.player_name, 
      player.current_position.name, 
      player.saves_made, 
      player.sent_off, 
      player.team,
      round(player.offensive_value/100,2),
      round(player.defensive_value/100,2),
      round(float(player.ability),2),
      round(player.offensive_ability/100,2),
      round(player.defensive_ability/100,2),
      round(player.attack_ability/100,2),
      round(player.defend_ability/100,2),
      round(player.off_perf_abi_change,2), 
      round(player.def_perf_abi_change,2), 
      player.goal_off_abi_change, 
      player.save_def_abi_change,
      round(player.defensive_rating,2),
      round(player.offensive_rating,2),
      player.sub_in,
      round(player.match_rating,1),
      player.att_pos_off_factor,
      player.att_pos_def_factor,
      player.def_pos_off_factor,
      player.def_pos_def_factor,
      player.current_pos_exp,
      player.team_tactics,
      player.attack_intensity,
      player.defence_intensity,
      player.routine_bonus,
      player.nervosity,
      player.team_motivation,
      player.team_motivation_change,
      player.max_attack_performance,
      player.max_defence_performance,
      player.attack_area_influence,
      player.defence_area_influence,
      round(player.sent_off_off_abi_change,2),
      round(player.sent_off_def_abi_change,2),
      round(player.attack_ability_change_performance,2),
      round(player.defence_ability_change_performance,2),
      round(player.attack_ability_change_effect,2),
      round(player.defence_ability_change_effect,2)
      ))
  conn.commit()
  c.close() 
 
def Full_round():
    for x in range(1,11):

        general.current_round += 1

        general.home_attack_area = Area.current_area()
        general.away_attack_area = Area.current_area()

        #resets offensive and defensive facotors for Position (determines how much of defensive or offensive ability 
        #will affect the player's attcking or defending performance)
        Position.reset()
        
        #resets moviational change for all players
        home_team.reset_values()
        away_team.reset_values()

        home_team.player_calculate_off_ability()

        Position.reset()
        away_team.player_calculate_def_ability()

        Position.reset()
        away_team.player_calculate_off_ability()

        Position.reset()
        home_team.player_calculate_def_ability()

        Player.calculate_max_performance_home_attack()
        Player.calculate_max_performance_away_attack()

        #player attack and defend
        home_team.player_attack()   
        away_team.player_defense()
        
        away_team.player_attack()   
        home_team.player_defense()

        
        home_team.team_attack()
        away_team.team_defense()
        

        round_attack(home_team,away_team)


        away_team.team_attack()
        home_team.team_defense()
        

        round_attack(away_team,home_team)

        round_status_update(home_team,away_team)

        home_team.team_motivation_update()
        away_team.team_motivation_update()

        home_team.fitness_update()
        away_team.fitness_update()

        home_team.player_motivation_update()
        away_team.player_motivation_update()

        home_team.special_event()
        away_team.special_event()
        

        home_team.tactics_change()
        away_team.tactics_change()

        home_team.intensity()
        away_team.intensity()

        Round_to_db()
        
        home_team.substitution()
        away_team.substitution()


def Penalties():
  #reset any sending off
  home_team.remove_sentoff()
  away_team.remove_sentoff()
  
  #initial Penalties
  initial_penalties()
  #print(str(home_team.after_penalties_score) + "-" + str(away_team.after_penalties_score))

  home_team.after_penalties_score = 1
  away_team.after_penalties_score = 1

  if home_team.after_penalties_score == away_team.after_penalties_score:
    sudden_death_penalties()

def initial_penalties():
  # for player in home_team.players:
  #   if player.current_position == GK and player.on_pitch == True:
  #     print(player.player_name)

  #home team penalties
  for player in home_team.players:
    if player.on_pitch ==True:
      shot = player.penaltyshot()
      for playeraway in away_team.players:
        if playeraway.current_position == GK:
          #print("GK found")
          save = playeraway.penaltysave()
      if shot > save:
        home_team.after_penalties_score += 1

  #away team penalties
  for player in away_team.players:
    if player.on_pitch ==True:
      shot = player.penaltyshot()
      for playerhome in home_team.players:
        if playerhome.current_position == GK:
          #print("GK found")
          save = playerhome.penaltysave()
      if shot > save:
        away_team.after_penalties_score += 1



def sudden_death_penalties():
  for player in home_team.players:
    if player.current_position == GK and player.on_pitch == True:
      homeGK = player
    elif player.current_position == LM and player.on_pitch == True:
      homeLM = player
    elif player.current_position == RM and player.on_pitch == True:
      homeRM = player
    elif player.current_position == ST and player.on_pitch == True:
      homeST = player

  for player in away_team.players:
    if player.current_position == GK and player.on_pitch == True:
      awayGK = player
    elif player.current_position == LM and player.on_pitch == True:
      awayLM = player
    elif player.current_position == RM and player.on_pitch == True:
      awayRM = player
    elif player.current_position == ST and player.on_pitch == True:
      awayST = player

  while home_team.after_penalties_score == away_team.after_penalties_score:
    shot = homeST.penaltyshot()
    save = awayGK.penaltysave()
    if shot > save:
      home_team.after_penalties_score += 1

    shot = awayST.penaltyshot()
    save = homeGK.penaltysave()
    if shot > save:
      away_team.after_penalties_score += 1
    #print(str(home_team.after_penalties_score) + "-" + str(away_team.after_penalties_score))
    if home_team.after_penalties_score != away_team.after_penalties_score:
      break

    shot = homeLM.penaltyshot()
    save = awayGK.penaltysave()
    if shot > save:
      home_team.after_penalties_score += 1

    shot = awayLM.penaltyshot()
    save = homeGK.penaltysave()
    if shot > save:
      away_team.after_penalties_score += 1
    #print(str(home_team.after_penalties_score) + "-" + str(away_team.after_penalties_score))
    if home_team.after_penalties_score != away_team.after_penalties_score:
      break

    shot = homeRM.penaltyshot()
    save = awayGK.penaltysave()
    if shot > save:
      home_team.after_penalties_score += 1

    shot = awayRM.penaltyshot()
    save = homeGK.penaltysave()
    if shot > save:
      away_team.after_penalties_score += 1
    #print(str(home_team.after_penalties_score) + "-" + str(away_team.after_penalties_score))
    if home_team.after_penalties_score != away_team.after_penalties_score:
      break

    shot = homeGK.penaltyshot()
    save = awayGK.penaltysave()
    if shot > save:
      home_team.after_penalties_score += 1

    shot = awayGK.penaltyshot()
    save = homeGK.penaltysave()
    if shot > save:
      away_team.after_penalties_score += 1
    #print(str(home_team.after_penalties_score) + "-" + str(away_team.after_penalties_score))
    if home_team.after_penalties_score != away_team.after_penalties_score:
      break

def Full_game():
  Player.list_of_players.clear()
  Initial_set_up()
  #print(len(Player.list_of_players))

  Full_round()

  #print(len(Player.list_of_players))

  #general.TypeOfGame = "Playoff" 
  #home_team.score = 1 
  #away_team.score = 1
  #penalties
  if general.TypeOfGame == "Playoff" and home_team.score == away_team.score:
    Penalties()

  Finshed_values()
  #print(len(Player.list_of_players))


#Penalties()

#Initial_set_up()
#Full_round()
if __name__ == "__main__":
  Full_game()


#close connection to database
#c.close()
#conn.close()      
         
