import sqlite3 as sql

con = sql.connect('employee.db')
cur = con.cursor()

sql = ''' CREATE TABLE "users"("ID" INTEGER PRIMARY KEY AUTOINCREMENT,"NAME" TEXT,"CONTACT" TEXT,"ADDRESS" TEXT)'''

cur.execute(sql)
con.commit()
con.close()