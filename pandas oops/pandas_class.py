import pandas as pd
import numpy as np

# df1 = pd.DataFrame({'a':[1,3,4]})
df1 = pd.read_csv('data.csv')

class Data():
    def __init__(self, df):
        self.df = df
        # print(df)
    def trade_df(self):
        self.df.Date = pd.to_datetime(self.df.Date,format='%Y%m%d')
        return self.df
    def account_df(self):
        df_account = pd.DataFrame({'Account':[1001,1002],'Name':['David','Tom']})
        # print(df_account)
        return df_account
    def stock_prices(self):

        df_stock = pd.DataFrame({
            'Stock_Code':[1,1,1,2,2,2,3,3,3],
            'Closing_Price':[2,3,2,2,3,5,5,6,7],
            'Date':[20190105,20190106,20190107,20190105,20190106,20190107,20190105,20190106,20190107]})
            
        df_stock.Date = pd.to_datetime(df_stock.Date,format='%Y%m%d')
        return df_stock


# m1 = Data(df1)
# print(type(m1))

# print(m1.account_df())
# print(m1.stock_prices())
class Book():
    def __init__(self):
        self._data = Data(df1)

    @property
    def trade_book_df(self):
        if not hasattr(self,'_trade_book_df'):
            df = self._data.trade_df().join(self._data.account_df().set_index('Account'),on='Account')
            df['Trade_Amount'] = df.Quantity * df.Unit_Price
            self._trade_book_df = df
        return self._trade_book_df

    def stock_prices(self,date=None):
        df = self._data.stock_prices()
        if date:
            df = df[df.Date == date]
        return df

    @property
    def holdings(self):
        return Holdings(self)

    @property
    def accounts(self):
        return Accounts(self.holdings)

print(Book().trade_book_df)
book = Book()
print(book.stock_prices())
class Holdings():
    def __init__(self,book):
        self._book = book
        print(book)

    def holdings_of(self,date):
        date = np.datetime64(date)
        # date64 = np.datetime64(date)
        trades_df = self._book.trade_book_df
        date_hld_df = trades_df[trades_df.Date <= date]
        # print(date_hld_df.Quantity)
        date_hld_df['qnt_change'] = date_hld_df[date_hld_df["BuySell"]=='B']=1 
        # data.loc[data.bidder == 'parakeet2004', 'bidderrate'] = 100
        print(date_hld_df.qnt_change)
        hld_df = date_hld_df.groupby(['Account','Stock_Code'],as_index=False)\
            .agg({'qnt_change':sum})\
            .rename(columns={'qnt_change':'Holdings'})
        hld_df = hld_df.join(self._book.stock_prices(date).set_index('Stock_Code'),on='Stock_Code')
        hld_df['Market_Value'] = hld_df.Closing_Price * hld_df.Holdings
        print(hld_df)
        return hld_df

from datetime import date
Book().holdings.holdings_of(date(2019,1,6))
# print(Book().holdings)