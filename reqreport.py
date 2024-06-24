from ibapi.client import *
from ibapi.wrapper import *
from ibapi.contract import Contract
import time
import threading
import time


class TradeApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def accountSummary(self, reqId: int, account: str, tag: str, value: str, currency: str):
        print("AccountSummary. ReqId:", reqId, "Account:", account, "Tag: ", tag, "Value:", value, "Currency:",
              currency)

    def accountSummaryEnd(self, reqId: int):
        print("AccountSummaryEnd. ReqId:", reqId)

def run_loop():
    app.run()

app=TradeApp()
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()


app.connect("127.0.0.1", 7496, clientId=1)
time.sleep(1)

app.reqAccountSummary(9001, "All", 'NetLiquidation')
app.run()
print("ssss22")
app.disconnect()