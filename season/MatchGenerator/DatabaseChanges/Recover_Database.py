import sqlite3, csv

from itertools import *
from ast import *



 
#01 Create a CSV-file based on Sqlite table
def Export_sqlite_to_CSV(Table_name, VarDelimiter):
	#connecting with sqlite database

	path = "C:\\Users\\ASV11691\\OneDrive\\ISL_Season\\db.sqlite3"
	conn = sqlite3.connect(path)
	c = conn.cursor()
	
	cursor = c.execute('SELECT * FROM ' + Table_name)
	data = c.fetchall()
	#print(data)
	Table_headers = list(map(lambda x: x[0], cursor.description))
	#print(Table_headers)


	with open(Table_name+'.csv', 'w', newline='') as f:
	    writer = csv.writer(f, delimiter = VarDelimiter)
	    writer.writerow(Table_headers)
	    writer.writerows(data)

	#close connection to database
	c.close()
	conn.close() 

#Export_sqlite_to_CSV("season_teaminfo",";")

#02 Delete sqlite table
def Delete_table(Table_name):
	#connecting with sqlite database
	path = "C:\\Users\\ASV11691\\OneDrive\\ISL_Season\\db.sqlite3"
	conn = sqlite3.connect(path)
	c = conn.cursor()

	c.execute('DROP TABLE IF EXISTS ' + Table_name)
	conn.commit()

	#close connection to database
	c.close()
	conn.close() 
#03 Create Sqlite table from CSV-file

#03 A) Find table headers
def Find_table_headers(Path, Table_name, VarDelimiter):
    """s
    Read the first row and store values in a tuple
    """
    csvFile = Path + Table_name + ".csv"
    with open(csvFile) as csvfile:
        firstRow = csvfile.readlines(1)
        fieldnames = list(firstRow[0].strip('\n').split(VarDelimiter))
    
    #print(fieldnames)
    return fieldnames

#03 B) Find data types for data in table
def Find_data_type(Table_name, VarDelimiter):
    """
    Read the first row and store values in a tuple
    """
    # with open(csvFile) as csvfile:
    #     all_rows = csvfile.readlines()
    #     sec_row = all_rows[1]
    #     sec_row_corr = tuple(sec_row[0].strip('\n').split(";"))
    # #return fieldnames
    # print(all_rows)

    csvFile = Table_name + ".csv"
    with open(csvFile, 'r') as f:
    	reader = csv.reader(f, delimiter = VarDelimiter)
    	header = next(reader)
    	second = next(reader)
    	#header_corr = tuple(sec_row[0].strip('\n').split(";")
    	#print(second)
    	data_types = []
    	for v in second:
    		try:
    			val = int(v)
    			data_types.append("INTEGER")
    		except Exception as e:
    			try:
    				val = float(v)
    				data_types.append("REAL")
    			except Exception as e2:
    				val = str(v)
    				data_types.append("TEXT")
    	return	data_types

#03 C) combine column name and data types
def Combining_column_name_and_data_types(Column_names, Data_types):
	z = zip(Column_names, Data_types)
	i = 0

	result = ""
	for col in z:
		for c in col:
			result = result + c
			i += 1
			if i % 2 == 0:
				result = result + ", "
			else:
				result = result + " "

	adjusted_result = "(" + result[:len(result)-2] + ")"
	#print(adjusted_result)
	return adjusted_result
	

#03 D) Create table
def Create_table_from_CSV(Table_name,VarDelimiter):
	#connecting with sqlite database
	path = "C:\\Users\\ASV11691\\OneDrive\\ISL_Season\\db.sqlite3"
	conn = sqlite3.connect(path)
	c = conn.cursor()
	Column_names = Find_table_headers(path2,Table_name,VarDelimiter)
	Data_types = Find_data_type(Table_name,VarDelimiter)
	Column_header = str(Combining_column_name_and_data_types(Column_names, Data_types))
	#print(Column_header)
	c.execute('CREATE TABLE IF NOT EXISTS ' + Table_name + Column_header)
	#close connection to database
	c.close()
	conn.close() 

#04 Fill table with data
def Fill_table_from_CSV(Path,Table_name,VarDelimiter):
	#connecting with sqlite database
	path = "C:\\Users\\ASV11691\\OneDrive\\ISL_Season\\db.sqlite3"
	conn = sqlite3.connect(path)
	c = conn.cursor()
	#print(Table_name)
	Column_header = tuple(Find_table_headers(Path, Table_name, VarDelimiter))
	Column_header_string = str(Column_header)
	csvFile = Table_name + ".csv"
	#defines the number of "?" that represent the values to be inserted in the table

	value_string = " Values ("
	for col in Column_header:
		value_string = value_string + "?,"

	adjusted_value_string = value_string[:len(value_string)-1] + ")"
	# blir just nu bara 1 värde ('Season;Name;Division;DivisionPlace',), borde vara 4 st olika. behöver ändras 


	with open(Path + csvFile,'rt') as csv_file:
	    # csv.DictReader uses first line in file for column headings by default
	    dr = csv.DictReader(csv_file, delimiter = VarDelimiter)

	    to_db = []
	    for row in dr:
	    	#print((row[Column_header[0]], row[Column_header[1]]))
	    	RowTup = ()
	    	for col in Column_header:
	    		#print(col)
	    		RowTup = RowTup + (row[str(col)],)
	    		#print(RowTup)
	    	to_db.append(RowTup)


	    #to_db =  [(row[Column_header[0]], row[Column_header[1]], row[Column_header[2]], row[Column_header[3]]) for row in dr]
	#print(adjusted_value_string)
	c.executemany("INSERT INTO " + Table_name +Column_header_string + adjusted_value_string, to_db)
	#close connection to database
	conn.commit()

	#close connection to database
	c.close()
	conn.close() 

#var1 = 1234


#print(Find_table_headers("season_team"))

#Export_sqlite_to_CSV("Season_GeneralSchedule",";")

#Create_table_from_CSV ("Season_Player",";")
#Path = "C:\\Users\\ASV11691\\OneDrive\\ISL_Season\\Workfiles\\Back-up\\"
#Fill_table_from_CSV(Path,"Season_Nation",";")

#Delete_table("Season_Player")

