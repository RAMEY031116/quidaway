import random
import time
from dataclasses import dataclass
from typing import List

import streamlit as st


# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="QuidAway | Budget Escape Decision Maker",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# -------------------------------------------------
# Data
# -------------------------------------------------
DESTINATIONS = [
    {
        "name": "Madeira",
        "country": "Portugal",
        "region": "Europe",
        "budget": "Medium",
        "vibes": ["Hiking", "Nature", "Adventure", "Relaxing"],
        "trip_lengths": ["3–5 days", "1 week"],
        "difficulty": "Moderate",
        "best_months": "March–June, September–November",
        "estimate": "£450–£850",
        "why": "Madeira is a brilliant budget-friendly island escape for hiking, dramatic viewpoints, levada walks and warm weather without needing a luxury budget.",
        "things": ["Pico do Arieiro sunrise", "Fanal Forest", "Levada walks"],
        "budget_tip": "Stay outside peak school holidays and choose guesthouses or apartments with kitchen access.",
        "avoid_if": "Avoid if you dislike hills, winding roads or walking-heavy trips.",
        "cheaper": "Albania",
        "similar": "Tenerife",
        "image": "https://images.unsplash.com/photo-1513735492246-483525079686?auto=format&fit=crop&w=1400&q=80",
    },
    {
        "name": "Krakow",
        "country": "Poland",
        "region": "Europe",
        "budget": "Low",
        "vibes": ["City", "Food", "Culture", "Budget"],
        "trip_lengths": ["Weekend", "3–5 days"],
        "difficulty": "Easy",
        "best_months": "April–June, September–December",
        "estimate": "£250–£550",
        "why": "Krakow is a strong budget city break with beautiful streets, affordable food, culture, nightlife and easy walking routes.",
        "things": ["Old Town", "Kazimierz", "Wieliczka Salt Mine"],
        "budget_tip": "Stay near tram links rather than directly in the main square to save money.",
        "avoid_if": "Avoid if you mainly want beaches or warm weather.",
        "cheaper": "Wroclaw",
        "similar": "Prague",
        "image": "https://images.unsplash.com/photo-1607427293702-036933bbf746?auto=format&fit=crop&w=1400&q=80",
    },
    {
        "name": "Snowdonia",
        "country": "Wales, UK",
        "region": "UK",
        "budget": "Low",
        "vibes": ["Hiking", "Nature", "Adventure", "Budget"],
        "trip_lengths": ["Weekend", "3–5 days"],
        "difficulty": "Moderate",
        "best_months": "May–September",
        "estimate": "£120–£350",
        "why": "Snowdonia is ideal if you want a proper hiking escape without leaving the UK. Great for mountains, lakes and scenic budget weekends.",
        "things": ["Yr Wyddfa / Snowdon", "Llanberis", "Waterfalls and lakes"],
        "budget_tip": "Use hostels, campsites or shared accommodation and travel outside peak summer weekends.",
        "avoid_if": "Avoid if you want guaranteed sun or a city-style holiday.",
        "cheaper": "Peak District",
        "similar": "Lake District",
        "image": "https://images.unsplash.com/photo-1598273372691-287a7d2dd8b4?auto=format&fit=crop&w=1400&q=80",
    },
    {
        "name": "Porto",
        "country": "Portugal",
        "region": "Europe",
        "budget": "Medium",
        "vibes": ["City", "Food", "Culture", "Relaxing"],
        "trip_lengths": ["Weekend", "3–5 days"],
        "difficulty": "Easy",
        "best_months": "April–June, September–October",
        "estimate": "£300–£650",
        "why": "Porto is a relaxed, walkable city break with riverside views, food, culture and a lower-cost feel compared with many major European capitals.",
        "things": ["Ribeira", "Dom Luís I Bridge", "Douro Valley day trip"],
        "budget_tip": "Stay across the river in Vila Nova de Gaia for good value and easy access.",
        "avoid_if": "Avoid if you want beaches directly in the city or nightlife-heavy travel.",
        "cheaper": "Krakow",
        "similar": "Lisbon",
        "image": "https://images.unsplash.com/photo-1555881400-74d7acaacd8b?auto=format&fit=crop&w=1400&q=80",
    },
    {
        "name": "Albanian Riviera",
        "country": "Albania",
        "region": "Europe",
        "budget": "Low",
        "vibes": ["Beach", "Adventure", "Nature", "Budget"],
        "trip_lengths": ["1 week", "2 weeks"],
        "difficulty": "Moderate",
        "best_months": "May–June, September",
        "estimate": "£400–£800",
        "why": "The Albanian Riviera is great for budget beach and adventure travel, with clear water, mountain roads and lower prices than many Mediterranean hotspots.",
        "things": ["Ksamil", "Himare", "Llogara Pass"],
        "budget_tip": "Avoid peak August and compare bus routes or car hire if moving around.",
        "avoid_if": "Avoid if you want everything to be super polished or resort-style.",
        "cheaper": "Montenegro coast",
        "similar": "Croatia",
        "image": "https://images.unsplash.com/photo-1621178727374-3793b75310bc?auto=format&fit=crop&w=1400&q=80",
    },
    {
        "name": "Tbilisi",
        "country": "Georgia",
        "region": "Worldwide",
        "budget": "Medium",
        "vibes": ["Food", "Culture", "Adventure", "Budget"],
        "trip_lengths": ["3–5 days", "1 week"],
        "difficulty": "Easy",
        "best_months": "May–June, September–October",
        "estimate": "£500–£950",
        "why": "Tbilisi is a budget-friendly cultural escape with amazing food, colourful streets, mountain day trips and a very different feel from common city breaks.",
        "things": ["Old Tbilisi", "Sulphur baths", "Kazbegi day trip"],
        "budget_tip": "Use local guesthouses and public transport for strong value.",
        "avoid_if": "Avoid if you only want short flight times from the UK.",
        "cheaper": "Krakow",
        "similar": "Yerevan",
        "image": "https://images.unsplash.com/photo-1565008576549-57569a49371d?auto=format&fit=crop&w=1400&q=80",
    },
    {
        "name": "Lake Bled",
        "country": "Slovenia",
        "region": "Europe",
        "budget": "Medium",
        "vibes": ["Hiking", "Nature", "Romantic", "Relaxing"],
        "trip_lengths": ["3–5 days", "1 week"],
        "difficulty": "Easy",
        "best_months": "May–September",
        "estimate": "£450–£850",
        "why": "Lake Bled is a scenic nature escape with lakes, mountains and easy outdoor activities. It feels special without being as expensive as Switzerland.",
        "things": ["Lake Bled walk", "Vintgar Gorge", "Triglav National Park"],
        "budget_tip": "Stay slightly outside Bled and use buses where possible.",
        "avoid_if": "Avoid if you want nightlife or very cheap food every day.",
        "cheaper": "Tatra Mountains, Poland",
        "similar": "Interlaken",
        "image": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1400&q=80",
    },
    {
        "name": "Valencia",
        "country": "Spain",
        "region": "Europe",
        "budget": "Medium",
        "vibes": ["Beach", "City", "Food", "Relaxing"],
        "trip_lengths": ["Weekend", "3–5 days", "1 week"],
        "difficulty": "Easy",
        "best_months": "April–June, September–October",
        "estimate": "£350–£700",
        "why": "Valencia gives you city, beach, food and sunshine in one trip, often feeling better value than Barcelona.",
        "things": ["City of Arts and Sciences", "Old Town", "Malvarrosa Beach"],
        "budget_tip": "Travel outside peak summer and use local menus for cheaper meals.",
        "avoid_if": "Avoid if you want mountain hiking as your main trip focus.",
        "cheaper": "Alicante",
        "similar": "Barcelona",
        "image": "https://images.unsplash.com/photo-1583422409516-2895a77efded?auto=format&fit=crop&w=1400&q=80",
    },
]


# -------------------------------------------------
# Styling
# -------------------------------------------------
st.markdown(
    """
<style>
    :root {
        --qa-bg: #0f172a;
        --qa-card: #ffffff;
        --qa-muted: #64748b;
        --qa-accent: #ffb703;
        --qa-accent-2: #38bdf8;
        --qa-green: #16a34a;
        --qa-red: #ef4444;
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 3rem;
        max-width: 1180px;
    }

    .hero {
        position: relative;
        overflow: hidden;
        border-radius: 30px;
        padding: 46px 42px;
        margin-bottom: 28px;
        background:
            linear-gradient(135deg, rgba(15,23,42,0.95), rgba(30,41,59,0.9)),
            url('https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=1600&q=80');
        background-size: cover;
        background-position: center;
        color: white;
        box-shadow: 0 22px 60px rgba(15, 23, 42, 0.22);
    }

    .hero h1 {
        font-size: clamp(2.4rem, 5vw, 4.9rem);
        line-height: 0.95;
        font-weight: 900;
        letter-spacing: -0.06em;
        margin-bottom: 14px;
    }

    .hero p {
        color: #e2e8f0;
        font-size: 1.15rem;
        max-width: 720px;
        line-height: 1.6;
    }

    .pill-row {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 24px;
    }

    .pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 14px;
        border-radius: 999px;
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.18);
        color: #fff;
        font-weight: 650;
        font-size: 0.92rem;
    }

    .section-title {
        font-size: 1.7rem;
        font-weight: 850;
        letter-spacing: -0.03em;
        margin-top: 6px;
        margin-bottom: 8px;
    }

    .subtle {
        color: #64748b;
        font-size: 1rem;
        line-height: 1.55;
    }

    .glass-card {
        border: 1px solid #e2e8f0;
        border-radius: 24px;
        padding: 22px;
        background: rgba(255, 255, 255, 0.92);
        box-shadow: 0 15px 45px rgba(15, 23, 42, 0.08);
    }

    .spin-card {
        border-radius: 28px;
        padding: 28px;
        background: linear-gradient(135deg, #f8fafc, #eef6ff);
        border: 1px solid #dbeafe;
        text-align: center;
    }

    .spinner-globe {
        font-size: 5.3rem;
        display: inline-block;
        animation: spin 0.38s linear infinite;
        margin: 18px 0;
        filter: drop-shadow(0 12px 18px rgba(15,23,42,.22));
    }

    @keyframes spin {
        from { transform: rotate(0deg) scale(1); }
        50% { transform: rotate(180deg) scale(1.08); }
        to { transform: rotate(360deg) scale(1); }
    }

    .result-hero {
        border-radius: 30px;
        overflow: hidden;
        background: #fff;
        border: 1px solid #e2e8f0;
        box-shadow: 0 22px 60px rgba(15, 23, 42, 0.14);
        margin-top: 16px;
    }

    .result-img {
        min-height: 330px;
        border-radius: 26px;
        background-size: cover;
        background-position: center;
        position: relative;
        overflow: hidden;
    }

    .result-img::after {
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(180deg, rgba(15,23,42,0.06), rgba(15,23,42,0.45));
    }

    .result-content {
        padding: 26px 28px;
    }

    .result-title {
        font-size: clamp(2rem, 4vw, 3.4rem);
        font-weight: 950;
        letter-spacing: -0.06em;
        color: #0f172a;
        margin: 0;
    }

    .result-country {
        color: #64748b;
        font-size: 1.15rem;
        margin-bottom: 18px;
    }

    .badge {
        display: inline-flex;
        margin: 5px 6px 5px 0;
        padding: 7px 11px;
        border-radius: 999px;
        background: #f1f5f9;
        color: #0f172a;
        border: 1px solid #e2e8f0;
        font-weight: 700;
        font-size: 0.9rem;
    }

    .score-wrap {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 18px;
        padding: 14px;
        margin-top: 12px;
    }

    .score-label {
        display: flex;
        justify-content: space-between;
        color: #334155;
        font-weight: 750;
        margin-bottom: 8px;
    }

    .score-bar-bg {
        height: 11px;
        border-radius: 999px;
        background: #e2e8f0;
        overflow: hidden;
    }

    .score-bar {
        height: 11px;
        border-radius: 999px;
        background: linear-gradient(90deg, #38bdf8, #22c55e);
    }

    .info-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 12px;
        margin: 18px 0;
    }

    .mini-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 18px;
        padding: 14px;
    }

    .mini-card strong {
        display: block;
        color: #0f172a;
        margin-bottom: 4px;
    }

    .mini-card span {
        color: #64748b;
    }

    .ad-placeholder {
        border: 1px dashed #94a3b8;
        background: #f8fafc;
        color: #64748b;
        border-radius: 18px;
        padding: 24px;
        text-align: center;
        margin: 18px 0;
        font-weight: 700;
    }

    .affiliate-box {
        border-radius: 22px;
        border: 1px solid #e2e8f0;
        padding: 18px;
        background: linear-gradient(135deg, #fff7ed, #ffffff);
        margin-top: 15px;
    }

    .fake-button {
        display: inline-block;
        padding: 11px 16px;
        border-radius: 999px;
        background: #0f172a;
        color: white !important;
        margin: 6px 6px 6px 0;
        font-weight: 800;
        text-decoration: none;
    }

    .fake-button.secondary {
        background: #ffffff;
        color: #0f172a !important;
        border: 1px solid #cbd5e1;
    }

    .footer-note {
        color: #64748b;
        font-size: 0.9rem;
        line-height: 1.6;
    }

    div[data-testid="stMetric"] {
        background: #ffffff;
        padding: 16px;
        border-radius: 18px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 8px 24px rgba(15,23,42,.05);
    }

    @media (max-width: 900px) {
        .hero {
            padding: 32px 24px;
            border-radius: 22px;
        }
        .info-grid {
            grid-template-columns: 1fr;
        }
        .result-content {
            padding: 20px;
        }
    }
</style>
    """,
    unsafe_allow_html=True,
)


# -------------------------------------------------
# Helper functions
# -------------------------------------------------
def calculate_match(place, region, budget, vibe, trip_length, difficulty):
    score = 40

    if region == "Surprise me" or place["region"] == region:
        score += 15

    if budget == "Any" or place["budget"] == budget:
        score += 18
    elif budget == "Low" and place["budget"] == "Medium":
        score += 7
    elif budget == "Medium" and place["budget"] in ["Low", "High"]:
        score += 7

    if vibe == "Surprise me" or vibe in place["vibes"]:
        score += 18

    if trip_length == "Flexible" or trip_length in place["trip_lengths"]:
        score += 12

    if difficulty == "Any" or place["difficulty"] == difficulty:
        score += 7

    return min(score, 99)


def filter_destinations(region, budget, vibe, trip_length, difficulty):
    scored = []
    for place in DESTINATIONS:
        score = calculate_match(place, region, budget, vibe, trip_length, difficulty)
        scored.append((score, place))

    # Keep decent matches, but do not be too strict for dummy prototype
    scored = sorted(scored, key=lambda x: x[0], reverse=True)
    top_pool = [item for item in scored if item[0] >= 62]

    if not top_pool:
        top_pool = scored[:5]

    # Randomly choose among top matches so it feels like a decision-maker
    chosen_score, chosen_place = random.choice(top_pool[:5])
    return chosen_place, chosen_score, scored[:5]


def render_score(label, value):
    st.markdown(
        f"""
        <div class="score-wrap">
            <div class="score-label"><span>{label}</span><span>{value}%</span></div>
            <div class="score-bar-bg"><div class="score-bar" style="width:{value}%"></div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_result(place, score, alternatives):
    st.markdown('<div class="result-hero">', unsafe_allow_html=True)

    col_img, col_info = st.columns([0.92, 1.08], gap="large")

    with col_img:
        st.markdown(
            f"""
            <div class="result-img" style="background-image:url('{place["image"]}')"></div>
            """,
            unsafe_allow_html=True,
        )

    with col_info:
        st.markdown('<div class="result-content">', unsafe_allow_html=True)
        st.markdown(
            f"""
            <h2 class="result-title">{place["name"]}</h2>
            <div class="result-country">{place["country"]} · {place["region"]}</div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            "".join([f'<span class="badge">{v}</span>' for v in place["vibes"][:4]]),
            unsafe_allow_html=True,
        )

        render_score("QuidAway match score", score)

        st.markdown(
            f"""
            <div class="info-grid">
                <div class="mini-card"><strong>Budget estimate</strong><span>{place["estimate"]}</span></div>
                <div class="mini-card"><strong>Best time</strong><span>{place["best_months"]}</span></div>
                <div class="mini-card"><strong>Difficulty</strong><span>{place["difficulty"]}</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(f"**Why this fits:** {place['why']}")
        st.markdown(f"**Budget tip:** {place['budget_tip']}")
        st.markdown(f"**Avoid if:** {place['avoid_if']}")

        st.markdown("**Things to consider:**")
        for thing in place["things"]:
            st.markdown(f"- {thing}")

        st.markdown(
            f"""
            <div class="affiliate-box">
                <strong>When ready, check live prices</strong>
                <p class="footer-note">
                    These are placeholder affiliate actions for the prototype. In WordPress, these would become
                    Travelpayouts / Booking / Skyscanner affiliate widgets or deep links.
                </p>
                <a class="fake-button" href="#">Check stays</a>
                <a class="fake-button secondary" href="#">Check flights</a>
                <a class="fake-button secondary" href="#">Things to do</a>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### Similar ideas")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info(f"**Cheaper alternative:** {place['cheaper']}")
    with c2:
        st.info(f"**Similar vibe:** {place['similar']}")
    with c3:
        alt = alternatives[1][1]["name"] if len(alternatives) > 1 else place["similar"]
        st.info(f"**Another match:** {alt}")


# -------------------------------------------------
# Hero
# -------------------------------------------------
st.markdown(
    """
<div class="hero">
    <h1>QuidAway</h1>
    <p>
        A budget escape decision-maker for people who know they want to go somewhere —
        but have no idea where. Pick your budget, vibe and trip length, then let QuidAway
        suggest a sensible escape.
    </p>
    <div class="pill-row">
        <span class="pill">🌍 Worldwide ideas</span>
        <span class="pill">🥾 Hiking & nature</span>
        <span class="pill">💸 Budget-first</span>
        <span class="pill">🎲 Randomised matches</span>
    </div>
</div>
""",
    unsafe_allow_html=True,
)


# -------------------------------------------------
# Top explanation
# -------------------------------------------------
left, right = st.columns([1.2, 0.8], gap="large")

with left:
    st.markdown('<div class="section-title">Find where your budget can take you</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <p class="subtle">
        This is a prototype of the website idea. The final WordPress version can use the same logic:
        a simple decision form, a spinning result animation, destination cards, budget estimates,
        optional affiliate links and AdSense placements.
        </p>
        """,
        unsafe_allow_html=True,
    )

with right:
    m1, m2 = st.columns(2)
    m1.metric("Demo places", len(DESTINATIONS))
    m2.metric("Main goal", "Decide")


# -------------------------------------------------
# Form
# -------------------------------------------------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("## Start your escape match")

with st.form("escape_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        budget = st.selectbox("Budget level", ["Low", "Medium", "High", "Any"], index=1)
        region = st.selectbox("Region", ["Europe", "UK", "Worldwide", "Surprise me"], index=0)

    with col2:
        vibe = st.selectbox(
            "Travel vibe",
            ["Hiking", "Nature", "Beach", "City", "Food", "Culture", "Adventure", "Relaxing", "Budget", "Surprise me"],
            index=0,
        )
        trip_length = st.selectbox("Trip length", ["Weekend", "3–5 days", "1 week", "2 weeks", "Flexible"], index=1)

    with col3:
        difficulty = st.selectbox("Activity level", ["Easy", "Moderate", "Challenging", "Any"], index=3)
        starting_from = st.text_input("Starting from", value="London")

    spin = st.form_submit_button("🌍 Find my escape", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)


# -------------------------------------------------
# Result state
# -------------------------------------------------
if "last_result" not in st.session_state:
    st.session_state.last_result = None


if spin:
    with st.container():
        st.markdown(
            """
            <div class="spin-card">
                <div class="spinner-globe">🌍</div>
                <h3>Matching your budget, vibe and escape style...</h3>
                <p class="subtle">Checking budget fit · comparing vibe · finding a sensible escape</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        time.sleep(1.6)

    chosen, score, alternatives = filter_destinations(region, budget, vibe, trip_length, difficulty)
    st.session_state.last_result = {
        "place": chosen,
        "score": score,
        "alternatives": alternatives,
        "starting_from": starting_from,
    }


if st.session_state.last_result:
    place = st.session_state.last_result["place"]
    score = st.session_state.last_result["score"]
    alternatives = st.session_state.last_result["alternatives"]

    st.markdown("## Your QuidAway result")
    render_result(place, score, alternatives)


# -------------------------------------------------
# AdSense and content sections
# -------------------------------------------------
st.markdown(
    """
<div class="ad-placeholder">
    AdSense placeholder: this area could show ads later after the site has enough content and is approved.
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("## How QuidAway would work on the real website")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        """
        <div class="mini-card">
            <strong>1. Choose your vibe</strong>
            <span>Budget, region, hiking, beach, city, nature, food or surprise me.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        """
        <div class="mini-card">
            <strong>2. Get a sensible match</strong>
            <span>The tool filters destinations first, then randomises from good matches.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        """
        <div class="mini-card">
            <strong>3. Decide, then check prices</strong>
            <span>Affiliate links are optional and appear after the destination explanation.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("## Future features")
future_col1, future_col2 = st.columns(2)

with future_col1:
    st.markdown(
        """
        - Save places you want to visit
        - Mark places as already travelled
        - Add user recommended routes
        - Hiking and nature filters
        - Cheaper alternative suggestions
        """
    )

with future_col2:
    st.markdown(
        """
        - Travelpayouts/Booking affiliate widgets
        - AdSense blocks after approval
        - Destination SEO pages
        - Login/profile expansion later
        - Community route posts later
        """
    )

st.markdown("---")
st.markdown(
    """
<p class="footer-note">
<strong>Prototype disclaimer:</strong> Budget estimates are dummy ranges for concept feedback only.
The final site should use clear disclaimers, affiliate disclosure, privacy policy and manually reviewed destination data.
</p>
""",
    unsafe_allow_html=True,
)
