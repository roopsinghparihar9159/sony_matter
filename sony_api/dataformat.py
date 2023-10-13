import pandas as pd
import numpy as np
import sqlalchemy
engine = sqlalchemy.create_engine('mysql+pymysql://root:E4M^ddMm@localhost:3306/django')

# df = pd.read_csv('./rai-rawdump/rai_dataset.csv')
df = pd.read_csv('/home/roop/main_folder/analysis_sony/rai-rawdump/rai_dataset.csv')
for columns in df.columns:
    if columns == "inserted_at":
        # print(df[columns][0:5])
        ins_date = df[columns]
        date_list = []
        for d in ins_date:
            res = d.split('.')[0]
            date_list.append(res)
        df_ins = pd.DataFrame({'ins_d': date_list})
        df['inserted_at'] = df_ins['ins_d']
        print(df['inserted_at'].head(5))
    if columns =='timestamp':
        # print(df[columns][0:5])
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_convert(None)
        # df['timestamp'] = df['Date']
        # df.drop(['Date'], axis=1, inplace=True)
        print(df['timestamp'].head())

# df.to_csv('/home/roop/Downloads/rai_data.csv',index=False)
df.to_sql(name='dailydata1',con=engine,index=False,if_exists = 'append')