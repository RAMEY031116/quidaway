import random
import time
from datetime import datetime
from urllib.parse import quote_plus

import streamlit as st


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="QuidAway | Budget Escape Decision Maker",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

APP_VERSION = "quidaway-fake-live-prices-v1"
if st.session_state.get("app_version") != APP_VERSION:
    st.session_state["app_version"] = APP_VERSION
    st.session_state["result"] = None


# =========================================================
# DESTINATION DATA
# Static destination data + fake live pricing demo
# In WordPress this would be stored in ACF / CPT fields.
# =========================================================
DESTINATIONS = [
    {
        "name": "Madeira",
        "country": "Portugal",
        "iata": "FNC",
        "region": "Europe",
        "budget_band": "££",
        "primary_vibe": "Hiking",
        "secondary_vibes": ["Nature", "Coastal views", "Warm escape"],
        "trip_lengths": ["3–5 days", "1 week"],
        "difficulty": "Moderate",
        "best_months": "March–June, September–November",
        "budget_confidence": "High",
        "daily_spend": "£45–£80/day",
        "fake_flight_from": 78,
        "fake_stay_from": 42,
        "fake_package_from": 389,
        "summary": "A warm island escape with dramatic hikes, levada walks and ocean views.",
        "why": "Madeira fits people who want adventure, views and sunshine without needing a luxury resort trip.",
        "good_to_know": "It is hilly and some routes are easier with tours or car hire.",
        "things": ["Pico do Arieiro sunrise", "Fanal Forest", "Levada walks", "Funchal old town"],
        "tip": "Stay in guesthouses or apartments outside peak school holidays.",
        "avoid": "Avoid if you dislike hills, winding roads or walking-heavy trips.",
        "cheaper": "Albania",
        "similar": "Tenerife",
        "image": "https://images.unsplash.com/photo-1513735492246-483525079686?auto=format&fit=crop&w=1600&q=80",
    },
    {
        "name": "Krakow",
        "country": "Poland",
        "iata": "KRK",
        "region": "Europe",
        "budget_band": "£",
        "primary_vibe": "City",
        "secondary_vibes": ["Food", "Culture", "Low-cost break"],
        "trip_lengths": ["Weekend", "3–5 days"],
        "difficulty": "Easy",
        "best_months": "April–June, September–December",
        "budget_confidence": "High",
        "daily_spend": "£30–£60/day",
        "fake_flight_from": 34,
        "fake_stay_from": 28,
        "fake_package_from": 219,
        "summary": "A low-cost city break with food, culture, history and walkable streets.",
        "why": "Krakow works well if you want a proper European city feeling without spending too much.",
        "good_to_know": "Better for culture and food than beaches or hiking.",
        "things": ["Old Town", "Kazimierz", "Wieliczka Salt Mine", "Local pierogi spots"],
        "tip": "Eat at traditional Milk Bars for hearty meals without spending much.",
        "avoid": "Avoid if you mainly want beaches or guaranteed warm weather.",
        "cheaper": "Wroclaw",
        "similar": "Prague",
        "image": "https://images.unsplash.com/photo-1607427293702-036933bbf746?auto=format&fit=crop&w=1600&q=80",
    },
    {
        "name": "Porto",
        "country": "Portugal",
        "iata": "OPO",
        "region": "Europe",
        "budget_band": "££",
        "primary_vibe": "Food",
        "secondary_vibes": ["City", "Culture", "Relaxed break"],
        "trip_lengths": ["Weekend", "3–5 days"],
        "difficulty": "Easy",
        "best_months": "April–June, September–October",
        "budget_confidence": "Medium",
        "daily_spend": "£40–£75/day",
        "fake_flight_from": 49,
        "fake_stay_from": 39,
        "fake_package_from": 279,
        "summary": "A relaxed city break with food, riverside views and culture.",
        "why": "Porto is compact and atmospheric, with a good balance of value, food and scenery.",
        "good_to_know": "There are hills and steps, but it is still easy to enjoy over a long weekend.",
        "things": ["Ribeira", "Dom Luís I Bridge", "Douro Valley day trip", "Francesinha"],
        "tip": "Stay across the river in Vila Nova de Gaia or slightly outside the centre.",
        "avoid": "Avoid if you want beaches directly in the city or heavy nightlife.",
        "cheaper": "Krakow",
        "similar": "Lisbon",
        "image": "https://images.unsplash.com/photo-1555881400-74d7acaacd8b?auto=format&fit=crop&w=1600&q=80",
    },
    {
        "name": "Albanian Riviera",
        "country": "Albania",
        "iata": "TIA",
        "region": "Europe",
        "budget_band": "£",
        "primary_vibe": "Beach",
        "secondary_vibes": ["Adventure", "Value", "Coastal road trip"],
        "trip_lengths": ["1 week", "2 weeks"],
        "difficulty": "Moderate",
        "best_months": "May–June, September",
        "budget_confidence": "Low",
        "daily_spend": "£30–£65/day",
        "fake_flight_from": 89,
        "fake_stay_from": 25,
        "fake_package_from": 349,
        "summary": "A budget-friendly beach and adventure route with clear water and coastal towns.",
        "why": "It gives Mediterranean-style views at a more budget-friendly level than many popular beach destinations.",
        "good_to_know": "Transport planning matters, especially if moving between towns.",
        "things": ["Ksamil", "Himare", "Llogara Pass", "Gjirokaster"],
        "tip": "Avoid August and compare guesthouses instead of resorts.",
        "avoid": "Avoid if you want everything polished, predictable or resort-style.",
        "cheaper": "Montenegro coast",
        "similar": "Croatia",
        "image": "https://images.unsplash.com/photo-1621178727374-3793b75310bc?auto=format&fit=crop&w=1600&q=80",
    },
    {
        "name": "Snowdonia",
        "country": "Wales, UK",
        "iata": "MAN",
        "region": "UK",
        "budget_band": "£",
        "primary_vibe": "Hiking",
        "secondary_vibes": ["Nature", "Mountains", "Weekend"],
        "trip_lengths": ["Weekend", "3–5 days"],
        "difficulty": "Moderate",
        "best_months": "May–September",
        "budget_confidence": "High",
        "daily_spend": "£25–£60/day",
        "fake_flight_from": 0,
        "fake_stay_from": 31,
        "fake_package_from": 149,
        "summary": "A proper UK mountain escape for hiking, lakes and budget adventure.",
        "why": "Snowdonia is a strong option if you want a scenic trip without paying for flights.",
        "good_to_know": "Weather can change quickly, so pack sensible layers and waterproofs.",
        "things": ["Yr Wyddfa / Snowdon", "Llanberis", "Waterfalls and lakes", "Betws-y-Coed"],
        "tip": "Use hostels, campsites or shared stays and avoid peak summer weekends.",
        "avoid": "Avoid if you want guaranteed sun or a city-style break.",
        "cheaper": "Peak District",
        "similar": "Lake District",
        "image": "https://images.unsplash.com/photo-1598273372691-287a7d2dd8b4?auto=format&fit=crop&w=1600&q=80",
    },
    {
        "name": "Valencia",
        "country": "Spain",
        "iata": "VLC",
        "region": "Europe",
        "budget_band": "££",
        "primary_vibe": "Beach",
        "secondary_vibes": ["City", "Food", "Sun"],
        "trip_lengths": ["Weekend", "3–5 days", "1 week"],
        "difficulty": "Easy",
        "best_months": "April–June, September–October",
        "budget_confidence": "Medium",
        "daily_spend": "£45–£85/day",
        "fake_flight_from": 55,
        "fake_stay_from": 45,
        "fake_package_from": 319,
        "summary": "A city-and-beach combo with food, sunshine and a relaxed pace.",
        "why": "Valencia is a good compromise between beach, city and food without defaulting to Barcelona.",
        "good_to_know": "Better for relaxed beach-city travel than mountain adventure.",
        "things": ["City of Arts and Sciences", "Old Town", "Malvarrosa Beach", "Paella"],
        "tip": "Travel outside peak summer and use local lunch menus.",
        "avoid": "Avoid if hiking or mountains are your main focus.",
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

:root {
  --bg:#f6f8fb;
  --card:#ffffff;
  --card2:#f8fafc;
  --text:#102033;
  --muted:#526173;
  --border:#d9e3ef;
  --primary:#0f766e;
  --primary2:#115e59;
  --shadow:rgba(15,23,42,.10);
  --chip:#eef6f3;
  --chiptext:#0f766e;
  --warning:#fff7df;
  --blue:#2563eb;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg:#0b1120;
    --card:#111827;
    --card2:#172033;
    --text:#f8fafc;
    --muted:#cbd5e1;
    --border:#334155;
    --primary:#14b8a6;
    --primary2:#0d9488;
    --shadow:rgba(0,0,0,.35);
    --chip:#083f3a;
    --chiptext:#99f6e4;
    --warning:#2a210b;
    --blue:#60a5fa;
  }
}

html, body, [class*="css"] { font-family:'Inter', sans-serif; }
[data-testid="stAppViewContainer"] { background:var(--bg); color:var(--text); }
.block-container { max-width:1160px; padding-top:1rem; padding-bottom:3rem; }
#MainMenu, footer, header { visibility:hidden; }

h1,h2,h3,h4,h5,h6,p,li,label,span,div { color:inherit; }
label, .stSelectbox label, .stTextInput label {
  color:var(--text)!important;
  font-weight:800!important;
}
div[data-baseweb="select"]>div, input {
  background-color:var(--card)!important;
  color:var(--text)!important;
  border-color:var(--border)!important;
}
div[data-baseweb="select"] span { color:var(--text)!important; }

.qa-nav {
  display:flex;
  justify-content:space-between;
  align-items:center;
  gap:16px;
  padding:10px 4px 18px;
}
.qa-logo {
  color:var(--text);
  font-size:1.45rem;
  font-weight:950;
  letter-spacing:-.045em;
}
.qa-nav-links { display:flex; flex-wrap:wrap; gap:10px; }
.qa-nav-chip {
  background:var(--card);
  border:1px solid var(--border);
  color:var(--text);
  padding:8px 12px;
  border-radius:999px;
  font-size:.88rem;
  font-weight:800;
}

.qa-hero {
  border-radius:32px;
  padding:52px 44px;
  margin-bottom:26px;
  color:#fff;
  background:
    linear-gradient(135deg,rgba(5,10,20,.88),rgba(20,45,65,.80)),
    url('https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1800&q=80');
  background-size:cover;
  background-position:center;
  box-shadow:0 24px 60px var(--shadow);
}
.qa-hero h1 {
  color:#fff;
  font-size:clamp(2.55rem,5.3vw,5.1rem);
  line-height:.96;
  margin:0 0 16px;
  font-weight:950;
  letter-spacing:-.07em;
}
.qa-hero p {
  color:#e6eef8;
  max-width:820px;
  font-size:1.16rem;
  line-height:1.66;
}
.qa-pills { display:flex; gap:10px; flex-wrap:wrap; margin-top:24px; }
.qa-pill {
  color:#fff;
  display:inline-flex;
  padding:9px 14px;
  border-radius:999px;
  background:rgba(255,255,255,.14);
  border:1px solid rgba(255,255,255,.24);
  font-weight:850;
}

.qa-card,.qa-result,.qa-panel,.qa-ad {
  background:var(--card);
  border:1px solid var(--border);
  color:var(--text);
}
.qa-card {
  border-radius:26px;
  padding:24px;
  box-shadow:0 16px 42px var(--shadow);
}
.qa-muted { color:var(--muted); line-height:1.62; }

div.stButton>button {
  background:var(--primary)!important;
  color:#fff!important;
  font-weight:950!important;
  border:0!important;
  border-radius:999px!important;
  padding:.85rem 1rem!important;
  box-shadow:0 12px 24px rgba(15,118,110,.20);
}
div.stButton>button:hover {
  background:var(--primary2)!important;
  transform:translateY(-1px);
}

.qa-spinner-box {
  text-align:center;
  padding:34px 24px;
  border-radius:28px;
  background:var(--card);
  color:var(--text);
  border:1px solid var(--border);
  box-shadow:0 16px 42px var(--shadow);
}
.qa-spinner {
  display:inline-block;
  font-size:5.2rem;
  animation:spin .42s linear infinite;
  margin-bottom:8px;
}
@keyframes spin {
  from { transform:rotate(0deg) scale(1); }
  50% { transform:rotate(180deg) scale(1.06); }
  to { transform:rotate(360deg) scale(1); }
}

.qa-result {
  overflow:hidden;
  border-radius:30px;
  box-shadow:0 24px 62px var(--shadow);
  margin-top:18px;
  padding:18px;
}
.qa-result-img {
  min-height:380px;
  border-radius:24px;
  background-size:cover;
  background-position:center;
}
.qa-result-body { padding:12px 8px 4px; color:var(--text); }
.qa-destination {
  color:var(--text);
  font-size:clamp(2.1rem,4.1vw,3.7rem);
  line-height:.98;
  font-weight:950;
  letter-spacing:-.065em;
  margin:0;
}
.qa-country {
  color:var(--muted);
  margin-top:8px;
  font-weight:750;
  font-size:1.05rem;
}
.qa-primary-badge {
  display:inline-flex;
  padding:8px 13px;
  border-radius:999px;
  background:var(--chip);
  color:var(--chiptext);
  border:1px solid var(--border);
  font-size:.9rem;
  font-weight:900;
  margin:12px 6px 2px 0;
}
.qa-tag {
  display:inline-flex;
  padding:7px 10px;
  border-radius:999px;
  background:var(--card2);
  border:1px solid var(--border);
  color:var(--text);
  font-size:.84rem;
  font-weight:800;
  margin:6px 6px 0 0;
}

.qa-score-wrapper { margin-top:1.5rem; margin-bottom:1.5rem; }
.qa-score-header {
  display:flex;
  align-items:center;
  gap:.75rem;
  margin-bottom:1rem;
}
.qa-score-label {
  font-size:.875rem;
  font-weight:800;
  color:var(--muted);
  text-transform:uppercase;
  letter-spacing:.05em;
}
.qa-score-track {
  flex-grow:1;
  background-color:var(--border);
  border-radius:9999px;
  height:.625rem;
}
.qa-score-fill {
  background:linear-gradient(90deg, var(--blue), #10b981);
  height:.625rem;
  border-radius:9999px;
}
.qa-score-value { font-weight:900; color:var(--blue); }

.qa-new-grid {
  display:grid;
  grid-template-columns:repeat(3,minmax(0,1fr));
  gap:1rem;
}
.qa-new-card {
  background:var(--card2);
  border:1px solid var(--border);
  border-radius:1rem;
  padding:1rem;
  text-align:center;
}
.qa-new-card strong {
  display:block;
  color:var(--text);
  margin-bottom:.25rem;
  font-size:.875rem;
}
.qa-new-card span.normal {
  color:var(--muted);
  font-weight:700;
}
.qa-new-card span.badge {
  display:inline-block;
  padding:.25rem .75rem;
  background:var(--warning);
  color:var(--text);
  border:1px solid var(--border);
  border-radius:9999px;
  font-size:.75rem;
  font-weight:900;
}

.qa-live-prices {
  margin-top:22px;
  padding:20px;
  border-radius:24px;
  background:var(--card2);
  border:1px solid var(--border);
}
.qa-live-head {
  display:flex;
  align-items:flex-start;
  justify-content:space-between;
  gap:14px;
  margin-bottom:14px;
}
.qa-live-head h3 {
  margin:0;
  color:var(--text);
  font-size:1.25rem;
}
.qa-live-head p {
  margin:.35rem 0 0;
  color:var(--muted);
}
.qa-live-pill {
  padding:7px 11px;
  border-radius:999px;
  border:1px solid var(--border);
  background:var(--card);
  color:var(--muted);
  font-size:.8rem;
  font-weight:850;
  white-space:nowrap;
}
.qa-price-grid {
  display:grid;
  grid-template-columns:repeat(3,minmax(0,1fr));
  gap:12px;
}
.qa-price-card {
  background:var(--card);
  border:1px solid var(--border);
  border-radius:18px;
  padding:16px;
}
.qa-price-card .provider {
  color:var(--muted);
  font-size:.82rem;
  font-weight:850;
}
.qa-price-card .price {
  color:var(--text);
  font-size:1.55rem;
  font-weight:950;
  margin:6px 0 4px;
}
.qa-price-card .desc {
  color:var(--muted);
  font-size:.88rem;
  min-height:36px;
}
.qa-price-card a {
  display:block;
  margin-top:12px;
  text-align:center;
  text-decoration:none!important;
  color:#fff!important;
  background:var(--primary);
  border-radius:999px;
  padding:10px 12px;
  font-weight:900;
}
.qa-price-card a.secondary {
  background:var(--blue);
}
.qa-disclosure {
  color:var(--muted);
  font-size:.82rem;
  line-height:1.55;
  margin-top:12px;
}
.qa-ad {
  margin:22px 0;
  padding:26px;
  border-style:dashed;
  border-radius:22px;
  text-align:center;
  color:var(--muted);
  font-weight:850;
}
.qa-panel {
  border-radius:22px;
  padding:20px;
  height:100%;
}
.qa-panel b { display:block; margin-bottom:8px; color:var(--text); }
.qa-footer {
  text-align:center;
  color:var(--muted);
  margin-top:38px;
  padding-top:20px;
  border-top:1px solid var(--border);
  font-size:.9rem;
  line-height:1.7;
}

@media(max-width:800px) {
  .qa-hero { padding:34px 24px; border-radius:25px; }
  .qa-new-grid, .qa-price-grid { grid-template-columns:1fr; }
  .qa-result-img { min-height:260px; }
  .qa-nav { align-items:flex-start; flex-direction:column; }
  .qa-live-head { flex-direction:column; }
}
</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# LOGIC
# =========================================================
def calc_score(place, region, budget, vibe, trip_length):
    score = 30

    if region == "Surprise me" or place["region"] == region:
        score += 20

    budget_map = {
        "£ (Shoestring)": "£",
        "££ (Moderate)": "££",
        "£££ (Comfort)": "£££",
        "Any": place["budget_band"],
    }
    target_band = budget_map.get(budget, "££")
    if target_band == place["budget_band"]:
        score += 25
    elif target_band == "£" and place["budget_band"] == "££":
        score += 10
    elif target_band == "££" and place["budget_band"] in ["£", "£££"]:
        score += 10

    if vibe == "Surprise me" or vibe == place["primary_vibe"] or vibe in place["secondary_vibes"]:
        score += 23

    if trip_length in place["trip_lengths"]:
        score += 12

    return min(score, 98)


def pick_destination(region, budget, vibe, trip_length):
    scored = [(calc_score(p, region, budget, vibe, trip_length), p) for p in DESTINATIONS]
    scored = sorted(scored, key=lambda x: x[0], reverse=True)
    top_pool = [x for x in scored if x[0] >= 65] or scored[:4]
    return random.choice(top_pool[:3]), scored


def fake_live_multiplier(trip_length):
    if trip_length == "Weekend":
        return 1.0
    if trip_length == "3–5 days":
        return 1.35
    if trip_length == "1 week":
        return 1.95
    if trip_length == "2 weeks":
        return 3.2
    return 1.25


def affiliate_url(provider, place, starting_from):
    destination = quote_plus(f"{place['name']} {place['country']}")
    origin = quote_plus(starting_from or "London")
    iata = quote_plus(place["iata"])
    partner = "quidaway-demo"

    if provider == "booking":
        return f"https://www.booking.com/searchresults.html?ss={destination}&aid={partner}"
    if provider == "skyscanner":
        return f"https://www.skyscanner.net/transport/flights/{origin}/{iata}/?associateid={partner}"
    if provider == "expedia":
        return f"https://www.expedia.co.uk/Hotel-Search?destination={destination}&affcid={partner}"
    if provider == "getyourguide":
        return f"https://www.getyourguide.co.uk/s/?q={destination}&partner_id={partner}"
    return "#"


# =========================================================
# RENDER FUNCTIONS
# =========================================================
def render_fake_live_prices(place, trip_length, starting_from):
    multiplier = fake_live_multiplier(trip_length)

    flight_from = place["fake_flight_from"]
    stay_from = int(place["fake_stay_from"] * multiplier)
    package_from = int(place["fake_package_from"] * multiplier)

    flight_label = "No flight needed" if flight_from == 0 else f"from £{flight_from}"
    stay_label = f"from £{stay_from}"
    package_label = f"from £{package_from}"

    st.markdown(
        f"""
<div class="qa-live-prices">
  <div class="qa-live-head">
    <div>
      <h3>Check live options</h3>
      <p>This is how the real site could show partner search cards. Demo prices are examples only — the buttons would send users to live partner searches.</p>
    </div>
    <div class="qa-live-pill">Demo refreshed: {datetime.now().strftime("%d %b %Y")}</div>
  </div>

  <div class="qa-price-grid">
    <div class="qa-price-card">
      <div class="provider">Skyscanner-style flights</div>
      <div class="price">{flight_label}</div>
      <div class="desc">Compare flights from {starting_from or "London"} to {place["iata"]}.</div>
      <a class="secondary" href="{affiliate_url("skyscanner", place, starting_from)}" target="_blank" rel="sponsored noopener">Compare flights</a>
    </div>

    <div class="qa-price-card">
      <div class="provider">Booking.com-style stays</div>
      <div class="price">{stay_label}</div>
      <div class="desc">Search stays in {place["name"]}. Price shown as demo nightly/guide style.</div>
      <a href="{affiliate_url("booking", place, starting_from)}" target="_blank" rel="sponsored noopener">Check stays</a>
    </div>

    <div class="qa-price-card">
      <div class="provider">Expedia-style package</div>
      <div class="price">{package_label}</div>
      <div class="desc">Demo package estimate for {trip_length.lower()} style planning.</div>
      <a href="{affiliate_url("expedia", place, starting_from)}" target="_blank" rel="sponsored noopener">View packages</a>
    </div>
  </div>

  <div class="qa-price-grid" style="margin-top:12px;">
    <div class="qa-price-card">
      <div class="provider">GetYourGuide-style activities</div>
      <div class="price">from £18</div>
      <div class="desc">Tours, viewpoints and activities related to this destination.</div>
      <a class="secondary" href="{affiliate_url("getyourguide", place, starting_from)}" target="_blank" rel="sponsored noopener">Find activities</a>
    </div>
    <div class="qa-price-card">
      <div class="provider">Budget confidence</div>
      <div class="price">{place["budget_confidence"]}</div>
      <div class="desc">How stable this destination usually feels for budget planning.</div>
      <a href="#" target="_self" rel="nofollow">Why this score?</a>
    </div>
    <div class="qa-price-card">
      <div class="provider">QuidAway note</div>
      <div class="price">{place["budget_band"]}</div>
      <div class="desc">Use this as planning guidance, then check live prices before booking.</div>
      <a href="#" target="_self" rel="nofollow">Save idea</a>
    </div>
  </div>

  <p class="qa-disclosure">
    Prototype disclosure: these are fake/demo price cards. In WordPress, these cards would become real affiliate widgets or deep links from Travelpayouts, Booking.com, Skyscanner, Expedia, GetYourGuide or similar. QuidAway should show budget guidance, not promise exact live prices.
  </p>
</div>
        """,
        unsafe_allow_html=True,
    )


def render_itinerary(place, trip_length):
    if trip_length == "Weekend":
        days = 2
    elif trip_length == "1 week":
        days = 5
    elif trip_length == "2 weeks":
        days = 7
    else:
        days = 3

    templates = []
    things = place["things"]

    for i in range(days):
        if i == 0:
            templates.append(["Arrive and settle in", things[-1], "Budget-friendly local dinner"])
        elif i == 1:
            templates.append([things[0], things[1], "Evening viewpoint or local walk"])
        elif i == 2:
            templates.append([things[2], "Local food stop", "Relaxed final evening"])
        elif i == days - 1:
            templates.append(["Slow morning", "Final photos", "Travel back"])
        else:
            templates.append(["Flexible day trip", "Local neighbourhood", "Cheap/free activity"])

    st.markdown("### Suggested route idea")
    cols = st.columns(min(3, days))
    for index, items in enumerate(templates):
        with cols[index % len(cols)]:
            bullet_html = "".join([f"<li>{item}</li>" for item in items])
            st.markdown(
                f"""
<div class="qa-panel">
  <b>Day {index + 1}</b>
  <ul>{bullet_html}</ul>
</div>
                """,
                unsafe_allow_html=True,
            )


def render_result(place, score, scored, trip_length, starting_from):
    st.markdown('<div class="qa-result">', unsafe_allow_html=True)
    col_img, col_text = st.columns([0.95, 1.05], gap="large")

    with col_img:
        st.markdown(
            f"<div class='qa-result-img' style=\"background-image:url('{place['image']}')\"></div>",
            unsafe_allow_html=True,
        )

    with col_text:
        tags = f"<span class='qa-primary-badge'>{place['primary_vibe']}</span>"
        tags += "".join([f"<span class='qa-tag'>{v}</span>" for v in place["secondary_vibes"][:3]])

        st.markdown(
            f"""
<div class="qa-result-body">
  <h2 class="qa-destination">{place['name']}</h2>
  <div class="qa-country">{place['country']} · IATA: {place['iata']}</div>
  <div>{tags}</div>

  <div class="qa-score-wrapper">
    <div class="qa-score-header">
      <span class="qa-score-label">Match Score</span>
      <div class="qa-score-track">
        <div class="qa-score-fill" style="width: {score}%"></div>
      </div>
      <span class="qa-score-value">{score}%</span>
    </div>

    <div class="qa-new-grid">
      <div class="qa-new-card">
        <strong>Budget Band</strong>
        <span class="normal">{place['budget_band']}</span>
      </div>
      <div class="qa-new-card">
        <strong>Est. Daily</strong>
        <span class="normal">{place['daily_spend']}</span>
      </div>
      <div class="qa-new-card">
        <strong>Pricing Confidence</strong>
        <span class="badge">{place['budget_confidence']}</span>
      </div>
    </div>
  </div>
</div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(f"**Quick decision:** {place['summary']}")
        st.markdown(f"**Why this works:** {place['why']}")
        st.markdown(f"**Good to know:** {place['good_to_know']}")
        st.markdown(f"**Budget tip:** {place['tip']}")
        st.warning(f"**Avoid if:** {place['avoid']}")

    st.markdown("</div>", unsafe_allow_html=True)

    render_fake_live_prices(place, trip_length, starting_from)

    st.markdown("### Not quite right?")
    a, b, c = st.columns(3)
    a.info(f"**Cheaper alternative:** {place['cheaper']}")
    b.info(f"**Similar vibe:** {place['similar']}")
    c.info(f"**Another option:** {scored[1][1]['name'] if len(scored) > 1 else place['similar']}")

    render_itinerary(place, trip_length)


# =========================================================
# MAIN APP LAYOUT
# =========================================================
st.markdown(
    """
<div class="qa-nav">
  <div class="qa-logo">🌍 QuidAway</div>
  <div class="qa-nav-links">
    <span class="qa-nav-chip">Budget-first</span>
    <span class="qa-nav-chip">Escape finder</span>
    <span class="qa-nav-chip">Fake live price demo</span>
    <span class="qa-nav-chip">WordPress-ready idea</span>
  </div>
</div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="qa-hero">
  <h1>Find your budget escape.</h1>
  <p>Tell us your budget band, travel vibe and trip length. QuidAway suggests where your money could go furthest, then shows how live partner searches would look on the real website.</p>
  <div>
    <span class="qa-pill">💸 Budget guidance</span>
    <span class="qa-pill">🌍 Destination decision-maker</span>
    <span class="qa-pill">🔗 Affiliate-ready layout</span>
    <span class="qa-pill">🧭 Route idea included</span>
  </div>
</div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="qa-card">', unsafe_allow_html=True)
st.markdown("## Where should you go?")

with st.form("quidaway_form"):
    c1, c2, c3 = st.columns(3)
    with c1:
        starting_from = st.text_input("Starting city", value="London")
        region = st.selectbox("Region", ["Europe", "UK", "Worldwide", "Surprise me"], index=0)
    with c2:
        budget = st.selectbox("Budget level", ["£ (Shoestring)", "££ (Moderate)", "£££ (Comfort)", "Any"], index=1)
        vibe = st.selectbox(
            "Travel vibe",
            ["City", "Beach", "Hiking", "Food", "Nature", "Culture", "Adventure", "Surprise me"],
            index=0,
        )
    with c3:
        trip_length = st.selectbox("Trip length", ["Weekend", "3–5 days", "1 week", "2 weeks"], index=1)
        st.markdown("<br>", unsafe_allow_html=True)

    submitted = st.form_submit_button("🌍 Find my escape", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

if submitted:
    placeholder = st.empty()
    with placeholder:
        st.markdown(
            """
<div class="qa-spinner-box">
  <div class="qa-spinner">🌍</div>
  <h3>Searching the globe...</h3>
  <p class="qa-muted">Matching budget · checking vibes · preparing fake live price cards</p>
</div>
            """,
            unsafe_allow_html=True,
        )
    time.sleep(1.2)
    placeholder.empty()

    (score, place), scored = pick_destination(region, budget, vibe, trip_length)
    st.session_state["result"] = {
        "place": place,
        "score": score,
        "scored": scored,
        "trip_length": trip_length,
        "starting_from": starting_from,
    }

if st.session_state.get("result"):
    st.markdown("## Your Match")
    render_result(
        st.session_state["result"]["place"],
        st.session_state["result"]["score"],
        st.session_state["result"]["scored"],
        st.session_state["result"]["trip_length"],
        st.session_state["result"]["starting_from"],
    )

st.markdown(
    """
<div class="qa-ad">
  AdSense placeholder — in the real WordPress site this could appear on SEO/destination pages, not necessarily inside the main tool.
</div>
    """,
    unsafe_allow_html=True,
)

st.markdown("## How this would become a real WordPress website")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(
        """
<div class="qa-panel">
  <b>1. Static destination data</b>
  Store destination name, airport code, budget band, vibe and route logic in WordPress ACF fields.
</div>
        """,
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        """
<div class="qa-panel">
  <b>2. Dynamic partner links</b>
  Use the destination name and IATA code to generate affiliate links/widgets automatically.
</div>
        """,
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        """
<div class="qa-panel">
  <b>3. No exact price promise</b>
  Show budget guidance and send users to partners for live prices.
</div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
<div class="qa-footer">
  QuidAway prototype. Fake live prices are visual examples only. Real website should use affiliate disclosure, privacy policy, terms/disclaimer and manually reviewed destination data.
</div>
    """,
    unsafe_allow_html=True,
)
