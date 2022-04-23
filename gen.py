import os
print(os.name)
import platform
print(platform.system(), platform.release())

import json
import argparse
import re
from bs4 import BeautifulSoup
import re
from datetime import datetime
from dateutil.parser import parse
from os import listdir
from os.path import isfile, join
from trade_details import *
# parse_file
#     parse_html
#         parse_tr
            # TradeDetails.from_tag




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
    # PATH_TO_REPORTS = '/Users/msab8448/Google Drive/FANCY__/Trader/IB/workspace'
    PATH_TO_REPORTS = '/home/max/winhome/Google Drive/FANCY__/Trader/IB/workspace'

    def __init__(self) -> None:
        self._current_asset_kind = assetKind.UNKNOWN

    def get_file_list(self, path):
        res = [join(path, f) for f in listdir(path) if isfile(join(path, f)) and re.match(r'^DailyTradeReport.\d{8}.html$', f)]
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
                    pass
                elif kind == app.TOKEN_NAME_TRADE_REC:
                    yield(token)


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
            title = soup.title.text
            yield (app.TOKEN_NAME_TITLE, soup.title.get_text())
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
