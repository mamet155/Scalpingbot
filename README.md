# scalpingbot

Bot scalping futures Binance versi M1.
Auto open posisi market dengan:
- Stop Loss otomatis di exchange
- Trailing profit di exchange (aman walau bot mati)
- Support isolated margin
- Bisa pilih DEMO / REAL di awal

⚠️ Gunakan dengan risiko sendiri.

---

## Fitur
- Market order otomatis
- Stop Loss exchange (-20% dari margin)
- Trailing profit exchange  
  - aktif mulai profit +10%  
  - trailing jarak 5%
- Isolated margin
- Pilih leverage & margin saat start
- Aman walau bot mati (SL & trailing di server Binance)
- Log langsung di Termux

---

## Cara Pakai (Termux dari nol)

### 1. Install bahan

pkg update pkg install python git -y pip install requests

### 2. Clone repo

gitclone https://github.com/mamet155/Scalpingbot.git
cd Scalpingbot cd Bot_scalping_future_binancem1

### 3. Setup API (pakai ENV)

export BINANCE_API_KEY="API_KEY_KAMU" export BINANCE_API_SECRET="API_SECRET_KAMU"

### 4. Jalankan bot

python main.py

Nanti bot akan tanya:
- Pilih DEMO / REAL
- Leverage
- Margin per posisi

---

## Catatan
- Jangan pakai dana besar dulu
- Test di DEMO dulu
- Futures = high risk


---
