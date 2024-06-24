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
        self.order_placed = threading.Event()

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextOrderId = orderId
        self.request_contract_details()

    def request_contract_details(self):
        # Create a contract
        contract = Contract()
        contract.symbol = 'DAX'
        contract.secType = 'FUT'
        contract.exchange = 'EUREX'
        contract.currency = 'EUR'
        contract.lastTradeDateOrContractMonth = '202409'
        contract.multiplier = "1"  # Adding the multiplier for the DAX contract
        contract.tradingClass = "FDXS"  # Adding the trading class for the DAX contract
        # Request contract details
        self.reqContractDetails(1, contract)

    def contractDetails(self, reqId, contractDetails):
        print(f"Contract Details - ReqId: {reqId}, Symbol: {contractDetails.contract.symbol}, SecType: {contractDetails.contract.secType}, Exchange: {contractDetails.contract.exchange}, Currency: {contractDetails.contract.currency}, LastTradeDate: {contractDetails.contract.lastTradeDateOrContractMonth}")
        self.contract_details_received.set()
        self.start(contractDetails.contract)

    def start(self, contract):
        # Create an order
        order = Order()
        order.action = "SELL"
        order.orderType = "LMT"
        order.totalQuantity = 1 * self.multiplier  # Use the multiplier here
        order.lmtPrice = 18500

        # Place the order
        self.placeOrder(self.nextOrderId, contract, order)
        print(f"Placed order to buy {order.totalQuantity} contracts at {order.lmtPrice}")
        self.nextOrderId += 1
        self.order_placed.set()

    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        print(f"Order Status - Id: {orderId}, Status: {status}, Filled: {filled}, Remaining: {remaining}, AvgFillPrice: {avgFillPrice}")
        if status in ['Filled', 'Cancelled', 'Inactive']:
            self.disconnect()

    def openOrder(self, orderId, contract, order, orderState):
        print(f"Open Order - Id: {orderId}, {contract.symbol}, {contract.secType}, {contract.exchange}, {order.action}, {order.orderType}, {order.totalQuantity}, {orderState.status}")

    def execDetails(self, reqId, contract, execution):
        print(f"ExecDetails - ReqId: {reqId}, Symbol: {contract.symbol}, SecType: {contract.secType}, Currency: {contract.currency}, ExecId: {execution.execId}, OrderId: {execution.orderId}, Shares: {execution.shares}, Price: {execution.price}")

def run_loop():
    app.run()

app = IBApi()
app.connect("127.0.0.1", 7496, 123)

api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

# Wait for the contract details to be received and order to be placed
app.contract_details_received.wait()
app.order_placed.wait()

# To ensure all messages are processed before disconnecting
time.sleep(2)

app.disconnect()
