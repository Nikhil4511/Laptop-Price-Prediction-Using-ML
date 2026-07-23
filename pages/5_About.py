import streamlit as st
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.theme import apply_theme, theme_toggle

st.set_page_config(
    page_title="About — Laptop",
    page_icon="ℹ️",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

apply_theme(st.session_state.theme)
theme_toggle()

st.markdown("""
<h2 style="background:linear-gradient(90deg,#6366f1,#06b6d4);
           -webkit-background-clip:text;-webkit-text-fill-color:transparent;
           font-size:2rem;font-weight:800;margin-bottom:0.2rem">
    ℹ️ About Laptop Price Prediction
</h2>
<p style="color:#9090b0;margin-bottom:1.5rem">
    A student capstone project in explainable machine learning.
</p>
""", unsafe_allow_html=True)

c1, c2 = st.columns([2, 1], gap="large")

with c1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">🎯 Project Goal</div>', unsafe_allow_html=True)
    st.markdown("""
This Model predicts the market price of a laptop from its hardware specifications using an XGBoost regression model.

What makes this project different from the typical price-predictor template is **explainability** — every prediction is accompanied by a SHAP waterfall that tells you exactly which spec raised or lowered the price, and by how much in rupees.

**Features at a glance:**
- 🔮 Price prediction from 12 hardware specs
- 🧠 SHAP-based per-prediction explanation (plain English + ₹ impact bars)
- 🖼️ Representative brand image shown alongside the result
- 🕓 Session-level prediction history with CSV export
- 📊 EDA dashboard with interactive Plotly charts
- 📈 Model diagnostics (R², MAE, residual plots)
- 🌙 / ☀️ Dark / Light theme toggle
- 📱 Responsive layout (mobile + desktop)
    """)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">🛠️ Tech Stack</div>', unsafe_allow_html=True)
    st.markdown("""
| Layer | Technology |
|-------|------------|
| UI Framework | Streamlit ≥ 1.32 |
| ML Model | XGBoost via scikit-learn Pipeline |
| Explainability | SHAP (TreeExplainer) |
| Visualisation | Plotly Express / Plotly Graph Objects |
| Data | ~1,300 real laptop listings (2019 e-commerce scrape) |
| Hosting | Streamlit Community Cloud (free tier) |
    """)
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📂 Project Structure</div>', unsafe_allow_html=True)
    st.code("""
laptop_predictor/
├── Home.py              ← landing page
├── pipe.pkl             ← trained Pipeline
├── df.pkl               ← cleaned dataset
├── pages/
│   ├── 1_Predict.py     ← main predictor
│   ├── 2_History.py     ← session history
│   ├── 3_EDA_Dashboard.py
│   ├── 4_Model_Performance.py
│   └── 5_About.py
└── utils/
    ├── theme.py         ← CSS + toggle
    ├── brand_images.py  ← image URLs
    └── shap_explain.py  ← SHAP wrapper
    """, language="text")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">🚀 Run Locally</div>', unsafe_allow_html=True)
    st.code("""
# Install deps
pip install streamlit xgboost shap plotly scikit-learn

# Run
streamlit run Home.py
    """, language="bash")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📦 requirements.txt</div>', unsafe_allow_html=True)
    st.code("""
streamlit>=1.32.0
xgboost>=2.0.0
shap>=0.44.0
scikit-learn>=1.4.0
plotly>=5.20.0
pandas>=2.0.0
numpy>=1.26.0
    """, language="text")
    st.markdown("</div>", unsafe_allow_html=True)
