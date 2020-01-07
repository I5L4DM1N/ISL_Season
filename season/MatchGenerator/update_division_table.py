if __name__ == "__main__":
  from DatabaseChanges.mysql_connector_scripts import *
  connection_string = {'host':'35.228.182.135',
                      'database':'isl',
                      'user':'admin',
                      'password':'pass123'}
else:    
    from season.MatchGenerator.DatabaseChanges.mysql_connector_scripts import *



def weekly_update(connection_string, current_week):
    if current_week < 9 :
        table_name = 'season_generalschedule'
        selection_columns_list = ['home','away','goals_home','goals_away']
        condition_dict = {'Week':current_week, 'TournamentName':['1','2','3','4','5','6']}
        games = select_data(connection_string,selection_columns_list,table_name,condition_dict)

        if games == []:
            return
        
        for g in games:

            home = g[0]
            away = g[1]
            goals_home = g[2]
            goals_away = g[3] 
            #update home team wld +-
            if goals_home < goals_away:
                new_lost = 1
                new_won = 0
                new_drawn = 0
            elif goals_home > goals_away:
                new_lost = 0
                new_won = 1
                new_drawn = 0
            else:
                new_lost = 0
                new_won = 0
                new_drawn = 1 
            update_teamdivisiondata(home,new_won,new_drawn,new_lost,goals_home,goals_away)
            #print(home,new_won,new_drawn,new_lost,goals_home,goals_away)
            #update away team wld +-
            if goals_home < goals_away:
                new_lost = 0
                new_won = 1
                new_drawn = 0

            elif goals_home > goals_away:
                new_lost = 1
                new_won = 0
                new_drawn = 0
            else:
                new_lost = 0
                new_won = 0
                new_drawn = 1 
            update_teamdivisiondata(away,new_won,new_drawn,new_lost,goals_away,goals_home)
            #print(away,new_won,new_drawn,new_lost,goals_away,goals_home)

        #update place in each division
        for division in range(1,7):
            update_teamdivisiondata_place(division)
    if current_week > 8:
        #update playoff
        play_off_update()




 
def update_teamdivisiondata(connection_string,team,new_won,new_drawn,new_lost,new_goals_scored,new_goals_conceded):
    #update wdl + - but not place


    new_goal_difference = new_goals_scored - new_goals_conceded
    new_points = new_won * 3 + new_drawn

    destination_database = connection_string['database']
    table_name = 'season_teamdivisiondata'
    columns_and_input = {
        'PlayedGames':'increment1',
        'Won':new_won,
        'Drawn':new_drawn,
        'Lost':new_lost,
        'GoalsScored':new_goals_scored,
        'GoalsConceded':new_goals_conceded,
        'GoalDifference':new_goal_difference,
        'Points':new_points
        }
    condition_dict = {'Name':team}
    
    update_data(connection_string, destination_database, table_name, columns_and_input, condition_dict)



# team = 'SL'
# new_won = 1
# new_drawn = 0
# new_lost = 0
# new_goals_scored = 3
# new_goals_conceded = 1

# Update_teamdivisiondata(connection_string,team,new_won,new_drawn,new_lost,new_goals_scored,new_goals_conceded)

def update_teamdivisiondata_place(connection_string, division):
    div = "Div " + str(division)

    table_name = 'season_teamdivisiondata'
    selection_columns_list = ['Name', 'Points', 'GoalDifference', 'GoalsScored', 'Won']
    condition_dict = {'division':div}
    DivTeams = select_data(connection_string,selection_columns_list,table_name,condition_dict)


    #sort based on points, goal difference, goals scored, games won, 
    sorted_div_teams = sorted(DivTeams,key=lambda team: (team[1],team[2],team[3],team[4]),reverse = True)
    count = 1
    for team in sorted_div_teams:
        team_name = team[0]
        destination_database = connection_string['database']
        table_name = 'season_teamdivisiondata'
        columns_and_input = {'Place':count}
        condition_dict = {'Name':team_name}
        
        update_data(connection_string, destination_database, table_name, columns_and_input, condition_dict)
        count += 1

# division = 1
# Update_teamdivisiondata_place(connection_string, division)

def play_off_update(connection_string):
    #TablePlace update
    table_place_update(connection_string)
    
    #GameWinner update
    game_winner_loser_update(connection_string, 'winner')

    #GameLooser update
    game_winner_loser_update(connection_string, 'loser')

    #Update TeamID
    update_team_id(connection_string)

def table_place_update(connection_string):
    table_name = 'season_generalschedule'
    selection_columns_list = ['GameID','TournamentName','home','away','SchedulingIdentifyerhome','SchedulingIdentifyeraway','Qualificationhome','Qualificationaway']
    condition_dict = {'TypeOfGame':'Playoff', 'Played':0, 'SchedulingIdentifyerhome':'TablePlace', 'TournamentName':['1','2','3','4','5','6']}
    NotPlayed = select_data(connection_string,selection_columns_list,table_name,condition_dict)


    destination_database = connection_string['database']
    table_name = 'season_teamdivisiondata'

    for Game in NotPlayed:
        GameID = Game[0]
        division = Game[1]
        homePlace = Game[6]
        awayPlace = Game[7]
        homeTeam = table_pLace_fetch(division,homePlace)
        awayTeam = table_pLace_fetch(division,awayPlace)

        divisionhome = division
        divisionaway = division
        divisionPlacehome = homePlace
        divisionPlaceaway = awayPlace
        divisionPlaceDifference = 0 # Dummy 
        FavouriteStatusaway = "Normal" #Dummy
        FavouriteStatushome = "Normal" #Dummy 
        FocusedEvent = ""
        PrestigeCupaway = 0 #Dummy
        PrestigeCuphome = 0 #Dummy
        PrestigePointsBasic = 0 #Dummy
        PrestigePointsdivisionBasic = 0 #Dummy
        PrestigePointsFocusedEvent = 0 #Dummy
        PrestigePointsRivalryaway = 0 #Dummy
        PrestigePointsRivalryhome = 0 #Dummy
        PrestigePointsTotalaway = 0 #Dummy
        PrestigePointsTotalhome = 0 #Dummy
        RoutinePoints = 0 #Dummy
        TeamMotivationaway = 1 #Dummy
        TeamMotivationFavouriteStatusaway = 1 #Dummy
        TeamMotivationFavouriteStatushome = 1 #Dummy
        TeamMotivationhome = 1 #Dummy
        TeamMotivationPreviousRoundaway = 1 #Dummy
        TeamMotivationPreviousRoundhome = 1 #Dummy
        TeamMotivationSituationaway = 0 #Dummy
        TeamMotivationSituationhome = 0 #Dummy
        TeamRankhome = 30 #Dummy
        TeamRankaway = 30 #Dummy
        TeamRankdivisionhome = 5 #Dummy
        TeamRankdivisionaway = 5 #Dummy
        TeamRankdivisionDifference = 0 # Dummy 
        TeamRankDifference = 0 # Dummy 
        TeamRivalryhome = 0 #Dummy
        TeamRivalryaway = 0 #Dummy
        TeamRivalryTotal = 0 #Dummy
        TeamTacticsValuehome = 0.5 #Dummy
        TeamTacticsValueaway = 0.5 #Dummy
        TeamTacticsGameValuehome = 0.5 #Dummy
        TeamTacticsGameValueaway = 0.5 #Dummy
        TeamTacticshome = "Balanced" #Dummy
        TeamTacticsaway = "Balanced" #Dummy


        columns_and_input = {
            'home':homeTeam,
            'away':awayTeam,
            'divisionhome':divisionhome, 
            'divisionaway':divisionaway, 
            'divisionPlacehome':divisionPlacehome, 
            'divisionPlaceaway':divisionPlaceaway, 
            'divisionPlaceDifference':divisionPlaceDifference, 
            'FavouriteStatusaway':FavouriteStatusaway, 
            'FavouriteStatushome':FavouriteStatushome, 
            'FocusedEvent':FocusedEvent, 
            'PrestigeCupaway':PrestigeCupaway, 
            'PrestigeCuphome':PrestigeCuphome, 
            'PrestigePointsBasic':PrestigePointsBasic, 
            'PrestigePointsdivisionBasic':PrestigePointsdivisionBasic, 
            'PrestigePointsFocusedEvent':PrestigePointsFocusedEvent, 
            'PrestigePointsRivalryaway':PrestigePointsRivalryaway, 
            'PrestigePointsRivalryhome':PrestigePointsRivalryhome, 
            'PrestigePointsTotalaway':PrestigePointsTotalaway, 
            'PrestigePointsTotalhome':PrestigePointsTotalhome, 
            'RoutinePoints':RoutinePoints, 
            'TeamMotivationaway':TeamMotivationaway, 
            'TeamMotivationFavouriteStatusaway':TeamMotivationFavouriteStatusaway, 
            'TeamMotivationFavouriteStatushome':TeamMotivationFavouriteStatushome, 
            'TeamMotivationhome':TeamMotivationhome, 
            'TeamMotivationPreviousRoundaway':TeamMotivationPreviousRoundaway, 
            'TeamMotivationPreviousRoundhome':TeamMotivationPreviousRoundhome, 
            'TeamMotivationSituationaway':TeamMotivationSituationaway, 
            'TeamMotivationSituationhome':TeamMotivationSituationhome, 
            'TeamRankhome':TeamRankhome, 
            'TeamRankaway':TeamRankaway, 
            'TeamRankdivisionhome':TeamRankdivisionhome, 
            'TeamRankdivisionaway':TeamRankdivisionaway, 
            'TeamRankdivisionDifference':TeamRankdivisionDifference, 
            'TeamRankDifference':TeamRankDifference, 
            'TeamRivalryhome':TeamRivalryhome, 
            'TeamRivalryaway':TeamRivalryaway, 
            'TeamRivalryTotal':TeamRivalryTotal, 
            'TeamTacticsValuehome':TeamTacticsValuehome, 
            'TeamTacticsValueaway':TeamTacticsValueaway, 
            'TeamTacticsGameValuehome':TeamTacticsGameValuehome, 
            'TeamTacticsGameValueaway':TeamTacticsGameValueaway, 
            'TeamTacticshome':TeamTacticshome, 
            'TeamTacticsaway':TeamTacticsaway
        }
        condition_dict = {'GameID':GameID}
        
        update_data(connection_string, destination_database, table_name, columns_and_input, condition_dict)

def table_pLace_fetch(connection_string,div,place):
    division = "Div " + str(div)
    table_name = 'season_teamdivisiondata'
    selection_columns_list = ['Name']
    condition_dict = {'Place':place, 'division':division}
    Team = select_data(connection_string,selection_columns_list,table_name,condition_dict)
    return Team[0]

def game_winner_loser_update(connection_string, winner_or_loser):

    if winner_or_loser == 'winner':
        game_winner_or_loser = 'GameWinner'
    else:
        game_winner_or_loser = 'GameLooser'
    table_name = 'season_generalschedule'
    selection_columns_list = ['GameID','TournamentName','home','away','SchedulingIdentifyerhome','SchedulingIdentifyeraway','Qualificationhome','Qualificationaway']
    condition_dict = {'TypeOfGame':'Playoff', 'Played':0, 'SchedulingIdentifyerhome':game_winner_or_loser, 'TournamentName':['1','2','3','4','5','6']}
    NotPlayed = select_data(connection_string,selection_columns_list,table_name,condition_dict)


    destination_database = connection_string['database']
    table_name = 'season_generalschedule'

    for game in NotPlayed:
        GameID = game[0]
        division = game[1]
        if winner_or_loser == 'winner':
            homeTeam = check_winner(connection_string, game[6])
        else:
            homeTeam = check_loser(connection_string, game[6])
        homeTeam = homeTeam[0]
        #print(homeTeam)
        if winner_or_loser == 'winner':
            homeTeam = check_winner(connection_string, game[7])
        else:
            homeTeam = check_loser(connection_string, game[7])
        awayTeam = awayTeam[0]
        #print(homeTeam)

        divisionhome = division
        divisionaway = division
        divisionPlacehome = 5 #Dummy
        divisionPlaceaway = 5 #Dummy
        divisionPlaceDifference = divisionPlacehome - divisionPlaceaway #Not relevant for cup games? 
        FavouriteStatusaway = "Normal" #Dummy
        FavouriteStatushome = "Normal" #Dummy 
        FocusedEvent = ""
        PrestigeCupaway = 0 #Dummy
        PrestigeCuphome = 0 #Dummy
        PrestigePointsBasic = 0 #Dummy
        PrestigePointsdivisionBasic = 0 #Dummy
        PrestigePointsFocusedEvent = 0 #Dummy
        PrestigePointsRivalryaway = 0 #Dummy
        PrestigePointsRivalryhome = 0 #Dummy
        PrestigePointsTotalaway = 0 #Dummy
        PrestigePointsTotalhome = 0 #Dummy
        RoutinePoints = 0 #Dummy
        TeamMotivationaway = 1 #Dummy
        TeamMotivationFavouriteStatusaway = 1 #Dummy
        TeamMotivationFavouriteStatushome = 1 #Dummy
        TeamMotivationhome = 1 #Dummy
        TeamMotivationPreviousRoundaway = 1 #Dummy
        TeamMotivationPreviousRoundhome = 1 #Dummy
        TeamMotivationSituationaway = 0 #Dummy
        TeamMotivationSituationhome = 0 #Dummy
        TeamRankhome = 30 #Dummy
        TeamRankaway = 30 #Dummy
        TeamRankdivisionhome = 5 #Dummy
        TeamRankdivisionaway = 5 #Dummy
        TeamRankdivisionDifference = TeamRankdivisionhome - TeamRankdivisionaway # Not relevant for Cup games? 
        TeamRankDifference = TeamRankhome - TeamRankaway
        TeamRivalryhome = 0 #Dummy
        TeamRivalryaway = 0 #Dummy
        TeamRivalryTotal = 0 #Dummy
        TeamTacticsValuehome = 0.5 #Dummy
        TeamTacticsValueaway = 0.5 #Dummy
        TeamTacticsGameValuehome = 0.5 #Dummy
        TeamTacticsGameValueaway = 0.5 #Dummy
        TeamTacticshome = "Balanced" #Dummy
        TeamTacticsaway = "Balanced" #Dummy

        columns_and_input = {
            'home':homeTeam,
            'away':awayTeam,
            'divisionhome':divisionhome,
            'divisionaway':divisionaway,
            'divisionPlacehome':divisionPlacehome,
            'divisionPlaceaway':divisionPlaceaway,
            'divisionPlaceDifference':divisionPlaceDifference,
            'FavouriteStatusaway':FavouriteStatusaway,
            'FavouriteStatushome':FavouriteStatushome,
            'FocusedEvent':FocusedEvent,
            'PrestigeCupaway':PrestigeCupaway,
            'PrestigeCuphome':PrestigeCuphome,
            'PrestigePointsBasic':PrestigePointsBasic,
            'PrestigePointsdivisionBasic':PrestigePointsdivisionBasic,
            'PrestigePointsFocusedEvent':PrestigePointsFocusedEvent,
            'PrestigePointsRivalryaway':PrestigePointsRivalryaway,
            'PrestigePointsRivalryhome':PrestigePointsRivalryhome,
            'PrestigePointsTotalaway':PrestigePointsTotalaway,
            'PrestigePointsTotalhome':PrestigePointsTotalhome,
            'RoutinePoints':RoutinePoints,
            'TeamMotivationaway':TeamMotivationaway,
            'TeamMotivationFavouriteStatusaway':TeamMotivationFavouriteStatusaway,
            'TeamMotivationFavouriteStatushome':TeamMotivationFavouriteStatushome,
            'TeamMotivationhome':TeamMotivationhome,
            'TeamMotivationPreviousRoundaway':TeamMotivationPreviousRoundaway,
            'TeamMotivationPreviousRoundhome':TeamMotivationPreviousRoundhome,
            'TeamMotivationSituationaway':TeamMotivationSituationaway,
            'TeamMotivationSituationhome':TeamMotivationSituationhome,
            'TeamRankhome':TeamRankhome,
            'TeamRankaway':TeamRankaway,
            'TeamRankdivisionhome':TeamRankdivisionhome,
            'TeamRankdivisionaway':TeamRankdivisionaway,
            'TeamRankdivisionDifference':TeamRankdivisionDifference,
            'TeamRankDifference':TeamRankDifference,
            'TeamRivalryhome':TeamRivalryhome,
            'TeamRivalryaway':TeamRivalryaway,
            'TeamRivalryTotal':TeamRivalryTotal,
            'TeamTacticsValuehome':TeamTacticsValuehome,
            'TeamTacticsValueaway':TeamTacticsValueaway,
            'TeamTacticsGameValuehome':TeamTacticsGameValuehome,
            'TeamTacticsGameValueaway':TeamTacticsGameValueaway,
            'TeamTacticshome':TeamTacticshome,
            'TeamTacticsawa':TeamTacticsaway,
        }

        condition_dict = {'GameID':GameID}
        
        update_data(connection_string, destination_database, table_name, columns_and_input, condition_dict)


def check_winner(connection_string, GameID):
    table_name = 'season_generalschedule'
    selection_columns_list = ['Winner']
    condition_dict = {'GameID':GameID}
    GameInfo = select_data(connection_string,selection_columns_list,table_name,condition_dict)
    return GameInfo

def check_loser(connection_string, GameID):   
    table_name = 'season_generalschedule'
    selection_columns_list = ['home', 'away', 'Winner']
    condition_dict = {'GameID':GameID}
    game_info = select_data(connection_string,selection_columns_list,table_name,condition_dict)
    
    home = game_info[0]
    away = game_info[1]
    winner = game_info[2]

    if home == winner:
        #print("Looser" + str(away))
        return away
    else:
        #print("Looser" + str(home))
        return home


def update_team_id(connection_string):
    connection_string_instance = connection_string
    del connection_string_instance['database']
    source_database = 'isl'
    destination_database = 'isl'
    source_table_name = 'season_team'
    destination_table_name = 'season_generalschedule'
    source_identifier_column = 'home'
    destination_identifier_column = 'Name'
    change_columns_dict = {'homeTeam_id':'id'}
    condition_dict = ""


    update_data_from_other_table(connection_string_instance, source_database, destination_database, 
    source_table_name, destination_table_name, source_identifier_column, destination_identifier_column, 
    change_columns_dict,condition_dict)

    source_identifier_column = 'away'
    change_columns_dict = {'awayTeam_id':'id'}

    update_data_from_other_table(connection_string_instance, source_database, destination_database, 
    source_table_name, destination_table_name, source_identifier_column, destination_identifier_column, 
    change_columns_dict,condition_dict)

#UpdateTeamID()

#Weekly_update(1)
#print (TablePLaceupdate(1,1))

#CheckLooser(3)
#GameLooserUpdate()
#PlayoffUpdate()
#GameWinnerUpdate()
