from ibapi.client import *
from ibapi.wrapper import *
import threading
import time


class TradingApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def position(self, account: str, contract: Contract, position: Decimal, avgCost: float):
        print("Position.", "Account:", account, "Contract:", contract, "Position:", position, "Avg cost:", avgCost)

    def positionEnd(self):
        print("PositionEnd")


def websocket_con():
    app.run()


app = TradingApp()
app.connect("127.0.0.1", 7496, clientId=123)
con_thread = threading.Thread(target=websocket_con, daemon=True)
con_thread.start()
time.sleep(1)
app.reqPositions()
time.sleep(1)