import sqlite3
 

def Weekly_update(current_week):
    if current_week < 9 :
        DatabasePath = "C:\\Users\\anton\\OneDrive\\ISL_Season\\db.sqlite3"
        conn = sqlite3.connect(DatabasePath)
        c = conn.cursor()
        #Fetch all games from the previous week
        c.execute('SELECT Home,Away,GoalsHome,GoalsAway \
            FROM Season_GeneralSchedule WHERE Week = (?) AND TournamentName IS NOT "Cup"', (current_week,))
        Games = c.fetchall()

        if Games == []:
            return
        
        for g in Games:

            Home = g[0]
            Away = g[1]
            GoalsHome = g[2]
            GoalsAway = g[3] 
            #update home team wld +-
            if GoalsHome < GoalsAway:
                NewLost = 1
                NewWon = 0
                NewDrawn = 0
            elif GoalsHome > GoalsAway:
                NewLost = 0
                NewWon = 1
                NewDrawn = 0
            else:
                NewLost = 0
                NewWon = 0
                NewDrawn = 1 
            Update_teamdivisiondata(Home,NewWon,NewDrawn,NewLost,GoalsHome,GoalsAway)
            #print(Home,NewWon,NewDrawn,NewLost,GoalsHome,GoalsAway)
            #update away team wld +-
            if GoalsHome < GoalsAway:
                NewLost = 0
                NewWon = 1
                NewDrawn = 0
            elif GoalsHome > GoalsAway:
                NewLost = 1
                NewWon = 0
                NewDrawn = 0
            else:
                NewLost = 0
                NewWon = 0
                NewDrawn = 1 
            Update_teamdivisiondata(Away,NewWon,NewDrawn,NewLost,GoalsAway,GoalsHome)
            #print(Away,NewWon,NewDrawn,NewLost,GoalsAway,GoalsHome)

        #update place in each division
        for Division in range(1,7):
            Update_teamdivisiondata_place(Division)
    if current_week > 8:
        #update playoff
        PlayoffUpdate()

    # c.execute('SELECT * \
    #     FROM Season_TeamDivisionData WHERE Division = (?)', ("Div 1",))
    # DivTeams = c.fetchall()
    # print(DivTeams)
    # print()

 
def Update_teamdivisiondata(team,NewWon,NewDrawn,NewLost,NewGoalsScored,NewGoalsConceded):
    #update wdl + - but not place
    DatabasePath = "C:\\Users\\anton\\OneDrive\\ISL_Season\\db.sqlite3"
    conn = sqlite3.connect(DatabasePath)
    c = conn.cursor()
    #print(team,NewWon,NewDrawn,NewLost,NewGoalsScored,NewGoalsConceded)
    NewGoalDifference = NewGoalsScored - NewGoalsConceded
    NewPoints = NewWon * 3 + NewDrawn
    # if team == "KÄ":
    #     c.execute('SELECT * \
    #         FROM Season_TeamDivisionData WHERE Division = (?)', ("Div 1",))
    #     DivTeams = c.fetchall()
    #     print(DivTeams)
    #     print()

    c.execute('UPDATE Season_TeamDivisionData \
        SET PlayedGames = PlayedGames + 1,\
        Won = Won + (?),\
        Drawn = Drawn + (?),\
        Lost = Lost + (?),\
        GoalsScored = GoalsScored + (?),\
        GoalsConceded = GoalsConceded + (?),\
        GoalDifference = GoalDifference + (?), \
        Points = Points + (?)\
        WHERE Name = (?)', (NewWon,NewDrawn,NewLost,NewGoalsScored,NewGoalsConceded,NewGoalDifference,NewPoints,team))
    # if team == "KÄ":
    #     c.execute('SELECT * \
    #         FROM Season_TeamDivisionData WHERE Division = (?)', ("Div 1",))
    #     DivTeams = c.fetchall()
    #     print(DivTeams)
    #     print()
    conn.commit()
    c.close()

#Weekly_update(3)

def Update_teamdivisiondata_place(division):
    div = "Div " + str(division)

    DatabasePath = "C:\\Users\\anton\\OneDrive\\ISL_Season\\db.sqlite3"
    conn = sqlite3.connect(DatabasePath)
    c = conn.cursor()
    c.execute('SELECT * \
        FROM Season_TeamDivisionData WHERE Division = (?)', (div,))
    DivTeams = c.fetchall()

    if div == "Div 1":
        c.execute('SELECT * \
            FROM Season_TeamDivisionData WHERE Division = (?)', ("Div 1",))
        DivTeams = c.fetchall()
        #print(DivTeams)
        #print()
    #sort based on points, goal difference, goals scored, games won, 
    sorted_div_teams = sorted(DivTeams,key=lambda team: (team[11],team[4],team[6],team[12]),reverse = True)
    count = 1
    for team in sorted_div_teams:
        team_name = team[8]
        c.execute('UPDATE Season_TeamDivisionData \
        SET Place = (?)\
        WHERE Name = (?)', (count,team_name,))
        conn.commit()
        count += 1

    # if div == "Div 1":
    #     c.execute('SELECT * \
    #         FROM Season_TeamDivisionData WHERE Division = (?)', ("Div 1",))
    #     DivTeams = c.fetchall()
    #     print(DivTeams)
    #     print()

    c.close()


def PlayoffUpdate():
    #TablePlace update
    TablePlaceUpdate()
    
    #GameWinner update
    GameWinnerUpdate()

    #GameLooser update
    GameLooserUpdate()

    #Update TeamID
    UpdateTeamID()

def TablePlaceUpdate():
    DatabasePath = "C:\\Users\\anton\\OneDrive\\ISL_Season\\db.sqlite3"
    conn = sqlite3.connect(DatabasePath)
    c = conn.cursor()
    c.execute('SELECT GameID,TournamentName,Home,Away,SchedulingIdentifyerHome,SchedulingIdentifyerAway,QualificationHome,QualificationAway \
        FROM Season_GeneralSchedule WHERE TypeOfGame = "Playoff" AND Played = 0 AND TournamentName IS NOT "Cup" AND SchedulingIdentifyerHome = "TablePlace"')
    NotPlayed = c.fetchall()


    for Game in NotPlayed:
        GameID = Game[0]
        Division = Game[1]
        HomePlace = Game[6]
        AwayPlace = Game[7]
        HomeTeam = TablePLaceFetch(Division,HomePlace)
        AwayTeam = TablePLaceFetch(Division,AwayPlace)

        DivisionHome = Division
        DivisionAway = Division
        DivisionPlaceHome = HomePlace
        DivisionPlaceAway = AwayPlace
        DivisionPlaceDifference = 0 # Dummy 
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
        TeamRankDivisionDifference = 0 # Dummy 
        TeamRankDifference = 0 # Dummy 
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

def TablePLaceFetch(div,place):
    division = "Div " + str(div)
    DatabasePath = "C:\\Users\\anton\\OneDrive\\ISL_Season\\db.sqlite3"
    conn = sqlite3.connect(DatabasePath)
    c = conn.cursor()
    c.execute('SELECT Name \
        FROM Season_TeamDivisionData WHERE Place = (?) AND Division =(?)', (place,division))
    Team = c.fetchone()
    return Team[0]

def GameWinnerUpdate():
    DatabasePath = "C:\\Users\\anton\\OneDrive\\ISL_Season\\db.sqlite3"
    conn = sqlite3.connect(DatabasePath)
    c = conn.cursor()
    c.execute('SELECT GameID,TournamentName,Home,Away,SchedulingIdentifyerHome,SchedulingIdentifyerAway,QualificationHome,QualificationAway \
    FROM Season_GeneralSchedule  \
    WHERE TypeOfGame = "Playoff" AND Played = 0 AND TournamentName IS NOT "Cup" AND SchedulingIdentifyerHome = "GameWinner"')
    NotPlayed = c.fetchall()

    for game in NotPlayed:
        GameID = game[0]
        Division = game[1]
        HomeTeam = CheckWinner(game[6])
        HomeTeam = HomeTeam[0]
        #print(HomeTeam)
        AwayTeam = CheckWinner(game[7])
        AwayTeam = AwayTeam[0]
        #print(HomeTeam)

        DivisionHome = Division
        DivisionAway = Division
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

def CheckWinner(GameID):
    DatabasePath = "C:\\Users\\anton\\OneDrive\\ISL_Season\\db.sqlite3"
    conn = sqlite3.connect(DatabasePath)
    c = conn.cursor()
    c.execute('SELECT Winner \
        FROM Season_GeneralSchedule WHERE GameID = (?)',(GameID,))
    GameInfo = c.fetchone()
    #print("Winner" + str(GameInfo))
    return GameInfo

def GameLooserUpdate():
    DatabasePath = "C:\\Users\\anton\\OneDrive\\ISL_Season\\db.sqlite3"
    conn = sqlite3.connect(DatabasePath)
    c = conn.cursor()
    c.execute('SELECT GameID,TournamentName,Home,Away,SchedulingIdentifyerHome,SchedulingIdentifyerAway,QualificationHome,QualificationAway \
    FROM Season_GeneralSchedule  \
    WHERE TypeOfGame = "Playoff" AND Played = 0 AND TournamentName IS NOT "Cup" AND SchedulingIdentifyerHome = "GameLooser"')
    NotPlayed = c.fetchall()

    for game in NotPlayed:
        GameID = game[0]
        Division = game[1]
        HomeTeam = CheckLooser(game[6])
        #print(HomeTeam)
        #HomeTeam = HomeTeam[0]
        AwayTeam = CheckLooser(game[7])
        #print(AwayTeam)
        #AwayTeam = AwayTeam[0]

        DivisionHome = Division
        DivisionAway = Division
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

def CheckLooser(GameID):
    DatabasePath = "C:\\Users\\anton\\OneDrive\\ISL_Season\\db.sqlite3"
    conn = sqlite3.connect(DatabasePath)
    c = conn.cursor()
    c.execute('SELECT Home,Away,Winner \
        FROM Season_GeneralSchedule WHERE GameID = (?)',(GameID,))
    GameInfo = c.fetchone()
    Home = GameInfo[0]
    Away = GameInfo[1]
    Winner = GameInfo[2]

    if Home == Winner:
        #print("Looser" + str(Away))
        return Away
    else:
        #print("Looser" + str(Home))
        return Home

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

#UpdateTeamID()

#Weekly_update(1)
#print (TablePLaceupdate(1,1))

#CheckLooser(3)
#GameLooserUpdate()
#PlayoffUpdate()
#GameWinnerUpdate()
