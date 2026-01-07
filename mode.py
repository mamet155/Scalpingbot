
import os

MODE = os.getenv("BOT_MODE", "DEMO")

if MODE == "DEMO":
    BASE_URL = "https://testnet.binancefuture.com"
    MODE_NAME = "DEMO (TESTNET)"
else:
    BASE_URL = "https://fapi.binance.com"
    MODE_NAME = "REAL (LIVE)"
