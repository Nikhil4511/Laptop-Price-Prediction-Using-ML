import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import sys
import plotly.express as px
import plotly.graph_objects as go

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.theme import apply_theme, theme_toggle

st.set_page_config(
    page_title="EDA — LaptopPrice Prediction",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

apply_theme(st.session_state.theme)
theme_toggle()

# ── Load data ──────────────────────────────────────────────────────────
@st.cache_data
def load_df():
    base = os.path.dirname(os.path.dirname(__file__))
    try:
        df = pickle.load(open(os.path.join(base, "df.pkl"), "rb"))
        return df
    except FileNotFoundError:
        # Demo data
        np.random.seed(0)
        n = 300
        brands  = ["Dell","Apple","Lenovo","HP","Asus","Acer","MSI"]
        types   = ["Notebook","Ultrabook","Gaming","2 in 1 Convertible","Workstation"]
        cpus    = ["Intel Core i5","Intel Core i7","AMD Ryzen 5","AMD Ryzen 7","Intel Core i3"]
        gpus    = ["Nvidia","AMD","Intel"]
        oss     = ["Windows","macOS","Linux","No OS"]
        rams    = [4,8,16,32]

        df = pd.DataFrame({
            "Company":   np.random.choice(brands, n),
            "TypeName":  np.random.choice(types,  n),
            "Cpu brand": np.random.choice(cpus,   n),
            "Gpu brand": np.random.choice(gpus,   n),
            "os":        np.random.choice(oss,    n),
            "Ram":       np.random.choice(rams,   n),
            "Price":     np.random.randint(25000, 200000, n),
        })
        return df

df = load_df()

# If the df has log-price, exponentiate
if "Price" not in df.columns and "price" in df.columns:
    df["Price"] = df["price"]
# Some datasets store log(Price)
if df["Price"].max() < 20:
    df["Price"] = np.exp(df["Price"]).astype(int)

PLOT_BG   = "rgba(0,0,0,0)"
GRID_COL  = "rgba(255,255,255,0.07)"
TEXT_COL  = "#b8b8d1"
ACCENT    = "#6366f1"
ACCENT2   = "#06b6d4"

def style_fig(fig, title=""):
    fig.update_layout(
        plot_bgcolor  = PLOT_BG,
        paper_bgcolor = PLOT_BG,
        font_color    = TEXT_COL,
        title_text    = title,
        title_font_size = 14,
        title_font_color = TEXT_COL,
        margin        = dict(l=10, r=10, t=40, b=10),
        legend        = dict(bgcolor="rgba(0,0,0,0)", font_color=TEXT_COL),
    )
    fig.update_xaxes(gridcolor=GRID_COL, zerolinecolor=GRID_COL, tickfont_color=TEXT_COL)
    fig.update_yaxes(gridcolor=GRID_COL, zerolinecolor=GRID_COL, tickfont_color=TEXT_COL)
    return fig


st.markdown("""
<h2 style="background:linear-gradient(90deg,#6366f1,#06b6d4);
           -webkit-background-clip:text;-webkit-text-fill-color:transparent;
           font-size:2rem;font-weight:800;margin-bottom:0.2rem">
    📊 EDA Dashboard
</h2>
<p style="color:#9090b0;margin-bottom:1.5rem">
    Explore how brand, specs, and type shape laptop prices across the training dataset.
</p>
""", unsafe_allow_html=True)

# ── KPIs ──────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("Laptops in Dataset", f"{len(df):,}")
k2.metric("Avg Price",          f"₹ {int(df['Price'].mean()):,}")
k3.metric("Median Price",       f"₹ {int(df['Price'].median()):,}")
k4.metric("Price Range",        f"₹ {int(df['Price'].min()):,} – ₹ {int(df['Price'].max()):,}")

st.markdown("<br>", unsafe_allow_html=True)

# ── Row 1: Brand box plots + RAM bar ──────────────────────────────────
r1c1, r1c2 = st.columns(2, gap="large")

with r1c1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Price Distribution by Brand</div>', unsafe_allow_html=True)
    order = df.groupby("Company")["Price"].median().sort_values(ascending=False).index.tolist()
    fig = px.box(
        df, x="Company", y="Price",
        category_orders={"Company": order},
        color_discrete_sequence=[ACCENT],
    )
    style_fig(fig)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with r1c2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Avg Price by RAM</div>', unsafe_allow_html=True)
    ram_df = df.groupby("Ram")["Price"].mean().reset_index()
    fig = px.bar(ram_df, x="Ram", y="Price",
                 color="Price",
                 color_continuous_scale=["#6366f1", "#06b6d4"],
                 labels={"Ram": "RAM (GB)", "Price": "Avg Price (₹)"})
    fig.update_coloraxes(showscale=False)
    style_fig(fig)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── Row 2: Type violin + GPU breakdown ────────────────────────────────
r2c1, r2c2 = st.columns(2, gap="large")

with r2c1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Price by Laptop Type</div>', unsafe_allow_html=True)
    fig = px.violin(
        df, x="TypeName", y="Price", box=True,
        color="TypeName",
        color_discrete_sequence=px.colors.sequential.Purpor,
    )
    style_fig(fig)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with r2c2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Avg Price by GPU Brand</div>', unsafe_allow_html=True)
    gpu_df = df.groupby("Gpu brand")["Price"].mean().reset_index()
    fig = px.bar(
        gpu_df, x="Gpu brand", y="Price",
        color="Gpu brand",
        color_discrete_sequence=[ACCENT, ACCENT2, "#f43f5e"],
    )
    style_fig(fig)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── Row 3: Price histogram + CPU breakdown ────────────────────────────
r3c1, r3c2 = st.columns(2, gap="large")

with r3c1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Overall Price Distribution</div>', unsafe_allow_html=True)
    fig = px.histogram(
        df, x="Price", nbins=40,
        color_discrete_sequence=[ACCENT],
        labels={"Price": "Price (₹)"},
    )
    style_fig(fig)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with r3c2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Avg Price by CPU Brand</div>', unsafe_allow_html=True)
    cpu_df = df.groupby("Cpu brand")["Price"].mean().reset_index().sort_values("Price", ascending=True)
    fig = px.bar(
        cpu_df, x="Price", y="Cpu brand",
        orientation="h",
        color="Price",
        color_continuous_scale=["#6366f1", "#06b6d4"],
    )
    fig.update_coloraxes(showscale=False)
    style_fig(fig)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── Interactive filter ────────────────────────────────────────────────
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<div class="section-header">🔍 Custom Exploration</div>', unsafe_allow_html=True)

fc1, fc2, fc3 = st.columns(3)
with fc1:
    sel_brand = st.multiselect("Filter by Brand", sorted(df["Company"].unique()), default=[])
with fc2:
    sel_type  = st.multiselect("Filter by Type",  df["TypeName"].unique(), default=[])
with fc3:
    price_range = st.slider(
        "Price Range (₹)", 
        int(df["Price"].min()), int(df["Price"].max()),
        (int(df["Price"].min()), int(df["Price"].max())),
        step=1000,
    )

filt = df.copy()
if sel_brand: filt = filt[filt["Company"].isin(sel_brand)]
if sel_type:  filt = filt[filt["TypeName"].isin(sel_type)]
filt = filt[(filt["Price"] >= price_range[0]) & (filt["Price"] <= price_range[1])]

st.markdown(f"**{len(filt):,} laptops** match your filters")
st.dataframe(filt[["Company","TypeName","Ram","Cpu brand","Gpu brand","os","Price"]].head(50), use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)
