import streamlit as st
import pandas as pd
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.theme import apply_theme, theme_toggle

st.set_page_config(
    page_title="History — LaptopIQ",
    page_icon="🕓",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "theme"   not in st.session_state: st.session_state.theme   = "dark"
if "history" not in st.session_state: st.session_state.history = []

apply_theme(st.session_state.theme)
theme_toggle()

st.markdown("""
<h2 style="background:linear-gradient(90deg,#6366f1,#06b6d4);
           -webkit-background-clip:text;-webkit-text-fill-color:transparent;
           font-size:2rem;font-weight:800;margin-bottom:0.2rem">
    🕓 Prediction History
</h2>
<p style="color:#9090b0;margin-bottom:1.5rem">
    Every estimate you ran in this session — download as CSV to compare.
</p>
""", unsafe_allow_html=True)

history = st.session_state.history

if not history:
    st.info("No predictions yet. Head to **Predict** to generate your first estimate.")
    if st.button("🔮 Go to Predict"):
        st.switch_page("pages/1_Predict.py")
else:
    df = pd.DataFrame(history)

    # ── Summary stats ─────────────────────────────────────────────────
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📊 Session Summary</div>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Predictions", len(df))
    m2.metric("Avg Price",   f"₹ {int(df['Price ₹'].mean()):,}")
    m3.metric("Lowest",      f"₹ {int(df['Price ₹'].min()):,}")
    m4.metric("Highest",     f"₹ {int(df['Price ₹'].max()):,}")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── History list ──────────────────────────────────────────────────
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📋 All Predictions</div>', unsafe_allow_html=True)

    for i, row in enumerate(reversed(history)):
        price = row["Price ₹"]
        specs = f"{row['Brand']} · {row['Type']} · {row['RAM']} · {row['CPU']} · {row['SSD']} SSD"
        st.markdown(f"""
        <div class="history-row">
            <span style="color:#9090b0;font-size:0.78rem;width:22px">#{len(history)-i}</span>
            <span class="history-price">₹ {price:,}</span>
            <span class="history-spec">{specs}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Full table (collapsible) ───────────────────────────────────────
    with st.expander("📄 View full table"):
        st.dataframe(df, use_container_width=True)

    # ── Download button ───────────────────────────────────────────────
    csv = df.to_csv(index=False).encode("utf-8")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name="laptopiq_predictions.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with col2:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.history = []
            st.rerun()
