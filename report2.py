from ibapi.client import *
from ibapi.wrapper import *
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
class TradeApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.data_received = threading.Event()

    def accountSummary(self, reqId: int, account: str, tag: str, value: str, currency: str):
        print("AccountSummary. ReqId:", reqId, "Account:", account, "Tag: ", tag, "Value:", value, "Currency:", currency)

    def accountSummaryEnd(self, reqId: int):
        print("AccountSummaryEnd. ReqId:", reqId)
        self.data_received.set()

def run_loop():
    app.run()
    app1.run()

app = TradeApp()
app.connect("127.0.0.1", 7496, clientId=1)
app1 = IBapi()


# Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

time.sleep(1)  # Give time for connection to establish

app.reqAccountSummary(9001, "All", 'NetLiquidation')

# Wait for the data to be received (with a timeout)
if not app.data_received.wait(timeout=10):
    print("Timeout waiting for account summary data")

# Create contract object
contract = Contract()
contract.symbol = "XAUUSD"
contract.secType = "CMDTY"
contract.exchange = "SMART"
contract.currency = "USD"



app.disconnect()
print("Disconnected")
app1.connect("127.0.0.1", 7496, clientId=1)
time.sleep(10)
app1.reqMarketDataType(3)
app1.reqMktData(1, contract, '', False, False, [])
app1.disconnect()
print("Disconnected2")
# Wait for the thread to finish
api_thread.join(timeout=5)