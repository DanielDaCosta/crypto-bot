from config import WEB_SCOCKET, RSI_PERIOD,\
    RSI_OVERBOUGHT, RSI_OVERSOLD, \
    TRADE_SYMBOL, \
    TRADE_QUANTITY, \
    API_KEY, \
    API_SECRET
import websocket, json
import talib, numpy as np
from pprint import pprint
from binance.client import Client
from binance.enums import *

last_closes_price = []  # Saves N-last close prices
in_position = False
client = Client(API_KEY, API_SECRET, tld='br')


def order(side, quantity, symbol,
          order_type=ORDER_TYPE_MARKET):
    try:
        print("sending order")
        order = client.create_order(
            symbol=symbol, side=side, type=order_type,
            quantity=quantity)
        print(order)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True


def on_open(ws):
    print('Open')


def on_close(ws):
    print('Close')


def on_message(ws, message):
    global last_closes_price, in_position
    print('Received')
    json_message = json.loads(message)
    # pprint(json_message)

    candle= json_message['k']  # Candle info
    is_candle_closed = candle['x']  # Is this kline closed?
    close = candle['c']  # Close Price

    if is_candle_closed:
        last_closes_price.append(close)
        print(last_closes_price)

        if len(last_closes_price) > RSI_PERIOD:
            np_closes = np.array(last_closes_price)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            print(rsi)
            last_rsi = rsi[-1]
            if last_rsi > RSI_OVERBOUGHT:
                if in_position:
                    print("Overbought! Sell! Sell! Sell!")
                    # Binace SELL order
                    order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                    if order_succeeded:
                        in_position = False
                else:
                    print("It is overbought, but we don't "
                          "own any. Nothing to do.")
            if last_rsi < RSI_OVERSOLD:
                if in_position:
                    print("It is oversold, but you already own it, "
                          "nothing to do.")
                else:
                    print("Oversold! Buy! Buy! Buy!")
                    # Binance BUY order logic here
                    order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                    if order_succeeded:
                        in_position = True


ws = websocket.WebSocketApp(
    WEB_SCOCKET, on_open=on_open,
    on_close=on_close,
    on_message=on_message)
ws.run_forever()
