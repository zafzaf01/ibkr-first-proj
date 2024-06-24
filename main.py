from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

import threading
import time



class IBapi(EWrapper, EClient):
	def __init__(self):
		EClient.__init__(self, self)
	def tickPrice(self, reqId, tickType, price, attrib):
		print("jjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
		if tickType == 2 and reqId == 1:
			print('The current ask price is: ', price)

def run_loop():
	app.run()


app = IBapi()
app.connect('127.0.0.1', 7496, 123)

#Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()


time.sleep(10) #Sleep interval to allow time for connection to server

# Check if the client is connected
if app.isConnected():
    print("Connected to TWS")
else:
    print("Failed to connect to TWS")

#Create contract object
contractt = Contract()
contractt.symbol = "XAUUSD"
contractt.secType = "CMDTY"
contractt.exchange = "SMART"
contractt.currency = "USD"



#Request Market Data
print("Hello here we start")
app.reqMarketDataType(3)
app.reqMktData(1, contractt, '', False, False, [])
print("Hello here we start2")
time.sleep(15) #Sleep interval to allow time for incoming price data
print("Hello here we start3")
app.disconnect()
print("Hello here we start4")

# if __name__ == "__main__":
#     main()