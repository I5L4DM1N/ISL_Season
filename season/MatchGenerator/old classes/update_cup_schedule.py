import sqlite3

def CupUpdate():
    DatabasePath = "C:\\Users\\anton\\OneDrive\\ISL_Season\\db.sqlite3"
    conn = sqlite3.connect(DatabasePath)
    c = conn.cursor()
    #Fetching all cup games that haven't been played yet
    c.execute('SELECT GameID,Home,Away,SchedulingIdentifyerHome,SchedulingIdentifyerAway,QualificationHome,QualificationAway \
        FROM Season_GeneralSchedule WHERE Played = 0 AND TournamentName = "Cup"')
    NotPlayed = c.fetchall()


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
                    GameInfo = CheckWinner(QualHome)
                    HomeTeam = GameInfo[0]
                    Played = GameInfo[1]
                    if Played == 0:
                        break
            else:
                HomeTeam = Home
            if SchedIDAway == "GameWinner":
                GameInfo = CheckWinner(QualAway)
                AwayTeam = GameInfo[0]
                Played = GameInfo[1]
                if Played == 0:
                    break
            else:
                AwayTeam = Away

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

            c.execute('UPDATE Season_GeneralSchedule SET \
                Home = (?),\
                Away = (?),\
                DivisionHome = (?),\
                DivisionAway = (?),\
                DivisionPlaceHome = (?),\
                DivisionPlaceAway = (?),\
                DivisionPlaceDifference = (?),\
                FavouriteStatusAway = (?),\
                FavouriteStatusHome = (?),\
                FocusedEvent = (?),\
                PrestigeCupAway = (?),\
                PrestigeCupHome = (?),\
                PrestigePointsBasic = (?),\
                PrestigePointsDivisionBasic = (?),\
                PrestigePointsFocusedEvent = (?),\
                PrestigePointsRivalryAway = (?),\
                PrestigePointsRivalryHome = (?),\
                PrestigePointsTotalAway = (?),\
                PrestigePointsTotalHome = (?),\
                RoutinePoints = (?),\
                TeamMotivationAway = (?),\
                TeamMotivationFavouriteStatusAway = (?),\
                TeamMotivationFavouriteStatusHome = (?),\
                TeamMotivationHome = (?),\
                TeamMotivationPreviousRoundAway = (?),\
                TeamMotivationPreviousRoundHome = (?),\
                TeamMotivationSituationAway = (?),\
                TeamMotivationSituationHome = (?),\
                TeamRankHome = (?),\
                TeamRankAway = (?),\
                TeamRankDivisionHome = (?),\
                TeamRankDivisionAway = (?),\
                TeamRankDivisionDifference = (?),\
                TeamRankDifference = (?),\
                TeamRivalryHome = (?),\
                TeamRivalryAway = (?),\
                TeamRivalryTotal = (?),\
                TeamTacticsValueHome = (?),\
                TeamTacticsValueAway = (?),\
                TeamTacticsGameValueHome = (?),\
                TeamTacticsGameValueAway = (?),\
                TeamTacticsHome = (?),\
                TeamTacticsAway = (?)\
                WHERE GameID = (?)',\
                (HomeTeam,AwayTeam,DivisionHome, DivisionAway, DivisionPlaceHome, DivisionPlaceAway, DivisionPlaceDifference, FavouriteStatusAway, FavouriteStatusHome, FocusedEvent, PrestigeCupAway, PrestigeCupHome, PrestigePointsBasic, PrestigePointsDivisionBasic, PrestigePointsFocusedEvent, PrestigePointsRivalryAway, PrestigePointsRivalryHome, PrestigePointsTotalAway, PrestigePointsTotalHome, RoutinePoints, TeamMotivationAway, TeamMotivationFavouriteStatusAway, TeamMotivationFavouriteStatusHome, TeamMotivationHome, TeamMotivationPreviousRoundAway, TeamMotivationPreviousRoundHome, TeamMotivationSituationAway, TeamMotivationSituationHome, TeamRankHome, TeamRankAway, TeamRankDivisionHome, TeamRankDivisionAway, TeamRankDivisionDifference, TeamRankDifference, TeamRivalryHome, TeamRivalryAway, TeamRivalryTotal, TeamTacticsValueHome, TeamTacticsValueAway, TeamTacticsGameValueHome, TeamTacticsGameValueAway, TeamTacticsHome, TeamTacticsAway, GameID,))
            conn.commit()
    c.close()


    UpdateTeamID()

            #print(HomeTeam,AwayTeam)




def CheckWinner(GameID):
    DatabasePath = "C:\\Users\\anton\\OneDrive\\ISL_Season\\db.sqlite3"
    conn = sqlite3.connect(DatabasePath)
    c = conn.cursor()
    c.execute('SELECT Winner,Played \
        FROM Season_GeneralSchedule WHERE GameID = (?)',(GameID,))
    GameInfo = c.fetchone()
    return GameInfo
        


def UpdateTeamID():
    DatabasePath = "C:\\Users\\anton\\OneDrive\\ISL_Season\\db.sqlite3"
    conn = sqlite3.connect(DatabasePath)
    c = conn.cursor()

    #updateing Team ID
    c.execute("UPDATE Season_GeneralSchedule \
        SET HomeTeam_id = (SELECT id\
                        FROM Season_Team\
                        WHERE Home = Season_Team.Name)")

    #updateing Team ID - Away
    c.execute("UPDATE Season_GeneralSchedule \
        SET AwayTeam_id = (SELECT id\
                        FROM Season_Team\
                        WHERE Away = Season_Team.Name)")

    conn.commit()
    c.close()

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
