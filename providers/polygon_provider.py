import requests
import pandas as pd
import streamlit as st
from providers.base_provider import BaseProvider, count_api_call

POLYGON_KEY = st.secrets.get("POLYGON_KEY", "")

class PolygonProvider(BaseProvider):
    def __init__(self):
        super().__init__("polygon", ttl=300)

    @count_api_call('polygon', 'aggregates')
    def fetch_aggregates(self, symbol: str, timespan: str = 'minute', multiplier: int = 15, from_date: str = None, to_date: str = None):
        # Implementazione chiamata API
        pass
