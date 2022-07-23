from enum import IntEnum

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
        return 'asset|{}|acc_id|{}|symbol|{}|trade_time|{}|settle_time|{}|trade_type|{}|quantity|{}|price|{}|commission|{}|fee|{}|proceeds|{}|'.format(
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


class tradeCollection:
    def __init__(self) -> None:
        self._records = []
    22
    def add_rec(self, rec):
        self._records.append(rec)

    def sort_asset_type(self):
        pass

