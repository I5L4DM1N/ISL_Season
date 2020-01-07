import sqlite3
import random

def Motivation_update(Day):
	DatabasePath = "C:\\Users\\anton\\OneDrive\\ISL_Season\\db.sqlite3"
	conn = sqlite3.connect(DatabasePath)
	c = conn.cursor()

	c.execute('SELECT id, PlayerMotivation FROM Season_Player')
	players = c.fetchall()

	To_log = []

	for player in players:
		ID = player[0]
		Old_motivation = round(player[1],2)

		Motivation_change = round(random.normalvariate(7.5,1.8) / 100,2)

		New_motivation = min(max(round(Old_motivation + Motivation_change,2),0),1)

		Mot_list = (Old_motivation,Motivation_change,New_motivation,ID, Day,"Dayly")
		To_log.append(Mot_list)

	#writing to motivation
	c.executemany('INSERT INTO Season_PlayerMotivationLog (OldMotivation,MotivationChange,NewMotivation,Player_id,Day,TypeOfUpdate) \
		VALUES(?,?,?,?,?,?)',
		To_log)
	conn.commit()

	#writing to temporrary motivation log
	c.executemany('INSERT INTO Season_TempMotivationLog (OldMotivation,MotivationChange,NewMotivation,Player_id,Day,TypeOfUpdate) \
		VALUES(?,?,?,?,?,?)',
		To_log)
	conn.commit()
	

	#updateing motivation for players based on the temporary motivation log
	c.execute("UPDATE Season_Player \
		SET PlayerMotivation = (SELECT NewMotivation\
						FROM Season_TempMotivationLog\
						WHERE Player_id = Season_Player.id)")

	conn.commit()

	#clearing the temporary motivation log
	Clear_table("Season_TempMotivationLog")


def Clear_table(TableName):
    #connecting with sqlite database
    DatabasePath = "C:\\Users\\anton\\OneDrive\\ISL_Season\\db.sqlite3"
    conn = sqlite3.connect(DatabasePath)
    c = conn.cursor()

    c.execute("DELETE FROM " + TableName)
    conn.commit()

    c.close()
    conn.close() 
	
#Motivation_update(1)
