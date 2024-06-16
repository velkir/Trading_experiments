import ccxt

exchange = ccxt.binance()

exchange.options = {'defaultType': 'future',
                    'adjustForTimeDifference': True}

symbol = 'BTC/USDT'
funding = exchange.fetch_funding_rate_history(symbol)
# print(type(funding))
print(funding)