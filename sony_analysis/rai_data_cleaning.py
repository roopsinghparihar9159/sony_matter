import pandas as pd
import numpy as np
import sqlalchemy

engine = sqlalchemy.create_engine('mysql+pymysql://root:E4M^ddMm@localhost:3306/RAI_DB')

df = pd.read_csv('./rai-rawdump/rai_dataset.csv')
print(len(df))
# df.drop(['Unnamed: 0'],axis=1,inplace=True)
# print(df.head())

if len(df)>0:
    for col in df.columns:
        if df[col].isna().sum()>=1:
            df[col]=df[col].fillna(method='ffill')
            df[col]=df[col].fillna(method='bfill')
            if 'customLog'==col:
                df[col]=df[col].fillna('No Value')
                df[col]=df[col].replace('NA','No Value')
                print('This is a custome log')
        elif 'timestamp'==col:
        #     date = pd.to_datetime(df['timestamp']).dt.date
        #     time = pd.to_datetime(df['timestamp']).dt.time
        #     df_timestamp = pd.DataFrame({'Date':date,'Time':time})
        #     # print(df_timestamp)
        #     df['timestamp1']=pd.to_datetime(df_timestamp.Date.astype(str)+' '+df_timestamp.Time.astype(str))
            print('Working on timestamp')
            df['Date'] = pd.to_datetime(df['timestamp']).dt.tz_convert(None)
            df['timestamp']=df['Date']
            df.drop(['Date'],axis=1,inplace=True)
            print(df['timestamp'].head())
        elif 'inserted_at'==col:
            print('Working on Inserted At')
            # ins_date = df.inserted_at
            ins_date = df[col]
            date_list = []
            for d in ins_date:
                res = d.split('.')[0]
                date_list.append(res)  
            df_ins = pd.DataFrame({'ins_d':date_list})
            df['inserted_at']=df_ins['ins_d']
            print(df['inserted_at'].head(20))  
        else:
            print('NaN value not present')
    # na_value = df.isna().sum()
    # df.to_csv('final.csv',index=False)
    # na_value.to_csv('na_value.csv')    
    df.to_sql(name='dailydata',con=engine,index=False,if_exists = 'append')
    print("Successfully Uploaded data in database")
else:
    print("No data found in sheet ")
