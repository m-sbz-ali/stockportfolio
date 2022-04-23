import json
import argparse
import re
from bs4 import BeautifulSoup
import re
from datetime import datetime
from dateutil.parser import parse
from enum import IntEnum
from os import listdir
from os.path import isfile, join

# parse_file
#     parse_html
#         parse_tr
            # TradeDetails.from_tag
    



class HTML_KEYS:
    CFDS = 'CFDs'

class assetKind(IntEnum):
    UNKNOWN = 0

    STOCK = 1
    CFD = 2
    FOREX = 3

    @staticmethod
    def name(kind) -> str:
        if kind == assetKind.STOCK:
            return 'Stock'
        if kind == assetKind.CFD:
            return 'CFD'
        if kind == assetKind.FOREX:
            return 'Forex'
        return "Unknown"

class tradeCollection:
    def __init__(self) -> None:
        self._records = []
    22
    def add_rec(self, rec):
        self._records.append(rec)
    
    def sort_asset_type(self):
        pass
        # sorted(self._records, )
        

class TradeDetails:
    def __init__(self) -> None:
        self.asset_kind = assetKind.UNKNOWN
        self.acc_id = ''
        self.symbol = ''
        self.trade_time = ''
        self.settle_time = ''
        self.trade_type = ''
        self.quantity = 0
        self.price = 0
        self.commission = 0
        self.fee = 0
        self.proceeds = 0
    @classmethod
    def from_tag(cls, tr, asset_kind):
        obj = cls()
        items = [x.get_text() for x in tr if x!= '\n']
        # tokens = '{}'.format(token).split(' ')
                    # asset = ''.join(t for t in tokens[0:2]).split(',')[0].replace(':','#')
                    # acc_id = tokens[2].replace(':','#')
                    # symbol = tokens[3].replace(':','#')
                    # trade_time = '{} {}'.format(tokens[4].replace(':','#').split(',')[0], tokens[5])
                    # settle_time = tokens[6].replace(':','#')
                    # trade_type = tokens[7].replace(':','#')
                    # quantity = tokens[8].replace(':','#')
                    # price = tokens[9].replace(':','#')
                    # commission = tokens[10].replace(':','#')
                    # fee = tokens[11].replace(':','#')
                    # proceeds = tokens[12].replace(':','#')
        
        
        obj.asset_kind = asset_kind
        obj.acc_id = items[0]
        obj.symbol = items[1]
        if obj.symbol[-1] == 'n' and asset_kind != assetKind.CFD:
            raise Exception("Bad Asset Type:{}".format(asset_kind))
        obj.trade_time = items[2]
        obj.settle_time = items[3]
        obj.trade_type = items[5]
        obj.quantity = items[6]
        obj.price = items[7]
        obj.proceeds = items[8]
        obj.commission = items[9]
        obj.fee = items[10]
        return obj


    def __repr__(self) -> str:
        return 'asset#{},acc_id#{},symbol#{},trade_time#{},settle_time#{},trade_type#{},quantity#{},price#{},commission#{},fee#{},proceeds#{}'.format(
            assetKind.name(self.asset_kind), 
            self.acc_id, self.symbol,
            self.trade_time,
            self.settle_time,
            self.trade_type,
            self.quantity,
            self.price,
            self.commission,
            self.fee,
            self.proceeds)

class app:
    TOKEN_NAME_CONTROL = 'control'
    TOKEN_NAME_TITLE = 'title'
    TOKEN_NAME_CONTENT = 'content'
    TOKEN_NAME_TRADE_REC = 'Trade'

    TOKEN_NAME_ACCOUNT = 'account'
    TOKEN_NAME_REPORT_TYPE_DTR = 'DTR'
    TOKEN_NAME_DATE = 'date'
    TOKEN_NAME_CFDS = 'CFDs'
    TOKEN_NAME_ASSET_TYPE_STOCK = 'Stocks'
    TOKEN_NAME_FOREX = 'Forex'
    
    TOKEN_NAME_CURRENCY_USD = 'USD'
    PATH_TO_REPORTS = '/Users/msab8448/Google Drive/FANCY__/Trader/IB/workspace'

    def __init__(self) -> None:
        self._current_asset_kind = assetKind.UNKNOWN

    def get_file_list(self, path):
        res = [f for f in listdir(path) if isfile(join(path, f)) and re.match(r'^DailyTradeReport.\d{8}.html$', f)]
        return res

    def parse_title(self, t : str):
        token = t.split()
        print(token)
        date_time_str = ' '.join(x for x in token[4:7])
        _date = parse(date_time_str)

        return {app.TOKEN_NAME_ACCOUNT : token[0], app.TOKEN_NAME_REPORT_TYPE_DTR : ' '.join(x for x in token[1:4]),
                app.TOKEN_NAME_DATE : '{}'.format(_date)
            }

    def parse_tr(self, tr):
        for _item in tr:
            for __item in _item:
                if 'U***' in __item.get_text():
                    return (app.TOKEN_NAME_TRADE_REC, TradeDetails.from_tag(_item, self._current_asset_kind))
                elif __item.get_text() == app.TOKEN_NAME_CFDS:
                    self._current_asset_kind = assetKind.CFD
                elif __item.get_text() == app.TOKEN_NAME_ASSET_TYPE_STOCK:
                    self._current_asset_kind = assetKind.STOCK
                elif __item.get_text() == app.TOKEN_NAME_FOREX:
                    self._current_asset_kind = assetKind.FOREX

        return None

    def parse_file(self, file_name):
        for item in self.parse_html(file_name):
            if item:
                kind,token = item
                if kind in (app.TOKEN_NAME_CONTROL,):
                    pass
                elif kind == app.TOKEN_NAME_TITLE:
                    # yield ('{}'.format(self.parse_title(token)))
                    pass
                elif kind == app.TOKEN_NAME_TRADE_REC:
                    yield(token)
                    # tokens = '{}'.format(token).split(' ')
                    # asset = ''.join(t for t in tokens[0:2]).split(',')[0].replace(':','#')
                    # acc_id = tokens[2].replace(':','#')
                    # symbol = tokens[3].replace(':','#')
                    # trade_time = '{} {}'.format(tokens[4].replace(':','#').split(',')[0], tokens[5])
                    # settle_time = tokens[6].replace(':','#')
                    # trade_type = tokens[7].replace(':','#')
                    # quantity = tokens[8].replace(':','#')
                    # price = tokens[9].replace(':','#')
                    # commission = tokens[10].replace(':','#')
                    # fee = tokens[11].replace(':','#')
                    # proceeds = tokens[12].replace(':','#')
                    # yield ('{},{},{},{},{},{},{},{},{},{},{}'.format(asset, acc_id, symbol, trade_time, settle_time, trade_type, quantity, price, commission, fee, proceeds))

    
    def run(self):
        state = 0
        cfd = False
        all_recs = []

        with open('trades.txt', 'a') as f:

            for in_file in self.get_file_list(app.PATH_TO_REPORTS):
                for _rec in self.parse_file(in_file):
                    if _rec:
                        all_recs.append(_rec)
                        f.write('{}'.format(_rec))
                        f.write('\n')

    def parse_html(self, file_name):
        with open(file_name, 'r') as f:
            contents = f.read()
            soup = BeautifulSoup(contents, 'lxml')
            # print(soup.prettify())
            # return 
            title = soup.title.text
            yield (app.TOKEN_NAME_TITLE, soup.title.get_text())
            # print(soup.title)
            # print(title)
            # print(soup.find('ul', id='mylist'))
            # # tags = soup.find_all(['h2', 'p'])
            # strings = soup.find_all(string=re.compile(HTML_KEYS.CFDS))
            # for txt in strings:
            #     print(' '.join(txt.split()))
            res = soup.find_all("tbody")

            for item in res:
                _res = item.find_all(['tr'])
                if _res:
                    yield self.parse_tr(_res)

def main():
    app_ = app()
    app_.run()

if __name__ == "__main__":
     main()
