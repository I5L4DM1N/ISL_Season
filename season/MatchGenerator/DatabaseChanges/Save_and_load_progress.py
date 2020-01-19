#import mysql_connector_scripts
from datetime import datetime
import os

if __name__ == "__main__":
  from mysql_connector_scripts import *
else:    
    from season.MatchGenerator.team import *
    from season.MatchGenerator.DatabaseChanges.mysql_connector_scripts import *

connection_string = {
	'host': os.environ.get('DB_HOST'),
	'database':'isl',
	'user': os.environ.get('DB_USER'),
	'password':os.environ.get('DB_PASS'),
	}


connection_string_destination = {
								'host': os.environ.get('DB_HOST'),
								'database':'isl_save',
								'user': os.environ.get('DB_USER'),
								'password':os.environ.get('DB_PASS')
	                    		}

connection_string_source = {
							'host': os.environ.get('DB_HOST'),
							'database':'isl',
							'user': os.environ.get('DB_USER'),
							'password':os.environ.get('DB_PASS')
							}

connection_string_instance = {
							'host': os.environ.get('DB_HOST'),
							'user': os.environ.get('DB_USER'),
							'password':os.environ.get('DB_PASS')
							}

source_database = 'isl'
destination_database = 'isl_save'


list_of_tables = [
#('season_nation',),	#No Change - Constant
('season_team',),	#Update
('season_player',), #Update
#('season_tournament',), #No Change - Constant
('season_daytable',),	#Update
('season_gamepenaltieslog',), #Insert
#('season_playerinfo',), #NUpdate root
#('season_playertransfer',),	#Constant
#('season_teamprevdiv',), #Constant
('season_playerabilitylog',), #Insert
('season_teammotivationlog',), #Insert
('season_playerfitnesslog',), #Insert
('season_tempfitnesslog',), #Insert
('season_tempmotivationlog',), #Insert
('season_playermotivationlog',), #Insert
('season_gameteamlog',), #Insert
('season_teamdivisiondata',), #Insert
('season_gameplayerlog',), #Insert
#('season_teaminfo',), #Update root
('season_generalschedule',) #Update
]

list_of_update_tables = [
('season_team',),	#Update
('season_player',), #Update
('season_generalschedule',), #Update
('season_daytable',) #Update
]

list_of_insert_tables = [
('season_gamepenaltieslog',), #Insert
('season_playerabilitylog',), #Insert
('season_teammotivationlog',), #Insert
('season_playerfitnesslog',), #Insert
('season_tempfitnesslog',), #Insert
('season_tempmotivationlog',), #Insert
('season_playermotivationlog',), #Insert
('season_gameteamlog',), #Insert
('season_teamdivisiondata',), #Insert
('season_gameplayerlog',), #Insert
]


def copy_tables_to_another_database(connection_string_instance, source_database, destination_database, list_of_tables):
	for table in list_of_tables:
		table_name = table[0]
		copy_table_to_another_database(connection_string_instance, source_database, destination_database, table_name)


def adding_save_column_to_tables(connection_string, list_of_tables):
	data_type_ristrictions = "INT(2) NULL"
	column_name = 'save_number'
	for table in list_of_tables:
		table_name = table[0]
		add_column_to_table(connection_string, table_name, column_name, data_type_ristrictions)



#adding_save_column_to_tables(connection_string_isl_save, list_of_tables)

def updating_save_tables(connection_string_instance, source_database, destination_database, list_of_tables, condition_dict, identifier_dict):
	table_columns = {}
	connection_string_source = connection_string_instance
	connection_string_source['database'] = source_database
	#print('inside function: ' + connection_string_destination['database'])
	for table in list_of_tables:
		table_name = table[0]
		source_table_name = table_name
		destination_table_name = table_name
		change_columns = get_column_headers(connection_string_source, table_name)
		change_columns_dict = {}
		for item in change_columns:
			if item == 'id' or item == 'save_number':
				change_columns.remove(item)
			else:
				change_columns_dict[item] = item
		source_identifier_column = identifier_dict[table_name]
		destination_identifier_column = source_identifier_column

		#print(change_columns)
		update_data_from_other_table(connection_string_instance, source_database, destination_database, 
			source_table_name, destination_table_name, source_identifier_column, destination_identifier_column, 
			change_columns_dict,condition_dict)
		#print('inside function loop: ' + connection_string_destination['database'])

# def deleting_data_from_tables(connection_string_source, source_database, destination_database, list_of_tables):
# 	for table in list_of_tables:
# 		table_name = table[0]
# 		#copy_table_to_another_database(connection_string_source, source_database, destination_database, table_name)


def update_save_number_in_tables(connection_string_instance, destination_database, list_of_tables, save_number):
	columns_and_input = {'save_number': save_number}
	condition_dict ={'save_number':None}
	for table in list_of_tables:
		table_name = table[0]
		update_data(connection_string_instance, destination_database, table_name, columns_and_input, condition_dict)

# save_number = 3
# update_save_number_in_tables(connection_string_instance, destination_database, list_of_tables, save_number)

def inserting_to_save_tables(connection_string_instance, source_database, destination_database, list_of_tables):
	connection_string_source = connection_string_instance
	connection_string_source['database'] = source_database
	for table in list_of_tables:
		table_name = table[0]
		list_of_columns = get_column_headers(connection_string_source, table_name)
		for item in list_of_columns:
			if item == 'id':
				list_of_columns.remove(item)
		#list_of_columns.remove('id')
		#print(list_of_columns)
		list_of_columns = build_column_string_for_insert(list_of_columns)
		insert_data_from_other_table(connection_string_instance, source_database, destination_database, table_name, list_of_columns)

# list_of_tables = [('season_teammotivationlog',),]
# inserting_to_save_tables(connection_string_instance, source_database, destination_database, list_of_tables)

def inserting_to_tables_conditionally(connection_string_instance, source_database, destination_database, list_of_tables, condition_dict):
	connection_string_source = connection_string_instance
	connection_string_source['database'] = source_database
	for table in list_of_tables:
		table_name = table[0]
		#print(table_name)
		list_of_columns = get_column_headers(connection_string_source, table_name)
		#print(list_of_columns)
		for item in list_of_columns:
			if item == 'id' or item == 'save_number':
				list_of_columns.remove(item)

		insert_data_from_other_table_conditionally(connection_string_instance, destination_database, source_database, table_name, list_of_columns, condition_dict)

def create_save_table(connection_string_destination):
	query_string = """CREATE TABLE save ( 
                            Id int(2) NOT NULL,
                            save_name varchar(100) NOT NULL,
                            PRIMARY KEY (Id)) """

	create_table(connection_string_destination, query_string)


def preparation(connection_string_destination, connection_string_instance, source_database, destination_database, list_of_tables, list_of_update_tables):
	#create save_table that holds info about the different save_numbers
	create_save_table(connection_string_destination)

	#add save_number 0 for restart files
	table_name = 'save'
	list_of_columns = ['Id', 'save_name']
	list_of_values = [1, 'restart' ]
	insert_data(connection_string_destination, table_name, list_of_columns, list_of_values)

	#create copies of relevant isl tables
	copy_tables_to_another_database(connection_string_instance, source_database, destination_database, list_of_tables)

	#add save_number column to the created tables
	adding_save_column_to_tables(connection_string_destination, list_of_tables)
	
	#fill update tables with data from isl
	inserting_to_save_tables(connection_string_instance, source_database, destination_database, list_of_update_tables)
	
	#change save_number to 1
	save_number = 1
	update_save_number_in_tables(connection_string_instance, destination_table, list_of_update_tables,save_number)
	
# preparation(connection_string_destination, connection_string_instance, source_database, destination_database, list_of_tables, list_of_update_tables)


def dropping_list_of_tables(connection_string_destination, list_of_tables):
	for table in list_of_tables:
		table_name = table[0]
		drop_table(connection_string_destination, table_name)


#dropping_list_of_tables(connection_string_destination, list_of_tables)

def save_progress(save_number, connection_string_instance, source_database, destination_database, list_of_tables, list_of_update_tables, list_of_insert_tables):
	connection_string_destination = connection_string_instance
	connection_string_destination['database'] = destination_database

	#Check if save_number exist in save table
	selection_columns_list = ['save_name']
	table_name = 'save'
	condition_dict = {'id':save_number}
	save_name = select_data(connection_string_destination, selection_columns_list, table_name, condition_dict)

	if save_name:
		#Show save_name
		save_name = save_name[0]
		save_name = save_name[0]
		print ('save exists, save name: ' + save_name)

		#update name in save-table
		table_name = 'save'
		save_name = str(datetime.now())
		columns_and_input  = {'save_name': save_name}
		condition_dict = {'id':save_number}
		update_data(connection_string_instance, destination_database, table_name, columns_and_input, condition_dict)
		#print('first print: ' + connection_string_destination['database'])
		
		#update data in update-tables
		condition_dict = {'save_number':save_number}
		identifier_column = 'id'
		updating_save_tables(connection_string_instance, source_database, destination_database, list_of_update_tables, condition_dict, identifier_column)
		#print('second print: ' + connection_string_destination['database'])
		
		#delete data in insert_tables in isl_save
		# I have no idea why, but destination database is for some reason set to isl instead of isl_save after updating_save_tables function
		# it is ok during the function itself. that's why I'm re-declaring the destination database
		connection_string_destination['database'] = destination_database
		for table in list_of_insert_tables:
			table_name = table[0]
			delete_data_conditionally(connection_string_destination, table_name, condition_dict)

		#insert data to insert_tables in isl_save
		inserting_to_save_tables(connection_string_instance, source_database, destination_database, list_of_insert_tables)
		#update save_number to X in insert_Tables where save_number is NULL
		update_save_number_in_tables(connection_string_instance, destination_database, list_of_insert_tables,save_number)

	else:
		print('save not created yet')
		#create entry in save table with new save number and current date and time as save name
		save_name = str(datetime.now())
		list_of_columns = ['id','save_name']
		list_of_values = [save_number, save_name]
		insert_data(connection_string_destination, table_name, list_of_columns, list_of_values)

		print('before inserting to tables')
		print(destination_database)
		print()
		#insert data to all tables
		inserting_to_save_tables(connection_string_instance, source_database, destination_database, list_of_tables)

		print('before updating save_number')
		print(destination_database)
		print()
		destination_database = 'isl_save'
		#update save_number to X in insert_Tables where save_number is NULL 
		update_save_number_in_tables(connection_string_instance, destination_database, list_of_tables, save_number)

# save_number = 2

# save_progress(save_number, connection_string_instance, 
# 				source_database, destination_database, 
# 				list_of_tables, list_of_update_tables, list_of_insert_tables)


def reset_save_database(connection_string_instance, source_database, destination_database,list_of_tables, list_of_update_tables):
	connection_string_destination = connection_string_instance
	connection_string_destination['database'] = destination_database

	# delete all saves but reset in save table
	table_name = 'save'
	condition_dict = {'id':2} #only works with 1 condition right now. 
	delete_data_conditionally(connection_string_destination, table_name, condition_dict)
	
	# delete data from all other tables
	for table in list_of_tables:
		table_name = table[0]
		delete_data(connection_string_instance, destination_database, table_name)

	# make inital update to update tables
	#fill update tables with data from isl
	inserting_to_save_tables(connection_string_instance, source_database, destination_database, list_of_update_tables)
	
	#change save_number to 1
	save_number = 1
	update_save_number_in_tables(connection_string_destination, list_of_update_tables,save_number)

#reset_save_database(connection_string_instance, source_database, destination_database,list_of_tables, list_of_update_tables)


def load_progress(save_number, connection_string_instance, source_database, destination_database, list_of_insert_tables, list_of_update_tables):
	connection_string_destination = connection_string_instance
	connection_string_source = connection_string_instance
	connection_string_destination['database'] = destination_database


	#Check if save_number exist in save table
	selection_columns_list = ['save_name']
	table_name = 'save'
	condition_dict = {'id':save_number}
	save_name = select_data(connection_string_destination, selection_columns_list, table_name, condition_dict)

	if save_name:
		print("save_number exists")
		#delete data in isl - insert tables

		#delete data in insert_tables in isl_save
		for table in list_of_insert_tables:
			table_name = table[0]
			delete_data(connection_string_instance, source_database, table_name)

		#insert data to insert_tables in isl_save
		#source and destination are switched since we aren't inserting to isl_save, but to isl

		#inserting conditionally where save_number = save_number
		condition_dict = {'save_number':save_number}
		inserting_to_tables_conditionally(connection_string_instance, source_database, destination_database, list_of_insert_tables, condition_dict)

		#update data in isl - update tables from isl_save where save_number = x
		condition_dict = {'save_number':save_number}
		identifier_dict = {'season_team':'Name', 'season_player':'Name','season_generalschedule':'GameID', 'season_daytable':'Day'}
		identifier_column = 'Name'
		updating_save_tables(connection_string_instance, destination_database, source_database, list_of_update_tables, condition_dict,identifier_dict)



	else:
		print("save_number doesn't exist")


# save_number = 1
# load_progress(save_number, connection_string_instance, source_database, destination_database, list_of_insert_tables, list_of_update_tables)


def reset_update_table(connection_string_instance, source_database, destination_database, table_name):
	#delete data from table
	delete_data(connection_string_instance, destination_database, table_name)

	#re-set auto increment
	reset_autoincrement(connection_string_instance, destination_database, table_name)

	#copy from save_table
	#connection_string_source = connection_string_instance
	#connection_string_source['database'] = source_database
	list_of_columns = get_column_headers(connection_string_source, table_name)
	for col in list_of_columns:
		if col == 'id':
			list_of_columns.remove(col)
	#print(list_of_columns)
	condition_dict = {'save_number':1}
	insert_data_from_other_table_conditionally(connection_string_instance, source_database, destination_database, table_name, list_of_columns, condition_dict)


# source_database = 'isl_save'
# destination_database = 'isl'
# table_name = 'season_generalschedule'

# reset_update_table(connection_string_instance, source_database, destination_database, table_name)

def restart():
	save_number = 1
	load_progress(save_number, connection_string_instance, source_database, destination_database, list_of_insert_tables, list_of_update_tables)


def test_save_progress(): #Not finished
	# insert muliple rows of data in into table in isl database
	connection_string = {'host':'35.228.182.135',
                    'database':'isl',
                    'user':'admin',
                    'password':'pass123'}
	TableName = 'season_teammotivationlog'
	list_of_columns = ['MotivationChange', 'Motivation', 'Name', 'Day', 'TypeOfUpdate', 'GameID']

	records_to_insert = [(0.20, 1.1, 'SF', 17, 'GameUpdate', '23'), (0.35, 3.4, 'DBL', 12, 'GameUpdate', '5'), (0.5, 0.8, 'TG', 16, 'GameUpdate', '58')]

	insert_many_data(connection_string, list_of_columns, records_to_insert, TableName)

	# save_number = 2

	# save_progress(save_number, connection_string_instance, 
	# 			source_database, destination_database, 
	# 			list_of_tables, list_of_update_tables, list_of_insert_tables)



#creating_save_tables(connection_string_isl, source_database, destination_database, list_of_tables)
#inserting_to_save_tables(connection_string_isl, source_database, destination_database, list_of_tables)


if __name__ == "__main__":
	restart()



# def remove_id(list_of_columns):



#updating_save_tables(connection_string_source, source_database, destination_database, tables_to_update)


# 	for item in list_of_columns:
# 		if item == 'id':
# 			list_of_columns.remove(item)

# 	print(list_of_columns)


# list_of_columns = ['id', 'name', 'test']

# remove_id(list_of_columns)