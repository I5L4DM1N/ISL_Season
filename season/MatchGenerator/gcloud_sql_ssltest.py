import os
from DatabaseChanges.mysql_connector_scripts import *


connection_string = {
    'host': os.environ.get('DB_HOST'),
    'database':'isl',
    'user': os.environ.get('DB_USER'),
    'password':os.environ.get('DB_PASS'),
	'ssl_ca': os.environ.get('SSL_CA_DIR'),
	'ssl_cert': os.environ.get('SSL_CERT_DIR'),
	'ssl_key': os.environ.get('SSL_KEY_DIR')
	#'ssl_ca':'C:/Users/ASV11691/OneDrive/ISL_Season/SSL_key/server-ca.pem',
	#'ssl_cert':'C:/Users/ASV11691/OneDrive/ISL_Season/SSL_key/client-cert.pem',
	#'ssl_key':'C:/Users/ASV11691/OneDrive/ISL_Season/SSL_key/client-key.pem'
    }

selection_columns_list = ['id','TournamentName','Day','TypeOfGame']
table_name = 'season_generalschedule'
condition_dict = {'Played':False}
match_data = select_data(connection_string,selection_columns_list,table_name,condition_dict)
print(match_data)