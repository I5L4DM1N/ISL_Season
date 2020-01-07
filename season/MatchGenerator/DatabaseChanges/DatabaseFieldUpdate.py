import sqlite3, csv
import os
import re

#connecting with sqlite database
path = "C:\\Users\\anton\\OneDrive\\ISL_Season\\db.sqlite3"
conn = sqlite3.connect(path)
c = conn.cursor()

def UpdateDBField ():

    #importing from Fixture_list
    c.execute('SELECT Name FROM season_generalteam')
    PlayerNames = c.fetchall()
    #c.close()
    for p in PlayerNames:
        pl = p[0]
        plogo = pl + ".png"
        #print(pl)
        c.execute('UPDATE season_generalteam SET Logo = (?) WHERE Name = (?)',(plogo,pl))
        conn.commit()

        #removing last character
    	# last_char = pl[-1:]
    	# if last_char == " ":
    	# 	play = pl[:-1]



    	#pla = pl.replace(" ","_")
    	#play = pl.replace(u'\xa0', u'')
    	#print(pl)
    	#c.execute('UPDATE season_generalplayer SET Name = (?) WHERE Name = (?)',(play,pl))
    	#c.execute('UPDATE season_generalplayer SET Name = (?) WHERE Name = (?)',(play,pl))
    	#conn.commit()

UpdateDBField()

def CheckDBField ():

    #importing from Fixture_list
    c.execute('SELECT Name FROM season_generalplayer')
    PlayerNames = c.fetchall()
    #c.close()
    for p in PlayerNames:
    	pl = p[0]
    	if pl.count(" ")<1:
    		print(pl)

def UpdateOtherDBField ():

    #importing from Fixture_list
    c.execute('SELECT Name FROM season_generalplayer')
    PlayerNames = c.fetchall()
    #c.close()
    for p in PlayerNames:
    	pl = p[0]
    	play = pl.replace(' ','_') + ".png"
    	#play = pl.replace('_',' ')
    	#print(play)
    	c.execute('UPDATE season_generalplayer SET Image = (?) WHERE Name = (?)',(play,pl))
    	conn.commit()


def DBFieldSetTrueRange ():
    for var in range(70,558):
        c.execute('UPDATE season_generalschedule SET FavoriteStatusHome = (?) WHERE id = (?)',(False,var))
        conn.commit()

def UpdateField ():
    c.execute('UPDATE season_GeneralPlayer SET Position = (?) WHERE Position = (?)',("ST","F"))
    conn.commit()



#CheckDBField()
#UpdateDBField()
#UpdateOtherDBField()
#DBFieldSetTrueRange()
#DBFieldSetTrueRange()
#UpdateField()


#close connection to database
c.close()
conn.close() 