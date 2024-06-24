from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract


class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def tickPrice(self, reqId, tickType, price, attrib):
        print("lets go")
        if tickType == 1:
            print(f'Bid Price: {price}')
        elif tickType == 2:
            print(f'Ask Price: {price}')
        elif tickType == 4:
            print(f'Last Price: {price}')



def run_loop():
    app.run()


app = IBapi()
app.connect('127.0.0.1', 7496, 123)

# Check if the client is connected
if app.isConnected():
    print("Connected to TWS")
else:
    print("Failed to connect to TWS")

# Define the E-mini S&P 500 futures contract
contractt = Contract()
contractt.symbol = 'ES'
contractt.secType = 'FUT'
contractt.exchange = 'CME'
contractt.currency = 'USD'
contractt.lastTradeDateOrContractMonth = '202409'  # September 2023 contract

# Request market data
app.reqMarketDataType(1)
app.reqMktData(1, contractt, "", False, False, [])

# Start the socket in a separate thread
import threading

api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

# Sleep while the socket runs in the background
import time

time.sleep(10)

# Disconnect
app.disconnect()