# providers/telegram_provider.py
import requests
import streamlit as st
from typing import Dict, Any, Optional
from datetime import datetime

@st.cache_data(ttl=60, show_spinner=False)
def send_telegram_alert(message: str, chat_id: Optional[str] = None) -> bool:
    """
    Invia un messaggio Telegram
    """
    bot_token = st.secrets.get("TELEGRAM_BOT_TOKEN", "")
    default_chat_id = st.secrets.get("TELEGRAM_CHAT_ID", "")
    
    chat_id = chat_id or default_chat_id
    
    if not bot_token or not chat_id:
        return False
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=5)
        return response.status_code == 200
    except Exception:
        return False


def format_signal_alert(signal_data: Dict[str, Any]) -> str:
    """
    Formatta un segnale per Telegram
    """
    asset = signal_data.get('asset', 'N/A')
    action = signal_data.get('signal', 'N/A')
    price = signal_data.get('price', 0)
    rsi = signal_data.get('rsi', 0)
    
    # Emoji per tipo segnale
    if "ACQUISTO" in action:
        emoji = "🟢"
    elif "VENDITA" in action:
        emoji = "🔴"
    else:
        emoji = "🟡"
    
    message = f"""
{emoji} <b>GOLDEN EYE PRO - SEGNALE</b> {emoji}

<b>Asset:</b> {asset}
<b>Segnale:</b> {action}
<b>Prezzo:</b> ${price:,.2f}
<b>RSI:</b> {rsi:.0f}
<b>Timestamp:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

🔗 <a href='https://golden-eye-pro-nrmz3e75ptgpbiqcknihpb.streamlit.app/'>Apri App</a>
    """
    return message


def send_radar_summary(radar_results: list) -> bool:
    """
    Invia riassunto radar via Telegram
    """
    if not radar_results:
        return False
    
    message = "📡 <b>RADAR SUMMARY</b>\n\n"
    
    for r in radar_results[:5]:  # Max 5 segnali
        emoji = "🟢" if "ACQUISTO" in r.get('signal', '') else "🔴"
        message += f"{emoji} {r['asset']}: {r['signal']} @ ${r['price']:,.2f} (RSI: {r['rsi']:.0f})\n"
    
    message += f"\n📊 Totale segnali: {len(radar_results)}"
    
    return send_telegram_alert(message)
