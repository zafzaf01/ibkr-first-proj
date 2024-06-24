from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from threading import Thread
import time


class IBApi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString):
        print(f"Error: {reqId}, Error Code: {errorCode}, Error Msg: {errorString}")

    def tickPrice(self, reqId, tickType, price, attrib):
        print(f"Tick Price. Ticker Id: {reqId}, tickType: {tickType}, Price: {price}")

    def tickSize(self, reqId, tickType, size):
        print(f"Tick Size. Ticker Id: {reqId}, tickType: {tickType}, Size: {size}")

    def connectAck(self):
        if self.asynchronous:
            print("API connected asynchronously")


def run_loop():
    app.run()


app = IBApi()
app.connect("127.0.0.1", 7496, 123)  # Ensure correct IP and port

# Start the socket in a thread
api_thread = Thread(target=run_loop, daemon=True)
api_thread.start()

time.sleep(5)  # Increased sleep interval to allow connection to server

# Check if the client is connected
if app.isConnected():
    print("Connected to TWS")
else:
    print("Failed to connect to TWS")

# Define the contract for the E-mini S&P 500 futures
contract = Contract()
contract.symbol = "ES"
contract.secType = "FUT"
contract.exchange = "CME"
contract.currency = "USD"
contract.lastTradeDateOrContractMonth = "202409"  # Example for September 2024 contract

# Request market data
app.reqMarketDataType(3)
app.reqMktData(1, contract, "", False, False, [])

# Keep the script running to get data
time.sleep(10)  # Adjust as needed
app.disconnect()