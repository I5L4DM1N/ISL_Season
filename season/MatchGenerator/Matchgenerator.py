import random
import sqlite3

if __name__ == "__main__":
  from team import *
  from DatabaseChanges.mysql_connector_scripts import *
else:    
    from season.MatchGenerator.team import *
    from season.MatchGenerator.DatabaseChanges.mysql_connector_scripts import *


connection_string = {'host':'35.228.182.135',
                      'database':'isl',
                      'user':'admin',
                      'password':'pass123'}



def one_dict_to_two_lists(dict_to_split):
  keyslist = []
  valueslist = []
  for key,value in dict_to_split.items():
    keyslist.append(key)
    valueslist.append(value)

  return keyslist, valueslist


def set_general_info(connection_string):
    #Fetching matchdata
    selection_columns_list = ['id','TournamentName','Day','TypeOfGame']
    table_name = 'season_generalschedule'
    condition_dict = {'Played':False}
    match_data = select_data(connection_string,selection_columns_list,table_name,condition_dict)
    match_data = match_data[0]

    # setting general match data
    general = General(match_data[0],match_data[1], match_data[2], match_data[3])

    return general


def set_teams(connection_string, general):
    match_id = general.match_ID

    selection_columns_list = ['Home','TeamTacticsValueHome','TeamMotivationHome','FavouriteStatusHome','Away','TeamTacticsValueAway','TeamMotivationAway','FavouriteStatusAway']
    table_name = 'season_generalschedule'
    condition_dict = {'id':match_id}

    teams_info = select_data(connection_string,selection_columns_list,table_name,condition_dict)
    teams_info = teams_info[0]

    #initiating teams - (home_or_away,name,tactics_value,motivation,favorite_status,players=None)
    home_team = Team('home',teams_info[0],teams_info[1],teams_info[2],teams_info[3],)
    away_team = Team('away',teams_info[4],teams_info[5],teams_info[6],teams_info[7],)
    return home_team, away_team


def create_player(players, team):
  for p in players:

    # Creating Class instance of PLayer
    #Player initiation
    #self,Player_name, Nation, Team, Home_Away, Position, Division_Rank, 
    #Ability, Offensive_Ability, Defensive_Ability, Routine,  \
    #Routine_Rank, Fitness, GK_pos_experience, LM_pos_experience, \
    #RM_pos_experience, ST_pos_experience, Personal_chemistry, Personal_motivation,player_id)
    player_ = Player(p[0],p[1],p[2],"home",p[3],p[4],\
      p[5],p[6],p[7],p[8],p[9],\
      p[10],p[11],p[12],p[13],p[14],\
      p[15],p[16],p[17])

    #adding player to team's list of players
    team.players.append(player_)

def set_players(connection_string, home_team, away_team):
  selection_columns_list = ['Name','Nation_id','Team','Position','DivisionRank','Ability','OffensiveAbility','DefensiveAbility','Routine','RoutineRank','Fitness', 'GKPosExperience', 'LMPosExperience', 'RMPosExperience', 'STPosExperience', 'PlayerChemistry', 'PlayerMotivation','id']
  table_name = 'season_player'

  condition_dict = {'Team':home_team.name}
  home_players = select_data(connection_string,selection_columns_list,table_name,condition_dict)

  condition_dict = {'Team':away_team.name}
  away_players = select_data(connection_string,selection_columns_list,table_name,condition_dict)

  create_player(home_players, home_team)
  create_player(away_players, away_team)


# general = set_general_info(connection_string)
# teams = set_teams(connection_string, general)
# home_team = teams[0]
# away_team = teams[1]

# set_players(connection_string, home_team, away_team)

def round_attack(attacking_team,defending_team, general):
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
  
def initial_set_up(connection_string):
  #Set_general_values()
  general = set_general_info(connection_string)
  teams = set_teams(connection_string, general)
  home_team = teams[0]
  away_team = teams[1]

  set_players(connection_string, home_team, away_team)

  home_team.initial_selection()
  away_team.initial_selection()

  return  general, home_team, away_team



def Finshed_values (connection_string, general, home_team, away_team):
    destination_database = connection_string['database']
    connection_string_instance = connection_string
    del connection_string_instance['database']

    #updating Season_GeneralSchedule
    table_name = 'season_generalschedule'

    columns_and_input = {
      'Played': True,
      'GoalsHome':home_team.score,
      'GoalsAway':away_team.score,
      'AfterPenaltyHome':home_team.after_penalties_score,
      'AfterPenaltyAway':away_team.after_penalties_score
    }

    #defining result symbols
    if general.TypeOfGame == "Playoff" and home_team.score == away_team.score:
      if home_team.after_penalties_score > away_team.after_penalties_score:
        columns_and_input['SignHome'] = "W"
        columns_and_input['SignAway'] = "L"
        columns_and_input['Winner'] = home_team.name
      else:
        columns_and_input['SignHome'] = "L"
        columns_and_input['SignAway'] = "W"
        columns_and_input['Winner'] = away_team.name
    elif home_team.score > away_team.score:
      columns_and_input['SignHome'] = "W"
      columns_and_input['SignAway'] = "L"
      columns_and_input['Winner'] = home_team.name
    elif home_team.score < away_team.score:
      columns_and_input['SignHome'] = "L"
      columns_and_input['SignAway'] = "W"
      columns_and_input['Winner'] = away_team.name
    else:
      columns_and_input['SignHome'] = "D"
      columns_and_input['SignAway'] = "D"
      columns_and_input['Winner'] = 'Draw'

    condition_dict = {'GameID':general.match_ID}

    update_data(connection_string_instance, destination_database, table_name, columns_and_input, condition_dict)

    #updating logs
    for player in Player.list_of_players:

      #Player motivation
      table_name = 'season_playermotivationlog'

      columns_and_values_dict = {
        'Player_id':player.player_id,
        'MotivationChange':player.total_motivation_change,
        'NewMotivation':player.personal_motivation,
        'Day':general.day,
        'TypeOfUpdate':'Game',
        'GameID':general.match_ID,
      }

      columns_and_values = one_dict_to_two_lists(columns_and_values_dict)

      list_of_columns = columns_and_values[0] 
      list_of_values = columns_and_values[1]

      connection_string['database'] = 'isl'
      insert_data(connection_string, table_name, list_of_columns, list_of_values)


      #PLayer Fitness
      table_name = 'season_playerfitnesslog'

      columns_and_values_dict = {
        'Player_id':player.player_id,
        'FitnessChange':player.total_fitness_change,
        'NewFitness':player.fitness,
        'Day':general.day,
        'TypeOfUpdate':'Game',
        'GameID':general.match_ID,
      }

      columns_and_values = one_dict_to_two_lists(columns_and_values_dict)

      list_of_columns = columns_and_values[0] 
      list_of_values = columns_and_values[1]

      insert_data(connection_string, table_name, list_of_columns, list_of_values)


      #PLayer Ability
      table_name = 'season_playerabilitylog'

      columns_and_values_dict = {
        'Name':player.player_name,
        'OffensiveAbilityChange':player.total_off_change,
        'OffensiveAbility':player.offensive_ability,
        'DefensiveAbilityChange':player.total_def_change,
        'DefensiveAbility':player.defensive_ability,
        'Day':general.day,
        'TypeOfUpdate':'Game',
        'GameID':general.match_ID
      }

      columns_and_values = one_dict_to_two_lists(columns_and_values_dict)

      list_of_columns = columns_and_values[0] 
      list_of_values = columns_and_values[1]

      insert_data(connection_string, table_name, list_of_columns, list_of_values)


      #Player update
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

      table_name = 'season_player'

      ability = player.ability/100
      defensive_ability = player.defensive_ability/100
      offensive_ability = player.offensive_ability/100

      columns_and_input = {
        'Ability': ability,
        'DefensiveAbility':defensive_ability,
        'Fitness':player.fitness,
        'GKPosExperience':player.GK_pos_experience,
        'LMPosExperience':player.LM_pos_experience,
        'OffensiveAbility':offensive_ability,
        'RMPosExperience':player.RM_pos_experience,
        'Routine':player.routine,
        'STPosExperience':player.ST_pos_experience,
        'PlayerMotivation':motivation,
      }

      condition_dict = {'Name':player.player_name}

      update_data(connection_string_instance, destination_database, table_name, columns_and_input, condition_dict)

     
    #Team Motivation home team
    table_name = 'season_teammotivationlog'

    columns_and_values_dict = {
      'Name':home_team.name,
      'MotivationChange':home_team.total_motivation_change,
      'Day':general.day,
      'TypeOfUpdate':'Game',
      'GameID':general.match_ID
    }

    columns_and_values = one_dict_to_two_lists(columns_and_values_dict)

    list_of_columns = columns_and_values[0] 
    list_of_values = columns_and_values[1]

    insert_data(connection_string, table_name, list_of_columns, list_of_values)

    #Team motivation away team
    columns_and_values_dict = {
      'Name':away_team.name,
      'MotivationChange':away_team.total_motivation_change,
      'Motivation':away_team.motivation,
      'Day':general.day,
      'TypeOfUpdate':'Game',
      'GameID':general.match_ID
    }

    columns_and_values = one_dict_to_two_lists(columns_and_values_dict)

    list_of_columns = columns_and_values[0] 
    list_of_values = columns_and_values[1]

    insert_data(connection_string, table_name, list_of_columns, list_of_values)


    #Home team update
    no_of_players = 0
    for player in home_team.players:
      home_team.total_ability = home_team.total_ability + (player.ability/100)
      no_of_players += 1

    home_team.average_ability = (home_team.total_ability/no_of_players)
    
    table_name = 'season_team'

    columns_and_input = {
      'AverageAbility': home_team.average_ability,
      'TotalAbility':home_team.total_ability,
    }

    condition_dict = {'Name':home_team.name}

    update_data(connection_string_instance, destination_database, table_name, columns_and_input, condition_dict)

    #Away team update
    no_of_players = 0
    for player in away_team.players:
      away_team.total_ability = away_team.total_ability + player.ability
      no_of_players += 1

    away_team.average_ability = (away_team.total_ability/no_of_players)
    
    columns_and_input = {
      'AverageAbility': away_team.average_ability,
      'TotalAbility':away_team.total_ability,
    }

    condition_dict = {'Name':away_team.name}

    update_data(connection_string_instance, destination_database, table_name, columns_and_input, condition_dict)

def Finshed_values_old (connection_string, home_team, away_team, general):

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
    # format
    # columns_and_input = {'save_number': 1, 'Flag':'Italy.png'}
    # condition_string = 'save_number is NULL'
    # condition_dict = {'id':2}
    # update_data(connection_string_instance, destination_database, table_name, columns_and_input, condition_dict)

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

def Round_to_db (connection_string, home_team, away_team, general):

  #inserting homwe team values
  table_name = 'season_gameteamlog'

  columns_and_values_dict = {
    'GameID':general.match_ID,
    'GameRound':general.current_round,
    'TeamName':home_team.name,
    'HomeOrAway':str("Home"),
    'AttckingArea':str(general.home_attack_area.name),
    'DefendingArea':str(general.away_attack_area.name),
    'AttackResult': home_team.attack_result,
    'DefenceResult': away_team.attack_result,
    'GoalsForwardAfterRound':home_team.score,
    'GoalsAgainstAfterRound':away_team.score,
    'TacticsValueChange': float(home_team.tactics_change_value),
    'TacticsValue': float(home_team.tactics_value),
    'Tactics': str(home_team.tactics),
    'Motivation': float(home_team.motivation),
    'MotivationChange':float(home_team.motivation_change),
    'Intensity':float(home_team.general_intensity),
    'AttackValue': float(home_team.attack_value),
    'DefenseValue':float(home_team.defense_value),
    'Status':str(home_team.current_status),
    'StatusChange':str(home_team.status_change),
    'EventPlayerAttack_id':home_team.player_score,
    'EventPlayerDefence_id': home_team.player_save
  }

  columns_and_values = one_dict_to_two_lists(columns_and_values_dict)

  list_of_columns = columns_and_values[0] 
  list_of_values = columns_and_values[1]

  insert_data(connection_string, table_name, list_of_columns, list_of_values)

  #inserting away team values
  columns_and_values_dict = {
    'GameID':general.match_ID,
    'GameRound':general.current_round,
    'TeamName':away_team.name,
    'HomeOrAway':str("Away"),
    'AttckingArea':str(general.away_attack_area.name),
    'DefendingArea':str(general.home_attack_area.name),
    'AttackResult': away_team.attack_result,
    'DefenceResult': home_team.attack_result,
    'GoalsForwardAfterRound':away_team.score,
    'GoalsAgainstAfterRound':home_team.score,
    'TacticsValueChange': float(away_team.tactics_change_value),
    'TacticsValue': float(away_team.tactics_value),
    'Tactics': str(away_team.tactics),
    'Motivation': float(away_team.motivation),
    'MotivationChange':float(away_team.motivation_change),
    'Intensity':float(away_team.general_intensity),
    'AttackValue': float(away_team.attack_value),
    'DefenseValue':float(away_team.defense_value),
    'Status':str(away_team.current_status),
    'StatusChange':str(away_team.status_change),
    'EventPlayerAttack_id':away_team.player_score,
    'EventPlayerDefence_id': away_team.player_save
  }

  columns_and_values = one_dict_to_two_lists(columns_and_values_dict)

  list_of_columns = columns_and_values[0] 
  list_of_values = columns_and_values[1]

  insert_data(connection_string, table_name, list_of_columns, list_of_values)


  #inserting player values

  table_name = 'season_gameplayerlog'


  for player in Player.list_of_players:
    #print(str(player.player_name) + " Round: " + str(general.current_round))
    if player.on_pitch == True:
      columns_and_values_dict = {
        'Player_id':player.player_id,
        'Chemestry':round(player.personal_chemistry,2), 
        'DefensivePerformance':round(player.defensive_performance/100,2),
        'MotivationAdjustedDefensivePerformance':round(player.motivation_adjusted_def_performance/100,2),
        'FitnessChange':round(player.fitness_change,2), 
        'GameID':general.match_ID, 
        'GameRound':general.current_round, 
        'GoalPlayer':player.goals_scored,
        'PersonalMotivationChange':round(player.personal_motivation_change,2), 
        'MotivationChange':round(player.motivation_change,2), 
        'TotalMotivationChange':round(player.total_motivation_change,2),
        'NewFitness':round(player.fitness,2), 
        'NewMotivation':round(player.motivation,2),
        'PersonalMotivation':round(player.personal_motivation,2),
        'AdjustedPersonalMotivation':round(player.adjusted_personal_motivation,2),   
        'OffensivePerformance':round(player.offensive_performance/100,2),
        'MotivationAdjustedOffensivePerformance':round(player.motivation_adjusted_off_performance/100,2),  
        'Name':player.player_name, 
        'Position':player.current_position.name, 
        'SavePlayer':player.saves_made, 
        'SentOff':player.sent_off, 
        'Team':player.team,
        'OffensiveValue':round(player.offensive_value/100,2),
        'DefensiveValue':round(player.defensive_value/100,2),
        'Ability':round(float(player.ability),2),
        'OffensiveAbility':round(player.offensive_ability/100,2),
        'DefensiveAbility':round(player.defensive_ability/100,2),
        'AttackAbility':round(player.attack_ability/100,2),
        'DefendAbility':round(player.defend_ability/100,2),
        'OffensiveAbilityChange':round(player.off_perf_abi_change,2), 
        'DefensiveAbilityChange':round(player.def_perf_abi_change,2), 
        'GoalOffAbilityChange':player.goal_off_abi_change, 
        'SaveDefAbilityChange':player.save_def_abi_change,
        'DefensiveRating':round(player.defensive_rating,2),
        'OffensiveRating':round(player.offensive_rating,2),
        'Substitute':player.sub_in,
        'MatchRating':round(player.match_rating,1),
        'AttackingPostionalOffensiveFactor':player.att_pos_off_factor,
        'AttackingPostionalDefensiveFactor':player.att_pos_def_factor,
        'DefendingPostionalOffensiveFactor':player.def_pos_off_factor,
        'DefendingPostionalDefensiveFactor':player.def_pos_def_factor,
        'PositionalExperience':player.current_pos_exp,
        'TeamTactics':player.team_tactics,
        'AttackIntensity':player.attack_intensity,
        'DefenceIntensity':player.defence_intensity,
        'RoutineBonus':player.routine_bonus,
        'Nervosity':player.nervosity,
        'TeamMotivation':player.team_motivation,
        'TeamMotivationChange':player.team_motivation_change,
        'MaxAttackPerformance':player.max_attack_performance,
        'MaxDefencePerformance':player.max_defence_performance,
        'AttackAreaInfluence':player.attack_area_influence,
        'DefenceAreaInfluence':player.defence_area_influence,
        'SentOffOffAbilityChange':round(player.sent_off_off_abi_change,2),
        'SentOffDefAbilityChange':round(player.sent_off_def_abi_change,2),
        'AttackAbilityChangePerformance':round(player.attack_ability_change_performance,2),
        'DefeneceAbilityChangePerformance':round(player.defence_ability_change_performance,2),
        'AttackAbilityChangeEffect':round(player.attack_ability_change_effect,2),
        'DefenceAbilityChangeEffect':round(player.defence_ability_change_effect,2)
      }

      #print(str(player.player_name) + " Round: " + str(general.current_round))
      if player.home_away == "home":
        columns_and_values_dict['AreaAttack'] = general.home_attack_area.name
        columns_and_values_dict['AreaDefence'] = general.away_attack_area.name
      elif player.home_away == "away":
        columns_and_values_dict['AreaAttack'] = general.away_attack_area.name
        columns_and_values_dict['AreaDefence'] = general.home_attack_area.name

      columns_and_values = one_dict_to_two_lists(columns_and_values_dict)

      list_of_columns = columns_and_values[0] 
      list_of_values = columns_and_values[1]

      insert_data(connection_string, table_name, list_of_columns, list_of_values)

def Full_round(general, home_team, away_team):
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

        Player.calculate_max_performance_home_attack(general)
        Player.calculate_max_performance_away_attack(general)

        #player attack and defend
        home_team.player_attack(general)   
        away_team.player_defense(general)
        
        away_team.player_attack(general)   
        home_team.player_defense(general)

        
        home_team.team_attack()
        away_team.team_defense()
        

        round_attack(home_team,away_team, general)


        away_team.team_attack()
        home_team.team_defense()
        

        round_attack(away_team,home_team, general)

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

        Round_to_db(connection_string, home_team, away_team, general)
        
        home_team.substitution()
        away_team.substitution()

def Penalties(home_team, away_team):
  #reset any sending off
  home_team.remove_sentoff()
  away_team.remove_sentoff()
  
  #initial Penalties
  initial_penalties(home_team, away_team)
  #print(str(home_team.after_penalties_score) + "-" + str(away_team.after_penalties_score))

  home_team.after_penalties_score = 1
  away_team.after_penalties_score = 1

  if home_team.after_penalties_score == away_team.after_penalties_score:
    sudden_death_penalties(home_team, away_team)

def initial_penalties(home_team, away_team):
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

def sudden_death_penalties(home_team, away_team):
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

def Full_game(connection_string):
  Player.list_of_players.clear()
  set_up = initial_set_up(connection_string)
  general = set_up[0]
  home_team = set_up[1]
  away_team = set_up[2]

  Full_round(general, home_team, away_team)

  # general.TypeOfGame = "Playoff" 
  # home_team.score = 1 
  # away_team.score = 1


  if general.TypeOfGame == "Playoff" and home_team.score == away_team.score:
    Penalties(home_team, away_team)

  Finshed_values(connection_string, general, home_team, away_team)
  #print(len(Player.list_of_players))




if __name__ == "__main__":
  Full_game(connection_string)

#Penalties()

#initial_set_up()
#Full_round()
# if __name__ == "__main__":
#   Full_game(connection_string)


#close connection to database
#c.close()
#conn.close()      
         
