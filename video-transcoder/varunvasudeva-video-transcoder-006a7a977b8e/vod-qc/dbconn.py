#Establish DB connection
from conf import *
import pymysql
def dbconn():	#DB connection parameters must be configured from conf file.
	db=pymysql.connect(
		host=dbHost,
		user=dbUser,
		password=dbPass,
		db=dbName
	)
	cur=db.cursor()
	return(cur,db)