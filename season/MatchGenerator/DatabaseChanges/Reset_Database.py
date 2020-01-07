import sqlite3
if __name__ == "__main__":
    import Recover_Database
else:    
    from season.MatchGenerator.DatabaseChanges import Recover_Database
#import Recover_Database

def Clear_table(TableName):
    #connecting with sqlite database
    DatabasePath = "C:\\Users\\ASV11691\\OneDrive\\ISL_Season\\db.sqlite3"
    conn = sqlite3.connect(DatabasePath)
    c = conn.cursor()

    c.execute("DELETE FROM " + TableName)
    conn.commit()

    c.close()
    conn.close()  

def AddPrefix(TableList):
    li_counter = 0
    for table in TableList:
        NewTable = "Season_"+table
        TableList[li_counter] = NewTable
        li_counter +=1

    return TableList

def ClearMulipleTables():
    ListOfTables = [
    "GamePlayerLog",
    "GameTeamLog",
    "GamePenaltiesLog",
    "PlayerMotivationLog",
    "PlayerFitnessLog",
    "PlayerAbilityLog",
    "TeamMotivationLog",
    "Team",
    "Player",
    "GeneralSchedule",
    "TeamDivisionData",
    "DayTable",
    "TeamInfo"
    ]

    TableList = AddPrefix(ListOfTables)

    for table in TableList:
        Clear_table(table)


def RecoverMulipleTables():
    ListOfTables = [
    "Player",
    "Team",
    "GeneralSchedule",
    "TeamDivisionData",
    "DayTable",
    "TeamInfo"
    ]

    TableList = AddPrefix(ListOfTables)
    
    Path = "C:\\Users\\ASV11691\\OneDrive\\ISL_Season\\Workfiles\\Back-up\\"

    for table in TableList:
        Recover_Database.Fill_table_from_CSV(Path,table,";")
        #Fill_table_from_CSV(Path,table,";")
def ReSetAll():
    ClearMulipleTables()
    RecoverMulipleTables()
    ChangeToNullValue()


def ExportMultipleTables():
    ListOfTables = [
    "Player",
    "Team",
    "GeneralSchedule",
    "TeamDivisionData",
    "DayTable",
    "TeamInfo"
    ]

    TableList = AddPrefix(ListOfTables)
    
    
    #Path = "C:\\Users\\ASV11691\\OneDrive\\ISL_Season\\Workfiles\\Back-up\\"

    for table in TableList:
        Recover_Database.Export_sqlite_to_CSV(table,";")
    
#ExportMultipleTables()


def BlankToNull(Table,Column):
    DatabasePath = "C:\\Users\\ASV11691\\OneDrive\\ISL_Season\\db.sqlite3"
    conn = sqlite3.connect(DatabasePath)
    c = conn.cursor()
    NewValue = None
    Value = ""
    c.execute("UPDATE " + Table + " SET " + Column + " = (?) WHERE " + Column + " = (?)",(NewValue, Value))
    conn.commit()

    c.close()
    conn.close()  


def ChangeToNullValue():
    #In order to be able to use optional values in foreign key fields will blank values have to be set to Null in SQL.
    #(When importing from CSV are values set to a blank string")
    #This function will convert blank strings to Null values in the SQL-database
    #Entering Tables as key and columns as values
    TablesAndColumns = {"season_GeneralSchedule":["AwayTeam_id", "HomeTeam_id"],"season_teaminfo":["team_id"] }
    for Table, Columns in TablesAndColumns.items():
        for Column in Columns:
            BlankToNull(Table, Column)


if __name__ == "__main__":
    ReSetAll()
 

#reset
#Player
#GeneralSchedule
#GeneralTeam
#TeamDivisionData

#close connection to database

