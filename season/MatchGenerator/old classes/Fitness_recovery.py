import sqlite3
import random


def Recovery(Day):
	DatabasePath = "C:\\Users\\anton\\OneDrive\\ISL_Season\\db.sqlite3"
	conn = sqlite3.connect(DatabasePath)
	c = conn.cursor()

	c.execute('SELECT id, Fitness FROM Season_Player')
	players = c.fetchall()

	To_log = []

	for player in players:
		ID = player[0]
		Old_Fitness = round(player[1],2)

		if Old_Fitness == 1:
			Fitness_change = 0
			New_fitness = Old_Fitness
		else:
			Fitness_change = round(random.normalvariate(7.5,1.8) / 100,2)
			New_fitness = min(max(round(Old_Fitness + Fitness_change,2),0),1)

		Fit_list = (Old_Fitness,Fitness_change,New_fitness,ID, Day,"Dayly")
		To_log.append(Fit_list)

	#writing to fitnesslogg
	c.executemany('INSERT INTO Season_PlayerFitnessLog (OldFitness,FitnessChange,NewFitness,Player_id,Day,TypeOfUpdate) \
		VALUES(?,?,?,?,?,?)',
		To_log)
	conn.commit()

	#writing to temporrary fitness log
	c.executemany('INSERT INTO Season_TempFitnessLog (OldFitness,FitnessChange,NewFitness,PLayer_id,Day,TypeOfUpdate) \
		VALUES(?,?,?,?,?,?)',
		To_log)
	conn.commit()
	

	#updateing fitness for players based on the temporary fitness log
	c.execute("UPDATE Season_Player \
		SET Fitness = (SELECT NewFitness\
						FROM Season_TempFitnessLog\
						WHERE PLayer_id = Season_Player.id)")

	conn.commit()

	#clearing the temporary fitness log
	Clear_table("Season_TempFitnessLog")


def Clear_table(TableName):
    #connecting with sqlite database
    DatabasePath = "C:\\Users\\anton\\OneDrive\\ISL_Season\\db.sqlite3"
    conn = sqlite3.connect(DatabasePath)
    c = conn.cursor()

    c.execute("DELETE FROM " + TableName)
    conn.commit()

    c.close()
    conn.close() 

#Season_TempFitnessLog
#Recovery(1)
#Clear_table("Season_TempFitnessLog")

#Dummyfitness()
#Recovery()
