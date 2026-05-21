import random
import time
import streamlit as st

# -----------------------------------------
# PAGE CONFIG
# -----------------------------------------
st.set_page_config(
    page_title="QuidAway",
    page_icon="🌍",
    layout="wide"
)

# -----------------------------------------
# STYLE (FULL UI UPGRADE)
# -----------------------------------------
st.markdown("""
<style>

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

/* NAVBAR */
.navbar {
    display:flex;
    justify-content:space-between;
    padding:12px 30px;
    border-bottom:1px solid #e2e8f0;
    margin-bottom:20px;
}
.nav-logo {
    font-weight:900;
    font-size:1.4rem;
}
.nav-links {
    color:#64748b;
    font-size:0.9rem;
}

/* HERO */
.hero {
    padding:60px;
    border-radius:24px;
    background:linear-gradient(120deg,#0f172a,#1e293b);
    color:white;
    margin-bottom:30px;
}
.hero h1 {
    font-size:4rem;
    font-weight:900;
}
.hero p {
    font-size:1.2rem;
    color:#cbd5e1;
}

/* CARDS */
.card {
    background:white;
    padding:20px;
    border-radius:20px;
    border:1px solid #e2e8f0;
    margin-top:15px;
}

/* BUTTON */
.stButton>button {
    background:#ffb703;
    color:black;
    font-weight:800;
    border-radius:999px;
    padding:10px;
}

/* RESULT */
.result-box {
    border-radius:26px;
    overflow:hidden;
    border:1px solid #e2e8f0;
    box-shadow:0 20px 60px rgba(0,0,0,0.1);
    margin-top:25px;
}
.result-img {
    height:350px;
    background-position:center;
    background-size:cover;
}
.result-content {
    padding:25px;
}
.badge {
    display:inline-block;
    padding:6px 10px;
    background:#f1f5f9;
    border-radius:20px;
    margin:3px;
    font-size:0.8rem;
}

/* FOOTER */
.footer {
    text-align:center;
    color:#64748b;
    margin-top:40px;
    padding:20px;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------------------
# NAVBAR
# -----------------------------------------
st.markdown("""
<div class="navbar">
    <div class="nav-logo">🌍 QuidAway</div>
    <div class="nav-links">Discover • Budget Travel • Explore</div>
</div>
""", unsafe_allow_html=True)


# -----------------------------------------
# HERO
# -----------------------------------------
st.markdown("""
<div class="hero">
    <h1>Find Your Next Escape</h1>
    <p>Stop overthinking travel. Pick your vibe and budget — we’ll choose your perfect destination.</p>
</div>
""", unsafe_allow_html=True)


# -----------------------------------------
# DATA (SHORTENED SAMPLE)
# -----------------------------------------
DESTINATIONS = [
    {
        "name": "Madeira",
        "country": "Portugal",
        "budget": "Medium",
        "vibes": ["Hiking","Nature"],
        "why": "Beautiful island with dramatic landscapes and great hiking.",
        "image": "https://images.unsplash.com/photo-1513735492246-483525079686?auto=format&fit=crop&w=1400&q=80"
    },
    {
        "name": "Krakow",
        "country": "Poland",
        "budget": "Low",
        "vibes": ["City","Food"],
        "why": "Perfect budget city break with culture and nightlife.",
        "image": "https://images.unsplash.com/photo-1607427293702-036933bbf746?auto=format&fit=crop&w=1400&q=80"
    },
    {
        "name": "Valencia",
        "country": "Spain",
        "budget": "Medium",
        "vibes": ["Beach","City"],
        "why": "Beach and city combined with great food and sun.",
        "image": "https://images.unsplash.com/photo-1583422409516-2895a77efded?auto=format&fit=crop&w=1400&q=80"
    },
]


# -----------------------------------------
# FORM
# -----------------------------------------
st.markdown("### ✈️ Plan your escape")

col1, col2 = st.columns(2)

with col1:
    budget = st.selectbox("Budget", ["Low","Medium","High"])
with col2:
    vibe = st.selectbox("Vibe", ["Hiking","City","Beach","Food","Nature"])

spin = st.button("🌍 Find my escape")

# -----------------------------------------
# RESULT
# -----------------------------------------
if spin:
    time.sleep(1)

    choice = random.choice(DESTINATIONS)

    st.markdown("## Your Destination ✨")

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
    © 2026 QuidAway • Built for smarter travel decisions
</div>
""", unsafe_allow_html=True)
