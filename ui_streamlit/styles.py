import streamlit as st

def apply_styles():
    st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    * { font-family: 'Inter', sans-serif; margin: 0; padding: 0; box-sizing: border-box; }

    .stApp {
        background: #0B0E14;
    }

    /* Nascondi elementi di default di Streamlit */
    section[data-testid="stSidebar"], header[data-testid="stHeader"] {
        display: none !important;
    }

    /* Header elegante (glassmorphism) */
    .trader-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(20, 24, 31, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 60px;
        padding: 0.6rem 2rem;
        margin: 1rem 2rem 1.5rem 2rem;
        border: 1px solid rgba(240, 185, 11, 0.25);
        box-shadow: 0 15px 30px -15px rgba(0,0,0,0.7);
    }

    .logo {
        font-size: 1.8rem;
        font-weight: 700;
        color: #E5E7EB;
        letter-spacing: 0.5px;
    }
    .logo span {
        color: #F0B90B;
        font-weight: 800;
    }

    .market-info {
        display: flex;
        gap: 2rem;
        color: #9CA3AF;
        font-size: 0.9rem;
        font-weight: 500;
    }

    .info-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .info-item .value {
        font-weight: 700;
        color: #F0B90B;
    }
    .info-item .value.green { color: #10B981; }
    .info-item .value.red { color: #EF4444; }

    /* Menu container - selettori basati su data-testid */
    .menu-container div[data-testid="column"] button[data-testid="stBaseButton-secondary"] {
        background: rgba(30, 36, 44, 0.6) !important;
        backdrop-filter: blur(4px) !important;
        border: 1px solid rgba(240, 185, 11, 0.3) !important;
        border-radius: 40px !important;
        color: #E5E7EB !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 0.7rem 0 !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        width: 100%;
    }

    .menu-container div[data-testid="column"] button[data-testid="stBaseButton-secondary"]:hover {
        background: rgba(45, 55, 68, 0.8) !important;
        border-color: #F0B90B !important;
        color: white !important;
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 12px 24px -8px rgba(240, 185, 11, 0.4) !important;
    }

    .menu-container div[data-testid="column"] button[data-testid="stBaseButton-primary"] {
        background: linear-gradient(145deg, #F0B90B, #D4A009) !important;
        border: none !important;
        color: #0B0E14 !important;
        font-weight: 700 !important;
        box-shadow: 0 6px 14px rgba(240, 185, 11, 0.3) !important;
        border-radius: 40px !important;
        padding: 0.7rem 0 !important;
        font-size: 0.95rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        width: 100%;
    }

    .menu-container div[data-testid="column"] button[data-testid="stBaseButton-primary"]:hover {
        background: linear-gradient(145deg, #FBBF24, #F0B90B) !important;
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 15px 30px -8px #F0B90B !important;
    }

    /* Divider personalizzato */
    hr {
        border-color: rgba(240, 185, 11, 0.2) !important;
        margin: 1.5rem 2rem !important;
    }

    /* Footer */
    .trader-footer {
        background: rgba(20, 24, 31, 0.8);
        backdrop-filter: blur(8px);
        border-radius: 40px;
        padding: 0.6rem 2rem;
        margin: 2rem 2rem 1rem 2rem;
        border: 1px solid rgba(240, 185, 11, 0.25);
        color: #9CA3AF;
        font-size: 0.85rem;
        display: flex;
        justify-content: space-between;
    }

    /* Metriche personalizzate */
    div[data-testid="stMetric"] {
        background: #14181F;
        border-radius: 24px;
        padding: 1rem;
        border: 1px solid #2A2F38;
        transition: all 0.2s;
    }
    div[data-testid="stMetric"]:hover {
        border-color: #F0B90B;
        box-shadow: 0 0 0 1px #F0B90B20;
    }
    div[data-testid="stMetric"] label {
        color: #9CA3AF !important;
        font-weight: 500 !important;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #F0B90B !important;
        font-weight: 700 !important;
    }

    /* Dataframe */
    .dataframe {
        background: #14181F !important;
        border-radius: 16px !important;
        border: 1px solid #2A2F38 !important;
    }
    .dataframe th {
        background: #1E242C !important;
        color: #F0B90B !important;
        font-weight: 600 !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: #14181F;
        padding: 0.5rem;
        border-radius: 40px;
        border: 1px solid #2A2F38;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 30px;
        padding: 0.5rem 1.5rem;
        color: #9CA3AF;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background: #F0B90B !important;
        color: #0B0E14 !important;
    }

    /* Badge personalizzati per le card */
    .badge-l5 { background: #10B981; color: black; padding: 0.2rem 0.8rem; border-radius: 30px; font-size: 0.8rem; font-weight: 700; display: inline-block; }
    .badge-l4 { background: #F0B90B; color: black; padding: 0.2rem 0.8rem; border-radius: 30px; font-size: 0.8rem; font-weight: 700; display: inline-block; }
    .badge-l3 { background: #3B82F6; color: white; padding: 0.2rem 0.8rem; border-radius: 30px; font-size: 0.8rem; font-weight: 700; display: inline-block; }
    .badge-l2 { background: #8B5CF6; color: white; padding: 0.2rem 0.8rem; border-radius: 30px; font-size: 0.8rem; font-weight: 700; display: inline-block; }
    .badge-l1 { background: #6B7280; color: white; padding: 0.2rem 0.8rem; border-radius: 30px; font-size: 0.8rem; font-weight: 700; display: inline-block; }
</style>
    """, unsafe_allow_html=True)
