import streamlit as st

# ── Palette definitions ───────────────────────────────────────────────
DARK = {
    "bg":           "#0d0d1a",
    "surface":      "rgba(255,255,255,0.05)",
    "border":       "rgba(255,255,255,0.10)",
    "accent":       "#6366f1",       # indigo-500
    "accent2":      "#06b6d4",       # cyan-500
    "text":         "#e4e4f0",
    "muted":        "#9090b0",
    "card_shadow":  "0 4px 32px rgba(0,0,0,0.45)",
    "gradient":     "linear-gradient(135deg,#0d0d1a 0%,#16163a 60%,#0d0d1a 100%)",
    "chip_bg":      "rgba(99,102,241,0.15)",
    "chip_border":  "rgba(99,102,241,0.45)",
}

LIGHT = {
    "bg":           "#f5f5fb",
    "surface":      "rgba(255,255,255,0.85)",
    "border":       "rgba(0,0,0,0.08)",
    "accent":       "#4f46e5",
    "accent2":      "#0891b2",
    "text":         "#1a1a2e",
    "muted":        "#6b6b8a",
    "card_shadow":  "0 4px 24px rgba(79,70,229,0.10)",
    "gradient":     "linear-gradient(135deg,#eef2ff 0%,#f0f9ff 60%,#faf5ff 100%)",
    "chip_bg":      "rgba(79,70,229,0.10)",
    "chip_border":  "rgba(79,70,229,0.30)",
}


def apply_theme(mode: str = "dark"):
    t = DARK if mode == "dark" else LIGHT

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    /* ── Root ──────────────────────────────────────────────────── */
    html, body, .stApp {{
        background: {t['gradient']} !important;
        font-family: 'Inter', sans-serif;
        color: {t['text']};
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background: {t['surface']} !important;
        border-right: 1px solid {t['border']};
    }}
    section[data-testid="stSidebar"] * {{
        color: {t['text']} !important;
    }}

    /* ── Glass card ─────────────────────────────────────────────── */
    .glass-card {{
        background: {t['surface']};
        border: 1px solid {t['border']};
        border-radius: 16px;
        padding: 1.5rem 1.75rem;
        margin-bottom: 1.2rem;
        box-shadow: {t['card_shadow']};
        backdrop-filter: blur(12px);
    }}

    /* ── Section header ─────────────────────────────────────────── */
    .section-header {{
        color: {t['accent2']};
        font-size: 0.95rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 0.9rem;
        padding-bottom: 0.45rem;
        border-bottom: 1px solid {t['border']};
    }}

    /* ── Hero ───────────────────────────────────────────────────── */
    .hero-wrap {{
        text-align: center;
        padding: 3rem 1rem 2rem;
    }}
    .hero-eyebrow {{
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: {t['accent']};
        margin-bottom: 0.6rem;
    }}
    .hero-title {{
        font-size: clamp(2.8rem, 6vw, 4.5rem);
        font-weight: 800;
        background: linear-gradient(90deg, {t['accent']}, {t['accent2']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
        margin: 0 0 0.8rem;
    }}
    .hero-sub {{
        font-size: 1.1rem;
        color: {t['muted']};
        max-width: 580px;
        margin: 0 auto 1.5rem;
        line-height: 1.7;
    }}

    /* ── Feature cards ──────────────────────────────────────────── */
    .feat-card {{
        background: {t['surface']};
        border: 1px solid {t['border']};
        border-radius: 14px;
        padding: 1.4rem 1.2rem;
        text-align: center;
        height: 100%;
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }}
    .feat-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 28px rgba(99,102,241,0.18);
    }}
    .feat-icon {{ font-size: 2rem; margin-bottom: 0.5rem; }}
    .feat-title {{ font-weight: 700; font-size: 1rem; color: {t['text']}; margin-bottom: 0.3rem; }}
    .feat-desc {{ font-size: 0.82rem; color: {t['muted']}; line-height: 1.5; }}

    /* ── Price result ───────────────────────────────────────────── */
    .price-box {{
        text-align: center;
        background: linear-gradient(135deg, {t['chip_bg']}, rgba(6,182,212,0.10));
        border: 1px solid {t['chip_border']};
        border-radius: 18px;
        padding: 2rem;
        margin-top: 0.5rem;
    }}
    .price-label {{ color: {t['muted']}; font-size: 0.9rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; }}
    .price-amount {{
        font-size: clamp(2.5rem, 5vw, 3.5rem);
        font-weight: 800;
        background: linear-gradient(90deg, {t['accent']}, {t['accent2']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
        margin: 0.3rem 0;
    }}
    .price-sub {{ color: {t['muted']}; font-size: 0.87rem; }}

    /* ── Chips ──────────────────────────────────────────────────── */
    .chip {{
        display: inline-block;
        background: {t['chip_bg']};
        border: 1px solid {t['chip_border']};
        color: {t['text']};
        padding: 0.28rem 0.75rem;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 500;
        margin: 0.2rem;
    }}

    /* ── SHAP explanation ───────────────────────────────────────── */
    .shap-row {{
        display: flex;
        align-items: center;
        gap: 0.8rem;
        padding: 0.55rem 0;
        border-bottom: 1px solid {t['border']};
        font-size: 0.9rem;
    }}
    .shap-row:last-child {{ border-bottom: none; }}
    .shap-bar-pos {{
        height: 8px;
        border-radius: 4px;
        background: linear-gradient(90deg, #6366f1, #06b6d4);
        min-width: 4px;
    }}
    .shap-bar-neg {{
        height: 8px;
        border-radius: 4px;
        background: linear-gradient(90deg, #f43f5e, #fb923c);
        min-width: 4px;
    }}
    .shap-feat {{ flex: 1; color: {t['text']}; font-weight: 500; }}
    .shap-val-pos {{ color: #6366f1; font-weight: 700; font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; width: 70px; text-align: right; }}
    .shap-val-neg {{ color: #f43f5e; font-weight: 700; font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; width: 70px; text-align: right; }}
    .shap-arrow-pos {{ font-size: 1rem; }}
    .shap-arrow-neg {{ font-size: 1rem; }}

    /* ── Link row ───────────────────────────────────────────────── */
    .link-row a {{
        display: inline-block;
        text-decoration: none;
        color: {t['text']} !important;
        background: {t['surface']};
        border: 1px solid {t['border']};
        padding: 0.55rem 1.1rem;
        border-radius: 10px;
        margin: 0.3rem 0.4rem 0.3rem 0;
        font-weight: 600;
        font-size: 0.88rem;
        transition: all 0.15s ease;
    }}
    .link-row a:hover {{
        background: {t['chip_bg']};
        border-color: {t['accent']};
    }}

    /* ── History table ──────────────────────────────────────────── */
    .history-row {{
        display: flex;
        align-items: center;
        gap: 0.6rem;
        padding: 0.6rem 0;
        border-bottom: 1px solid {t['border']};
        font-size: 0.88rem;
    }}
    .history-row:last-child {{ border-bottom: none; }}
    .history-price {{
        font-weight: 700;
        color: {t['accent']};
        font-family: 'JetBrains Mono', monospace;
        width: 90px;
    }}
    .history-spec {{ flex: 1; color: {t['muted']}; }}

    /* ── Buttons ────────────────────────────────────────────────── */
    div.stButton > button {{
        background: linear-gradient(90deg, {t['accent']}, {t['accent2']});
        color: white !important;
        font-weight: 700;
        font-size: 1rem;
        padding: 0.65rem 0;
        border-radius: 12px;
        border: none;
        width: 100%;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }}
    div.stButton > button:hover {{
        transform: scale(1.015);
        box-shadow: 0 0 20px rgba(99,102,241,0.45);
    }}

    /* ── Inputs ─────────────────────────────────────────────────── */
    .stSelectbox label, .stNumberInput label, .stSlider label {{
        color: {t['muted']} !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }}

    /* ── Metrics ─────────────────────────────────────────────────── */
    [data-testid="metric-container"] {{
        background: {t['surface']};
        border: 1px solid {t['border']};
        border-radius: 12px;
        padding: 1rem;
    }}
    [data-testid="metric-container"] label {{
        color: {t['muted']} !important;
        font-size: 0.8rem !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }}
    [data-testid="metric-container"] [data-testid="stMetricValue"] {{
        color: {t['accent']} !important;
        font-weight: 800;
    }}

    /* ── Nav hint ─────────────────────────────────────────────── */
    .nav-hint {{ color: {t['muted']}; font-size: 0.9rem; margin-bottom: 0.6rem; }}

    /* ── Brand image placeholder ──────────────────────────────── */
    .brand-img-wrap {{
        text-align: center;
        padding: 1.2rem;
        background: {t['surface']};
        border: 1px solid {t['border']};
        border-radius: 14px;
    }}
    .brand-emoji {{ font-size: 4rem; }}
    .brand-name {{ color: {t['muted']}; font-size: 0.85rem; margin-top: 0.4rem; }}

    /* ── Step loader ──────────────────────────────────────────── */
    .step-item {{
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.5rem 0;
        color: {t['muted']};
        font-size: 0.9rem;
        transition: color 0.3s;
    }}
    .step-item.done {{ color: {t['accent2']}; }}
    .step-dot {{
        width: 10px; height: 10px;
        border-radius: 50%;
        background: {t['border']};
        flex-shrink: 0;
    }}
    .step-dot.active {{
        background: {t['accent2']};
        box-shadow: 0 0 8px {t['accent2']};
    }}

    /* Mobile responsive */
    @media (max-width: 640px) {{
        .hero-title {{ font-size: 2.2rem !important; }}
        .glass-card {{ padding: 1rem 1.1rem; }}
        .feat-card {{ margin-bottom: 0.8rem; }}
    }}
    </style>
    """, unsafe_allow_html=True)


def theme_toggle():
    """Renders a compact toggle in the sidebar."""
    with st.sidebar:
        st.markdown("---")
        current = st.session_state.get("theme", "dark")
        label = "☀️ Switch to Light" if current == "dark" else "🌙 Switch to Dark"
        if st.button(label, key="theme_btn", use_container_width=True):
            st.session_state.theme = "light" if current == "dark" else "dark"
            st.rerun()
