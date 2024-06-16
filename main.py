from ccxt_download_OHLCV import get_ticker_data

df, filename = get_ticker_data("BTC/USDT")

print(df)