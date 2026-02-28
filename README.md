# 🦅 Golden Eye Pro 2026

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/tuo-username/golden-eye-pro)

Scanner multi-asset professionale con sistema a **5 livelli di confidenza** e AI integrata.

## 🚀 Caratteristiche

- 📡 **Radar Multi-Asset** - Scan automatico con Yahoo Finance
- 🎯 **Sistema a 5 Livelli** - Da L1 (laterale) a L5 (segnale forte)
- 📊 **Backtest Avanzato** - Test strategia con classificazione STRONG/WEAK
- 🤖 **AI Suggeritore** - Analisi contestuale con pesi calibrati
- 💰 **Money Management** - Calcolo position size con risk management
- 📝 **Paper Trading** - Simula trading con capitale virtuale
- ⚙️ **Ottimizzazione** - Trova parametri ottimali per ogni asset

## 🏁 Installazione Locale

```bash
# Clona il repository
git clone https://github.com/tuo-username/golden-eye-pro.git
cd golden-eye-pro

# Crea ambiente virtuale
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Installa dipendenze
pip install -r requirements.txt

# Configura API keys
mkdir -p .streamlit
echo "TWELVEDATA_KEY = \"tua_chiave\"" > .streamlit/secrets.toml
echo "ALPHA_VANTAGE_KEY = \"tua_chiave\"" >> .streamlit/secrets.toml
echo "MARKETAUX_TOKEN = \"tuo_token\"" >> .streamlit/secrets.toml

# Avvia l'app
streamlit run App.py
