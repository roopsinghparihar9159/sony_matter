import pandas as pd
from io import StringIO
from datetime import date

class Data():

    def trade_df(self):
        # This method should handle the import of source data
        data = StringIO()

        s = """
        Account|Stock_Code|BuySell|Date|Quantity|Unit_Price
        1001|001|B|20190105|8|2
        1001|002|B|20190105|4|3
        1001|002|S|20190106|3|1
        1001|003|B|20190106|6|5
        1001|003|S|20190106|4|6
        1001|001|S|20190107|6|3
        1002|001|B|20190105|6|2
        1002|002|B|20190105|8|3
        1002|002|S|20190106|3|1
        1002|003|B|20190106|5|5
        1002|003|S|20190106|4|6
        1002|001|S|20190107|6|3
        """

        data.write(s.replace(' ',''))
        data.seek(0)
        df = pd.read_csv(data,sep='|',dtype={'Account':str,
                                                'Date':str,
                                                'Stock_Code':str,
                                                "Date":str})
        df.Date = pd.to_datetime(df.Date,format='%Y%m%d')
        # print(df.head())
        return df

    def account_df(self):
        data = StringIO()

        s = """
        Account|Name
        1001|David
        1002|Tom
        """

        data.write(s.replace(' ',''))
        data.seek(0)
        df = pd.read_csv(data, sep='|', dtype={'Account': str,
                                                  'Name': str})
        return df

    def stock_prices(self):

        data = StringIO()

        s = """
        Stock_Code|Closing_Price|Date
        001|2|20190105
        001|3|20190106
        001|2|20190107
        002|2|20190105
        002|3|20190106
        002|5|20190107
        003|5|20190105
        003|6|20190106
        003|7|20190107
        """

        data.write(s.replace(' ',''))
        data.seek(0)
        df = pd.read_csv(data, sep='|', dtype={'Stock_Code': str,
                                                  'Date': str})
        df.Date = pd.to_datetime(df.Date,format='%Y%m%d')
        return df

class Holdings():
    def __init__(self,book):
        self._book = book

    def holdings_of(self,date):
        trades_df = self._book.trade_book_df
        date_hld_df = trades_df[trades_df.Date <= date]
        date_hld_df['qnt_change'] = date_hld_df['BuySell'].map({'B':1,'S':-1}) * date_hld_df.Quantity
        hld_df = date_hld_df.groupby(['Account','Stock_Code'],as_index=False)\
            .agg({'qnt_change':sum})\
            .rename(columns={'qnt_change':'Holdings'})
        hld_df = hld_df.join(self._book.stock_prices(date).set_index('Stock_Code'),on='Stock_Code')
        hld_df['Market_Value'] = hld_df.Closing_Price * hld_df.Holdings
        return hld_df

# Book().holdings.holdings_of(date(2019,1,6))

class Accounts():
    def __init__(self,holdings):
        self._holdings = holdings

    def account_value(self,date):
        df = self._holdings.holdings_of(date)
        return df.groupby('Account',as_index=False).agg({'Market_Value':sum,
                                                         'Date':'first'})

# Book().accounts.account_value(date(2019,1,6))



class Book():
    def __init__(self):
        self._data = Data()

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

Book().trade_book_df
# Book().accounts.account_value(date(2019,1,6))
