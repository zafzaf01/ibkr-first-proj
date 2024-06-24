def symbolSamples(self, reqId: int, contractDescriptions):
  print("Symbol Samples. Request Id: ", reqId)
  for contractDescription in contractDescriptions:
    derivSecTypes = ""
    for derivSecType in contractDescription.derivativeSecTypes:
      derivSecTypes += " "
      derivSecTypes += derivSecType
      print("Contract: conId:%s, symbol:%s, secType:%s primExchange:%s, "
        "currency:%s, derivativeSecTypes:%s, description:%s, issuerId:%s" % (
        contractDescription.contract.conId,
        contractDescription.contract.symbol,
        contractDescription.contract.secType,
        contractDescription.contract.primaryExchange,
        contractDescription.contract.currency, derivSecTypes,
        contractDescription.contract.description,
        contractDescription.contract.issuerId))