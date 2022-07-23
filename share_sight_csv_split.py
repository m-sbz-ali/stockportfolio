
import csv
from os.path import isfile, join


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

    def __init__(self, row_val) -> None:

        self.is_valid = False

        if len (row_val) < 17:
            return

        self.FXRateToBase = row_val[csvRecord.FXRATETOBASE]
        self.Symbol = row_val[csvRecord.SYMBOL]
        self.CUSIP = row_val[csvRecord.CUSIP]
        self.TradeID = row_val[csvRecord.TRADEID]
        self.DateTime = row_val[csvRecord.DATETIME]
        self.Quantity = row_val[csvRecord.QUANTITY]
        self.TradePrice = row_val[csvRecord.TRADEPRICE]
        self.Proceeds = row_val[csvRecord.PROCEEDS]
        self.CostBasis = row_val[csvRecord.COSTBASIS]
        self.FifoPnlRealized = row_val[csvRecord.FIFOPNLREALIZED]
        self.Open_CloseIndicator= row_val[csvRecord.OPEN_CLOSEINDICATOR]
        self.Buy_Sell = row_val[csvRecord.BUY_SELL]
        self.CurrencyPrimary= row_val[csvRecord.CURRENCYPRIMARY]
        self.Description = row_val[csvRecord.DESCRIPTION]
        self.IBCommission = row_val[csvRecord.IBCOMMISSION]
        self.IBCommissionCurrency = row_val[csvRecord.IBCOMMISSIONCURRENCY]
        self.NetCash = row_val[csvRecord.NETCASH]
        self.FxPnl = row_val[csvRecord.FXPNL]

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
            self.NetCash,
            self.FxPnl)

class csvSplit:
    CSV_PATH = "/home/max/stockportfolio/tests"
    FILE_NAME = "test.csv"

    def __init__(self) -> None:
        pass

    def load_csv(self, file=""):

        f = join(self.CSV_PATH,self.FILE_NAME)
        if len(file) > 0:
            f = join(self.CSV_PATH,file)

        with open(f, newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            for row in csv_reader:
                rec = csvRecord(row)
                if rec.is_valid:
                    print(rec)

    def split(self):
        pass

    def save(self):
        pass