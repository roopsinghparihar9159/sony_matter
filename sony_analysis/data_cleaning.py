import pandas as pd
import numpy as np
import sqlalchemy

engine = sqlalchemy.create_engine('mysql+pymysql://root:password@localhost:3306/RAI_DB')

# df = pd.read_sql_table("dailydata",engine,columns=['casted','convivaSessionId','chipset','bufferStatus'])
# print(df)
df = pd.read_csv('person.csv')
# print(len(df))
if len(df)>0:
    # print(df)
    df.rename(columns={'Last Name':'LastName','First Name':'FirstName'},inplace=True)
    df.to_sql(name='Persons',con=engine,index=False,if_exists = 'append')
    print("Successfully Uploaded data in database")