
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

import threading
import time

class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)


    def tickPrice(self, reqId, tickType, price, attrib):
        if tickType == 2:  # Ask price tick type
            print(f"Ask Price: {price}")

def run_loop():
    app.run()

app = IBapi()
app.connect('127.0.0.1', 7496, 123)

# Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

time.sleep(1)  # Give the API some time to establish a connection

contract = Contract()
contract.symbol = "ES"
contract.secType = "FUT"
contract.exchange = "CME"
contract.currency = "USD"
contract.lastTradeDateOrContractMonth = "202409"

#Request Market Data
app.reqMarketDataType(2)
app.reqMktData(1, contract, '', False, False, [])


time.sleep(10) #Sleep interval to allow time for incoming price data
app.disconnect()