import random
import time
from urllib.parse import quote_plus

import streamlit as st

st.set_page_config(
    page_title="QuidAway | Budget Escape Decision Maker",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

DESTINATIONS = [
    {
        "name": "Madeira", "country": "Portugal", "region": "Europe", "budget": "Medium",
        "vibes": ["Hiking", "Nature", "Adventure", "Warm Weather"],
        "trip_lengths": ["3–5 days", "1 week"], "difficulty": "Moderate",
        "best_months": "March–June, September–November", "estimate": "£450–£850", "daily_spend": "£45–£80/day",
        "why": "Madeira gives you mountain views, levada walks, coastal scenery and warm weather without feeling like a luxury-only destination.",
        "things": ["Pico do Arieiro sunrise", "Fanal Forest", "Levada walks", "Funchal old town"],
        "budget_tip": "Stay in guesthouses or apartments outside peak school holidays and use public buses where possible.",
        "avoid_if": "Avoid if you dislike hills, winding roads or walking-heavy trips.",
        "cheaper": "Albania", "similar": "Tenerife",
        "image": "https://images.unsplash.com/photo-1513735492246-483525079686?auto=format&fit=crop&w=1600&q=80",
    },
    {
        "name": "Krakow", "country": "Poland", "region": "Europe", "budget": "Low",
        "vibes": ["City", "Food", "Culture", "Budget"],
        "trip_lengths": ["Weekend", "3–5 days"], "difficulty": "Easy",
        "best_months": "April–June, September–December", "estimate": "£250–£550", "daily_spend": "£30–£60/day",
        "why": "Krakow is a strong budget city break with culture, affordable food, walkable streets and plenty to do in a short trip.",
        "things": ["Old Town", "Kazimierz", "Wieliczka Salt Mine", "Cheap pierogi spots"],
        "budget_tip": "Stay near tram links rather than directly in the main square to save money.",
        "avoid_if": "Avoid if you mainly want beaches or guaranteed warm weather.",
        "cheaper": "Wroclaw", "similar": "Prague",
        "image": "https://images.unsplash.com/photo-1607427293702-036933bbf746?auto=format&fit=crop&w=1600&q=80",
    },
    {
        "name": "Snowdonia", "country": "Wales, UK", "region": "UK", "budget": "Low",
        "vibes": ["Hiking", "Nature", "Adventure", "Budget"],
        "trip_lengths": ["Weekend", "3–5 days"], "difficulty": "Moderate",
        "best_months": "May–September", "estimate": "£120–£350", "daily_spend": "£25–£60/day",
        "why": "Snowdonia is ideal if you want a proper hiking escape without leaving the UK. Mountains, lakes and scenic routes make it feel like a real adventure.",
        "things": ["Yr Wyddfa / Snowdon", "Llanberis", "Waterfalls and lakes", "Betws-y-Coed"],
        "budget_tip": "Use hostels, campsites or shared accommodation and avoid peak summer weekends.",
        "avoid_if": "Avoid if you want guaranteed sun or a city-style holiday.",
        "cheaper": "Peak District", "similar": "Lake District",
        "image": "https://images.unsplash.com/photo-1598273372691-287a7d2dd8b4?auto=format&fit=crop&w=1600&q=80",
    },
    {
        "name": "Porto", "country": "Portugal", "region": "Europe", "budget": "Medium",
        "vibes": ["City", "Food", "Culture", "Relaxing"],
        "trip_lengths": ["Weekend", "3–5 days"], "difficulty": "Easy",
        "best_months": "April–June, September–October", "estimate": "£300–£650", "daily_spend": "£40–£75/day",
        "why": "Porto is a relaxed, walkable city break with riverside views, food, culture and a lower-cost feel compared with many major European capitals.",
        "things": ["Ribeira", "Dom Luís I Bridge", "Douro Valley day trip", "Francesinha"],
        "budget_tip": "Stay across the river in Vila Nova de Gaia for value and easy access.",
        "avoid_if": "Avoid if you want beaches directly in the city or nightlife-heavy travel.",
        "cheaper": "Krakow", "similar": "Lisbon",
        "image": "https://images.unsplash.com/photo-1555881400-74d7acaacd8b?auto=format&fit=crop&w=1600&q=80",
    },
    {
        "name": "Albanian Riviera", "country": "Albania", "region": "Europe", "budget": "Low",
        "vibes": ["Beach", "Adventure", "Nature", "Budget"],
        "trip_lengths": ["1 week", "2 weeks"], "difficulty": "Moderate",
        "best_months": "May–June, September", "estimate": "£400–£800", "daily_spend": "£30–£65/day",
        "why": "The Albanian Riviera is a budget-friendly beach and adventure option with clear water, mountain roads and lower prices than many Mediterranean hotspots.",
        "things": ["Ksamil", "Himare", "Llogara Pass", "Gjirokaster"],
        "budget_tip": "Avoid peak August and compare bus routes or car hire if moving around.",
        "avoid_if": "Avoid if you want everything to be polished, predictable or resort-style.",
        "cheaper": "Montenegro coast", "similar": "Croatia",
        "image": "https://images.unsplash.com/photo-1621178727374-3793b75310bc?auto=format&fit=crop&w=1600&q=80",
    },
    {
        "name": "Tbilisi", "country": "Georgia", "region": "Worldwide", "budget": "Medium",
        "vibes": ["Food", "Culture", "Adventure", "Budget"],
        "trip_lengths": ["3–5 days", "1 week"], "difficulty": "Easy",
        "best_months": "May–June, September–October", "estimate": "£500–£950", "daily_spend": "£30–£65/day",
        "why": "Tbilisi is a budget-friendly cultural escape with colourful streets, amazing food, sulphur baths and mountain day-trip potential.",
        "things": ["Old Tbilisi", "Sulphur baths", "Kazbegi day trip", "Khinkali and khachapuri"],
        "budget_tip": "Use local guesthouses and public transport for strong value.",
        "avoid_if": "Avoid if you only want short flight times from the UK.",
        "cheaper": "Krakow", "similar": "Yerevan",
        "image": "https://images.unsplash.com/photo-1565008576549-57569a49371d?auto=format&fit=crop&w=1600&q=80",
    },
    {
        "name": "Lake Bled", "country": "Slovenia", "region": "Europe", "budget": "Medium",
        "vibes": ["Hiking", "Nature", "Romantic", "Relaxing"],
        "trip_lengths": ["3–5 days", "1 week"], "difficulty": "Easy",
        "best_months": "May–September", "estimate": "£450–£850", "daily_spend": "£50–£90/day",
        "why": "Lake Bled is a scenic nature escape with lakes, mountains and easy outdoor activities. It feels special without being as expensive as Switzerland.",
        "things": ["Lake Bled walk", "Vintgar Gorge", "Triglav National Park", "Bled Castle viewpoint"],
        "budget_tip": "Stay slightly outside Bled and use buses where possible.",
        "avoid_if": "Avoid if you want nightlife or very cheap food every day.",
        "cheaper": "Tatra Mountains", "similar": "Interlaken",
        "image": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1600&q=80",
    },
    {
        "name": "Valencia", "country": "Spain", "region": "Europe", "budget": "Medium",
        "vibes": ["Beach", "City", "Food", "Relaxing"],
        "trip_lengths": ["Weekend", "3–5 days", "1 week"], "difficulty": "Easy",
        "best_months": "April–June, September–October", "estimate": "£350–£700", "daily_spend": "£45–£85/day",
        "why": "Valencia gives you city, beach, food and sunshine in one trip, often feeling better value than Barcelona.",
        "things": ["City of Arts and Sciences", "Old Town", "Malvarrosa Beach", "Paella"],
        "budget_tip": "Travel outside peak summer and use local lunch menus for cheaper meals.",
        "avoid_if": "Avoid if you want mountain hiking as your main focus.",
        "cheaper": "Alicante", "similar": "Barcelona",
        "image": "https://images.unsplash.com/photo-1583422409516-2895a77efded?auto=format&fit=crop&w=1600&q=80",
    },
]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.block-container { max-width: 1180px; padding-top: 1.1rem; padding-bottom: 3rem; }
#MainMenu, footer, header { visibility: hidden; }
.qa-nav { display:flex; align-items:center; justify-content:space-between; gap:16px; padding: 12px 4px 18px 4px; }
.qa-logo { font-weight: 950; font-size: 1.45rem; letter-spacing: -0.04em; color: #0f172a; }
.qa-nav-links { display:flex; gap:10px; flex-wrap:wrap; }
.qa-nav-chip { padding: 8px 12px; border-radius: 999px; background:#f8fafc; border:1px solid #e2e8f0; color:#334155; font-weight:700; font-size:.88rem; }
.qa-hero { position: relative; overflow: hidden; border-radius: 34px; padding: 54px 44px; margin-bottom: 26px; background: radial-gradient(circle at top left, rgba(255,183,3,.35), transparent 34%), linear-gradient(135deg, rgba(15,23,42,.96), rgba(30,41,59,.92)), url('https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=1800&q=80'); background-size: cover; background-position: center; color: white; box-shadow: 0 25px 65px rgba(15, 23, 42, 0.24); }
.qa-hero h1 { font-size: clamp(2.7rem, 5.7vw, 5.6rem); line-height: .92; margin: 0 0 16px; font-weight: 950; letter-spacing: -0.075em; }
.qa-hero p { max-width: 780px; font-size: 1.16rem; color:#e2e8f0; line-height:1.65; }
.qa-pills { display:flex; gap:10px; flex-wrap:wrap; margin-top:24px; }
.qa-pill { display:inline-flex; gap:8px; align-items:center; padding:9px 14px; border-radius:999px; background:rgba(255,255,255,.12); border:1px solid rgba(255,255,255,.18); color:#fff; font-weight:800; font-size:.92rem; }
.qa-card { background:#ffffff; border:1px solid #e2e8f0; border-radius: 26px; padding:24px; box-shadow: 0 16px 45px rgba(15,23,42,.08); }
.qa-section-title { font-size: 1.75rem; font-weight: 950; letter-spacing:-.045em; color:#0f172a; margin: 2px 0 8px 0; }
.qa-muted { color:#64748b; line-height:1.6; }
div.stButton > button { background: linear-gradient(135deg, #ffb703, #fb8500) !important; color: #111827 !important; font-weight: 950 !important; border: 0 !important; border-radius: 999px !important; padding: .85rem 1rem !important; box-shadow: 0 12px 24px rgba(251, 133, 0, .24); }
.qa-spinner-box { text-align:center; padding: 34px 24px; border-radius: 28px; background: radial-gradient(circle at center, #ffffff, #eef6ff); border:1px solid #dbeafe; box-shadow: 0 16px 42px rgba(15,23,42,.08); }
.qa-spinner { display:inline-block; font-size:5.2rem; animation: spin 0.38s linear infinite; filter: drop-shadow(0 16px 18px rgba(15,23,42,.22)); margin-bottom: 8px; }
@keyframes spin { from { transform: rotate(0deg) scale(1); } 50% { transform: rotate(180deg) scale(1.08); } to { transform: rotate(360deg) scale(1); } }
.qa-result { overflow:hidden; border-radius: 34px; background:white; border:1px solid #e2e8f0; box-shadow: 0 26px 70px rgba(15,23,42,.16); margin-top: 18px; padding: 18px; }
.qa-result-img { min-height: 380px; border-radius: 28px; background-size: cover; background-position: center; position:relative; overflow:hidden; }
.qa-result-img::after { content:""; position:absolute; inset:0; background:linear-gradient(180deg, rgba(15,23,42,.04), rgba(15,23,42,.52)); }
.qa-result-body { padding: 12px 10px; }
.qa-destination { font-size: clamp(2.25rem, 4.2vw, 4rem); line-height:.95; font-weight: 950; letter-spacing:-.075em; color:#0f172a; margin: 0; }
.qa-country { margin-top:8px; color:#64748b; font-weight:700; font-size:1.05rem; }
.qa-badge { display:inline-flex; padding:7px 11px; border-radius:999px; background:#f1f5f9; border:1px solid #e2e8f0; color:#0f172a; font-size:.86rem; font-weight:800; margin: 6px 6px 0 0; }
.qa-score-box { margin:16px 0; padding:14px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:18px; }
.qa-score-label { display:flex; justify-content:space-between; gap:12px; margin-bottom:8px; color:#334155; font-weight:900; }
.qa-score-bg { height:12px; border-radius:999px; overflow:hidden; background:#e2e8f0; }
.qa-score-fill { height:12px; border-radius:999px; background: linear-gradient(90deg, #38bdf8, #22c55e); }
.qa-grid-3 { display:grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap:12px; margin: 16px 0; }
.qa-mini { background:#f8fafc; border:1px solid #e2e8f0; border-radius:18px; padding:14px; }
.qa-mini strong { display:block; color:#0f172a; margin-bottom:4px; }
.qa-mini span { color:#64748b; font-size:.92rem; }
.qa-affiliate { margin-top:18px; padding:20px; border-radius:24px; background: radial-gradient(circle at top right, rgba(255,183,3,.22), transparent 30%), linear-gradient(135deg,#fff7ed,#ffffff); border:1px solid #fed7aa; }
.qa-affiliate-title { font-weight:950; color:#0f172a; font-size:1.15rem; margin-bottom:5px; }
.qa-aff-grid { display:grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap:10px; margin-top:14px; }
.qa-aff-link { display:block; text-decoration:none !important; color:#0f172a !important; background:#fff; border:1px solid #e2e8f0; border-radius:18px; padding:13px; font-weight:900; box-shadow:0 8px 20px rgba(15,23,42,.06); }
.qa-aff-link span { display:block; color:#64748b; font-size:.78rem; font-weight:700; margin-top:3px; }
.qa-ad { margin: 22px 0; padding: 26px; border: 1px dashed #94a3b8; background:#f8fafc; border-radius:22px; text-align:center; color:#64748b; font-weight:850; }
.qa-feature { background:#ffffff; border:1px solid #e2e8f0; border-radius:22px; padding:20px; height:100%; box-shadow:0 10px 28px rgba(15,23,42,.05); }
.qa-feature b { color:#0f172a; font-size:1.05rem; }
.qa-footer { text-align:center; color:#64748b; margin-top:38px; padding-top:20px; border-top:1px solid #e2e8f0; font-size:.9rem; line-height:1.7; }
@media(max-width: 900px) { .qa-hero { padding:34px 24px; border-radius:25px; } .qa-grid-3, .qa-aff-grid { grid-template-columns: 1fr; } .qa-result-img { min-height:260px; } }
</style>
""", unsafe_allow_html=True)


def affiliate_url(kind, place):
    q = quote_plus(f"{place['name']} {place['country']}")
    city = quote_plus(place["name"])
    fake_partner = "quidaway-demo"
    if kind == "stays":
        return f"https://example-affiliate.com/hotels/search?destination={q}&partner={fake_partner}&subid=quidaway_result"
    if kind == "flights":
        return f"https://example-affiliate.com/flights/search?to={city}&partner={fake_partner}&subid=quidaway_result"
    if kind == "activities":
        return f"https://example-affiliate.com/activities/search?q={q}&partner={fake_partner}&subid=quidaway_result"
    if kind == "insurance":
        return f"https://example-affiliate.com/travel-insurance?destination={q}&partner={fake_partner}&subid=quidaway_result"
    return "#"


def calc_score(place, region, budget, vibe, trip_length, difficulty):
    score = 35
    if region == "Surprise me" or place["region"] == region:
        score += 16
    if budget == "Any" or place["budget"] == budget:
        score += 20
    elif budget == "Low" and place["budget"] == "Medium":
        score += 8
    elif budget == "Medium" and place["budget"] in ["Low", "High"]:
        score += 8
    if vibe == "Surprise me" or vibe in place["vibes"]:
        score += 20
    if trip_length == "Flexible" or trip_length in place["trip_lengths"]:
        score += 12
    if difficulty == "Any" or difficulty == place["difficulty"]:
        score += 7
    return min(score, 99)


def pick_destination(region, budget, vibe, trip_length, difficulty):
    scored = [(calc_score(p, region, budget, vibe, trip_length, difficulty), p) for p in DESTINATIONS]
    scored = sorted(scored, key=lambda x: x[0], reverse=True)
    top_pool = [x for x in scored if x[0] >= 60] or scored[:5]
    score, place = random.choice(top_pool[:5])
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
    st.markdown(f"""
        <div class="qa-affiliate">
            <div class="qa-affiliate-title">When you are ready, check live options</div>
            <div class="qa-muted">
                Dummy affiliate layout. In WordPress, these would be Travelpayouts / Booking / Skyscanner / Expedia / GetYourGuide style links.
                The main value of QuidAway is helping people decide first — booking links come after the recommendation.
            </div>
            <div class="qa-aff-grid">
                <a class="qa-aff-link" href="{stays}" target="_blank" rel="sponsored noopener">🏨 Check stays<span>Demo hotel affiliate link</span></a>
                <a class="qa-aff-link" href="{flights}" target="_blank" rel="sponsored noopener">✈️ Compare flights<span>Demo flight affiliate link</span></a>
                <a class="qa-aff-link" href="{activities}" target="_blank" rel="sponsored noopener">🎟️ Things to do<span>Demo activity affiliate link</span></a>
                <a class="qa-aff-link" href="{insurance}" target="_blank" rel="sponsored noopener">🛡️ Travel cover<span>Demo insurance affiliate link</span></a>
            </div>
            <p class="qa-muted" style="font-size:.84rem;margin-top:12px;">Affiliate disclosure: some links may earn QuidAway a commission at no extra cost to the visitor.</p>
        </div>
    """, unsafe_allow_html=True)


def render_result(place, score, scored):
    col_img, col_text = st.columns([0.95, 1.05], gap="large")
    with col_img:
        st.markdown(f"<div class='qa-result-img' style=\"background-image:url('{place['image']}')\"></div>", unsafe_allow_html=True)
    with col_text:
        st.markdown(f"""
            <div class="qa-result-body">
            <h2 class="qa-destination">{place['name']}</h2>
            <div class="qa-country">{place['country']} · {place['region']}</div>
            <div>{''.join([f"<span class='qa-badge'>{v}</span>" for v in place['vibes'][:5]])}</div>
            {score_bar('QuidAway match score', score)}
            <div class="qa-grid-3">
                <div class="qa-mini"><strong>Budget range</strong><span>{place['estimate']}</span></div>
                <div class="qa-mini"><strong>Daily spend</strong><span>{place['daily_spend']}</span></div>
                <div class="qa-mini"><strong>Best time</strong><span>{place['best_months']}</span></div>
            </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"**Why this fits:** {place['why']}")
        st.markdown(f"**Budget tip:** {place['budget_tip']}")
        st.markdown(f"**Avoid if:** {place['avoid_if']}")
        st.markdown("**Things to consider:**")
        for thing in place["things"]:
            st.markdown(f"- {thing}")
        render_affiliate_block(place)
    st.markdown("### More decision help")
    a, b, c = st.columns(3)
    a.info(f"**Cheaper alternative:** {place['cheaper']}")
    b.info(f"**Similar vibe:** {place['similar']}")
    another = scored[1][1]["name"] if len(scored) > 1 else place["similar"]
    c.info(f"**Another strong match:** {another}")


st.markdown("""
<div class="qa-nav">
    <div class="qa-logo">🌍 QuidAway</div>
    <div class="qa-nav-links">
        <span class="qa-nav-chip">Budget escapes</span>
        <span class="qa-nav-chip">Hiking</span>
        <span class="qa-nav-chip">City breaks</span>
        <span class="qa-nav-chip">Worldwide</span>
    </div>
</div>
<div class="qa-hero">
    <h1>Can’t decide where to go?</h1>
    <p>QuidAway is a budget escape decision-maker. Choose your budget, vibe and trip length, then get a sensible travel idea with a match score, budget estimate, alternatives and optional live-price links.</p>
    <div class="qa-pills">
        <span class="qa-pill">💸 Budget-first</span>
        <span class="qa-pill">🥾 Hiking & nature</span>
        <span class="qa-pill">🎲 Randomised result</span>
        <span class="qa-pill">🔗 Affiliate-ready</span>
    </div>
</div>
""", unsafe_allow_html=True)

intro_left, intro_right = st.columns([1.25, 0.75], gap="large")
with intro_left:
    st.markdown('<div class="qa-section-title">A decision tool, not a booking site</div>', unsafe_allow_html=True)
    st.markdown('<p class="qa-muted">Visitors use QuidAway because they do not know where to go yet. The tool helps them decide by matching their budget, vibe and travel style. Affiliate links are shown only after the destination has been explained.</p>', unsafe_allow_html=True)
with intro_right:
    m1, m2 = st.columns(2)
    m1.metric("Demo destinations", len(DESTINATIONS))
    m2.metric("Prototype goal", "Feedback")

st.markdown('<div class="qa-card">', unsafe_allow_html=True)
st.markdown("## Find my escape")
with st.form("quidaway_form"):
    c1, c2, c3 = st.columns(3)
    with c1:
        budget = st.selectbox("Budget level", ["Low", "Medium", "High", "Any"], index=1)
        region = st.selectbox("Where?", ["Europe", "UK", "Worldwide", "Surprise me"], index=0)
    with c2:
        vibe = st.selectbox("Travel vibe", ["Hiking", "Nature", "Beach", "City", "Food", "Culture", "Adventure", "Relaxing", "Budget", "Warm Weather", "Surprise me"], index=0)
        trip_length = st.selectbox("Trip length", ["Weekend", "3–5 days", "1 week", "2 weeks", "Flexible"], index=1)
    with c3:
        difficulty = st.selectbox("Activity level", ["Easy", "Moderate", "Challenging", "Any"], index=3)
        starting_from = st.text_input("Starting from", value="London")
    submitted = st.form_submit_button("🌍 Spin my escape", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

if "result" not in st.session_state:
    st.session_state["result"] = None

if submitted:
    placeholder = st.empty()
    with placeholder:
        st.markdown("""
        <div class="qa-spinner-box">
            <div class="qa-spinner">🌍</div>
            <h3>Finding your QuidAway match...</h3>
            <p class="qa-muted">Checking budget fit · comparing vibe · finding cheaper alternatives</p>
        </div>
        """, unsafe_allow_html=True)
    time.sleep(1.8)
    placeholder.empty()
    place, score, scored = pick_destination(region, budget, vibe, trip_length, difficulty)
    st.session_state["result"] = {"place": place, "score": score, "scored": scored, "starting_from": starting_from}

if st.session_state["result"]:
    st.markdown("## Your result")
    st.markdown('<div class="qa-result">', unsafe_allow_html=True)
    render_result(st.session_state["result"]["place"], st.session_state["result"]["score"], st.session_state["result"]["scored"])
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="qa-ad">AdSense placeholder — in WordPress this could be inserted using Google Site Kit or an ad inserter plugin after approval.</div>', unsafe_allow_html=True)

st.markdown("## Unique features to make QuidAway different")
f1, f2, f3 = st.columns(3)
with f1:
    st.markdown('<div class="qa-feature"><b>Smart alternatives</b><br><br>Not just one destination. Show cheaper, similar and easier alternatives so users can compare quickly.</div>', unsafe_allow_html=True)
with f2:
    st.markdown('<div class="qa-feature"><b>Honest “avoid if” tips</b><br><br>Most travel sites sell everything. QuidAway can feel more trustworthy by saying who a place is not for.</div>', unsafe_allow_html=True)
with f3:
    st.markdown('<div class="qa-feature"><b>Budget fit score</b><br><br>Give a clear match score using budget, vibe, region, trip length and activity level.</div>', unsafe_allow_html=True)

st.markdown("## How this can work in WordPress")
wp1, wp2 = st.columns(2)
with wp1:
    st.markdown("""
**Simple WordPress setup**
- WordPress + Kadence/Astra theme
- Custom HTML/JavaScript block for the spinner tool
- Travelpayouts/Booking/Skyscanner affiliate links or widgets
- Google Site Kit or Ad Inserter for AdSense
- RankMath for SEO pages
""")
with wp2:
    st.markdown("""
**Later expansion**
- Save destinations using browser storage first
- User login later with Ultimate Member/ProfileGrid
- User submitted routes with WP User Frontend
- Destination pages for SEO
- Google Sheets/Airtable as destination database
""")

st.markdown('<div class="qa-footer">Prototype only. Budget ranges are examples, not live prices. Affiliate buttons are dummy links for design feedback. The final website should include Privacy Policy, Affiliate Disclosure, Terms/Disclaimer and manually reviewed destination data.</div>', unsafe_allow_html=True)
