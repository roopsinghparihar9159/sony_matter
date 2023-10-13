"""Normal connection"""
import mysql.connector

def dbconn():	#DB connection parameters must be configured from conf file.
	mydb = mysql.connector.connect(
  host = "173.16.16.14",
  user = "vod", #"root",
  #password="Cyberlinks",
  database="vodTranscoder"# charset="utf8"
)
	cur = mydb.cursor()
	return(cur,mydb)


# print("mydb",mydb)
# c = mydb.cursor()
# '''-------------------------------------'''
# # print(c)

# c.execute("SHOW DATABASES")
# l = c.fetchall()
# print("all_databases: ",l)
# c.execute("SHOW DATABASES")

# c.execute("SELECT * FROM transcoder")

# myresult = c.fetchall()

# for x in myresult:
#   print(x)