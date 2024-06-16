import ccxt
import datetime
import pandas as pd
import logging

def get_ticker_data(Ticker, Since="2017-01-01T00:00:00Z", To='2025-08-01T00:00:00Z', Timeframe='4h', Exchange=ccxt.binance()):
    logger = logging.getLogger('download_ccxt')
    logger.propagate = False
    # Initialize Binance API
    exchange = Exchange
    # exchange = ccxt.binance()

    # Define the market and timeframe
    market = Ticker
    # market = 'DOGE/USDT'
    timeframe = Timeframe  # 4 hour timeframe
    # timeframe = '4h'

    # Define the date range
    since = exchange.parse8601(Since)
    to = exchange.parse8601(To)
    # since = exchange.parse8601('2017-01-01T00:00:00Z')  # 01-01-2015
    # to = exchange.parse8601('2023-08-01T00:00:00Z')  # 01-06-2023

    # Empty list to hold data
    data = []

    # Fetch OHLCV data in batches
    while since < to:
        try:
            print(f'Fetching OHLCV data since {exchange.iso8601(since)}')
            ohlcv = exchange.fetch_ohlcv(market, timeframe, since)
            if len(ohlcv) == 0:
                break
            else:
                data.extend(ohlcv)
                since = ohlcv[-1][0] + 1  # Update 'since' to the timestamp of the last data point + 1 millisecond
        except Exception as e:
            print(f'Error occurred: {e}')
            break

    print(f'Fetched {len(data)} data points')

    # Process data
    df = pd.DataFrame(data, columns=['timestamp', 'Open', 'High', 'Low', 'Close', 'Vol'])

    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    filename = str(f"{market.replace('/', '')}_{str(datetime.datetime.strptime(Since, '%Y-%m-%dT%H:%M:%SZ').date()).replace('-', '')}_{str(datetime.datetime.strptime(To, '%Y-%m-%dT%H:%M:%SZ').date()).replace('-', '')}_{timeframe}")
    # df.to_csv("csv/" + filename +".csv", index=False)
    # df.to_csv("ohlc.csv")
    # Split timestamp into date and time columns
    # df['DATE'] = df['timestamp'].dt.strftime('%Y%m%d')
    # df['TIME'] = df['timestamp'].dt.strftime('%H%M%S')

    return df, filename