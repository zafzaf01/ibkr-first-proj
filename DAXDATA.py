from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
import threading
import time

class IBApi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.multiplier = 1  # Set your desired multiplier here
        self.nextOrderId = None
        self.contract_details_received = threading.Event()
        self.market_data_received = threading.Event()
        self.order_status_received = threading.Event()
        self.bid_price = None
        self.ask_price = None

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextOrderId = orderId
        print(f"Next valid order ID: {orderId}")
        self.request_contract_details()

    def request_contract_details(self):
        # Create a contract for Micro DAX (FDXS)
        contract = Contract()
        contract.symbol = 'DAX'
        contract.secType = 'FUT'
        contract.exchange = 'EUREX'
        contract.currency = 'EUR'
        contract.lastTradeDateOrContractMonth = '202409'
        contract.multiplier = "1"  # Multiplier for the Micro DAX contract
        contract.tradingClass = "FDXS"  # Trading class for the Micro DAX contract
        # Request contract details
        print("Requesting contract details")
        self.reqContractDetails(1, contract)  # reqId = 1

    def contractDetails(self, reqId, contractDetails):
        print(f"Contract Details - ReqId: {reqId}, Symbol: {contractDetails.contract.symbol}, SecType: {contractDetails.contract.secType}, Exchange: {contractDetails.contract.exchange}, Currency: {contractDetails.contract.currency}, LastTradeDate: {contractDetails.contract.lastTradeDateOrContractMonth}")
        if reqId == 1:
            self.contract_details_received.set()
            self.request_market_data(contractDetails.contract)

    def request_market_data(self, contract):
        # Request market data snapshot
        print("Requesting market data")
        self.reqMktData(2, contract, "", False, False, [])  # reqId = 2

    def tickPrice(self, reqId, tickType, price, attrib):
        if reqId == 2:
            if tickType == 1:  # BID price
                self.bid_price = price
                print(f"Received BID price: {price}")
            elif tickType == 2:  # ASK price
                self.ask_price = price
                print(f"Received ASK price: {price}")
            if self.bid_price is not None and self.ask_price is not None:
                self.market_data_received.set()
                self.start()

    def start(self):
        # Create a contract for Micro DAX (FDXS)
        contract = Contract()
        contract.symbol = 'DAX'
        contract.secType = 'FUT'
        contract.exchange = 'EUREX'
        contract.currency = 'EUR'
        contract.lastTradeDateOrContractMonth = '202409'
        contract.multiplier = "1"
        contract.tradingClass = "FDXS"

        # Create an order
        order = Order()
        order.action = "BUY"
        order.orderType = "LMT"
        order.totalQuantity = 1 * self.multiplier  # Use the multiplier here
        order.lmtPrice = self.bid_price + 1  # Example: Buy at the bid price + 1

        # Place the order
        print(f"Placing order to buy {order.totalQuantity} contracts at {order.lmtPrice}")
        self.placeOrder(self.nextOrderId, contract, order)
        self.nextOrderId += 1

    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        print(f"Order Status - Id: {orderId}, Status: {status}, Filled: {filled}, Remaining: {remaining}, AvgFillPrice: {avgFillPrice}")
        if status in ['Filled', 'Cancelled', 'Inactive']:
            self.order_status_received.set()

    def openOrder(self, orderId, contract, order, orderState):
        print(f"Open Order - Id: {orderId}, {contract.symbol}, {contract.secType}, {contract.exchange}, {order.action}, {order.orderType}, {order.totalQuantity}, {orderState.status}")

    def execDetails(self, reqId, contract, execution):
        print(f"ExecDetails - ReqId: {reqId}, Symbol: {contract.symbol}, SecType: {contract.secType}, Currency: {contract.currency}, ExecId: {execution.execId}, OrderId: {execution.orderId}, Shares: {execution.shares}, Price: {execution.price}")

    def error(self, reqId, errorCode, errorString):
        print(f"Error - ReqId: {reqId}, Code: {errorCode}, Msg: {errorString}")
        if errorCode == 354:  # Market data subscription error
            self.market_data_received.set()  # Ensure the event is set to avoid hanging

def run_loop():
    app.run()

app = IBApi()
app.connect("127.0.0.1", 7496, 123)

api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

# Wait for the contract details to be received, market data to be received, and order status to be received
app.contract_details_received.wait()
app.market_data_received.wait()
app.order_status_received.wait()

# To ensure all messages are processed before disconnecting
time.sleep(2)

app.disconnect()
print("Disconnected")
