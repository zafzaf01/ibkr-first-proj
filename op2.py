# Replace with your actual IB TWS API client class and methods
class IBClient:
  def reqSecDefOptParams(self, reqId, exchange, underlyingSymbol, tradingClass=None, multiplier=None, expirations=None, strikes=None):
    # Your client implementation to send the request to TWS API
    print(f"Sending request (reqId: {reqId}) - Underlying: {underlyingSymbol}, Exchange: {exchange}")
    # ... (communication logic with TWS API)

  # ... other client methods (e.g., for connecting/disconnecting)

# Define functions to handle data received from TWS (replace with your actual logic)
def securityDefinitionOptionParameter(reqId, exchange, underlyingConId, tradingClass, multiplier, expirations, strikes):
  # Process the received option chain data (partial)
  # This function would likely be called multiple times as data arrives in parts
  print(f"Received Option Chain Data (reqId: {reqId}):")
  print(f"  Exchange: {exchange}, Underlying ConId: {underlyingConId}")
  print(f"  Trading Class: {tradingClass}, Multiplier: {multiplier}")
  if expirations is not None:
      print(f"  Expirations: {expirations}")
  if strikes is not None:
      print(f"  Strikes: {strikes}")
  # ... further process the option details (e.g., contract ID, symbol, expiration date, strike price, etc.)

def securityDefinitionOptionParameterEnd(reqId):
  # Process any post-processing logic after receiving all data
  print(f"Received Option Chain Data (reqId: {reqId}) - All data received.")
  # ... perform actions after complete data retrieval (e.g., display results, store data)

# Example usage
client = IBClient()

# Request option chain data for AAPL on NASDAQ (all expirations and strikes)
client.reqSecDefOptParams(100, "NASDAQ", "AAPL", None, None, None, None)