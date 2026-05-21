import random
import time
import streamlit as st

# -----------------------------------------
# PAGE CONFIG
# -----------------------------------------
st.set_page_config(page_title="QuidAway by Bipzilla", page_icon="🌍", layout="wide")

# -----------------------------------------
# STYLE
# -----------------------------------------
st.markdown("""
<style>

/* FONT */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* NAVBAR */
.navbar {
    display:flex;
    justify-content:space-between;
    padding:12px 30px;
    border-bottom:1px solid #e2e8f0;
}
.nav-logo {
    font-weight:900;
    font-size:1.3rem;
}

/* HERO */
.hero {
    padding:60px;
    border-radius:24px;
    background:linear-gradient(120deg,#0f172a,#1e293b);
    color:white;
    margin-top:15px;
    margin-bottom:30px;
}
.hero h1 {
    font-size:3.5rem;
    font-weight:900;
}
.hero p {
    color:#cbd5e1;
    font-size:1.2rem;
}

/* BUTTON */
.stButton button {
    background:#ffb703 !important;
    color:black !important;
    font-weight:800 !important;
    border-radius:999px !important;
}

/* SPINNER */
.spinner {
    font-size:5rem;
    animation: spin 0.6s linear infinite;
    display:inline-block;
}

@keyframes spin {
    from { transform: rotate(0deg);}
    to { transform: rotate(360deg);}
}

/* LOADING CARD */
.loading-card {
    background:#f8fafc;
    padding:40px;
    border-radius:24px;
    text-align:center;
    border:1px solid #e2e8f0;
    margin-top:20px;
}

/* RESULT */
.result-box {
    border-radius:24px;
    overflow:hidden;
    border:1px solid #e2e8f0;
    box-shadow:0 20px 60px rgba(0,0,0,0.1);
}
.result-img {
    height:350px;
    background-size:cover;
    background-position:center;
}
.result-content {
    padding:25px;
}

/* BADGE */
.badge {
    display:inline-block;
    background:#f1f5f9;
    padding:6px 10px;
    margin:4px;
    border-radius:20px;
}

/* FOOTER */
.footer {
    text-align:center;
    margin-top:40px;
    color:#64748b;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------------------
# NAVBAR
# -----------------------------------------
st.markdown("""
<div class="navbar">
    <div class="nav-logo">🌍 QuidAway by bipzilla</div>
</div>
""", unsafe_allow_html=True)


# -----------------------------------------
# HERO
# -----------------------------------------
st.markdown("""
<div class="hero">
    <h1>Find Your Next Escape</h1>
    <p>Choose your vibe and budget — we decide where you go.</p>
</div>
""", unsafe_allow_html=True)


# -----------------------------------------
# DATA
# -----------------------------------------
DESTINATIONS = [
    {
        "name": "Madeira",
        "country": "Portugal",
        "vibes": ["Hiking","Nature"],
        "why": "Beautiful island with dramatic landscapes.",
        "image": "https://images.unsplash.com/photo-1513735492246-483525079686?auto=format&fit=crop&w=1400&q=80"
    },
    {
        "name": "Krakow",
        "country": "Poland",
        "vibes": ["City","Food"],
        "why": "A perfect budget-friendly cultural city.",
        "image": "https://images.unsplash.com/photo-1607427293702-036933bbf746?auto=format&fit=crop&w=1400&q=80"
    },
    {
        "name": "Valencia",
        "country": "Spain",
        "vibes": ["Beach","City"],
        "why": "Sun, beach and city in one place.",
        "image": "https://images.unsplash.com/photo-1583422409516-2895a77efded?auto=format&fit=crop&w=1400&q=80"
    }
]


# -----------------------------------------
# FORM
# -----------------------------------------
st.markdown("### ✈️ Start")

col1, col2 = st.columns(2)

with col1:
    budget = st.selectbox("Budget", ["Low","Medium","High"])
with col2:
    vibe = st.selectbox("Vibe", ["Hiking","City","Beach","Food","Nature"])

spin = st.button("🌍 Find my escape")


# -----------------------------------------
# RESULT / SPINNING EFFECT
# -----------------------------------------
if spin:
    loading = st.empty()

    loading.markdown("""
    <div class="loading-card">
        <div class="spinner">🌍</div>
        <h3>Finding your perfect escape...</h3>
        <p>Matching vibe • Checking budget • Picking destination</p>
    </div>
    """, unsafe_allow_html=True)

    time.sleep(2)

    choice = random.choice(DESTINATIONS)

    loading.empty()

    st.markdown(f"""
    <div class="result-box">
        <div class="result-img" style="background-image:url('{choice["image"]}')"></div>
        <div class="result-content">
            <h2>{choice["name"]}, {choice["country"]}</h2>
            {"".join([f"<span class='badge'>{v}</span>" for v in choice["vibes"]])}
            <p><b>Why go:</b> {choice["why"]}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


# -----------------------------------------
# FOOTER
# -----------------------------------------
st.markdown("""
<div class="footer">
    © 2026 QuidAway — Smart travel decisions
</div>
""", unsafe_allow_html=True)
