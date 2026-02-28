import streamlit as st

def apply_styles():
    st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: radial-gradient(circle at 10% 20%, #1a1f35, #0a0e1a);
    }
    
    /* Nascondi sidebar e header default */
    section[data-testid="stSidebar"], header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* Header fisso personalizzato */
    .custom-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: rgba(18, 23, 40, 0.95);
        backdrop-filter: blur(12px);
        border-bottom: 2px solid #f0b90b;
        padding: 0.5rem 2rem;
        z-index: 9999;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 8px 20px rgba(0,0,0,0.6);
    }
    
    .logo {
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #f0b90b, #fbbf24);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .menu-container {
        display: flex;
        gap: 0.5rem;
        background: rgba(44, 44, 58, 0.6);
        padding: 0.3rem;
        border-radius: 40px;
        border: 1px solid rgba(240, 185, 11, 0.3);
    }
    
    .menu-btn {
        padding: 0.5rem 1.5rem;
        border-radius: 30px;
        border: none;
        font-weight: 600;
        font-size: 0.9rem;
        background: transparent;
        color: #9ca3af;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .menu-btn:hover {
        background: rgba(60, 60, 74, 0.8);
        color: white;
    }
    
    .menu-btn.active {
        background: #f0b90b;
        color: #0a0a0f;
        box-shadow: 0 4px 12px rgba(240, 185, 11, 0.4);
    }
    
    .watchlist-badge {
        background: #2c2c3a;
        border: 1px solid #f0b90b;
        border-radius: 30px;
        padding: 0.3rem 1rem;
        color: #f0b90b;
        font-weight: 600;
    }
    
    /* Market bar */
    .market-bar {
        background: linear-gradient(135deg, #1e2338, #161b2f);
        border-radius: 20px;
        padding: 1.2rem 2rem;
        margin: 6rem 2rem 2rem 2rem;
        border-left: 6px solid #f0b90b;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        display: flex;
        flex-wrap: wrap;
        gap: 2rem;
        align-items: center;
        justify-content: space-between;
    }
    
    .market-item {
        display: flex;
        flex-direction: column;
    }
    
    .market-label {
        color: #94a3b8;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .market-value {
        font-size: 1.5rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Card personalizzata */
    .custom-card {
        background: linear-gradient(135deg, #1e2338, #161b2f);
        border-radius: 24px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 6px solid;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .custom-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }
    
    .badge {
        display: inline-block;
        padding: 0.2rem 1rem;
        border-radius: 30px;
        font-size: 0.8rem;
        font-weight: 700;
        margin-left: 1rem;
    }
    
    .badge-l5 { background: #00ff88; color: black; }
    .badge-l4 { background: #f0b90b; color: black; }
    .badge-l3 { background: #3b82f6; color: white; }
    .badge-l2 { background: #8b5cf6; color: white; }
    .badge-l1 { background: #94a3b8; color: black; }
    
    /* Footer */
    .custom-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(18, 23, 40, 0.95);
        backdrop-filter: blur(12px);
        border-top: 1px solid #f0b90b;
        padding: 0.8rem 2rem;
        color: #94a3b8;
        font-size: 0.8rem;
        display: flex;
        justify-content: space-between;
        z-index: 9999;
    }
    
    /* Spazio per il contenuto principale */
    .main-content {
        margin-top: 5rem;
        margin-bottom: 4rem;
        padding: 0 2rem;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .custom-header { flex-direction: column; height: auto; padding: 0.5rem; }
        .menu-container { flex-wrap: wrap; justify-content: center; }
        .market-bar { flex-direction: column; align-items: start; }
        .main-content { margin-top: 10rem; }
    }
</style>
    """, unsafe_allow_html=True)
