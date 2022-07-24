
import csv
from os.path import isfile, join
from typing import Dict, List
import xlsxwriter
import string

# FXRateToBase	Symbol	CUSIP	TradeID	DateTime	Quantity	TradePrice	Proceeds	CostBasis	FifoPnlRealized	Open/CloseIndicator	Buy/Sell	CurrencyPrimary	Description	IBCommission	IBCommissionCurrency	NetCash	FxPnl


class csvRecord:
    FXRATETOBASE = 0
    SYMBOL = 1
    CUSIP = 2
    TRADEID = 3
    DATETIME = 4
    QUANTITY = 5
    TRADEPRICE = 6
    PROCEEDS = 7
    COSTBASIS = 8
    FIFOPNLREALIZED = 9
    OPEN_CLOSEINDICATOR= 10
    BUY_SELL = 11
    CURRENCYPRIMARY= 12
    DESCRIPTION = 13
    IBCOMMISSION = 14
    IBCOMMISSIONCURRENCY = 15
    NETCASH = 16
    FXPNL = 17
    CELL_FORMATS ={'FXRateToBase' : '0.0000',
            'Symbol':'',
            'CUSIP':'',
            'TradeID':'0',
            'DateTime':'@',
            'Quantity':'0',
            'TradePrice':'$#,##0.000',
            'Proceeds':'$#,##0.00;-$#,##0.00',
            'CostBasis':'$#,##0.00;-$#,##0.00',
            'FifoPnlRealized':'$#,##0.00;-$#,##0.00',
            'Open_CloseIndicator':'',
            'Buy_Sell':'',
            'CurrencyPrimary':'',
            'Description':'',
            'IBCommission':'$#,##0.00;-$#,##0.00',
            'IBCommissionCurrency':'',
            # 'NetCash':'$#,##0.00;-$#,##0.00',
            # 'FxPnl':'$#,##0.00;-$#,##0.00',
        }

    def to_float(val_lst, index):
        try:
            return float(val_lst[index])
        except ValueError:
            return  val_lst[index]

    def to_int(val_lst, index):
        try:
            return int(val_lst[index])
        except ValueError:
            return  val_lst[index]

    def __init__(self, row_val) -> None:

        self.is_valid = False

        if len (row_val) < 17:
            return

        self.FXRateToBase = csvRecord.to_float(row_val, csvRecord.FXRATETOBASE)

        self.Symbol = row_val[csvRecord.SYMBOL]
        self.CUSIP = row_val[csvRecord.CUSIP]

        self.TradeID = csvRecord.to_float(row_val, csvRecord.TRADEID)

        self.DateTime = row_val[csvRecord.DATETIME]

        self.Quantity = csvRecord.to_float(row_val, csvRecord.QUANTITY)

        self.TradePrice = csvRecord.to_float(row_val, csvRecord.TRADEPRICE)
        self.Proceeds = csvRecord.to_float(row_val, csvRecord.PROCEEDS)
        self.CostBasis = csvRecord.to_float(row_val, csvRecord.COSTBASIS)
        self.FifoPnlRealized = csvRecord.to_float(row_val, csvRecord.FIFOPNLREALIZED)
        self.Open_CloseIndicator= row_val[csvRecord.OPEN_CLOSEINDICATOR]
        self.Buy_Sell = row_val[csvRecord.BUY_SELL]
        self.CurrencyPrimary= row_val[csvRecord.CURRENCYPRIMARY]
        self.Description = row_val[csvRecord.DESCRIPTION]
        self.IBCommission = csvRecord.to_float(row_val, csvRecord.IBCOMMISSION)
        self.IBCommissionCurrency = row_val[csvRecord.IBCOMMISSIONCURRENCY]
        # self.NetCash = csvRecord.to_float(row_val, csvRecord.NETCASH)
        # self.FxPnl = csvRecord.to_float(row_val, csvRecord.FXPNL)

        self.is_valid = True

    def __str__(self) -> str:
        return '{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},'.format(
            self.FXRateToBase,
            self.Symbol,
            self.CUSIP,
            self.TradeID,
            self.DateTime,
            self.Quantity,
            self.TradePrice,
            self.Proceeds,
            self.CostBasis,
            self.FifoPnlRealized,
            self.Open_CloseIndicator,
            self.Buy_Sell,
            self.CurrencyPrimary,
            self.Description,
            self.IBCommission,
            self.IBCommissionCurrency,
            # self.NetCash,
            # self.FxPnl
            )

    def __repr__(self) -> str:
        return self.__str__()

class csvSplit:
    # CSV_PATH = "/home/max/stockportfolio/tests"
    CSV_PATH = "/home/max/winhome/work/tax/2023/trades/IB/"
    FILE_NAME = "U4612743_U4612743_20210701_20220630.csv"
    clmmns_letters = string.ascii_uppercase

    def __init__(self) -> None:
        pass

    def load_csv(self, file="", ignore_first_n_recs = 0):

        f = join(self.CSV_PATH,self.FILE_NAME)
        if len(file) > 0:
            f = join(self.CSV_PATH,file)

        self.rec_lst = {} # type Dict(List[csvRecord])

        with open(f, newline='') as csvfile:

            csv_reader = csv.reader(csvfile, delimiter=',')
            rec_no = 1
            for row in csv_reader:
                if rec_no <= ignore_first_n_recs:
                    rec_no += 1
                    continue
                rec = csvRecord(row)
                if rec.is_valid:
                    try:
                        self.rec_lst[rec.Symbol].append(rec)
                    except KeyError:
                        self.rec_lst[rec.Symbol] = [rec]

                rec_no += 1

            for key in self.rec_lst.keys():
                print(key, ':', len (self.rec_lst.get(key)))

    def split(self):
        csv.excel_tab()
        pass


    def get_cell_format(self, field_name):

        return

    def save_header(self, worksheet, symbol):
        filed_names=[]
        for trade in self.rec_lst[symbol]:
            trade_fields = trade.__dict__
            clmmn_index = 0
            for field in trade_fields.keys():
                if field in ('is_valid',):
                    continue
                _clm_name = '{}{}'.format(csvSplit.clmmns_letters[clmmn_index], 1)
                clmmn_index += 1
                filed_names.append(field)
                worksheet.write(_clm_name, '{}'.format(field))
            return


    def save_to_xls(self):
        workbook = xlsxwriter.Workbook('all_trades.xlsx')
        for symbol in self.rec_lst.keys():
            worksheet  = workbook.add_worksheet('{}_trades'.format(symbol))
            self.save_header(worksheet, symbol)
            row = 2
            for trade in self.rec_lst[symbol]:
                trade_fields = trade.__dict__
                clmmn_index = 0
                for field in trade_fields.keys():
                    if field in ('is_valid',):
                        continue
                    _clm_name = '{}{}'.format(csvSplit.clmmns_letters[clmmn_index], row)
                    clmmn_index += 1
                    worksheet.write(_clm_name, trade_fields[field])
                row +=1

        workbook.close()


        pass