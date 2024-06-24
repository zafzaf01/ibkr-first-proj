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

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextOrderId = orderId
        self.start()

    def start(self):
        # Create a contract
        contract = Contract()
        contract.symbol = 'ES'
        contract.secType = 'FUT'
        contract.exchange = 'CME'
        contract.currency = 'USD'
        contract.lastTradeDateOrContractMonth = '202412'

        # Create an order
        order = Order()
        order.action = "BUY"
        order.orderType ="LMT"
        order.totalQuantity = 1 * self.multiplier  # Use the multiplier here
        order.lmtPrice = 5300
        # Place the order
        self.placeOrder(self.nextOrderId, contract, order)
        print(f"Placed order to buy {order.totalQuantity} contracts at {order.lmtPrice}")
        self.nextOrderId += 1

    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        print(f"Order Status - Id: {orderId}, Status: {status}, Filled: {filled}, Remaining: {remaining}, AvgFillPrice: {avgFillPrice}")

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

# Wait for the order to be placed and processed
time.sleep(10)

app.disconnect()