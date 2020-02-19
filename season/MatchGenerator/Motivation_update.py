import random
import os

if __name__ == "__main__":
  from DatabaseChanges.mysql_connector_scripts import *
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

def Motivation_update(connection_string, Day):

	table_name = 'season_player'
	selection_columns_list = ['id', 'PlayerMotivation']
	condition_dict = ""
	players = select_data(connection_string,selection_columns_list,table_name,condition_dict)

	To_log = []

	for player in players:
		ID = player[0]
		Old_motivation = round(player[1],2)

		Motivation_change = round(random.normalvariate(7.5,1.8) / 100,2)

		New_motivation = min(max(round(Old_motivation + Motivation_change,2),0),1)

		Mot_list = (Old_motivation,Motivation_change,New_motivation,ID, Day,"Dayly")
		To_log.append(Mot_list)

	#print(To_log)

	table_name = 'season_playermotivationlog'
	list_of_columns = ['OldMotivation','MotivationChange','NewMotivation','Player_id','Day','TypeOfUpdate']
	records_to_insert = To_log

	insert_many_data(connection_string, list_of_columns, records_to_insert, table_name)

	table_name = 'season_tempmotivationlog'
	insert_many_data(connection_string, list_of_columns, records_to_insert, table_name)

	#the function used for copying from another table was created to copy from another database, in this case we want to copy 
	#from the same database, but from another table
	source_database = connection_string['database']
	destination_database = source_database
	connection_string_instance = connection_string
	del connection_string_instance['database']
	source_table_name = 'season_tempmotivationlog'
	destination_table_name = 'season_player'
	source_identifier_column = 'Player_id'
	destination_identifier_column = 'id'

	connection_string['database'] = 'isl'
	change_columns_dict = {'PlayerMotivation':'NewMotivation'}

	condition_dict = ''

	update_data_from_other_table(connection_string_instance, source_database, destination_database, 
    source_table_name, destination_table_name, source_identifier_column, destination_identifier_column, change_columns_dict,condition_dict)


	table_name = 'season_tempmotivationlog'
	database_name = connection_string['database']
	
	delete_data(connection_string_instance, database_name, table_name)



# Day = 1

# Motivation_update(connection_string, Day)
