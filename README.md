---

🧠 Scalpingbot — Binance Futures M1

Bot scalping otomatis untuk Binance Futures dengan sistem aman karena:
Stop Loss & Trailing dipasang langsung di exchange (bukan cuma di bot).

⚠️ Gunakan dengan risiko sendiri.


---

🚀 Fitur Utama

✅ Market order otomatis

✅ Stop Loss di exchange

default: -20% dari margin


✅ Trailing Profit di exchange

aktif saat profit +10%

jarak trailing 5%


✅ Isolated margin

✅ Pilih DEMO / REAL saat start

✅ Pilih leverage & margin saat start

✅ Aman walau bot mati (SL & trailing tetap jalan)

✅ Log langsung di Termux



---

📦 Struktur File

Scalpingbot/
│
├── main.py        # core bot
├── api.py         # koneksi ke Binance
├── config.py      # pair & setting default
├── env_loader.py  # loader .env
├── mode.py        # demo / real switch
├── .gitignore
└── README.md


---

🛠 Cara Pakai (Termux dari nol)

1️⃣ Install bahan

pkg update
pkg install python git -y
pip install requests python-dotenv


---

2️⃣ Clone repo

git clone https://github.com/mamet155/Scalpingbot.git
cd Scalpingbot


---

3️⃣ Setup API (aman pakai ENV)

Untuk DEMO

nano .env.demo

Isi:

API_KEY=ISI_API_KEY_TESTNET
API_SECRET=ISI_API_SECRET_TESTNET

Untuk REAL

nano .env.real

Isi:

API_KEY=ISI_API_KEY_REAL
API_SECRET=ISI_API_SECRET_REAL


---

4️⃣ Jalankan bot

python main.py


---

🎮 Alur Saat Bot Start

1. Pilih mode:

demo  → TESTNET
real  → AKUN ASLI


2. Masukkan:

Leverage (contoh: 10, 20, 50, 100)

Margin per trade (USDT)



3. Bot akan:

set isolated

set leverage

buka posisi market

pasang SL & trailing di exchange





---

🔐 Keamanan

API tidak disimpan di kode

Pakai file .env

.env sudah di-ignore oleh git

Aman share repo tanpa bocor API



---

🧪 Mode DEMO dulu!

Wajib test di TESTNET sebelum pakai uang asli.


---

🧾 Catatan Penting

Bot ini scalping agresif

Cocok untuk:

akun kecil

eksperimen

latihan automation


Bukan holy grail, tetap perlu:

manajemen risiko

mental kuat

siap loss




---
