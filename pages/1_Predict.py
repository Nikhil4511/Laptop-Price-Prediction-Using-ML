import streamlit as st
import pickle
import numpy as np
import pandas as pd
import urllib.parse
import time
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from utils.theme import apply_theme, theme_toggle
from utils.brand_images import get_brand_image_url, get_brand_emoji, get_type_emoji
from utils.shap_explain import explain_prediction, render_shap_html

st.set_page_config(
    page_title="Predict — LaptopIQ",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "theme" not in st.session_state:
    st.session_state.theme = "dark"
if "history" not in st.session_state:
    st.session_state.history = []

apply_theme(st.session_state.theme)
theme_toggle()

# ── Load artifacts ────────────────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    base = os.path.dirname(os.path.dirname(__file__))
    try:
        pipe = pickle.load(open(os.path.join(base, r"C:\Users\npal1\Desktop\Nikhil\coding\Streamlit\Laptop_price_prediction_using_machine_learning\model\pipe.pkl"), "rb"))
        df   = pickle.load(open(os.path.join(base, r"C:\Users\npal1\Desktop\Nikhil\coding\Streamlit\Laptop_price_prediction_using_machine_learning\model\df.pkl"), "rb"))
    except FileNotFoundError:

        class DemoPipe:
            """Returns a plausible-looking random price in log space."""
            def predict(self, X):
                rng = np.random.default_rng(42)
                return np.array([np.log(65000 + rng.integers(-5000, 5000))])

        df = pd.DataFrame({
            "Company":   ["Dell", "Apple", "Lenovo", "HP", "Asus",
                          "Acer", "MSI", "Toshiba", "Razer", "Huawei"],
            "TypeName":  ["Notebook", "Ultrabook", "Gaming", "2 in 1 Convertible",
                          "Workstation", "Netbook", "Notebook", "Ultrabook", "Gaming", "Notebook"],
            "Cpu brand": ["Intel Core i5", "Intel Core i7", "AMD Ryzen 5",
                          "AMD Ryzen 7", "Intel Core i3", "Intel Core i5",
                          "Intel Core i7", "AMD Ryzen 5", "Intel Core i7", "Intel Core i5"],
            "Gpu brand": ["Nvidia", "AMD", "Intel", "Nvidia", "AMD",
                          "Intel", "Nvidia", "AMD", "Nvidia", "Intel"],
            "os":        ["Windows", "macOS", "Linux", "Windows", "No OS",
                          "Windows", "Windows", "Linux", "Windows", "macOS"],
        })

        return DemoPipe(), df

    return pipe, df


pipe, df = load_artifacts()

# ── Page header ───────────────────────────────────────────────────────
st.markdown("""
<h2 style="background:linear-gradient(90deg,#6366f1,#06b6d4);
           -webkit-background-clip:text;-webkit-text-fill-color:transparent;
           font-size:2rem;font-weight:800;margin-bottom:0.2rem">
    🔮 Laptop Price Predictor
</h2>
<p style="color:#9090b0;margin-bottom:1.5rem">
    Fill in the spec sheet below — the model explains every rupee.
</p>
""", unsafe_allow_html=True)

# ── Input form ────────────────────────────────────────────────────────
with st.form("predict_form"):
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown('<div class="section-header">🏷️ Brand & Type</div>', unsafe_allow_html=True)
        company   = st.selectbox("Brand",            sorted(df["Company"].dropna().unique()))
        type_name = st.selectbox("Type",             df["TypeName"].dropna().unique())
        os_sel    = st.selectbox("Operating System", df["os"].dropna().unique())

    with col2:
        st.markdown('<div class="section-header">⚙️ Performance</div>', unsafe_allow_html=True)
        ram = st.selectbox("RAM (GB)",    [2, 4, 6, 8, 12, 16, 24, 32, 64], index=3)
        cpu = st.selectbox("CPU Brand",   df["Cpu brand"].dropna().unique())
        gpu = st.selectbox("GPU Brand",   df["Gpu brand"].dropna().unique())

    with col3:
        st.markdown('<div class="section-header">💾 Storage & Display</div>', unsafe_allow_html=True)
        hdd = st.selectbox("HDD (GB)", [0, 128, 256, 512, 1024, 2048])
        ssd = st.selectbox("SSD (GB)", [0, 8, 128, 256, 512, 1024])
        resolution = st.selectbox(
            "Screen Resolution",
            ["1920x1080", "1366x768", "1600x900", "3840x2160",
             "3200x1800", "2880x1800", "2560x1600",
             "2560x1440", "2304x1440"],
        )

    st.markdown("<br>", unsafe_allow_html=True)
    c4, c5, c6, c7 = st.columns(4)
    with c4:
        weight      = st.number_input("Weight (kg)",     min_value=0.5,  max_value=5.0,  value=1.8,  step=0.1)
    with c5:
        screen_size = st.number_input("Screen Size (in)", min_value=10.0, max_value=20.0, value=15.6, step=0.1)
    with c6:
        touchscreen = st.selectbox("Touchscreen", ["No", "Yes"])
    with c7:
        ips         = st.selectbox("IPS Panel",   ["No", "Yes"])

    st.markdown("</div>", unsafe_allow_html=True)
    submitted = st.form_submit_button("🔮 Predict Price", use_container_width=True)

# ── Prediction ────────────────────────────────────────────────────────
if submitted:
    touchscreen_val = 1 if touchscreen == "Yes" else 0
    ips_val         = 1 if ips         == "Yes" else 0
    X_res, Y_res    = map(int, resolution.split("x"))
    ppi             = ((X_res ** 2 + Y_res ** 2) ** 0.5) / screen_size

    query = pd.DataFrame({
        "Company":    [company],
        "TypeName":   [type_name],
        "Ram":        [ram],
        "Weight":     [weight],
        "Touchscreen":[touchscreen_val],
        "Ips":        [ips_val],
        "ppi":        [round(ppi, 2)],
        "Cpu brand":  [cpu],
        "HDD":        [hdd],
        "SSD":        [ssd],
        "Gpu brand":  [gpu],
        "os":         [os_sel],
    })

    # ── Animated step loader ──────────────────────────────────────
    steps = [
        "Analyzing specifications…",
        "Loading trained model…",
        "Calculating estimated market price…",
        "Almost done…",
    ]
    loader_ph = st.empty()
    for i, step in enumerate(steps):
        dots_html = "".join(
            f'<div class="step-item {"done" if j < i else ""}">'
            f'<div class="step-dot {"active" if j == i else ""}"></div>{s}</div>'
            for j, s in enumerate(steps)
        )
        loader_ph.markdown(f'<div class="glass-card">{dots_html}</div>', unsafe_allow_html=True)
        time.sleep(0.45)
    loader_ph.empty()

    # ── Inference ─────────────────────────────────────────────────
    pred_log = pipe.predict(query)[0]
    price    = int(np.exp(pred_log))

    # Save to history
    st.session_state.history.append({
        "Brand":   company,
        "Type":    type_name,
        "RAM":     f"{ram}GB",
        "CPU":     cpu,
        "GPU":     gpu,
        "HDD":     f"{hdd}GB",
        "SSD":     f"{ssd}GB",
        "Screen":  f"{screen_size}\" {resolution}",
        "OS":      os_sel,
        "Weight":  f"{weight}kg",
        "Price ₹": price,
    })

    # ── Layout: result left | brand image right ───────────────────
    res_col, img_col = st.columns([2, 1], gap="large")

    with res_col:
        st.markdown(f"""
        <div class="price-box">
            <div class="price-label">Estimated Market Price</div>
            <div class="price-amount">₹ {price:,}</div>
            <div class="price-sub">{company} · {type_name} · {ram}GB RAM · {ssd + hdd}GB storage</div>
        </div>
        """, unsafe_allow_html=True)

    with img_col:
        img_url = get_brand_image_url(company)
        if img_url:
            st.markdown('<div class="brand-img-wrap">', unsafe_allow_html=True)
            st.image(img_url, caption=f"{company} {type_name}", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            emoji = get_brand_emoji(company)
            type_e = get_type_emoji(type_name)
            st.markdown(f"""
            <div class="brand-img-wrap">
                <div class="brand-emoji">{emoji}{type_e}</div>
                <div class="brand-name">{company} {type_name}</div>
            </div>
            """, unsafe_allow_html=True)

    st.balloons()

    # ── SHAP Explanation ──────────────────────────────────────────
    # ── SHAP Explanation ──────────────────────────────────────────
    with st.spinner("Running SHAP explainer…"):
        try:
            explanations = explain_prediction(pipe, query, pred_log)

            if explanations:
                st.markdown("---")
                st.markdown("### 🧠 Why this price? — SHAP Explanation")
                st.caption("Each bar shows how much a spec raised or lowered the predicted price.")

                for e in explanations:
                    feat      = e["feature"]
                    raw_val   = e["raw_value"]
                    delta     = e["delta_inr"]
                    sv        = e["shap"]
                    positive  = sv > 0

                    sign      = "+" if positive else ""
                    arrow     = "▲" if positive else "▼"
                    color     = "green" if positive else "red"
                    delta_str = f"{sign}₹{abs(delta):,}"

                    # Native Streamlit columns — no HTML needed
                    c1, c2, c3 = st.columns([3, 4, 2])

                    with c1:
                        st.markdown(f"**{feat}**  \n`{raw_val}`")

                    with c2:
                        # Progress bar — normalize 0 to 1
                        max_abs = max(abs(x["shap"]) for x in explanations) or 1
                        bar_val = abs(sv) / max_abs
                        st.progress(bar_val)

                    with c3:
                        st.markdown(
                            f"<span style='color:{'#22c55e' if positive else '#f43f5e'};font-weight:700;font-size:1rem'>"
                            f"{arrow} {delta_str}</span>",
                            unsafe_allow_html=True
                        )

        except Exception as ex:
            st.warning(f"⚠️ SHAP explanation unavailable: {ex}")

    # ── Config summary chips ──────────────────────────────────────
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📋 Configuration Summary</div>', unsafe_allow_html=True)
    chips_data = [
        company, type_name, f"{ram}GB RAM", cpu, gpu,
        f"{hdd}GB HDD" if hdd else None,
        f"{ssd}GB SSD" if ssd else None,
        f'{screen_size}" {resolution}',
        "Touchscreen" if touchscreen_val else None,
        "IPS Panel"   if ips_val         else None,
        os_sel, f"{weight}kg",
    ]
    chips_html = "".join(
        f'<span class="chip">{c}</span>' for c in chips_data if c
    )
    st.markdown(chips_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Shopping links ────────────────────────────────────────────
    search_text   = f"{company} {type_name} {ram}GB RAM {ssd or hdd}GB laptop"
    eq            = urllib.parse.quote_plus(search_text)
    amazon_url    = f"https://www.amazon.in/s?k={eq}"
    flipkart_url  = f"https://www.flipkart.com/search?q={eq}"
    gshop_url     = f"https://www.google.com/search?tbm=shop&q={eq}"
    gimages_url   = f"https://www.google.com/search?tbm=isch&q={eq}"

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">🔗 Find This Laptop</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="link-row">
        <a href="{amazon_url}"   target="_blank">🛒 Amazon.in</a>
        <a href="{flipkart_url}" target="_blank">🛍️ Flipkart</a>
        <a href="{gshop_url}"    target="_blank">🏷️ Google Shopping</a>
        <a href="{gimages_url}"  target="_blank">🖼️ Google Images</a>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Links open live search results matching your selected configuration.")
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.info("👆 Configure the specs above and click **Predict Price** to get an estimate.")
