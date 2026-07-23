import streamlit as st
from utils.theme import apply_theme, theme_toggle

st.set_page_config(
    page_title="Laptop Price Predictor",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Init session state defaults
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
if "history" not in st.session_state:
    st.session_state.history = []

apply_theme(st.session_state.theme)
theme_toggle()

# ── Hero ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-eyebrow">AI-Powered · Explainable · Free</div>
    <h1 class="hero-title">Laptop Price Prediction Using-ML</h1>
    <p class="hero-sub">
        Configure any laptop spec and get an instant price estimate — with a plain-English
        explanation of <em>why</em> the model made that call.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Feature tiles ─────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

tiles = [
    ("🔮", "Predict", "XGBoost model trained on 1,300+ real listings"),
    ("🧠", "Explain", "SHAP waterfall shows which spec drove the price"),
    ("📊", "EDA", "Explore how brand, RAM, and GPU affect price"),
    ("📈", "Performance", "See model accuracy metrics and residual plots"),
]

for col, (icon, title, desc) in zip([col1, col2, col3, col4], tiles):
    col.markdown(f"""
    <div class="feat-card">
        <div class="feat-icon">{icon}</div>
        <div class="feat-title">{title}</div>
        <div class="feat-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Quick nav ─────────────────────────────────────────────────────────
st.markdown('<p class="nav-hint">👈 Use the sidebar to navigate, or jump straight to:</p>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    if st.button("🔮 Start Predicting", use_container_width=True):
        st.switch_page("pages/1_Predict.py")
with c2:
    if st.button("📊 Explore the Data", use_container_width=True):
        st.switch_page("pages/3_EDA_Dashboard.py")
