import random
import time
import streamlit as st

# -----------------------------------------
# PAGE CONFIG
# -----------------------------------------
st.set_page_config(page_title="QuidAway", page_icon="🌍", layout="wide")

# -----------------------------------------
# STYLE
# -----------------------------------------
st.markdown("""
<style>
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* NAV */
.navbar {
    display:flex;
    justify-content:space-between;
    padding:12px 30px;
    border-bottom:1px solid #e2e8f0;
}
.nav-logo { font-weight:900; font-size:1.3rem; }

/* HERO */
.hero {
    padding:60px;
    border-radius:24px;
    background:linear-gradient(120deg,#0f172a,#1e293b);
    color:white;
    margin:20px 0;
}
.hero h1 { font-size:3.5rem; font-weight:900; }
.hero p { color:#cbd5e1; font-size:1.2rem; }

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
    animation:spin 0.6s linear infinite;
}
@keyframes spin {
    from { transform:rotate(0deg); }
    to { transform:rotate(360deg); }
}

/* LOADING */
.loading {
    text-align:center;
    padding:40px;
    border-radius:20px;
    background:#f8fafc;
    border:1px solid #e2e8f0;
}

/* RESULT */
.result {
    border-radius:24px;
    overflow:hidden;
    border:1px solid #e2e8f0;
    box-shadow:0 20px 50px rgba(0,0,0,0.1);
}
.result-img {
    height:350px;
    background-size:cover;
    background-position:center;
}
.result-content { padding:25px; }
.badge {
    display:inline-block;
    background:#f1f5f9;
    padding:6px 10px;
    margin:4px;
    border-radius:20px;
    font-size:0.85rem;
}

/* CARDS */
.card {
    background:#fff;
    padding:18px;
    border-radius:18px;
    border:1px solid #e2e8f0;
}

/* FOOTER */
.footer {
    text-align:center;
    color:#64748b;
    margin-top:30px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------------
# NAV
# -----------------------------------------
st.markdown('<div class="navbar"><div class="nav-logo">🌍 QuidAway by Bipzilla</div></div>', unsafe_allow_html=True)

# -----------------------------------------
# HERO
# -----------------------------------------
st.markdown("""
<div class="hero">
    <h1>Find Your Next Escape</h1>
    <p>Choose your vibe and budget — we’ll decide where you go.</p>
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
        "why": "Beautiful island with hikes and views.",
        "image": "https://images.unsplash.com/photo-1513735492246-483525079686?auto=format&fit=crop&w=1400&q=80"
    },
    {
        "name": "Krakow",
        "country": "Poland",
        "vibes": ["City","Food"],
        "why": "Great budget city and culture.",
        "image": "https://images.unsplash.com/photo-1607427293702-036933bbf746?auto=format&fit=crop&w=1400&q=80"
    },
    {
        "name": "Valencia",
        "country": "Spain",
        "vibes": ["Beach","City"],
        "why": "Sun + food + beach combo.",
        "image": "https://images.unsplash.com/photo-1583422409516-2895a77efded?auto=format&fit=crop&w=1400&q=80"
    }
]

# -----------------------------------------
# FORM
# -----------------------------------------
st.markdown("### ✈️ Start your escape")

col1, col2 = st.columns(2)
with col1:
    budget = st.selectbox("Budget", ["Low","Medium","High"])
with col2:
    vibe = st.selectbox("Vibe", ["Hiking","City","Beach","Food","Nature"])

spin = st.button("🌍 Find my escape")

# -----------------------------------------
# RESULT + SPIN
# -----------------------------------------
if spin:
    loader = st.empty()

    loader.markdown("""
    <div class="loading">
        <div class="spinner">🌍</div>
        <h3>Finding your escape...</h3>
        <p>Checking vibe • Matching budget • Picking destination</p>
    </div>
    """, unsafe_allow_html=True)

    time.sleep(2)

    choice = random.choice(DESTINATIONS)
    loader.empty()

    st.markdown("## Your Destination ✨")
    st.markdown(f"""
    <div class="result">
        <div class="result-img" style="background-image:url('{choice["image"]}')"></div>
        <div class="result-content">
            <h2>{choice["name"]}, {choice["country"]}</h2>
            {"".join([f"<span class='badge'>{v}</span>" for v in choice["vibes"]])}
            <p><b>Why go:</b> {choice["why"]}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------
# HOW IT WORKS (RE-ADDED)
# -----------------------------------------
st.markdown("## How QuidAway works")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("<div class='card'><b>1. Choose vibe</b><br>Pick your travel style.</div>", unsafe_allow_html=True)
with c2:
    st.markdown("<div class='card'><b>2. Match</b><br>We filter best options.</div>", unsafe_allow_html=True)
with c3:
    st.markdown("<div class='card'><b>3. Decide</b><br>Pick and go.</div>", unsafe_allow_html=True)

# -----------------------------------------
# FUTURE FEATURES (RE-ADDED)
# -----------------------------------------
st.markdown("## Future features")

f1, f2 = st.columns(2)

with f1:
    st.markdown("""
- Save destinations  
- Track trips  
- Recommendations  
""")

with f2:
    st.markdown("""
- Flight search  
- Hotel links  
- Affiliate integration  
""")

# -----------------------------------------
# FOOTER DISCLAIMER (RE-ADDED)
# -----------------------------------------
st.markdown("""
<div class="footer">
Prototype only • Prices and suggestions are estimates
</div>
""", unsafe_allow_html=True)
