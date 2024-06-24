from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

import threading
import time

print("Hello here we start")

class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def tickPrice(self, reqId, tickType, price, attrib):
        if reqId == 1:
            if tickType == 1:
                print('The current bid price is: ', price)
            elif tickType == 2:
                print('The current ask price is: ', price)
            elif tickType == 4:
                print('The current last price is: ', price)

    def error(self, reqId, errorCode, errorString):
        print(f"Error {errorCode}: {errorString}")

def run_loop():
    app.run()

app = IBapi()
app.connect('127.0.0.1', 7496, 123)

# Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

time.sleep(1)  # Sleep interval to allow time for connection to server

# Check if the client is connected
if app.isConnected():
    print("Connected to TWS")
else:
    print("Failed to connect to TWS")
    exit()

# Create contract object
contract = Contract()
contract.symbol = "AAPL"
contract.secType = "STK"
contract.exchange = "SMART"
contract.currency = "USD"

# Request Market Data
app.reqMarketDataType(3)  # Changed to 3 for delayed data
app.reqMktData(1, contract, '', False, False, [])

time.sleep(15)  # Increased sleep time for delayed data

app.disconnect()