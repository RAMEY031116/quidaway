import random
import time
from urllib.parse import quote_plus

import streamlit as st


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="QuidAway | Budget-Friendly Escape Finder",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

APP_DATA_VERSION = "clean-wordpress-demo-v2"

# Clear old cached result objects after app updates.
# This prevents KeyError if Streamlit Cloud keeps an older session_state result
# from a previous version of the destination data.
if st.session_state.get("app_data_version") != APP_DATA_VERSION:
    st.session_state["app_data_version"] = APP_DATA_VERSION
    st.session_state["result"] = None


# =========================================================
# DESTINATION DATA
# =========================================================
DESTINATIONS = [
    {
        "name": "Madeira",
        "country": "Portugal",
        "region": "Europe",
        "budget": "Medium",
        "primary_vibe": "Hiking",
        "secondary_vibes": ["Nature", "Coastal views", "Warm escape"],
        "trip_lengths": ["3–5 days", "1 week"],
        "difficulty": "Moderate",
        "best_for": ["Hikers", "Couples", "Nature lovers"],
        "best_months": "March–June, September–November",
        "budget_range": "£450–£850",
        "daily_spend": "£45–£80/day",
        "decision_summary": "Best for someone who wants dramatic views, proper walking routes and a warmer outdoor trip without going full luxury.",
        "why": "Madeira gives you mountain viewpoints, levada walks, coastal scenery and warm weather. It works well when you want a trip that feels adventurous but still manageable for a 4–7 day escape.",
        "good_to_know": "Public buses can help, but some routes are easier with tours or car hire. The island is hilly, so it is not a flat walking destination.",
        "things": ["Pico do Arieiro sunrise", "Fanal Forest", "Levada walks", "Funchal old town"],
        "budget_tip": "Choose guesthouses or apartments outside peak school holidays and stay somewhere with kitchen access.",
        "avoid_if": "Avoid if you dislike hills, winding roads or walking-heavy trips.",
        "cheaper": "Albania",
        "similar": "Tenerife",
        "image": "https://images.unsplash.com/photo-1513735492246-483525079686?auto=format&fit=crop&w=1600&q=80",
    },
    {
        "name": "Krakow",
        "country": "Poland",
        "region": "Europe",
        "budget": "Low",
        "primary_vibe": "City",
        "secondary_vibes": ["Food", "Culture", "Low-cost break"],
        "trip_lengths": ["Weekend", "3–5 days"],
        "difficulty": "Easy",
        "best_for": ["Friends", "Solo travellers", "First budget city break"],
        "best_months": "April–June, September–December",
        "budget_range": "£250–£550",
        "daily_spend": "£30–£60/day",
        "decision_summary": "Best for a low-cost city break where you still want culture, food and a proper travel feeling.",
        "why": "Krakow is walkable, atmospheric and usually easier on the wallet than many Western European cities. It is a strong option if someone wants a short trip with food, history and nightlife.",
        "good_to_know": "It is better for culture and food than beaches or hiking. Winter can be cold, but Christmas-market style trips can work well.",
        "things": ["Old Town", "Kazimierz", "Wieliczka Salt Mine", "Local pierogi spots"],
        "budget_tip": "Stay near tram links rather than directly on the main square.",
        "avoid_if": "Avoid if you mainly want beaches, guaranteed sun or a nature-first escape.",
        "cheaper": "Wroclaw",
        "similar": "Prague",
        "image": "https://images.unsplash.com/photo-1607427293702-036933bbf746?auto=format&fit=crop&w=1600&q=80",
    },
    {
        "name": "Snowdonia",
        "country": "Wales, UK",
        "region": "UK",
        "budget": "Low",
        "primary_vibe": "Hiking",
        "secondary_vibes": ["Nature", "UK weekend", "Mountains"],
        "trip_lengths": ["Weekend", "3–5 days"],
        "difficulty": "Moderate",
        "best_for": ["Hikers", "Groups", "Budget travellers"],
        "best_months": "May–September",
        "budget_range": "£120–£350",
        "daily_spend": "£25–£60/day",
        "decision_summary": "Best for a proper mountain escape without needing flights.",
        "why": "Snowdonia is ideal if you want lakes, mountains and a serious hiking feeling while keeping the trip UK-based. It works well for people who want adventure but have limited time or budget.",
        "good_to_know": "Weather can change quickly, so waterproofs and sensible footwear matter. Popular routes can be busy during peak weekends.",
        "things": ["Yr Wyddfa / Snowdon", "Llanberis", "Waterfalls and lakes", "Betws-y-Coed"],
        "budget_tip": "Use hostels, campsites or shared stays and avoid peak summer weekends.",
        "avoid_if": "Avoid if you want guaranteed sun, warm evenings or a city-style trip.",
        "cheaper": "Peak District",
        "similar": "Lake District",
        "image": "https://images.unsplash.com/photo-1598273372691-287a7d2dd8b4?auto=format&fit=crop&w=1600&q=80",
    },
    {
        "name": "Porto",
        "country": "Portugal",
        "region": "Europe",
        "budget": "Medium",
        "primary_vibe": "Food",
        "secondary_vibes": ["City", "Culture", "Relaxed break"],
        "trip_lengths": ["Weekend", "3–5 days"],
        "difficulty": "Easy",
        "best_for": ["Couples", "Foodies", "Slow travellers"],
        "best_months": "April–June, September–October",
        "budget_range": "£300–£650",
        "daily_spend": "£40–£75/day",
        "decision_summary": "Best for a relaxed city break with food, views and culture without feeling too expensive.",
        "why": "Porto is compact, atmospheric and good for people who like food, riverside walks, viewpoints and a slower pace than bigger capitals.",
        "good_to_know": "There are hills and steps, but the city is still easy to enjoy over a long weekend.",
        "things": ["Ribeira", "Dom Luís I Bridge", "Douro Valley day trip", "Francesinha"],
        "budget_tip": "Stay across the river in Vila Nova de Gaia or slightly outside the centre for better value.",
        "avoid_if": "Avoid if you want beaches directly in the city or a heavy nightlife trip.",
        "cheaper": "Krakow",
        "similar": "Lisbon",
        "image": "https://images.unsplash.com/photo-1555881400-74d7acaacd8b?auto=format&fit=crop&w=1600&q=80",
    },
    {
        "name": "Albanian Riviera",
        "country": "Albania",
        "region": "Europe",
        "budget": "Low",
        "primary_vibe": "Beach",
        "secondary_vibes": ["Adventure", "Value", "Coastal road trip"],
        "trip_lengths": ["1 week", "2 weeks"],
        "difficulty": "Moderate",
        "best_for": ["Backpackers", "Beach lovers", "Adventurous travellers"],
        "best_months": "May–June, September",
        "budget_range": "£400–£800",
        "daily_spend": "£30–£65/day",
        "decision_summary": "Best for beach and adventure travellers who want Mediterranean-style views without Mediterranean-style prices.",
        "why": "The Albanian Riviera can feel like a high-value coastal escape with clear water, mountain roads and smaller beach towns.",
        "good_to_know": "Transport planning matters. Some areas are easier if you are comfortable with buses, transfers or car hire.",
        "things": ["Ksamil", "Himare", "Llogara Pass", "Gjirokaster"],
        "budget_tip": "Avoid August and compare simple guesthouses rather than resort-style stays.",
        "avoid_if": "Avoid if you want everything polished, predictable or luxury-resort style.",
        "cheaper": "Montenegro coast",
        "similar": "Croatia",
        "image": "https://images.unsplash.com/photo-1621178727374-3793b75310bc?auto=format&fit=crop&w=1600&q=80",
    },
    {
        "name": "Tbilisi",
        "country": "Georgia",
        "region": "Worldwide",
        "budget": "Medium",
        "primary_vibe": "Culture",
        "secondary_vibes": ["Food", "Different", "Adventure"],
        "trip_lengths": ["3–5 days", "1 week"],
        "difficulty": "Easy",
        "best_for": ["Foodies", "Culture seekers", "Curious travellers"],
        "best_months": "May–June, September–October",
        "budget_range": "£500–£950",
        "daily_spend": "£30–£65/day",
        "decision_summary": "Best when you want somewhere memorable, food-focused and less obvious than the usual Europe city break.",
        "why": "Tbilisi offers colourful streets, sulphur baths, big food culture and access to mountain day trips. It can feel more unique than standard weekend destinations.",
        "good_to_know": "Flights can be longer or less direct from the UK, so it suits people who want something different.",
        "things": ["Old Tbilisi", "Sulphur baths", "Kazbegi day trip", "Khinkali and khachapuri"],
        "budget_tip": "Use local guesthouses and public transport for strong value.",
        "avoid_if": "Avoid if you only want short flight times or a very simple weekend trip.",
        "cheaper": "Krakow",
        "similar": "Yerevan",
        "image": "https://images.unsplash.com/photo-1565008576549-57569a49371d?auto=format&fit=crop&w=1600&q=80",
    },
    {
        "name": "Lake Bled",
        "country": "Slovenia",
        "region": "Europe",
        "budget": "Medium",
        "primary_vibe": "Nature",
        "secondary_vibes": ["Hiking", "Romantic", "Scenic"],
        "trip_lengths": ["3–5 days", "1 week"],
        "difficulty": "Easy",
        "best_for": ["Couples", "Nature lovers", "First-time hikers"],
        "best_months": "May–September",
        "budget_range": "£450–£850",
        "daily_spend": "£50–£90/day",
        "decision_summary": "Best for a scenic nature escape that feels special but still more realistic than Switzerland for many budgets.",
        "why": "Lake Bled gives you mountain views, lake walks, viewpoints and easy outdoor activities. It is strong for people who want nature without extreme hiking.",
        "good_to_know": "It is not the cheapest place in Europe, so staying slightly outside Bled can help.",
        "things": ["Lake Bled walk", "Vintgar Gorge", "Triglav National Park", "Bled Castle viewpoint"],
        "budget_tip": "Stay outside the main lake area and use buses where practical.",
        "avoid_if": "Avoid if you want nightlife or very cheap food every day.",
        "cheaper": "Tatra Mountains",
        "similar": "Interlaken",
        "image": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1600&q=80",
    },
    {
        "name": "Valencia",
        "country": "Spain",
        "region": "Europe",
        "budget": "Medium",
        "primary_vibe": "Beach",
        "secondary_vibes": ["City", "Food", "Sun"],
        "trip_lengths": ["Weekend", "3–5 days", "1 week"],
        "difficulty": "Easy",
        "best_for": ["Couples", "Friends", "Beach-city travellers"],
        "best_months": "April–June, September–October",
        "budget_range": "£350–£700",
        "daily_spend": "£45–£85/day",
        "decision_summary": "Best when you want city, beach and food in one trip without defaulting to Barcelona.",
        "why": "Valencia gives you sunshine, a beach, food culture and an easy city break structure. It can be a good compromise between relaxing and exploring.",
        "good_to_know": "It is better for relaxed beach-city travel than mountain adventure.",
        "things": ["City of Arts and Sciences", "Old Town", "Malvarrosa Beach", "Paella"],
        "budget_tip": "Travel outside peak summer and use local lunch menus for cheaper meals.",
        "avoid_if": "Avoid if hiking or mountains are your main focus.",
        "cheaper": "Alicante",
        "similar": "Barcelona",
        "image": "https://images.unsplash.com/photo-1583422409516-2895a77efded?auto=format&fit=crop&w=1600&q=80",
    },
]


# =========================================================
# CSS
# =========================================================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1160px;
    padding-top: 1rem;
    padding-bottom: 3rem;
}

#MainMenu, footer, header {
    visibility: hidden;
}

[data-testid="stAppViewContainer"] {
    background: #f6f8fb;
}

/* Navigation */
.qa-nav {
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:16px;
    padding: 10px 4px 18px 4px;
}

.qa-logo {
    font-weight: 950;
    font-size: 1.45rem;
    letter-spacing: -0.045em;
    color: #0f172a;
}

.qa-nav-links {
    display:flex;
    gap:10px;
    flex-wrap:wrap;
}

.qa-nav-chip {
    padding: 8px 12px;
    border-radius: 999px;
    background:#ffffff;
    border:1px solid #dbe3ef;
    color:#334155;
    font-weight:700;
    font-size:.88rem;
}

/* Hero */
.qa-hero {
    position: relative;
    overflow: hidden;
    border-radius: 32px;
    padding: 52px 44px;
    margin-bottom: 26px;
    background:
        linear-gradient(135deg, rgba(10,18,32,.90), rgba(18,35,58,.82)),
        url('https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1800&q=80');
    background-size: cover;
    background-position: center;
    color: white;
    box-shadow: 0 24px 60px rgba(15, 23, 42, 0.20);
}

.qa-hero h1 {
    font-size: clamp(2.55rem, 5.3vw, 5.1rem);
    line-height: .96;
    margin: 0 0 16px;
    font-weight: 950;
    letter-spacing: -0.07em;
}

.qa-hero p {
    max-width: 780px;
    font-size: 1.16rem;
    color:#e5edf7;
    line-height:1.66;
}

.qa-pills {
    display:flex;
    gap:10px;
    flex-wrap:wrap;
    margin-top:24px;
}

.qa-pill {
    display:inline-flex;
    gap:8px;
    align-items:center;
    padding:9px 14px;
    border-radius:999px;
    background:rgba(255,255,255,.14);
    border:1px solid rgba(255,255,255,.22);
    color:#fff;
    font-weight:800;
    font-size:.92rem;
}

/* Cards */
.qa-card {
    background:#ffffff;
    border:1px solid #dfe7f2;
    border-radius: 26px;
    padding:24px;
    box-shadow: 0 16px 42px rgba(15,23,42,.07);
}

.qa-soft-card {
    background:#ffffff;
    border:1px solid #dfe7f2;
    border-radius:22px;
    padding:20px;
    height:100%;
}

.qa-section-title {
    font-size: 1.75rem;
    font-weight: 950;
    letter-spacing:-.045em;
    color:#0f172a;
    margin: 2px 0 8px 0;
}

.qa-muted {
    color:#526173;
    line-height:1.62;
}

.qa-problem {
    background:#ffffff;
    border:1px solid #dfe7f2;
    border-radius:22px;
    padding:20px;
    height:100%;
}

.qa-problem b {
    display:block;
    color:#0f172a;
    font-size:1.05rem;
    margin-bottom:6px;
}

/* Streamlit button */
div.stButton > button {
    background: #0f766e !important;
    color: #ffffff !important;
    font-weight: 950 !important;
    border: 0 !important;
    border-radius: 999px !important;
    padding: .85rem 1rem !important;
    box-shadow: 0 12px 24px rgba(15, 118, 110, .20);
}

div.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 18px 30px rgba(15, 118, 110, .25);
}

/* Spinner */
.qa-spinner-box {
    text-align:center;
    padding: 34px 24px;
    border-radius: 28px;
    background:#ffffff;
    border:1px solid #dbeafe;
    box-shadow: 0 16px 42px rgba(15,23,42,.08);
}

.qa-spinner {
    display:inline-block;
    font-size:5.2rem;
    animation: spin 0.42s linear infinite;
    filter: drop-shadow(0 16px 18px rgba(15,23,42,.20));
    margin-bottom: 8px;
}

@keyframes spin {
    from { transform: rotate(0deg) scale(1); }
    50% { transform: rotate(180deg) scale(1.06); }
    to { transform: rotate(360deg) scale(1); }
}

/* Result */
.qa-result {
    overflow:hidden;
    border-radius: 30px;
    background:white;
    border:1px solid #dfe7f2;
    box-shadow: 0 24px 62px rgba(15,23,42,.14);
    margin-top: 18px;
}

.qa-result-img {
    min-height: 380px;
    border-radius: 24px;
    background-size: cover;
    background-position: center;
    position:relative;
    overflow:hidden;
}

.qa-result-img::after {
    content:"";
    position:absolute;
    inset:0;
    background:linear-gradient(180deg, rgba(15,23,42,.03), rgba(15,23,42,.38));
}

.qa-result-body {
    padding: 28px 30px;
}

.qa-destination {
    font-size: clamp(2.1rem, 4.1vw, 3.7rem);
    line-height:.98;
    font-weight: 950;
    letter-spacing:-.065em;
    color:#0f172a;
    margin: 0;
}

.qa-country {
    margin-top:8px;
    color:#526173;
    font-weight:700;
    font-size:1.05rem;
}

.qa-primary-badge {
    display:inline-flex;
    padding:8px 13px;
    border-radius:999px;
    background:#ecfdf5;
    border:1px solid #bbf7d0;
    color:#166534;
    font-size:.9rem;
    font-weight:900;
    margin: 12px 6px 2px 0;
}

.qa-tag {
    display:inline-flex;
    padding:7px 10px;
    border-radius:999px;
    background:#f1f5f9;
    border:1px solid #dbe3ef;
    color:#334155;
    font-size:.84rem;
    font-weight:750;
    margin: 6px 6px 0 0;
}

.qa-score-box {
    margin:16px 0;
    padding:14px;
    background:#f8fafc;
    border:1px solid #dbe3ef;
    border-radius:18px;
}

.qa-score-label {
    display:flex;
    justify-content:space-between;
    gap:12px;
    margin-bottom:8px;
    color:#334155;
    font-weight:900;
}

.qa-score-bg {
    height:12px;
    border-radius:999px;
    overflow:hidden;
    background:#dbe3ef;
}

.qa-score-fill {
    height:12px;
    border-radius:999px;
    background: linear-gradient(90deg, #0ea5e9, #10b981);
}

.qa-grid-3 {
    display:grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap:12px;
    margin: 16px 0;
}

.qa-mini {
    background:#f8fafc;
    border:1px solid #dbe3ef;
    border-radius:18px;
    padding:14px;
}

.qa-mini strong {
    display:block;
    color:#0f172a;
    margin-bottom:4px;
}

.qa-mini span {
    color:#526173;
    font-size:.92rem;
}

/* Affiliate */
.qa-affiliate {
    margin-top:18px;
    padding:20px;
    border-radius:24px;
    background:#fffbeb;
    border:1px solid #fde68a;
}

.qa-affiliate-title {
    font-weight:950;
    color:#0f172a;
    font-size:1.12rem;
    margin-bottom:5px;
}

.qa-aff-grid {
    display:grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap:10px;
    margin-top:14px;
}

.qa-aff-link {
    display:block;
    text-decoration:none !important;
    color:#0f172a !important;
    background:#ffffff;
    border:1px solid #eadfb8;
    border-radius:18px;
    padding:13px;
    font-weight:900;
    box-shadow:0 8px 20px rgba(15,23,42,.05);
}

.qa-aff-link span {
    display:block;
    color:#526173;
    font-size:.78rem;
    font-weight:700;
    margin-top:3px;
}

/* Ads */
.qa-ad {
    margin: 22px 0;
    padding: 26px;
    border: 1px dashed #8aa0b7;
    background:#ffffff;
    border-radius:22px;
    text-align:center;
    color:#526173;
    font-weight:850;
}

/* Footer */
.qa-footer {
    text-align:center;
    color:#526173;
    margin-top:38px;
    padding-top:20px;
    border-top:1px solid #dfe7f2;
    font-size:.9rem;
    line-height:1.7;
}

div[data-testid="stMetric"] {
    background:#ffffff;
    border:1px solid #dfe7f2;
    border-radius:18px;
    padding:14px;
    box-shadow:0 8px 20px rgba(15,23,42,.04);
}

@media(max-width: 900px) {
    .qa-hero { padding:34px 24px; border-radius:25px; }
    .qa-grid-3, .qa-aff-grid { grid-template-columns: 1fr; }
    .qa-result-img { min-height:260px; }
    .qa-nav { align-items:flex-start; flex-direction:column; }
}
</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# HELPERS
# =========================================================
def affiliate_url(kind: str, place: dict) -> str:
    q = quote_plus(f"{place['name']} {place['country']}")
    city = quote_plus(place["name"])
    fake_partner = "quidaway-demo"

    if kind == "stays":
        return f"https://example-affiliate.com/hotels/search?destination={q}&partner={fake_partner}&subid=quidaway"
    if kind == "flights":
        return f"https://example-affiliate.com/flights/search?to={city}&partner={fake_partner}&subid=quidaway"
    if kind == "activities":
        return f"https://example-affiliate.com/activities/search?q={q}&partner={fake_partner}&subid=quidaway"
    if kind == "insurance":
        return f"https://example-affiliate.com/travel-insurance?destination={q}&partner={fake_partner}&subid=quidaway"
    return "#"


def calc_score(place, region, budget, vibe, trip_length, difficulty):
    score = 32

    if region == "Surprise me" or place["region"] == region:
        score += 16

    if budget == "Any" or place["budget"] == budget:
        score += 20
    elif budget == "Low" and place["budget"] == "Medium":
        score += 8
    elif budget == "Medium" and place["budget"] in ["Low", "High"]:
        score += 8

    primary_vibe = place.get("primary_vibe", "")
    secondary_vibes = place.get("secondary_vibes", place.get("vibes", []))

    if vibe == "Surprise me" or vibe == primary_vibe or vibe in secondary_vibes:
        score += 22

    if trip_length == "Flexible" or trip_length in place["trip_lengths"]:
        score += 12

    if difficulty == "Any" or difficulty == place["difficulty"]:
        score += 8

    return min(score, 99)


def pick_destination(region, budget, vibe, trip_length, difficulty):
    scored = [(calc_score(p, region, budget, vibe, trip_length, difficulty), p) for p in DESTINATIONS]
    scored = sorted(scored, key=lambda x: x[0], reverse=True)

    top_pool = [x for x in scored if x[0] >= 60] or scored[:5]
    score, place = random.choice(top_pool[:4])
    return place, score, scored


def score_bar(label, value):
    return f"""
    <div class="qa-score-box">
        <div class="qa-score-label"><span>{label}</span><span>{value}%</span></div>
        <div class="qa-score-bg"><div class="qa-score-fill" style="width:{value}%"></div></div>
    </div>
    """


def render_affiliate_block(place):
    stays = affiliate_url("stays", place)
    flights = affiliate_url("flights", place)
    activities = affiliate_url("activities", place)
    insurance = affiliate_url("insurance", place)

    st.markdown(
        f"""
        <div class="qa-affiliate">
            <div class="qa-affiliate-title">Check real prices when you are ready</div>
            <div class="qa-muted">
                Demo affiliate area. On the real WordPress site, these would become Travelpayouts, Booking, Skyscanner,
                Expedia or activity-provider links. QuidAway helps the visitor decide first — these links are the next step.
            </div>
            <div class="qa-aff-grid">
                <a class="qa-aff-link" href="{stays}" target="_blank" rel="sponsored noopener">
                    🏨 Stays
                    <span>Demo hotel search</span>
                </a>
                <a class="qa-aff-link" href="{flights}" target="_blank" rel="sponsored noopener">
                    ✈️ Flights
                    <span>Demo flight search</span>
                </a>
                <a class="qa-aff-link" href="{activities}" target="_blank" rel="sponsored noopener">
                    🎟️ Activities
                    <span>Demo things to do</span>
                </a>
                <a class="qa-aff-link" href="{insurance}" target="_blank" rel="sponsored noopener">
                    🛡️ Cover
                    <span>Demo travel cover</span>
                </a>
            </div>
            <p class="qa-muted" style="font-size:.84rem;margin-top:12px;">
                Affiliate disclosure example: QuidAway may earn a commission if a visitor uses these links, at no extra cost to them.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_result(place, score, scored):
    col_img, col_text = st.columns([0.95, 1.05], gap="large")

    with col_img:
        st.markdown(
            f"""
            <div class="qa-result-img" style="background-image:url('{place["image"]}')"></div>
            """,
            unsafe_allow_html=True,
        )

    with col_text:
        st.markdown('<div class="qa-result-body">', unsafe_allow_html=True)

        # Safe fallbacks make the app resilient if old session_state data exists
        primary_vibe = place.get("primary_vibe", place.get("vibes", ["Escape"])[0] if place.get("vibes") else "Escape")
        secondary_vibes = place.get("secondary_vibes", place.get("vibes", [])[1:4])
        budget_range = place.get("budget_range", place.get("estimate", "Estimate varies"))
        daily_spend = place.get("daily_spend", "Varies by season")
        best_months = place.get("best_months", "Depends on season")
        decision_summary = place.get("decision_summary", "A practical escape idea based on your selected budget and vibe.")
        good_to_know = place.get("good_to_know", "Check live prices and travel details before planning.")
        budget_tip = place.get("budget_tip", "Travel outside peak dates and compare accommodation areas.")
        avoid_if = place.get("avoid_if", "Avoid if the destination style does not match your travel mood.")
        things = place.get("things", ["Explore the area", "Compare stays", "Check transport options"])

        st.markdown(
            f"""
            <h2 class="qa-destination">{place.get("name", "Destination")}</h2>
            <div class="qa-country">{place.get("country", "")} · {place.get("region", "")}</div>
            <div>
                <span class="qa-primary-badge">{primary_vibe}</span>
                {"".join([f"<span class='qa-tag'>{v}</span>" for v in secondary_vibes[:3]])}
            </div>
            {score_bar("QuidAway decision match", score)}
            <div class="qa-grid-3">
                <div class="qa-mini"><strong>Budget range</strong><span>{budget_range}</span></div>
                <div class="qa-mini"><strong>Daily spend</strong><span>{daily_spend}</span></div>
                <div class="qa-mini"><strong>Best time</strong><span>{best_months}</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(f"**Quick decision:** {decision_summary}")
        st.markdown(f"**Why this place works:** {place.get('why', 'This destination matches your selected travel style.')}")
        st.markdown(f"**Good to know:** {good_to_know}")
        st.markdown(f"**Budget tip:** {budget_tip}")
        st.markdown(f"**Avoid if:** {avoid_if}")

        st.markdown("**Simple trip ideas:**")
        for thing in things:
            st.markdown(f"- {thing}")

        render_affiliate_block(place)

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### More decision help")
    a, b, c = st.columns(3)
    a.info(f"**Cheaper option:** {place.get('cheaper', 'Show another lower-budget option')}")
    b.info(f"**Similar vibe:** {place.get('similar', 'Show a similar destination')}")
    another = scored[1][1]["name"] if len(scored) > 1 else place["similar"]
    c.info(f"**Another good match:** {another}")


# =========================================================
# NAV + HERO
# =========================================================
st.markdown(
    """
<div class="qa-nav">
    <div class="qa-logo">🌍 QuidAway</div>
    <div class="qa-nav-links">
        <span class="qa-nav-chip">Budget-first</span>
        <span class="qa-nav-chip">Escape finder</span>
        <span class="qa-nav-chip">Hiking & nature</span>
        <span class="qa-nav-chip">Worldwide ideas</span>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="qa-hero">
    <h1>Find a place that fits your budget and vibe.</h1>
    <p>
        QuidAway helps people who want to go somewhere but cannot decide where.
        Choose your budget, trip style and time available — then get a practical destination idea
        with honest tips, estimated costs and alternatives.
    </p>
    <div class="qa-pills">
        <span class="qa-pill">💸 Budget-friendly ideas</span>
        <span class="qa-pill">🥾 Hiking, city, beach & nature</span>
        <span class="qa-pill">🧭 Decision maker</span>
        <span class="qa-pill">🔗 Affiliate-ready demo</span>
    </div>
</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# PROBLEM SECTION
# =========================================================
intro_left, intro_right = st.columns([1.25, 0.75], gap="large")

with intro_left:
    st.markdown('<div class="qa-section-title">The problem it solves</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <p class="qa-muted">
        Most travel sites are built for people who already know where they want to go.
        QuidAway is for the earlier moment: “I have a budget and a vibe, but I have no idea where to go.”
        It makes the decision easier before the visitor checks prices or books anything.
        </p>
        """,
        unsafe_allow_html=True,
    )

with intro_right:
    m1, m2 = st.columns(2)
    m1.metric("Demo places", len(DESTINATIONS))
    m2.metric("Main use", "Decide")

p1, p2, p3 = st.columns(3)
with p1:
    st.markdown("<div class='qa-problem'><b>1. Too many choices</b><span class='qa-muted'>People see endless flights, hotels and TikTok ideas but still do not know what fits them.</span></div>", unsafe_allow_html=True)
with p2:
    st.markdown("<div class='qa-problem'><b>2. Budget confusion</b><span class='qa-muted'>A cheap flight does not always mean a cheap trip. QuidAway explains the likely budget fit.</span></div>", unsafe_allow_html=True)
with p3:
    st.markdown("<div class='qa-problem'><b>3. Wrong destination risk</b><span class='qa-muted'>The tool shows who a place suits, who should avoid it and what cheaper options exist.</span></div>", unsafe_allow_html=True)


# =========================================================
# FORM
# =========================================================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="qa-card">', unsafe_allow_html=True)
st.markdown("## Find my escape")

with st.form("quidaway_form"):
    c1, c2, c3 = st.columns(3)

    with c1:
        budget = st.selectbox("Budget level", ["Low", "Medium", "High", "Any"], index=1)
        region = st.selectbox("Where are you open to?", ["Europe", "UK", "Worldwide", "Surprise me"], index=0)

    with c2:
        vibe = st.selectbox(
            "What kind of trip do you want?",
            ["Hiking", "Nature", "Beach", "City", "Food", "Culture", "Adventure", "Relaxing", "Budget", "Warm escape", "Surprise me"],
            index=0,
        )
        trip_length = st.selectbox("How long?", ["Weekend", "3–5 days", "1 week", "2 weeks", "Flexible"], index=1)

    with c3:
        difficulty = st.selectbox("Activity level", ["Easy", "Moderate", "Challenging", "Any"], index=3)
        starting_from = st.text_input("Starting from", value="London")

    submitted = st.form_submit_button("🌍 Find my escape", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# SPIN + RESULT
# =========================================================
if "result" not in st.session_state:
    st.session_state["result"] = None

if submitted:
    placeholder = st.empty()
    with placeholder:
        st.markdown(
            """
            <div class="qa-spinner-box">
                <div class="qa-spinner">🌍</div>
                <h3>Finding a sensible escape...</h3>
                <p class="qa-muted">Checking budget fit · matching your vibe · looking for useful alternatives</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    time.sleep(1.6)
    placeholder.empty()

    place, score, scored = pick_destination(region, budget, vibe, trip_length, difficulty)
    st.session_state["result"] = {
        "place": place,
        "score": score,
        "scored": scored,
        "starting_from": starting_from,
    }

if st.session_state["result"]:
    st.markdown("## Your QuidAway suggestion")
    st.markdown('<div class="qa-result">', unsafe_allow_html=True)
    render_result(
        st.session_state["result"]["place"],
        st.session_state["result"]["score"],
        st.session_state["result"]["scored"],
    )
    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# ADSENSE DEMO
# =========================================================
st.markdown(
    """
<div class="qa-ad">
    AdSense demo placement — this could appear after the tool or between destination sections once the real site is approved.
</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# REAL WEBSITE FEATURES
# =========================================================
st.markdown("## What would make this website unique")

f1, f2, f3 = st.columns(3)

with f1:
    st.markdown(
        """
        <div class="qa-soft-card">
            <b>Budget fit, not just random places</b><br><br>
            The tool does not simply pick a country. It explains whether the destination makes sense for the visitor's budget and trip length.
        </div>
        """,
        unsafe_allow_html=True,
    )

with f2:
    st.markdown(
        """
        <div class="qa-soft-card">
            <b>Honest travel decision help</b><br><br>
            Each result includes “avoid if” notes and good-to-know context, so it feels more trustworthy than a normal affiliate site.
        </div>
        """,
        unsafe_allow_html=True,
    )

with f3:
    st.markdown(
        """
        <div class="qa-soft-card">
            <b>Cheaper and similar alternatives</b><br><br>
            If a destination is not right, the visitor immediately gets cheaper or similar ideas instead of starting again.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("## How this could work in WordPress")

wp1, wp2 = st.columns(2)

with wp1:
    st.markdown(
        """
        **Simple WordPress setup**
        - WordPress with Kadence or Astra theme
        - One-page homepage with this tool embedded
        - Custom HTML/JavaScript for the decision maker
        - RankMath for SEO pages
        - Google Site Kit or Ad Inserter for AdSense
        - Travelpayouts/Booking/Skyscanner style affiliate links
        """
    )

with wp2:
    st.markdown(
        """
        **Expansion features later**
        - Save places in the browser first
        - Login and profiles later
        - “Want to go” and “Already visited” lists
        - User recommended routes
        - Destination pages for SEO
        - Google Sheets or Airtable as a simple destination database
        """
    )


# =========================================================
# FOOTER
# =========================================================
st.markdown(
    """
<div class="qa-footer">
    Prototype only. Budget ranges are example estimates, not live prices. Affiliate links are dummy demo links.
    A real website should include Privacy Policy, Affiliate Disclosure, Terms/Disclaimer and manually reviewed destination data.
</div>
""",
    unsafe_allow_html=True,
)
