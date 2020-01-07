import sqlite3

if __name__ == "__main__":
  from DatabaseChanges.mysql_connector_scripts import *
  connection_string = {'host':'35.228.182.135',
                      'database':'isl',
                      'user':'admin',
                      'password':'pass123'}
else:    
    from season.MatchGenerator.DatabaseChanges.mysql_connector_scripts import *

def Change_of_Day(connection_string, current_day):

	next_day = current_day +1
	two_days_from_now = current_day +2
	
	connection_string_instance = connection_string
	destination_database = connection_string['database']
	table_name = 'season_daytable'
	columns_and_input = {'EndofDay': True, 'Status':'Past'}
	condition_dict = {'Day': current_day}

	update_data(connection_string_instance, destination_database, table_name, columns_and_input, condition_dict)

	columns_and_input = {'Status': 'Current'}
	condition_dict = {'Day':next_day}
	update_data(connection_string_instance, destination_database, table_name, columns_and_input, condition_dict)

	columns_and_input = {'Status': 'Next'}
	condition_dict = {'Day':two_days_from_now}
	update_data(connection_string_instance, destination_database, table_name, columns_and_input, condition_dict)


def Set_End_of_Day(connection_string, current_day):
	connection_string_instance = connection_string
	destination_database = connection_string['database']
	table_name = 'season_daytable'
	columns_and_input = {'EndofDay': True}
	condition_dict = {'Day': current_day}

	update_data(connection_string_instance, destination_database, table_name, columns_and_input, condition_dict)


def Remove_End_of_Day(connection_string, current_day):
	connection_string_instance = connection_string
	destination_database = connection_string['database']
	table_name = 'season_daytable'
	columns_and_input = {'EndofDay': False}
	condition_dict = {'Day': current_day}

	update_data(connection_string_instance, destination_database, table_name, columns_and_input, condition_dict)


def Set_End_of_Week(connection_string, current_day):
	connection_string_instance = connection_string
	destination_database = connection_string['database']
	table_name = 'season_daytable'
	columns_and_input = {'EndofWeek': True}
	condition_dict = {'Day': current_day}

	update_data(connection_string_instance, destination_database, table_name, columns_and_input, condition_dict)


def Remove_End_of_Week(connection_string, current_day):
	connection_string_instance = connection_string
	destination_database = connection_string['database']
	table_name = 'season_daytable'
	columns_and_input = {'EndofWeek': False}
	condition_dict = {'Day': current_day}

	update_data(connection_string_instance, destination_database, table_name, columns_and_input, condition_dict)

