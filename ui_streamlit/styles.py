# ui_streamlit/styles.py
import streamlit as st

def apply_styles():
    """Applica tutti gli stili CSS all'app"""
    
    st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* ============================================
       VARIABILI GLOBALI
    ============================================ */
    :root {
        --gold: #f0b90b;
        --gold-light: #fbbf24;
        --green: #00ff88;
        --red: #ff3344;
        --blue: #3b82f6;
        --purple: #8b5cf6;
        --gray: #94a3b8;
        --bg-dark: #0A0A0F;
        --bg-card: #1A1A24;
        --border: #3C3C4A;
    }
    
    /* ============================================
       RESET E BASE
    ============================================ */
    .stApp {
        background: linear-gradient(135deg, #0a0e17 0%, #0f141f 100%);
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    .main {
        background: transparent;
        padding: 0 !important;
    }
    
    /* Nascondi sidebar */
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* ============================================
       HEADER FISSO CON GLASSMORPHISM
    ============================================ */
    .main-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: rgba(26, 31, 46, 0.95);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(240, 185, 11, 0.2);
        padding: 8px 32px;
        z-index: 999;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    
    /* ============================================
       MENU PRINCIPALE
    ============================================ */
    .top-menu {
        display: flex;
        gap: 8px;
        background: rgba(44, 44, 58, 0.5);
        padding: 4px;
        border-radius: 40px;
        border: 1px solid rgba(240, 185, 11, 0.2);
        backdrop-filter: blur(5px);
    }
    
    .menu-item {
        padding: 10px 24px;
        border-radius: 30px;
        color: #9E9EB0;
        font-size: 14px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        border: none;
        background: transparent;
    }
    
    .menu-item:hover {
        background: rgba(60, 60, 74, 0.8);
        color: white;
        transform: translateY(-2px);
    }
    
    .menu-item.active {
        background: linear-gradient(135deg, var(--gold), var(--gold-light));
        color: #0A0A0F;
        box-shadow: 0 4px 15px rgba(240, 185, 11, 0.3);
    }
    
    /* ============================================
       TOP BAR MERCATI (GLASSMORPHISM)
    ============================================ */
    .market-bar {
        background: rgba(26, 31, 46, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 16px 24px;
        margin-bottom: 24px;
        border: 1px solid rgba(240, 185, 11, 0.2);
        border-left: 6px solid var(--gold);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        animation: slideIn 0.5s ease;
    }
    
    .market-item {
        display: flex;
        flex-direction: column;
        gap: 4px;
    }
    
    .market-label {
        color: #94a3b8;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .market-value {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .market-status {
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    /* ============================================
       CARD METRICHE
    ============================================ */
    .metric-card {
        background: linear-gradient(135deg, #1e1e2e, #1a1a2a);
        border-radius: 16px;
        padding: 16px;
        border: 1px solid var(--border);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-align: center;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        border-color: var(--gold);
        box-shadow: 0 8px 24px rgba(240, 185, 11, 0.15);
    }
    
    .metric-label {
        color: #94a3b8;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        line-height: 1.2;
    }
    
    /* ============================================
       CARD RISULTATI SCAN
    ============================================ */
    .result-card {
        background: linear-gradient(135deg, #1e1e2e, #1a1a2a);
        border-left: 8px solid;
        border-radius: 24px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .result-card:hover {
        transform: translateY(-6px) scale(1.02);
    }
    
    .result-card.level-5 {
        border-left-color: var(--green);
        background: linear-gradient(135deg, #00ff8815, #00ff8805);
    }
    
    .result-card.level-4 {
        border-left-color: var(--gold);
        background: linear-gradient(135deg, #f0b90b15, #f0b90b05);
    }
    
    .result-card.level-3 {
        border-left-color: var(--blue);
        background: linear-gradient(135deg, #3b82f615, #3b82f605);
    }
    
    .result-card.level-2 {
        border-left-color: var(--purple);
        background: linear-gradient(135deg, #8b5cf615, #8b5cf605);
    }
    
    .result-card.level-1 {
        border-left-color: var(--gray);
        background: linear-gradient(135deg, #94a3b815, #94a3b805);
    }
    
    .level-badge {
        position: absolute;
        top: 0;
        right: 0;
        padding: 8px 24px;
        border-radius: 0 24px 0 24px;
        font-weight: 700;
        font-size: 0.9rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    
    .level-badge.level-5 {
        background: var(--green);
        color: #000;
    }
    
    .level-badge.level-4 {
        background: var(--gold);
        color: #000;
    }
    
    .level-badge.level-3 {
        background: var(--blue);
        color: #fff;
    }
    
    .level-badge.level-2 {
        background: var(--purple);
        color: #fff;
    }
    
    .level-badge.level-1 {
        background: var(--gray);
        color: #000;
    }
    
    /* ============================================
       BADGE E TAG
    ============================================ */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 30px;
        font-size: 12px;
        font-weight: 600;
        background: rgba(240, 185, 11, 0.1);
        border: 1px solid rgba(240, 185, 11, 0.3);
        color: var(--gold);
    }
    
    .badge-green {
        background: rgba(0, 255, 136, 0.1);
        border: 1px solid rgba(0, 255, 136, 0.3);
        color: var(--green);
    }
    
    .badge-red {
        background: rgba(255, 51, 68, 0.1);
        border: 1px solid rgba(255, 51, 68, 0.3);
        color: var(--red);
    }
    
    /* ============================================
       BOTTONI
    ============================================ */
    .stButton > button {
        background: linear-gradient(135deg, #1f2937, #374151);
        border: 1px solid rgba(240, 185, 11, 0.3);
        border-radius: 30px;
        padding: 12px 24px;
        font-weight: 700;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        color: white;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--gold), var(--gold-light));
        border-color: var(--gold);
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(240, 185, 11, 0.4);
        color: #1f2937 !important;
    }
    
    .stButton > button[data-baseweb="button"][kind="primary"] {
        background: linear-gradient(135deg, var(--gold), var(--gold-light));
        color: #1f2937;
        border: none;
    }
    
    /* ============================================
       PROGRESS BAR
    ============================================ */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--gold), var(--gold-light));
        border-radius: 10px;
    }
    
    /* ============================================
       DATAFRAME
    ============================================ */
    .dataframe {
        background: rgba(22, 27, 34, 0.9) !important;
        border-radius: 16px !important;
        border: 1px solid var(--border) !important;
    }
    
    .dataframe th {
        background: linear-gradient(135deg, #1f2937, #374151) !important;
        color: #f0f6fc !important;
        border: none !important;
    }
    
    /* ============================================
       TABS
    ============================================ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(22, 27, 34, 0.8);
        padding: 6px;
        border-radius: 40px;
        border: 1px solid rgba(240, 185, 11, 0.2);
        margin-bottom: 20px;
        backdrop-filter: blur(5px);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 30px;
        padding: 8px 20px;
        font-size: 0.9rem;
        font-weight: 600;
        background: rgba(31, 41, 55, 0.6);
        color: #94a3b8;
        transition: all 0.2s ease;
        margin: 0 2px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--gold), var(--gold-light));
        color: #1f2937 !important;
        font-weight: 700;
        border: none;
        box-shadow: 0 4px 12px rgba(240, 185, 11, 0.3);
    }
    
    /* ============================================
       FOOTER
    ============================================ */
    .app-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(26, 31, 46, 0.95);
        backdrop-filter: blur(10px);
        border-top: 1px solid rgba(240, 185, 11, 0.2);
        padding: 12px 32px;
        color: #9E9EB0;
        font-size: 12px;
        display: flex;
        justify-content: space-between;
        z-index: 999;
    }
    
    /* ============================================
       ANIMAZIONI
    ============================================ */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
        100% { transform: translateY(0px); }
    }
    
    @keyframes pulse {
        0% { border-color: rgba(240, 185, 11, 0.3); }
        50% { border-color: rgba(240, 185, 11, 0.8); }
        100% { border-color: rgba(240, 185, 11, 0.3); }
    }
    
    .float-animation {
        animation: float 3s ease-in-out infinite;
    }
    
    .pulse-animation {
        animation: pulse 2s infinite;
    }
    
    /* ============================================
       SCROLLBAR PERSONALIZZATA
    ============================================ */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1f2e;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--gold);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--gold-light);
    }
    
    /* ============================================
       RESPONSIVE
    ============================================ */
    @media (max-width: 768px) {
        .main-header {
            padding: 8px 16px;
            flex-direction: column;
            gap: 10px;
        }
        
        .top-menu {
            flex-wrap: wrap;
            justify-content: center;
            width: 100%;
        }
        
        .menu-item {
            padding: 8px 16px;
            font-size: 12px;
            flex: 1;
            text-align: center;
        }
        
        .main-content {
            margin-top: 120px;
            padding: 16px;
        }
        
        .market-bar {
            padding: 12px;
        }
        
        .market-value {
            flex-wrap: wrap;
        }
        
        .metric-value {
            font-size: 1.5rem;
        }
        
        .result-card {
            padding: 16px;
        }
        
        .level-badge {
            padding: 4px 16px;
            font-size: 0.8rem;
        }
    }
    
    @media (min-width: 769px) and (max-width: 1024px) {
        .main-content {
            padding: 16px 24px;
        }
        
        .menu-item {
            padding: 8px 18px;
        }
    }
    
    /* ============================================
       UTILITY CLASSES
    ============================================ */
    .text-gradient {
        background: linear-gradient(135deg, #fff, #f0f6fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .text-gold {
        color: var(--gold) !important;
    }
    
    .text-green {
        color: var(--green) !important;
    }
    
    .text-red {
        color: var(--red) !important;
    }
    
    .bg-glass {
        background: rgba(26, 31, 46, 0.8);
        backdrop-filter: blur(10px);
    }
    
    .border-gold {
        border: 1px solid var(--gold);
    }
    
    .shadow-gold {
        box-shadow: 0 4px 20px rgba(240, 185, 11, 0.2);
    }
</style>
    """, unsafe_allow_html=True)
