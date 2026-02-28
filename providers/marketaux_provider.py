# providers/marketaux_provider.py
import requests
import streamlit as st
from typing import Dict, Any, List
from datetime import datetime, timedelta
from utils.error_handler import error_handler
from providers.base_provider import count_api_call

@st.cache_data(ttl=3600, show_spinner=False)
@count_api_call('marketaux', 'news')
def fetch_marketaux_sentiment(symbols: List[str]) -> Dict[str, Any]:
    """Marketaux con caching Streamlit (parametri semplici)"""
    api_key = st.secrets.get("MARKETAUX_TOKEN", "")
    if not api_key:
        return {}
    
    symbols_str = ",".join(symbols[:3])
    
    url = "https://api.marketaux.com/v1/news/all"
    params = {
        "symbols": symbols_str,
        "filter_entities": "true",
        "language": "en",
        "api_token": api_key,
        "limit": 5,
        "published_after": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
        "sort": "published_desc"
    }
    
    try:
        response = requests.get(url, params=params, timeout=5)
        if response.status_code != 200:
            return {}
        
        data = response.json()
        articles = data.get('data', [])
        
        sentiments = []
        for article in articles[:5]:
            sentiment = article.get('sentiment_score', 0.5)
            sentiments.append(sentiment)
        
        avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0.5
        
        if avg_sentiment > 0.6:
            color = "🟢"
            label = "POSITIVO"
        elif avg_sentiment < 0.4:
            color = "🔴"
            label = "NEGATIVO"
        else:
            color = "🟡"
            label = "NEUTRO"
        
        result = {
            "count": len(articles),
            "sentiment": round(avg_sentiment, 2),
            "label": f"{color} {label}",
            "color": color
        }
        
        st.session_state.marketaux_data = result
        return result
        
    except Exception as e:
        error_handler.logger.error(f"Marketaux error: {e}")
        return {}