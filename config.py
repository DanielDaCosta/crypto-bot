from dotenv import load_dotenv
from os import getenv
load_dotenv()

WEB_SCOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = 'ETHUSD'
TRADE_QUANTITY = 0.01
API_KEY= getenv('API_KEY')
API_SECRET= getenv('API_SECRET')
