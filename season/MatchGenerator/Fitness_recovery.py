import sqlite3
import random


if __name__ == "__main__":
  from DatabaseChanges.mysql_connector_scripts import *
  connection_string = {'host':'35.228.182.135',
                      'database':'isl',
                      'user':'admin',
                      'password':'pass123'}
else:    
    from season.MatchGenerator.DatabaseChanges.mysql_connector_scripts import *

def Recovery(connection_string,Day):


	table_name = 'season_player'
	selection_columns_list = ['id', 'Fitness']
	condition_dict = ""
	players = select_data(connection_string,selection_columns_list,table_name,condition_dict)


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



	table_name = 'season_playerfitnesslog'
	list_of_columns = ['OldFitness','FitnessChange','NewFitness','Player_id','Day','TypeOfUpdate']
	records_to_insert = To_log

	insert_many_data(connection_string, list_of_columns, records_to_insert, table_name)

	table_name = 'season_tempfitnesslog'
	insert_many_data(connection_string, list_of_columns, records_to_insert, table_name)


	#the function used for copying from another table was created to copy from another database, in this case we want to copy 
	#from the same database, but from another table
	source_database = connection_string['database']
	destination_database = source_database
	connection_string_instance = connection_string
	del connection_string_instance['database']
	source_table_name = 'season_tempfitnesslog'
	destination_table_name = 'season_player'
	source_identifier_column = 'Player_id'
	destination_identifier_column = 'id'

	connection_string['database'] = 'isl'
	change_columns_dict = {'Fitness':'NewFitness'}

	condition_dict = ''

	update_data_from_other_table(connection_string_instance, source_database, destination_database, 
    source_table_name, destination_table_name, source_identifier_column, destination_identifier_column, change_columns_dict,condition_dict)


	table_name = 'season_tempfitnesslog'
	database_name = connection_string['database']
	
	delete_data(connection_string_instance, database_name, table_name)

# Day = 1

# Recovery(connection_string,Day)