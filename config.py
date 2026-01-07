# ===== PAIR =====
SYMBOLS = ["BTCUSDT", "ETHUSDT"]

# ===== STOP LOSS (EXCHANGE) =====
STOP_LOSS_PCT = -0.20    # -20% dari harga entry

# ===== TRAILING (EXCHANGE) =====
TRAILING_EX_START_PCT = 0.05   # aktif saat profit >= 5%
TRAILING_CALLBACK_PCT = 0.20   # jarak trailing 20%

# ===== TRAILING LOGIC (BOT) =====
TRAIL_START_PCT = 0.10   # mulai logic trailing saat profit >= 10%
TRAIL_DROP_PCT  = 0.20   # auto close jika profit turun 20% dari peak

# ===== LOOP =====
CHECK_INTERVAL = 3

# ===== SIGNAL M1 =====
MIN_CANDLE_MOVE = 0.0005  # 0.05%
