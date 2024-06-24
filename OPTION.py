def securityDefinitionOptionParameter(self, reqId: int, exchange: str, underlyingConId: int, tradingClass: str,
                                      multiplier: str, expirations, strikes):
    print("SecurityDefinitionOptionParameter.", "ReqId:", reqId, "Exchange:", exchange, "Underlying conId:",
          underlyingConId, "TradingClass:", tradingClass, "Multiplier:", multiplier, "Expirations:", expirations,
          "Strikes:", strikes)


securityDefinitionOptionParameter(100, "AAPL","NASDAQ",None, None, None,None,None)
