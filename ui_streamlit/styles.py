# ui_streamlit/styles.py
import streamlit as st

def apply_styles():
    st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0e17 0%, #0f141f 100%);
        color: #e2e8f0;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    /* Header Moderno */
    .main-header {
        background: linear-gradient(90deg, #1a1f2e 0%, #16213e 100%);
        backdrop-filter: blur(20px);
        padding: 16px 24px;
        border-radius: 20px;
        border: 1px solid rgba(240, 185, 11, 0.2);
        border-left: 5px solid #f0b90b;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 8px 32px rgba(240, 185, 11, 0.1);
        position: relative;
        overflow: hidden;
    }
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, #f0b90b, transparent);
    }
    
    /* Badge Ultra Moderni */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 8px 16px;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        backdrop-filter: blur(10px);
        border: 1px solid;
        box-shadow: 0 4px 14px rgba(0,0,0,0.3);
    }
    .source-td { background: linear-gradient(135deg, #1e40af, #3b82f6); border-color: #60a5fa; color: white; }
    .source-yf { background: linear-gradient(135deg, #7c3aed, #a855f7); border-color: #c084fc; color: white; }
    .source-err { background: linear-gradient(135deg, #4b5563, #6b7280); border-color: #9ca3af; color: #f3f4f6; }
    .market-open { background: linear-gradient(135deg, #059669, #10b981); border-color: #34d399; color: white; }
    .market-closed { background: linear-gradient(135deg, #dc2626, #ef4444); border-color: #f87171; color: white; }
    .market-unknown { background: linear-gradient(135deg, #d97706, #f59e0b); border-color: #fbbf24; color: white; }
    
    /* Cards Glassmorphism */
    .card {
        background: rgba(22, 27, 34, 0.8);
        backdrop-filter: blur(20px);
        padding: 24px;
        border-radius: 24px;
        border: 1px solid rgba(48, 54, 61, 0.5);
        margin-bottom: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3), 0 0 0 1px rgba(255,255,255,0.05);
        position: relative;
        transition: all 0.3s ease;
    }
    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 25px 50px rgba(0,0,0,0.4), 0 0 0 1px rgba(240, 185, 11, 0.2);
        border-color: rgba(240, 185, 11, 0.3);
    }
    
    /* Signal Header Neon */
    .signal-header {
        text-align: center;
        padding: 16px 24px;
        border-radius: 20px;
        font-weight: 800;
        font-size: 1.3rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 20px;
        border: 2px solid;
        background: linear-gradient(145deg, rgba(0,0,0,0.3), rgba(255,255,255,0.05));
        position: relative;
        overflow: hidden;
    }
    .signal-header::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s;
    }
    .signal-header:hover::before { left: 100%; }
    
    /* Prezzo Monumentale */
    .price-large {
        font-size: 3.5rem !important;
        font-weight: 900;
        background: linear-gradient(135deg, #ffffff, #f0f6fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1;
        text-shadow: 0 0 30px rgba(240, 185, 11, 0.5);
    }
    
    /* Metriche Eleganti */
    .metric-small {
        color: #9ca3af;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 4px;
    }
    .metric-val {
        font-size: 1.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #f0f6fc, #e2e8f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Radar Moderni */
    .radar-buy {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.15), rgba(16, 185, 129, 0.1));
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 255, 136, 0.4);
        padding: 16px 20px;
        border-radius: 20px;
        margin: 12px 0;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(0, 255, 136, 0.15);
    }
    .radar-buy:hover { transform: translateX(8px); box-shadow: 0 12px 35px rgba(0, 255, 136, 0.25); }
    
    .radar-sell {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(220, 38, 38, 0.1));
        backdrop-filter: blur(10px);
        border: 1px solid rgba(239, 68, 68, 0.4);
        padding: 16px 20px;
        border-radius: 20px;
        margin: 12px 0;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(239, 68, 68, 0.15);
    }
    .radar-sell:hover { transform: translateX(-8px); box-shadow: 0 12px 35px rgba(239, 68, 68, 0.25); }
    
    /* Validazione Gradient */
    .validation-ok { background: linear-gradient(135deg, rgba(0, 255, 136, 0.15), rgba(16, 185, 129, 0.1)); border: 1px solid rgba(0, 255, 136, 0.5); }
    .validation-warn { background: linear-gradient(135deg, rgba(251, 191, 36, 0.15), rgba(245, 158, 11, 0.1)); border: 1px solid rgba(251, 191, 36, 0.5); }
    .validation-error { background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(220, 38, 38, 0.1)); border: 1px solid rgba(239, 68, 68, 0.5); }
    
    /* Bottoni Neon */
    .stButton > button {
        background: linear-gradient(135deg, #1f2937, #374151);
        border: 1px solid rgba(240, 185, 11, 0.3);
        border-radius: 16px;
        padding: 12px 24px;
        font-weight: 700;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #f0b90b, #fbbf24);
        border-color: #f0b90b;
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(240, 185, 11, 0.4);
        color: #1f2937 !important;
    }
    
    /* Progress Bar Moderna */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #f0b90b, #fbbf24);
        border-radius: 10px;
    }
    
    /* Dataframe Moderno */
    .dataframe {
        background: rgba(22, 27, 34, 0.9) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(48, 54, 61, 0.5) !important;
    }
    .dataframe th {
        background: linear-gradient(135deg, #1f2937, #374151) !important;
        color: #f0f6fc !important;
        border: none !important;
    }
    
    /* Tabs Moderni */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(22, 27, 34, 0.6);
        padding: 8px;
        border-radius: 16px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(48, 54, 61, 0.5);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 8px 16px;
        background: rgba(31, 41, 55, 0.6);
        color: #94a3b8;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #f0b90b, #fbbf24);
        color: #1f2937 !important;
        font-weight: 700;
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .main-header {
            flex-direction: column;
            text-align: center;
            gap: 10px;
            padding: 12px;
        }
        
        .price-large {
            font-size: 2.2rem !important;
        }
        
        .metric-val {
            font-size: 1.2rem !important;
        }
        
        .signal-header {
            font-size: 1rem;
            padding: 12px;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            flex-wrap: wrap;
        }
        
        .stTabs [data-baseweb="tab"] {
            width: 100%;
            margin: 2px 0;
        }
        
        div[data-testid="column"] {
            min-width: 100% !important;
        }
        
        .card {
            padding: 16px;
        }
        
        .badge {
            padding: 4px 8px;
            font-size: 0.7rem;
        }
        
        .radar-buy, .radar-sell {
            padding: 12px;
        }
    }
    
    /* Tablet */
    @media (min-width: 769px) and (max-width: 1024px) {
        .price-large {
            font-size: 2.8rem !important;
        }
        
        .metric-val {
            font-size: 1.3rem !important;
        }
        
        .main-header {
            padding: 14px 20px;
        }
    }
    
    /* Animazioni */
    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }
    
    .loading-pulse {
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    /* Scrollbar personalizzata */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1f2e;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #f0b90b;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #fbbf24;
    }
    /* Radar neutral - per segnali laterali */
.radar-neutral {
    background: linear-gradient(135deg, rgba(148, 163, 184, 0.15), rgba(100, 116, 139, 0.1));
    backdrop-filter: blur(10px);
    border: 1px solid rgba(148, 163, 184, 0.4);
    padding: 16px 20px;
    border-radius: 20px;
    margin: 12px 0;
    transition: all 0.3s ease;
    box-shadow: 0 8px 25px rgba(148, 163, 184, 0.15);
}
.radar-neutral:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 35px rgba(148, 163, 184, 0.25);
}

/* Badge per forza segnale */
.signal-strength {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.7rem;
    font-weight: 600;
    margin-left: 8px;
}
.strength-alta { background: #00ff8820; color: #00ff88; border: 1px solid #00ff8840; }
.strength-media { background: #f0b90b20; color: #f0b90b; border: 1px solid #f0b90b40; }
.strength-debole { background: #94a3b820; color: #94a3b8; border: 1px solid #94a3b840; }
.strength-neutrale { background: #94a3b810; color: #94a3b8; border: 1px solid #94a3b820; }
/* Radar neutral - per segnali laterali */
.radar-neutral {
    background: linear-gradient(135deg, rgba(148, 163, 184, 0.15), rgba(100, 116, 139, 0.1));
    backdrop-filter: blur(10px);
    border: 1px solid rgba(148, 163, 184, 0.4);
    padding: 16px 20px;
    border-radius: 20px;
    margin: 12px 0;
    transition: all 0.3s ease;
    box-shadow: 0 8px 25px rgba(148, 163, 184, 0.15);
}
.radar-neutral:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 35px rgba(148, 163, 184, 0.25);
}

/* Badge per livello segnale */
.signal-level {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 0.7rem;
    font-weight: 600;
    margin-left: 8px;
}
.level-5 { background: #00ff8820; color: #00ff88; border: 1px solid #00ff8840; }
.level-4 { background: #f0b90b20; color: #f0b90b; border: 1px solid #f0b90b40; }
.level-3 { background: #3b82f620; color: #3b82f6; border: 1px solid #3b82f640; }
.level-2 { background: #8b5cf620; color: #8b5cf6; border: 1px solid #8b5cf640; }
.level-1 { background: #94a3b820; color: #94a3b8; border: 1px solid #94a3b840; }

/* Tooltip personalizzato */
.tooltip {
    position: relative;
    display: inline-block;
    cursor: help;
    border-bottom: 1px dotted #94a3b8;
}
.tooltip .tooltiptext {
    visibility: hidden;
    width: 200px;
    background: #1f2937;
    color: #fff;
    text-align: center;
    padding: 8px;
    border-radius: 8px;
    position: absolute;
    z-index: 1;
    bottom: 125%;
    left: 50%;
    margin-left: -100px;
    opacity: 0;
    transition: opacity 0.3s;
    border: 1px solid #f0b90b;
    font-size: 0.8rem;
}
.tooltip:hover .tooltiptext {
    visibility: visible;
    opacity: 1;
}
</style>
""", unsafe_allow_html=True)
