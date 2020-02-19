import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode


def get_cursor(connection_string):
    host = connection_string["host"]
    database = connection_string["database"]
    user = connection_string["user"]
    password = connection_string["password"]
    ssl_ca = connection_string['ssl_ca']
    ssl_cert = connection_string['ssl_cert']
    ssl_key = connection_string['ssl_key']
    try:
        connection = mysql.connector.connect(host=host,
                                             database=database,
                                             user=user,
                                             password=password,
                                             ssl_ca=ssl_ca,
                                             ssl_cert=ssl_cert,
                                             ssl_key=ssl_key
                                             )

        cursor = connection.cursor()
        print("Cursor created")
        return cursor, connection

    except mysql.connector.Error as error:
         print("Sql error: {}".format(error))


def close_connection(cursor,connection):
    cursor.close()
    connection.close()
    print("MySQL connection is closed")


def get_column_headers(connection_string_source, table_name):
    host = connection_string_source["host"]
    database = connection_string_source["database"]
    user = connection_string_source["user"]
    password = connection_string_source["password"]
    ssl_ca = connection_string_source['ssl_ca']
    ssl_cert = connection_string_source['ssl_cert']
    ssl_key = connection_string_source['ssl_key']

    database_and_table = database + '.' + table_name
    try:
        connection = mysql.connector.connect(host=host,
                                             database=database,
                                             user=user,
                                             password=password,                                             
                                             ssl_ca=ssl_ca,
                                             ssl_cert=ssl_cert,
                                             ssl_key=ssl_key)

        MySQLQuery = "show columns FROM {};".format(database_and_table);
        cursor = connection.cursor()
        cursor.execute(MySQLQuery)
        table_headers = [column[0] for column in cursor.fetchall()]
        print("Table headers collected")

    except mysql.connector.Error as error:
         print("Failed to select data: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
            return table_headers


# connection_string = {'host':'35.228.182.135',
#                     'database':'isl',
#                     'user':'admin',
#                     'password':'pass123'}

# table_name = 'season_nation'


# col = get_column_headers(connection_string, table_name)

# print(col)



def build_column_string_for_insert(list_of_columns):
    #building a string of column names based on a list of column names
    #Example input: ['Name','Flag', 'save_number']
    #Example output: Name, Flag, save_number
    insert_string = ''
    for col in list_of_columns:
        insert_string += col + ', '
    insert_string = insert_string[:len(insert_string)-2]
    return insert_string

def build_values_string_for_insert(list_of_values):
    #Building a string to be used in insert statements based on a list of values
    #Example input: ['AntonLand2','AL2.png',2]
    #Example output: 'AntonLand2', 'AL2.png', 2
    values_string =''
    for value in list_of_values:
        #print(key)
        #print(columns_and_input[key])
        if value == None:
            input_value = 'NULL'
        elif isinstance(value,(float,int)):
            input_value = str(value)
        elif isinstance(value,str):
            input_value = "'" + str(value) + "'"
        values_string += input_value + ', '
    values_string = values_string[:len(values_string)-2]
    return values_string



def build_values_placeholders(list_of_columns):
    # Format 
    # exmple input: ['Name','Flag', 'save_number']
    # example output: "%s, %s, %s, %s"
    placeholders_string = ""
    for col in list_of_columns:
        placeholders_string += '%s, '
    placeholders_string = placeholders_string[:len(placeholders_string)-2]
    return placeholders_string


# list_of_columns = ['Name','Flag', 'save_number']
# print(build_values_placeholders(list_of_columns))


def field_and_increment_string(field_name, increment):
    #input field_name, 3
    #output filed_name = field_name + 3
    return str(field_name) + ' = ' + str(field_name) + ' + ' + str(increment)

            


# fields_and_increments = {'field_name1':1'fieldname_2':5}
# fields_and_increments_update(fields_and_increments)
 

def columns_and_input_string_for_update(columns_and_input):
    #building a string of columns and input for a update satatment from a dictionary with keys and value pairs
    #example input: {'save_number': 1, 'Flag':'Italy.png'}
    #example output: save_number = 1, Flag = 'Italy.png'
    #example None as input: columns_and_input = {'save_number': None}
    #Output: save_number IS NULL
    #example increment as input: {'save_number':increment1}
    #Output: 'savenumber = save_number + 1'
    input_string =''
    for key in columns_and_input:
        #print(key)
        #print(columns_and_input[key])
        value = columns_and_input[key]
        if value == None:
            input_string = key + ' IS NULL'
            return input_string
        elif isinstance(columns_and_input[key],(float,int)):
            input_value = str(columns_and_input[key])
        elif value[:9] == 'increment':
            field_and_increment = field_and_increment_string(key, value[9:])
            input_value = field_and_increment
        elif isinstance(columns_and_input[key],str):
            input_value = "'" + str(columns_and_input[key]) + "'"
        input_string +=key + ' = ' + input_value + ', '
    input_string = input_string[:len(input_string)-2]
    return input_string

# columns_and_input = {'save_number': 'increment78390', 'bla_bla':43}

# print(columns_and_input_string_for_update (columns_and_input))
  


def condition_string_from_dict(condition_dict):
    #example input: condition_dict = {'id':2}
    #example output: WHERE id = 2
    #example input multiple values, one key: condition_dict = {'id':[2,3]}
    #example output  WHERE `id`  IN (2,3);
    #example None as input: condition_dict = {'save_number': None}
    #Output: save_number IS NULL

    #chech for multiple items
    no_of_items = len(condition_dict)
    if no_of_items < 2:
        #checking for muliple values
        for key in condition_dict:
            if isinstance(condition_dict[key],list):
                condition_string= 'WHERE ' + key +' IN ('
                for item in condition_dict[key]:
                    condition_string += str(item) +','
                condition_string = condition_string[:len(condition_string)-1]
                condition_string+= ')'
                return condition_string

        #building condition string for single values
        if condition_dict:
            condition_string = 'WHERE ' + columns_and_input_string_for_update(condition_dict)
            return condition_string
        else:
            return FALSE
    else:
        condition_string = 'WHERE '
        counter = 0
        for key in condition_dict:
            if isinstance(condition_dict[key],list):
                condition_string= 'WHERE ' + key +' IN ('
                for item in condition_dict[key]:
                    condition_string += str(item) +','
                condition_string = condition_string[:len(condition_string)-1]
                condition_string+= ')'

        # for key,value in condition_dict.items():
        #     if isinstance(condition_dict[value],list):
        #         condition_string += key + ' IN ('
        #         for item in condition_dict[value]:
        #             condition_string += str(item) +','
        #         condition_string = condition_string[:len(condition_string)-1]
        #         condition_string+= ')'
            else:
                temp_dict = {}
                temp_dict[key] = condition_dict[key]
                condition_string += columns_and_input_string_for_update(temp_dict)
            counter += 1
            if counter < no_of_items:
                condition_string += ' AND '

    #print(condition_string)
    return condition_string



# condition_dict = {'key1':['value1','value2'], 'key2':'value3'}
# condition_string_from_dict(condition_dict)

# condition_dict = {'id':[2,3]}
# condition_dict = {'save_number': None}

# print(condition_string_from_dict(condition_dict))

def test_database_connection(connection_string):

    host = connection_string["host"]
    database = connection_string["database"]
    user = connection_string["user"]
    password = connection_string["password"]
    ssl_ca = connection_string['ssl_ca']
    ssl_cert = connection_string['ssl_cert']
    ssl_key = connection_string['ssl_key']

    try:
        connection = mysql.connector.connect(host=host,
                                             database=database,
                                             user=user,
                                             password=password,
                                             ssl_ca=ssl_ca,
                                             ssl_cert=ssl_cert,
                                             ssl_key=ssl_key)
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("Your connected to database: ", record)
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def connect_to_database(connection_string):

    host = connection_string["host"]
    database = connection_string["database"]
    user = connection_string["user"]
    password = connection_string["password"]
    ssl_ca = connection_string['ssl_ca']
    ssl_cert = connection_string['ssl_cert']
    ssl_key = connection_string['ssl_key']

    try:
        connection = mysql.connector.connect(host=host,
                                             database=database,
                                             user=user,
                                             password=password,
                                             ssl_ca=ssl_ca,
                                             ssl_cert=ssl_cert,
                                             ssl_key=ssl_key)
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("Your connected to database: ", record)
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def create_table(connection_string, query_string):
    host = connection_string["host"]
    database = connection_string["database"]
    user = connection_string["user"]
    password = connection_string["password"]
    ssl_ca = connection_string['ssl_ca']
    ssl_cert = connection_string['ssl_cert']
    ssl_key = connection_string['ssl_key']

    try:
        connection = mysql.connector.connect(host=host,
                                             database=database,
                                             user=user,
                                             password=password,
                                             ssl_ca=ssl_ca,
                                             ssl_cert=ssl_cert,
                                             ssl_key=ssl_key)


        cursor = connection.cursor()
        result = cursor.execute(query_string)
        print("Table created successfully")
    except mysql.connector.Error as error:
         print("Failed to create table in MySQL: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


# connection_string = {'host':'35.228.182.135',
#                     'database':'isl_save',
#                     'user':'admin',
#                     'password':'pass123'}


# query_string = """CREATE TABLE save ( 
#                             Id int(2) NOT NULL,
#                             save_name varchar(100) NOT NULL,
#                             time_stamp Date NOT NULL,
#                             PRIMARY KEY (Id)) """

# create_table(connection_string, query_string)

def copy_table_to_another_database(connection_string_instance, source_database, destination_database, table_name):
    source_host = connection_string_instance["host"]
    #source_database = connection_string_source["database"]
    source_user = connection_string_instance["user"]
    source_password = connection_string_instance["password"]
    ssl_ca = connection_string_instance['ssl_ca']
    ssl_cert = connection_string_instance['ssl_cert']
    ssl_key = connection_string_instance['ssl_key']

    source_db_and_table = source_database + '.' + table_name
    destination_db_and_table = destination_database + '.' + table_name
    try:
        connection = mysql.connector.connect(host=source_host,
                                             #database=destination_database,
                                             user=source_user,
                                             password=source_password,
                                             ssl_ca=ssl_ca,
                                             ssl_cert=ssl_cert,
                                             ssl_key=ssl_key)

        # connection_destination = mysql.connector.connect(host=destination_host,
        #                                      database=destination_database,
        #                                      user=destination_user,
        #                                      password=destination_password)

        #MySQLQuery = """CREATE TABLE {} SELECT * FROM {}""".format (destination_database.table_name, source_database.table_name)
        MySQLQuery = """CREATE TABLE {} LIKE {}""".format(destination_db_and_table, source_db_and_table)
        cursor = connection.cursor()
        result = cursor.execute(MySQLQuery)
        print("{} table created successfully in {} ".format(table_name, destination_database))
    except mysql.connector.Error as error:
         print("Failed to create table {} in MySQL: {}".format(table_name, error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


# connection_string_instance = {'host':'35.228.182.135',
#                     'user':'admin',
#                     'password':'pass123'}

# table_name = 'season_nation'
# source_database = 'isl'
# destination_database = 'isl_save'

# copy_table_to_another_database(connection_string_instance,source_database, destination_database,table_name)


def drop_table(connection_string, table_name):
    host = connection_string["host"]
    database = connection_string["database"]
    user = connection_string["user"]
    password = connection_string["password"]
    ssl_ca = connection_string['ssl_ca']
    ssl_cert = connection_string['ssl_cert']
    ssl_key = connection_string['ssl_key']

    try:
        connection = mysql.connector.connect(host=host,
                                             database=database,
                                             user=user,
                                             password=password,
                                             ssl_ca=ssl_ca,
                                             ssl_cert=ssl_cert,
                                             ssl_key=ssl_key)

        MySQLQuery = """DROP TABLE IF EXISTS """ + table_name

        cursor = connection.cursor()
        result = cursor.execute(MySQLQuery)
        print("Table {} dropped successfully ".format(table_name))
    except mysql.connector.Error as error:
         print("Failed to drop table in MySQL: {}".format('Table:' + table_name + ' Error msg: ' + error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

# connection_string_isl_save = {'host':'35.228.182.135',
#                     'database':'isl_save',
#                     'user':'admin',
#                     'password':'pass123'}

# table_name = 'save'

# drop_table(connection_string_isl_save, table_name)


def delete_data(connection_string_instance, database_name, table_name):
    host = connection_string_instance["host"]
    database = database_name
    user = connection_string_instance["user"]
    password = connection_string_instance["password"]
    ssl_ca = connection_string_instance['ssl_ca']
    ssl_cert = connection_string_instance['ssl_cert']
    ssl_key = connection_string_instance['ssl_key']
    
    query_string = """DELETE FROM """ + table_name
    try:
        connection = mysql.connector.connect(host=host,
                                             database=database,
                                             user=user,
                                             password=password,
                                             ssl_ca=ssl_ca,
                                             ssl_cert=ssl_cert,
                                             ssl_key=ssl_key)

        MySQLQuery = query_string

        cursor = connection.cursor()
        result = cursor.execute(MySQLQuery)
        print("Data deleted successfully from table: {}".format(table_name))
        connection.commit()
    except mysql.connector.Error as error:
         print("Failed to delete data in MySQL: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


# connection_string_isl_save = {'host':'35.228.182.135',
#                     'database':'isl_save',
#                     'user':'admin',
#                     'password':'pass123'}

# table_name = 'season_nation'

# delete_data(connection_string_isl_save, table_name)


def delete_data_conditionally(connection_string, table_name, condition_dict):
    #example input: condition_dict = {'id':2}
    host = connection_string["host"]
    database = connection_string["database"]
    user = connection_string["user"]
    password = connection_string["password"]
    ssl_ca = connection_string['ssl_ca']
    ssl_cert = connection_string['ssl_cert']
    ssl_key = connection_string['ssl_key']

    #destination_db_and_table = database + '.' + table_name
    condition_string = condition_string_from_dict(condition_dict)

    #condition_string = "WHERE save_number <> 1"

    #print(condition_string)
    query_string = """DELETE FROM """ + table_name +' '+ condition_string
    print(query_string)
    try:
        connection = mysql.connector.connect(host=host,
                                             database=database,
                                             user=user,
                                             password=password,
                                             ssl_ca=ssl_ca,
                                             ssl_cert=ssl_cert,
                                             ssl_key=ssl_key)

        MySQLQuery = query_string

        cursor = connection.cursor()
        result = cursor.execute(MySQLQuery)
        print("Data deleted successfully from table: {}".format(table_name))
        connection.commit()
    except mysql.connector.Error as error:
         print("Failed to delete data in MySQL: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


# connection_string_isl_save = {'host':'35.228.182.135',
#                     'database':'isl_save',
#                     'user':'admin',
#                     'password':'pass123'}

# table_name = 'season_generalschedule'
# #condition_dict = {'id':[2,3]}
# condition_dict = {'save_number':2}


# delete_data_conditionally(connection_string_isl_save, table_name, condition_dict)



def add_column_to_table(connection_string, table_name, column_name, data_type_ristrictions):
    host = connection_string["host"]
    database = connection_string["database"]
    user = connection_string["user"]
    password = connection_string["password"]
    ssl_ca = connection_string['ssl_ca']
    ssl_cert = connection_string['ssl_cert']
    ssl_key = connection_string['ssl_key']

    database_and_table = database + '.' + table_name
    try:
        connection = mysql.connector.connect(host=host,
                                             database=database,
                                             user=user,
                                             password=password,
                                             ssl_ca=ssl_ca,
                                             ssl_cert=ssl_cert,
                                             ssl_key=ssl_key)

        MySQLQuery = """ALTER TABLE {} ADD {} {}""".format(database_and_table, column_name, data_type_ristrictions)
        #MySQLQuery = """ALTER TABLE isl_save.season_nation ADD save_number INT(2) NULL"""
        #MySQLQuery = """ALTER TABLE isl_save.season_nation ADD COLUMN save_number 
        #tilllägg om man vill lägga till foreind key samtidigt som man lägger till kolumn
        #MySQLQuery = """ALTER TABLE {} ADD {} {}, ADD FOREIGN KEY fk_name(fk_column) REFERENCES save(Id) ON DELETE CASCADE, """.format(table_name, column_name, data_type_ristrictions)
        #MySQLQuery = """ALTER TABLE database.table ADD COLUMN columnname INT DEFAULT(1), ADD FOREIGN KEY fk_name(fk_column) REFERENCES reftable(refcolumn) ON DELETE CASCADE;"""
        cursor = connection.cursor()
        result = cursor.execute(MySQLQuery)
        #cursor.execute()
        print("column: {} added to table: {} ".format(column_name, table_name))
    except mysql.connector.Error as error:
         print("Failed to insert column: {} to table: {} error message: {}".format(column_name, table_name, error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

# connection_string_isl_save = {'host':'35.228.182.135',
#                     'database':'isl_save',
#                     'user':'admin',
#                     'password':'pass123'}
# table_name = 'season_nation'
# data_type_ristrictions = "INT(2) NULL"
# column_name = 'save_number'
# # 
# add_column_to_table(connection_string_isl_save, table_name, column_name, data_type_ristrictions)


def insert_data(connection_string, table_name, list_of_columns, list_of_values):
    #connection_string including database
    #format: 
    # list_of_columns = ['Name','Flag', 'save_number']
    # list_of_values = ['AntonLand2','AL2.png',2]
    host = connection_string["host"]
    database = connection_string["database"]
    user = connection_string["user"]
    password = connection_string["password"]
    ssl_ca = connection_string['ssl_ca']
    ssl_cert = connection_string['ssl_cert']
    ssl_key = connection_string['ssl_key']

    #combining columns into an insert string that is used in the query
    insert_string = build_column_string_for_insert(list_of_columns)

    values_string = build_values_string_for_insert(list_of_values)
    #print(values_string)
    try:
        connection = mysql.connector.connect(host=host,
                                             database=database,
                                             user=user,
                                             password=password,
                                             ssl_ca=ssl_ca,
                                             ssl_cert=ssl_cert,
                                             ssl_key=ssl_key)
        query_string = """INSERT INTO {} ({}) VALUES ({}) """.format(table_name, insert_string,values_string)
        cursor = connection.cursor()
        result = cursor.execute(query_string)
        connection.commit()
        print("data inserted successfully ")
    except mysql.connector.Error as error:
         print("Failed to insert data: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


# connection_string = {'host':'35.228.182.135',
#                     'database':'isl_save',
#                     'user':'admin',
#                     'password':'pass123'}

# table_name = 'season_nation'
# list_of_columns = ['Name','Flag', 'save_number']
# list_of_values = ['AntonLand2','AL2.png',2]

# insert_data(connection_string, table_name, list_of_columns, list_of_values)

def insert_data_from_other_table(connection_string_instance, source_database, destination_database, table_name, list_of_columns):
    source_host = connection_string_instance["host"]
    #source_database = connection_string_instance["database"]
    source_user = connection_string_instance["user"]
    source_password = connection_string_instance["password"]
    ssl_ca = connection_string_instance['ssl_ca']
    ssl_cert = connection_string_instance['ssl_cert']
    ssl_key = connection_string_instance['ssl_key']

    source_db_and_table = source_database + '.' + table_name
    destination_db_and_table = destination_database + '.' + table_name

    try:
        connection = mysql.connector.connect(host=source_host,
                                             #database=source_database,
                                             user=source_user,
                                             password=source_password,
                                             ssl_ca=ssl_ca,
                                             ssl_cert=ssl_cert,
                                             ssl_key=ssl_key)

        MySQLQuery = """INSERT INTO {} ({}) SELECT {} FROM {}""".format(destination_db_and_table, list_of_columns, list_of_columns, source_db_and_table)
        print(MySQLQuery)
        cursor = connection.cursor()
        result = cursor.execute(MySQLQuery)
        connection.commit()
        print("data inserted successfully in table: {}".format(destination_db_and_table))
    except mysql.connector.Error as error:
         print("Failed to insert data to table {} error message: {}".format(destination_db_and_table, error))
         #print("Failed to insert data to table error message: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

# connection_string_instance = {'host':'35.228.182.135',
#                     'user':'admin',
#                     'database':'isl_save',
#                     'password':'pass123'}

# table_name = 'season_nation'
# list_of_columns = "Name, Flag"
# source_database = 'isl'
# destination_database = 'isl_save'

# insert_data_from_other_table(connection_string_source, source_database, destination_database, table_name, list_of_columns)

def insert_data_from_other_table_conditionally(connection_string_instance, source_database, destination_database, table_name, list_of_columns, condition_dict):
    # INSERT INTO isl.season_teammotivationlog(MotivationChange, Motivation, Name, Day, TypeOfUpdate, GameID) SELECT MotivationChange, Motivation, Name, Day, TypeOfUpdate, GameID FROM isl_save.season_teammotivationlog WHERE save_number = 3
    source_host = connection_string_instance["host"]
    source_user = connection_string_instance["user"]
    source_password = connection_string_instance["password"]
    ssl_ca = connection_string_instance['ssl_ca']
    ssl_cert = connection_string_instance['ssl_cert']
    ssl_key = connection_string_instance['ssl_key']

    source_db_and_table = source_database + '.' + table_name
    destination_db_and_table = destination_database + '.' + table_name

    columns_string = build_column_string_for_insert(list_of_columns)

    if condition_dict:
        condition_string = condition_string_from_dict(condition_dict)
    else:
        condition_string = ""

    try:
        connection = mysql.connector.connect(host=source_host,
                                             #database=source_database,
                                             user=source_user,
                                             password=source_password,
                                             ssl_ca=ssl_ca,
                                             ssl_cert=ssl_cert,
                                             ssl_key=ssl_key)

        MySQLQuery = """INSERT INTO {}({}) SELECT {} FROM {} {}""".format(destination_db_and_table, 
                                                                        columns_string, 
                                                                        columns_string, 
                                                                        source_db_and_table,
                                                                        condition_string)
        #print(MySQLQuery)
        #MySQLQuery = """INSERT INTO isl_save.season_nation (Name, Flag) SELECT Name, Flag FROM isl.season_nation"""
        cursor = connection.cursor()
        result = cursor.execute(MySQLQuery)
        connection.commit()
        print("data inserted successfully in table: {}".format(destination_db_and_table))
    except mysql.connector.Error as error:
         print("Failed to insert data to table {} error message: {}".format(destination_db_and_table, error))
         #print("Failed to insert data to table error message: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

# connection_string_instance = {'host':'35.228.182.135',
#                     'user':'admin',
#                     'password':'pass123'}

# table_name = 'season_teammotivationlog'
# list_of_columns = 'MotivationChange', 'Motivation', 'Name', 'Day', 'TypeOfUpdate', 'GameID'
# source_database = 'isl_save'
# destination_database = 'isl'
# condition_dict = {'save_number':3}


# insert_data_from_other_table_conditionally(connection_string_instance, source_database, destination_database, table_name, list_of_columns, condition_dict)





def update_data_from_other_table(connection_string_instance, source_database, destination_database, 
    source_table_name, destination_table_name, source_identifier_column, destination_identifier_column, 
    change_columns_dict,condition_dict):
    #format
    #change_columns_dict = {'SET_column':'SELECT_column'}

    source_host = connection_string_instance["host"]
    #source_database = connection_string_source["database"]
    source_user = connection_string_instance["user"]
    source_password = connection_string_instance["password"]
    ssl_ca = connection_string_instance['ssl_ca']
    ssl_cert = connection_string_instance['ssl_cert']
    ssl_key = connection_string_instance['ssl_key']

    source_db_and_table = source_database + '.' + source_table_name
    destination_db_and_table = destination_database + '.' + destination_table_name
    source_db_table_identifier = source_db_and_table + '.' + source_identifier_column
    destination_db_table_identifier = destination_db_and_table + '.' + destination_identifier_column

    columns_to_change = ''

    for key,value in change_columns_dict.items():
        columns_to_change = columns_to_change + destination_db_and_table + '.' + key + ' = ' + source_db_and_table + '.' + value + ', '
    columns_to_change = columns_to_change[:len(columns_to_change)-2]
    #print(columns_to_change)
    if condition_dict:
        condition_string = condition_string_from_dict(condition_dict)
    else:
        condition_string = ""

    try:
        connection = mysql.connector.connect(host=source_host,
                                             #database=database,
                                             user=source_user,
                                             password=source_password,
                                             ssl_ca=ssl_ca,
                                             ssl_cert=ssl_cert,
                                             ssl_key=ssl_key)

        MySQLQuery = """UPDATE {} 
                        INNER JOIN {} ON {} = {} 
                        SET {} {}""".format(destination_db_and_table, source_db_and_table,destination_db_table_identifier,
                            source_db_table_identifier,columns_to_change, condition_string)
        #print(MySQLQuery)
        cursor = connection.cursor()
        result = cursor.execute(MySQLQuery)
        connection.commit()
        print("data updated successfully in table: {}".format(destination_db_and_table))
    except mysql.connector.Error as error:
         print("Failed to update data to table {} error message: {}".format(destination_db_and_table, error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

# connection_string_source = {'host':'35.228.182.135',
#                     'user':'admin',
#                     'password':'pass123'}

# source_database = 'isl'
# destination_database = 'isl_save'
# table_name = 'season_team'
# identifier_column = 'id'
# #change_columns = ['Flag', 'Name']

# #condition_dict = {'save_number':1}
# condition_dict ={}

# update_data_from_other_table(connection_string_source, source_database, destination_database, table_name, identifier_column, change_columns, condition_dict)


def select_data(connection_string,selection_columns_list,table_name,condition_dict):
    cursor_and_connection = get_cursor(connection_string)
    cursor = cursor_and_connection[0]
    connection = cursor_and_connection[1]

    column_string = build_column_string_for_insert(selection_columns_list)

    if condition_dict:
        #will only work whith one condition currently, the function will return ',' as seperator instead of AND
        condition_string = condition_string_from_dict(condition_dict)
    else:
        condition_string = ''

    try:
        if condition_string:
            MySQLQuery = "SELECT {} FROM {} {}".format(column_string, table_name, condition_string)
        else:
            MySQLQuery = "SELECT {} FROM {}".format(column_string, table_name)
        #print(MySQLQuery)
        result = cursor.execute(MySQLQuery)
        records = cursor.fetchall()
        #records = cursor.fetchone()
        print("Total number of rows in selection is: ", cursor.rowcount)

    except mysql.connector.Error as error:
         print("Failed to select data: {}".format(error))
    finally:
        if (connection.is_connected()):
            close_connection(cursor,connection)
            return records

# connection_string = {'host':'35.228.182.135',
#                     'user':'admin',
#                     'database':'isl_save',
#                     'password':'pass123'}
# selection_columns_list = ['id']
# table_name = 'season_teammotivationlog'
# condition_dict = {'save_number':3}



# print(select_data(connection_string,selection_columns_list,table_name,condition_dict))

def test_parse(connection_string):
    host = connection_string["host"]
    print(host)

def insert_many_data(connection_string, list_of_columns, records_to_insert, table_name):
    #Format:
    # records_to_insert = [(4, 'HP Pavilion Power', 1999, '2019-01-11'),
    #                     (5, 'MSI WS75 9TL-496', 5799, '2019-02-27'),
    #                     (6, 'Microsoft Surface', 2330, '2019-07-23')]
    # list_of_columns = ['Name','Flag', 'save_number']

    columns_string = build_column_string_for_insert(list_of_columns)
    values_placeholders = build_values_placeholders(list_of_columns)

    #query_string = """INSERT INTO Laptop (Id, Name, Price, Purchase_date) VALUES (%s, %s, %s, %s) """
    query_string ="""INSERT INTO """ + table_name + """ (""" + columns_string + """) VALUES (""" + values_placeholders + """) """
    #print(query_string)
    host = connection_string["host"]
    database = connection_string["database"]
    user = connection_string["user"]
    password = connection_string["password"]
    ssl_ca = connection_string['ssl_ca']
    ssl_cert = connection_string['ssl_cert']
    ssl_key = connection_string['ssl_key']

    try:
        connection = mysql.connector.connect(host=host,
                                             database=database,
                                             user=user,
                                             password=password,
                                             ssl_ca=ssl_ca,
                                             ssl_cert=ssl_cert,
                                             ssl_key=ssl_key)


        cursor = connection.cursor()
        cursor.executemany(query_string, records_to_insert)
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into table: {}".format(table_name))
    except mysql.connector.Error as error:
        print("Failed to insert data: {}".format(table_name + '' + str(error)))
        print("Failed to insert data: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")




# connection_string = {'host':'35.228.182.135',
#                     'database':'isl',
#                     'user':'admin',
#                     'password':'pass123'}
# table_name = 'season_teammotivationlog'

# #delete_data(connection_string, table_name)

# list_of_columns = ['MotivationChange', 'Motivation', 'Name', 'Day', 'TypeOfUpdate', 'GameID']

# records_to_insert = [(0.20, 1.1, 'SF', 17, 'GameUpdate', '23'), (0.35, 3.4, 'DBL', 12, 'GameUpdate', '5'), (0.5, 0.8, 'TG', 16, 'GameUpdate', '58')]

# ##records_to_insert = [(1, 1, 0.04956378699703717, 'Div 1', 'Div 1-1', 'KÄ', 6, 'A', 'Neutral', 0.410958904109589, 0.297382721982223, 'KÄ.png', 1, 'Kämparna'), (2, 2, 0.04862171968797572, 'Div 1', 'Div 1-2', 'DBL', 6, 'A', 'Defensiv', 0.1, 0.2917303181278543, 'DBL.png', 2, 'Det Bästa Laget'),]

# # query_string = """INSERT INTO Laptop (Id, Name, Price, Purchase_date) VALUES (%s, %s, %s, %s) """


# # records_to_insert = [(4, 'HP Pavilion Power', 1999, '2019-01-11'),
# #                     (5, 'MSI WS75 9TL-496', 5799, '2019-02-27'),
# #                     (6, 'Microsoft Surface', 2330, '2019-07-23')]



# insert_many_data(connection_string, list_of_columns, records_to_insert, table_name)

def update_data(connection_string_instance, destination_database, table_name, columns_and_input, condition_dict):
    # format
    # columns_and_input = {'save_number': 1, 'Flag':'Italy.png','save_number':increment1}
    # condition_string = 'save_number is NULL'
    #example columns_and_input increment as input: {'save_number':increment1}
    #Output: 'savenumber = save_number + 1'
    host = connection_string_instance["host"]
    database = destination_database
    user = connection_string_instance["user"]
    password = connection_string_instance["password"]
    ssl_ca = connection_string_instance['ssl_ca']
    ssl_cert = connection_string_instance['ssl_cert']
    ssl_key = connection_string_instance['ssl_key']

    database_and_table = str(database +'.'+ table_name)
    
    input_string = columns_and_input_string_for_update (columns_and_input)
    condition_string = condition_string_from_dict(condition_dict)
    try:
        connection = mysql.connector.connect(host=host,
                                             database=database,
                                             user=user,
                                             password=password,
                                             ssl_ca=ssl_ca,
                                             ssl_cert=ssl_cert,
                                             ssl_key=ssl_key)

        query_string = """UPDATE {} SET {} {} """.format(database_and_table, input_string, condition_string)
        #print(query_string)
        #query_string = """UPDATE season_nation SET save_number = 2, Flag = 'Italy.png' WHERE save_number IS NULL"""
        cursor = connection.cursor()
        cursor.execute(query_string)
        connection.commit()
        print(cursor.rowcount, "rows has successfully been updated in table:{}".format(database_and_table))
    except mysql.connector.Error as error:
        print("Failed to update data in{}: {}".format(database_and_table, error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


# connection_string_instance = {'host':'35.228.182.135',
#                     'user':'admin',
#                     'password':'pass123'}
# destination_database = 'isl'

# table_name = 'season_teammotivationlog'
# #columns_and_input = {'save_number': 1, 'Flag':'Italy.png'}
# columns_and_input = {'TypeOfUpdate':"TestUpdate"}
# #condition_string = 'save_number is NULL'
# condition_dict = {'id':1}

# update_data(connection_string_instance, destination_database, table_name, columns_and_input, condition_dict)


def reset_autoincrement(connection_string_instance, destination_database, table_name):
    host = connection_string_instance["host"]
    database = destination_database
    user = connection_string_instance["user"]
    password = connection_string_instance["password"]
    ssl_ca = connection_string_instance['ssl_ca']
    ssl_cert = connection_string_instance['ssl_cert']
    ssl_key = connection_string_instance['ssl_key']

    database_and_table = str(database +'.'+ table_name)
    
    try:
        connection = mysql.connector.connect(host=host,
                                             database=database,
                                             user=user,
                                             password=password,
                                             ssl_ca=ssl_ca,
                                             ssl_cert=ssl_cert,
                                             ssl_key=ssl_key)

        query_string = """ALTER TABLE {} AUTO_INCREMENT = 1;""".format(database_and_table,)
        #print(query_string)
        #query_string = """UPDATE season_nation SET save_number = 2, Flag = 'Italy.png' WHERE save_number IS NULL"""
        cursor = connection.cursor()
        cursor.execute(query_string)
        connection.commit()
        print("Auto increment has been re-set for table:{}".format(database_and_table))
    except mysql.connector.Error as error:
        print("Failed to re-set auto increment in table: {}: {}".format(database_and_table, error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")



#type_of_query = 'insert many'

#delete_data(connection_string)
#mysql_query(connection_string, type_of_query, query_string)
#drop_table(connection_string)
#create_table(connection_string)
#test_parse(connection_string)
#insert_data(connection_string)
#select_data(connection_string)

#connect_to_databse(connection_string)

#if __name__ == "__main__":
    #connect_to_databse()