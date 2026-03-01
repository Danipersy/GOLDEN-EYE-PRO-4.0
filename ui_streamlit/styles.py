import streamlit as st

def apply_styles():
    st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    * { font-family: 'Inter', sans-serif; margin: 0; padding: 0; box-sizing: border-box; }

    .stApp {
        background: #0B0E14;
    }

    /* Nascondi SOLO l'header di default di Streamlit */
    header[data-testid="stHeader"] {
        display: none !important;
    }

    /* Sidebar personalizzata - la creiamo noi con HTML */
    .custom-sidebar {
        position: fixed;
        top: 0;
        left: 0;
        width: 260px;
        height: 100vh;
        background: #14181F;
        border-right: 1px solid #2A2F38;
        padding: 2rem 1rem;
        z-index: 9999;
        overflow-y: auto;
        box-shadow: 4px 0 15px rgba(0,0,0,0.5);
    }

    .custom-sidebar .section-title {
        color: #F0B90B;
        font-size: 1.1rem;
        font-weight: 700;
        margin: 1.5rem 0 0.8rem 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .custom-sidebar .sidebar-btn {
        width: 100%;
        background: #1E242C;
        border: 1px solid #2A2F38;
        border-radius: 40px;
        padding: 0.7rem 1rem;
        margin-bottom: 0.5rem;
        color: #E5E7EB;
        font-weight: 600;
        font-size: 0.95rem;
        text-align: left;
        cursor: pointer;
        transition: all 0.2s ease;
        border: none;
    }

    .custom-sidebar .sidebar-btn:hover {
        background: #2A2F38;
        border-color: #F0B90B;
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(240, 185, 11, 0.3);
    }

    .custom-sidebar .sidebar-btn.active {
        background: linear-gradient(145deg, #F0B90B, #D4A009);
        color: #0B0E14;
        font-weight: 700;
        border: none;
    }

    .custom-sidebar .separator {
        border-top: 1px solid #2A2F38;
        margin: 1.5rem 0;
    }

    .custom-sidebar .footer-info {
        color: #9CA3AF;
        font-size: 0.8rem;
        margin-top: 2rem;
        text-align: center;
    }

    /* Contenuto principale - con margine per la sidebar */
    .main-content {
        margin-left: 260px;
        padding: 0 2rem;
    }

    /* Bottoni globali */
    .stButton button {
        border-radius: 40px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        border: 1px solid #2A2F38 !important;
        background: #14181F !important;
        color: #E5E7EB !important;
        box-shadow: none !important;
        font-size: 0.9rem;
    }

    .stButton button:hover {
        border-color: #F0B90B !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(240, 185, 11, 0.3) !important;
    }

    .stButton button[kind="primary"] {
        background: linear-gradient(145deg, #F0B90B, #D4A009) !important;
        border: none !important;
        color: #0B0E14 !important;
        font-weight: 700 !important;
    }

    .stButton button[kind="primary"]:hover {
        background: linear-gradient(145deg, #FBBF24, #F0B90B) !important;
        box-shadow: 0 6px 14px rgba(240, 185, 11, 0.4) !important;
    }

    /* Header */
    .trader-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(20, 24, 31, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 60px;
        padding: 0.6rem 2rem;
        margin: 1rem 0 1.5rem 0;
        border: 1px solid rgba(240, 185, 11, 0.25);
        box-shadow: 0 15px 30px -15px rgba(0,0,0,0.7);
        flex-wrap: wrap;
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
        flex-wrap: wrap;
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

    /* Metriche */
    div[data-testid="stMetric"] {
        background: #14181F;
        border-radius: 16px;
        padding: 1rem;
        border: 1px solid #2A2F38;
        transition: all 0.2s;
    }
    div[data-testid="stMetric"]:hover {
        border-color: #F0B90B;
    }
    div[data-testid="stMetric"] label {
        color: #9CA3AF !important;
        font-weight: 500 !important;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #F0B90B !important;
        font-weight: 700 !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: #14181F;
        padding: 0.5rem;
        border-radius: 40px;
        border: 1px solid #2A2F38;
        flex-wrap: wrap;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 30px;
        padding: 0.5rem 1.5rem;
        color: #9CA3AF;
        font-weight: 600;
        font-size: 0.9rem;
    }
    .stTabs [aria-selected="true"] {
        background: #F0B90B !important;
        color: #0B0E14 !important;
    }

    /* Divider */
    hr {
        border-color: rgba(240, 185, 11, 0.2) !important;
        margin: 1.5rem 0 !important;
    }

    /* Footer */
    .trader-footer {
        background: rgba(20, 24, 31, 0.8);
        backdrop-filter: blur(8px);
        border-radius: 40px;
        padding: 0.6rem 2rem;
        margin: 2rem 0 1rem 0;
        border: 1px solid rgba(240, 185, 11, 0.25);
        color: #9CA3AF;
        font-size: 0.85rem;
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 0.5rem;
    }

    /* Badge per le card */
    .badge-l5 { background: #10B981; color: black; padding: 0.2rem 0.8rem; border-radius: 30px; font-size: 0.8rem; font-weight: 700; display: inline-block; }
    .badge-l4 { background: #F0B90B; color: black; padding: 0.2rem 0.8rem; border-radius: 30px; font-size: 0.8rem; font-weight: 700; display: inline-block; }
    .badge-l3 { background: #3B82F6; color: white; padding: 0.2rem 0.8rem; border-radius: 30px; font-size: 0.8rem; font-weight: 700; display: inline-block; }
    .badge-l2 { background: #8B5CF6; color: white; padding: 0.2rem 0.8rem; border-radius: 30px; font-size: 0.8rem; font-weight: 700; display: inline-block; }
    .badge-l1 { background: #6B7280; color: white; padding: 0.2rem 0.8rem; border-radius: 30px; font-size: 0.8rem; font-weight: 700; display: inline-block; }

    /* Responsive per mobile */
    @media (max-width: 768px) {
        .custom-sidebar {
            width: 100%;
            height: auto;
            position: relative;
            margin-bottom: 1rem;
        }
        .main-content {
            margin-left: 0;
        }
        .trader-header {
            flex-direction: column;
            align-items: flex-start;
            gap: 0.5rem;
            padding: 0.6rem 1rem;
        }
        .market-info {
            gap: 1rem;
        }
        .stButton button {
            font-size: 0.8rem;
            padding: 0.4rem 0.6rem !important;
        }
        div[data-testid="stMetric"] {
            padding: 0.5rem;
        }
        .trader-footer {
            flex-direction: column;
            align-items: center;
            text-align: center;
        }
    }
</style>
    """, unsafe_allow_html=True)