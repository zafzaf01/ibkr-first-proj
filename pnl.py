from ibapi.client import *
from ibapi.wrapper import *
import time


class TradeApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def pnlSingle(self, reqId: int, pos: Decimal, dailyPnL: float, unrealizedPnL: float, realizedPnL: float,
                  value: float):
        print("Daily PnL Single. ReqId:", reqId, "Position:", pos, "DailyPnL:", dailyPnL, "UnrealizedPnL:",
              unrealizedPnL, "RealizedPnL:", realizedPnL, "Value:", value)


app = TradeApp()
app.connect("127.0.0.1", 7496, clientId=1)
time.sleep(1)
app.reqPnLSingle(101, "U1307494", "", 459113767)  # IBM conId: 8314
app.run()