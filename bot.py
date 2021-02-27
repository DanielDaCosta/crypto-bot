from config import WEB_SCOCKET
import websocket, json
from pprint import pprint

last_closes_price = []  # Saves N-last close prices

def on_open(ws):
    print('Open')


def on_close(ws):
    print('Close')


def on_message(ws, message):
    global last_closes_price
    print('Received')
    json_message = json.loads(message)
    # pprint(json_message)

    candle= json_message['k']  # Candle info
    is_candle_closed = candle['x']  # Is this kline closed?
    close = candle['c']  # Close Price

    if is_candle_closed:
        last_closes_price.append(close)
        print(last_closes_price)


ws = websocket.WebSocketApp(
    WEB_SCOCKET, on_open=on_open,
    on_close=on_close,
    on_message=on_message)
ws.run_forever()
