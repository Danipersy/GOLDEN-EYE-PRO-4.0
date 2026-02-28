# test_import.py
print("🔍 TEST IMPORTAZIONI")
print("="*50)

try:
    from ui_streamlit.pages import render_trading_view
    print(f"✅ render_trading_view importata correttamente")
except ImportError as e:
    print(f"❌ Errore: {e}")
    
    import ui_streamlit.pages
    print(f"\n📦 Contenuto di ui_streamlit.pages:")
    print(f"   __file__: {ui_streamlit.pages.__file__}")
    print(f"   Attributi: {[k for k in dir(ui_streamlit.pages) if not k.startswith('_')]}")