import os, sys, time, signal
from env_loader import load_keys

def input_number(prompt, min_val=0.0001, as_int=False):
    while True:
        try:
            v = float(input(prompt).strip())
            if v < min_val:
                print(f"Nilai harus >= {min_val}")
                continue
            return int(v) if as_int else v
        except:
            print("Masukkan angka yang benar.")

def pilih_mode():
    print("\n==============================")
    print(" PILIH MODE BOT")
    print("==============================")
    print("Ketik:")
    print("  demo  → latihan / TESTNET")
    print("  real  → trading ASLI")
    print("------------------------------")
    m = input("Pilihan kamu : ").strip().lower()
    if m not in ["demo", "real"]:
        print("❌ Pilihan salah. Ketik: demo atau real.")
        sys.exit(1)
    return m

MODE = pilih_mode()
os.environ["BOT_MODE"] = "DEMO" if MODE == "demo" else "REAL"

print("\n==============================")
print(" SETTING TRADING")
print("==============================")
LEVERAGE = input_number("Masukkan LEVERAGE (contoh: 10, 20, 50): ", 1, as_int=True)
MARGIN_PER_TRADE = input_number("Masukkan MARGIN per trade (USDT, contoh: 0.5, 1, 5): ", 0.01)
print(f"\nSetting dipakai:")
print(f"  Leverage : {LEVERAGE}x")
print(f"  Margin   : {MARGIN_PER_TRADE} USDT")
print("------------------------------\n")

try:
    load_keys("DEMO" if MODE == "demo" else "REAL")
except Exception as e:
    print("\n⚠️  API belum siap.")
    print(str(e))
    print("\nBuat file berikut lalu isi API:")
    print("  → .env.demo" if MODE=="demo" else "  → .env.real")
    print("\nFormat:")
    print("API_KEY=ISI_API_KEY")
    print("API_SECRET=ISI_API_SECRET")
    sys.exit(1)

from api import (
    get_price, get_last_candle,
    set_leverage, set_margin_type,
    market_order, close_position,
    place_stop_loss, place_trailing_stop
)
from config import (
    SYMBOLS, STOP_LOSS_PCT,
    TRAILING_EX_START_PCT, TRAILING_CALLBACK_PCT,
    TRAIL_START_PCT, TRAIL_DROP_PCT,
    CHECK_INTERVAL, MIN_CANDLE_MOVE
)
from mode import MODE_NAME

positions = {}

def log(msg):
    print(f"[BOT] {msg}")

def calc_qty(price):
    return round((MARGIN_PER_TRADE * LEVERAGE) / price, 3)

def handle_exit(sig=None, frame=None):
    log("⛔ Bot stop. Closing semua posisi…")
    for s, p in list(positions.items()):
        try:
            close_position(s, p["side"], p["qty"])
        except:
            pass
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

log(f"🔥 BOT START — {MODE_NAME}")

for s in SYMBOLS:
    try:
        set_margin_type(s, "ISOLATED")
        set_leverage(s, LEVERAGE)
        log(f"⚙️ Setup {s}: ISOLATED + {LEVERAGE}x")
    except:
        log(f"⚠️ Gagal setup {s}")

def get_signal(symbol):
    o, h, l, c = get_last_candle(symbol)
    move = (c - o) / o
    if move >= MIN_CANDLE_MOVE:
        return "BUY"
    if move <= -MIN_CANDLE_MOVE:
        return "SELL"
    return None

def open_trade(symbol, side):
    price = get_price(symbol)
    qty = calc_qty(price)
    market_order(symbol, side, qty)
    log(f"🚀 OPEN {symbol} {side} | QTY {qty}")
    place_stop_loss(symbol, side, price, STOP_LOSS_PCT)
    log(f"🛑 SL dipasang {symbol} ({int(abs(STOP_LOSS_PCT)*100)}%)")
    positions[symbol] = {
        "side": side,
        "entry": price,
        "qty": qty,
        "trailing_set": False,
        "peak_profit": 0.0,
        "logic_trail_on": False
    }

def check_trailing(symbol):
    p = positions[symbol]
    now = get_price(symbol)
    entry = p["entry"]
    side = p["side"]
    pnl_ratio = (now-entry)/entry if side=="BUY" else (entry-now)/entry
    if (not p["trailing_set"]) and pnl_ratio >= TRAILING_EX_START_PCT:
        place_trailing_stop(symbol, side, TRAILING_CALLBACK_PCT)
        p["trailing_set"] = True
        log(f"🔐 TRAILING EXCHANGE AKTIF {symbol} | Profit ≥ {int(TRAILING_EX_START_PCT*100)}%")

def check_logic_trailing(symbol):
    p = positions[symbol]
    now = get_price(symbol)
    entry = p["entry"]
    side = p["side"]

    profit_pct = (now-entry)/entry if side=="BUY" else (entry-now)/entry

    # aktifkan logic trailing saat profit >= 10%
    if (not p["logic_trail_on"]) and profit_pct >= TRAIL_START_PCT:
        p["logic_trail_on"] = True
        p["peak_profit"] = profit_pct
        log(f"🔄 LOGIC TRAILING ON {symbol} @ {profit_pct*100:.2f}%")

    # update peak & cek auto close
    if p["logic_trail_on"]:
        if profit_pct > p["peak_profit"]:
            p["peak_profit"] = profit_pct

        # auto close jika turun 20% dari peak
        if profit_pct <= p["peak_profit"] * (1 - TRAIL_DROP_PCT):
            log(
                f"🔐 AUTO CLOSE {symbol} | "
                f"Now:{profit_pct*100:.2f}% Peak:{p['peak_profit']*100:.2f}%"
            )
            close_position(symbol, side, p["qty"])
            positions.pop(symbol, None)

def main_loop():
    while True:
        for s in SYMBOLS:
            if s not in positions:
                sig = get_signal(s)
                if not sig:
                    log(f"⏸️ No signal {s}")
                    continue
                open_trade(s, sig)
            else:
                check_trailing(s)        # fitur lama (exchange trailing)
                check_logic_trailing(s) # fitur baru (logic trailing + auto close)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main_loop()
