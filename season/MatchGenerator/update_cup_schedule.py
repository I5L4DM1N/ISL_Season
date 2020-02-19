import sqlite3
if __name__ == "__main__":
  from DatabaseChanges.mysql_connector_scripts import *
  from update_division_table import *
  connection_string = {
    'host': os.environ.get('DB_HOST'),
    'database':'isl',
    'user': os.environ.get('DB_USER'),
    'password':os.environ.get('DB_PASS'),
    'ssl_ca': os.environ.get('SSL_CA_DIR'),
    'ssl_cert': os.environ.get('SSL_CERT_DIR'),
    'ssl_key': os.environ.get('SSL_KEY_DIR')
    }
else:    
    from season.MatchGenerator.DatabaseChanges.mysql_connector_scripts import *
    from season.MatchGenerator.update_division_table import *


def cup_cupdate(connection_string):

    table_name = 'season_generalschedule'
    selection_columns_list = ['GameID','Home','Away','SchedulingIdentifyerHome','SchedulingIdentifyerAway','QualificationHome','QualificationAway']
    condition_dict = {'Played':0, 'TournamentName':'Cup'}
    NotPlayed = select_data(connection_string,selection_columns_list,table_name,condition_dict)


    for Game in NotPlayed:
        GameID = Game[0]
        Home = Game[1]
        Away = Game[2]
        if Away == "":
            SchedIDHome = Game[3]
            SchedIDAway = Game[4]
            QualHome = Game[5]
            QualAway = Game[6]
            if Home =="":
                if SchedIDHome == "GameWinner":
                    GameInfo = check_winner(connection_string, QualHome)
                    HomeTeam = GameInfo[0]
                    Played = GameInfo[1]
                    if Played == 0:
                        break
            else:
                HomeTeam = Home
            if SchedIDAway == "GameWinner":
                GameInfo = check_winner(connection_string, QualHome)
                AwayTeam = GameInfo[0]
                Played = GameInfo[1]
                if Played == 0:
                    break
            else:
                AwayTeam = Away

            destination_database = connection_string['database']
            table_name = 'season_generalschedule'

            DivisionHome = 5 #Dummy
            DivisionAway = 5 #Dummy
            DivisionPlaceHome = 5 #Dummy
            DivisionPlaceAway = 5 #Dummy
            DivisionPlaceDifference = DivisionPlaceHome - DivisionPlaceAway #Not relevant for cup games? 
            FavouriteStatusAway = "Normal" #Dummy
            FavouriteStatusHome = "Normal" #Dummy 
            FocusedEvent = ""
            PrestigeCupAway = 0 #Dummy
            PrestigeCupHome = 0 #Dummy
            PrestigePointsBasic = 0 #Dummy
            PrestigePointsDivisionBasic = 0 #Dummy
            PrestigePointsFocusedEvent = 0 #Dummy
            PrestigePointsRivalryAway = 0 #Dummy
            PrestigePointsRivalryHome = 0 #Dummy
            PrestigePointsTotalAway = 0 #Dummy
            PrestigePointsTotalHome = 0 #Dummy
            RoutinePoints = 0 #Dummy
            TeamMotivationAway = 1 #Dummy
            TeamMotivationFavouriteStatusAway = 1 #Dummy
            TeamMotivationFavouriteStatusHome = 1 #Dummy
            TeamMotivationHome = 1 #Dummy
            TeamMotivationPreviousRoundAway = 1 #Dummy
            TeamMotivationPreviousRoundHome = 1 #Dummy
            TeamMotivationSituationAway = 0 #Dummy
            TeamMotivationSituationHome = 0 #Dummy
            TeamRankHome = 30 #Dummy
            TeamRankAway = 30 #Dummy
            TeamRankDivisionHome = 5 #Dummy
            TeamRankDivisionAway = 5 #Dummy
            TeamRankDivisionDifference = TeamRankDivisionHome - TeamRankDivisionAway # Not relevant for Cup games? 
            TeamRankDifference = TeamRankHome - TeamRankAway
            TeamRivalryHome = 0 #Dummy
            TeamRivalryAway = 0 #Dummy
            TeamRivalryTotal = 0 #Dummy
            TeamTacticsValueHome = 0.5 #Dummy
            TeamTacticsValueAway = 0.5 #Dummy
            TeamTacticsGameValueHome = 0.5 #Dummy
            TeamTacticsGameValueAway = 0.5 #Dummy
            TeamTacticsHome = "Balanced" #Dummy
            TeamTacticsAway = "Balanced" #Dummy

            columns_and_input = {
                'Home':HomeTeam,    
                'Away':AwayTeam,    
                'Divisionhome':Divisionhome,    
                'Divisionaway':Divisionaway,    
                'DivisionPlacehome':DivisionPlacehome,  
                'DivisionPlaceaway':DivisionPlaceaway,  
                'DivisionPlaceDifference':DivisionPlaceDifference,  
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


    update_team_id(connection_string)





    #c.close()

#CupUpdate()
#updatera lag för kommande matcher

#uppdatera favourite status
#focused event
#prestige
#routine
#team motivation
#rank
#rivalry
#tactics
