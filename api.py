
import time, hmac, hashlib, requests, os
from mode import BASE_URL

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

def _headers():
    return {"X-MBX-APIKEY": API_KEY}

def _sign(params):
    query = "&".join([f"{k}={v}" for k,v in params.items()])
    sig = hmac.new(API_SECRET.encode(), query.encode(), hashlib.sha256).hexdigest()
    return query + "&signature=" + sig

def get_price(symbol):
    url = BASE_URL + "/fapi/v1/ticker/price"
    r = requests.get(url, params={"symbol": symbol}).json()
    return float(r["price"])

def get_last_candle(symbol, interval="1m"):
    url = BASE_URL + "/fapi/v1/klines"
    params = {"symbol": symbol, "interval": interval, "limit": 2}
    r = requests.get(url, params=params).json()
    c = r[-2]  # candle terakhir yang sudah close
    o = float(c[1])
    h = float(c[2])
    l = float(c[3])
    cl = float(c[4])
    return o, h, l, cl

def set_leverage(symbol, lev):
    url = BASE_URL + "/fapi/v1/leverage"
    p = {"symbol": symbol, "leverage": lev, "timestamp": int(time.time()*1000)}
    requests.post(url+"?"+_sign(p), headers=_headers())

def set_margin_type(symbol, mtype="ISOLATED"):
    url = BASE_URL + "/fapi/v1/marginType"
    p = {"symbol": symbol, "marginType": mtype, "timestamp": int(time.time()*1000)}
    requests.post(url+"?"+_sign(p), headers=_headers())

def market_order(symbol, side, qty):
    url = BASE_URL + "/fapi/v1/order"
    p = {
        "symbol": symbol,
        "side": side,
        "type": "MARKET",
        "quantity": qty,
        "timestamp": int(time.time()*1000)
    }
    return requests.post(url+"?"+_sign(p), headers=_headers()).json()

def close_position(symbol, side, qty):
    opp = "SELL" if side=="BUY" else "BUY"
    return market_order(symbol, opp, qty)

def place_stop_loss(symbol, side, entry_price, sl_pct):
    if side == "BUY":
        stop_price = entry_price * (1 + sl_pct)
        stop_side = "SELL"
    else:
        stop_price = entry_price * (1 - sl_pct)
        stop_side = "BUY"

    url = BASE_URL + "/fapi/v1/order"
    p = {
        "symbol": symbol,
        "side": stop_side,
        "type": "STOP_MARKET",
        "stopPrice": round(stop_price, 2),
        "closePosition": "true",
        "timestamp": int(time.time()*1000)
    }
    return requests.post(url+"?"+_sign(p), headers=_headers()).json()

def place_trailing_stop(symbol, side, callback_pct):
    close_side = "SELL" if side=="BUY" else "BUY"
    url = BASE_URL + "/fapi/v1/order"
    p = {
        "symbol": symbol,
        "side": close_side,
        "type": "TRAILING_STOP_MARKET",
        "callbackRate": int(callback_pct * 100),
        "closePosition": "true",
        "timestamp": int(time.time()*1000)
    }
    return requests.post(url+"?"+_sign(p), headers=_headers()).json()
