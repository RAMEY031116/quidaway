import random
import time
from datetime import datetime
from urllib.parse import quote_plus

import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium


st.set_page_config(
    page_title="QuidAway | Budget Escape Finder",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

APP_VERSION = "complete-mvp-map-v1"
if st.session_state.get("app_version") != APP_VERSION:
    st.session_state["app_version"] = APP_VERSION
    st.session_state["result"] = None


# =========================================================
# DESTINATION DATA
# In WordPress production, this becomes destination posts + ACF fields.
# =========================================================
DESTINATIONS = [
    {
        "name": "Porto",
        "country": "Portugal",
        "region": "Europe",
        "iata": "OPO",
        "lat": 41.1579,
        "lon": -8.6291,
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
        "tip": "Stay across the river in Vila Nova de Gaia or slightly outside the centre.",
        "avoid": "Avoid if you want beaches directly in the city or heavy nightlife.",
        "cheaper": "Krakow",
        "similar": "Lisbon",
        "image": "https://images.unsplash.com/photo-1555881400-74d7acaacd8b?auto=format&fit=crop&w=1400&q=80",
        "attractions": [
            {"name": "Ribeira", "type": "Old town / riverside", "lat": 41.1406, "lon": -8.6110},
            {"name": "Dom Luís I Bridge", "type": "Viewpoint", "lat": 41.1402, "lon": -8.6096},
            {"name": "Livraria Lello", "type": "Culture", "lat": 41.1469, "lon": -8.6147},
            {"name": "Vila Nova de Gaia", "type": "Stay area / river views", "lat": 41.1336, "lon": -8.6174},
        ],
    },
    {
        "name": "Madeira",
        "country": "Portugal",
        "region": "Europe",
        "iata": "FNC",
        "lat": 32.7607,
        "lon": -16.9595,
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
        "tip": "Stay in guesthouses or apartments outside peak school holidays.",
        "avoid": "Avoid if you dislike hills, winding roads or walking-heavy trips.",
        "cheaper": "Albania",
        "similar": "Tenerife",
        "image": "https://images.unsplash.com/photo-1513735492246-483525079686?auto=format&fit=crop&w=1400&q=80",
        "attractions": [
            {"name": "Pico do Arieiro", "type": "Mountain viewpoint", "lat": 32.7350, "lon": -16.9287},
            {"name": "Fanal Forest", "type": "Nature / forest", "lat": 32.8126, "lon": -17.1457},
            {"name": "Funchal Old Town", "type": "City base", "lat": 32.6480, "lon": -16.9080},
            {"name": "Levada Walk Area", "type": "Hiking", "lat": 32.7455, "lon": -16.9702},
        ],
    },
    {
        "name": "Krakow",
        "country": "Poland",
        "region": "Europe",
        "iata": "KRK",
        "lat": 50.0647,
        "lon": 19.9450,
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
        "tip": "Eat at traditional Milk Bars for hearty meals without spending much.",
        "avoid": "Avoid if you mainly want beaches or guaranteed warm weather.",
        "cheaper": "Wroclaw",
        "similar": "Prague",
        "image": "https://images.unsplash.com/photo-1607427293702-036933bbf746?auto=format&fit=crop&w=1400&q=80",
        "attractions": [
            {"name": "Main Market Square", "type": "Old town", "lat": 50.0617, "lon": 19.9373},
            {"name": "Kazimierz", "type": "Food / culture", "lat": 50.0516, "lon": 19.9449},
            {"name": "Wawel Castle", "type": "Historic site", "lat": 50.0540, "lon": 19.9353},
            {"name": "Wieliczka Salt Mine", "type": "Day trip", "lat": 49.9876, "lon": 20.0648},
        ],
    },
    {
        "name": "Valencia",
        "country": "Spain",
        "region": "Europe",
        "iata": "VLC",
        "lat": 39.4699,
        "lon": -0.3763,
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
        "tip": "Travel outside peak summer and use local lunch menus.",
        "avoid": "Avoid if hiking or mountains are your main focus.",
        "cheaper": "Alicante",
        "similar": "Barcelona",
        "image": "https://images.unsplash.com/photo-1583422409516-2895a77efded?auto=format&fit=crop&w=1400&q=80",
        "attractions": [
            {"name": "City of Arts and Sciences", "type": "Landmark", "lat": 39.4549, "lon": -0.3505},
            {"name": "Valencia Old Town", "type": "Culture", "lat": 39.4744, "lon": -0.3765},
            {"name": "Malvarrosa Beach", "type": "Beach", "lat": 39.4793, "lon": -0.3244},
            {"name": "Central Market", "type": "Food", "lat": 39.4736, "lon": -0.3794},
        ],
    },
    {
        "name": "Snowdonia",
        "country": "Wales, UK",
        "region": "UK",
        "iata": "MAN",
        "lat": 53.0685,
        "lon": -4.0763,
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
        "tip": "Use hostels, campsites or shared stays and avoid peak summer weekends.",
        "avoid": "Avoid if you want guaranteed sun or a city-style break.",
        "cheaper": "Peak District",
        "similar": "Lake District",
        "image": "https://images.unsplash.com/photo-1598273372691-287a7d2dd8b4?auto=format&fit=crop&w=1400&q=80",
        "attractions": [
            {"name": "Yr Wyddfa / Snowdon", "type": "Mountain hike", "lat": 53.0685, "lon": -4.0763},
            {"name": "Llanberis", "type": "Base town", "lat": 53.1180, "lon": -4.1291},
            {"name": "Betws-y-Coed", "type": "Village / stay area", "lat": 53.0931, "lon": -3.8015},
            {"name": "Swallow Falls", "type": "Waterfall", "lat": 53.1012, "lon": -3.8460},
        ],
    },
    {
        "name": "Albanian Riviera",
        "country": "Albania",
        "region": "Europe",
        "iata": "TIA",
        "lat": 40.1017,
        "lon": 19.7448,
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
        "tip": "Avoid August and compare guesthouses instead of resorts.",
        "avoid": "Avoid if you want everything polished, predictable or resort-style.",
        "cheaper": "Montenegro coast",
        "similar": "Croatia",
        "image": "https://images.unsplash.com/photo-1621178727374-3793b75310bc?auto=format&fit=crop&w=1400&q=80",
        "attractions": [
            {"name": "Ksamil", "type": "Beach", "lat": 39.7689, "lon": 20.0054},
            {"name": "Himare", "type": "Beach town", "lat": 40.1017, "lon": 19.7448},
            {"name": "Llogara Pass", "type": "Scenic route", "lat": 40.1890, "lon": 19.6000},
            {"name": "Gjirokaster", "type": "Culture day trip", "lat": 40.0758, "lon": 20.1389},
        ],
    },
]


# =========================================================
# STYLING
# =========================================================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
:root{--bg:#f6f8fb;--card:#fff;--card2:#f8fafc;--text:#102033;--muted:#526173;--border:#d9e3ef;--primary:#0f766e;--blue:#2563eb;--shadow:rgba(15,23,42,.10);--chip:#eef6f3;--chiptext:#0f766e;--warning:#fff7df}
@media(prefers-color-scheme:dark){:root{--bg:#0b1120;--card:#111827;--card2:#172033;--text:#f8fafc;--muted:#cbd5e1;--border:#334155;--primary:#14b8a6;--blue:#60a5fa;--shadow:rgba(0,0,0,.35);--chip:#083f3a;--chiptext:#99f6e4;--warning:#2a210b}}
html,body,[class*="css"]{font-family:Inter,sans-serif}[data-testid="stAppViewContainer"]{background:var(--bg);color:var(--text)}.block-container{max-width:1180px;padding-top:1rem;padding-bottom:3rem}#MainMenu,footer,header{visibility:hidden}h1,h2,h3,h4,h5,h6,p,li,label,span,div{color:inherit}
label,.stSelectbox label,.stTextInput label{color:var(--text)!important;font-weight:800!important}div[data-baseweb="select"]>div,input{background:var(--card)!important;color:var(--text)!important;border-color:var(--border)!important}div[data-baseweb="select"] span{color:var(--text)!important}
.qa-nav{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:10px 4px 18px}.qa-logo{color:var(--text);font-size:1.45rem;font-weight:950;letter-spacing:-.045em}.qa-nav-links{display:flex;flex-wrap:wrap;gap:10px}.qa-nav-chip{background:var(--card);border:1px solid var(--border);color:var(--text);padding:8px 12px;border-radius:999px;font-size:.88rem;font-weight:800}
.qa-hero{border-radius:30px;padding:44px 38px;margin-bottom:22px;color:#fff;background:linear-gradient(135deg,rgba(5,10,20,.88),rgba(20,45,65,.80)),url('https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1800&q=80');background-size:cover;background-position:center;box-shadow:0 24px 60px var(--shadow)}.qa-hero h1{color:#fff;font-size:clamp(2.35rem,4.8vw,4.5rem);line-height:.98;margin:0 0 12px;font-weight:950;letter-spacing:-.07em}.qa-hero p{color:#e6eef8;max-width:860px;font-size:1.1rem;line-height:1.58}.qa-pill{color:#fff;display:inline-flex;padding:8px 13px;border-radius:999px;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.24);font-weight:850;margin:4px}
.qa-card,.qa-result,.qa-panel,.qa-ad,.qa-price-card,.qa-mini-card,.qa-route-card,.qa-map-card,.qa-activity-card{background:var(--card);border:1px solid var(--border);color:var(--text)}.qa-card{border-radius:24px;padding:22px;box-shadow:0 16px 42px var(--shadow)}.qa-muted{color:var(--muted);line-height:1.55}
div.stButton>button{background:var(--primary)!important;color:#fff!important;font-weight:950!important;border:0!important;border-radius:999px!important;padding:.85rem 1rem!important;box-shadow:0 12px 24px rgba(15,118,110,.20)}
.qa-spinner-box{text-align:center;padding:28px 22px;border-radius:24px;background:var(--card);border:1px solid var(--border);box-shadow:0 16px 42px var(--shadow)}.qa-spinner{display:inline-block;font-size:4.5rem;animation:spin .42s linear infinite;margin-bottom:8px}@keyframes spin{from{transform:rotate(0deg) scale(1)}50%{transform:rotate(180deg) scale(1.06)}to{transform:rotate(360deg) scale(1)}}
.qa-result{overflow:hidden;border-radius:28px;box-shadow:0 20px 55px var(--shadow);margin-top:14px;padding:14px}.qa-result-img{height:280px;border-radius:20px;background-size:cover;background-position:center}.qa-destination{color:var(--text);font-size:clamp(2rem,3.8vw,3.25rem);line-height:1;font-weight:950;letter-spacing:-.065em;margin:0}.qa-country{color:var(--muted);margin-top:8px;font-weight:750}.qa-primary-badge{display:inline-flex;padding:8px 13px;border-radius:999px;background:var(--chip);color:var(--chiptext);border:1px solid var(--border);font-size:.9rem;font-weight:900;margin:10px 6px 2px 0}.qa-tag{display:inline-flex;padding:7px 10px;border-radius:999px;background:var(--card2);border:1px solid var(--border);font-size:.84rem;font-weight:800;margin:6px 6px 0 0}
.qa-score-row{display:flex;align-items:center;gap:.75rem;margin:16px 0 12px}.qa-score-label{font-size:.85rem;font-weight:900;color:var(--muted);text-transform:uppercase;letter-spacing:.05em}.qa-score-track{flex-grow:1;background:var(--border);border-radius:9999px;height:.625rem}.qa-score-fill{background:linear-gradient(90deg,var(--blue),#10b981);height:.625rem;border-radius:9999px}.qa-score-value{font-weight:950;color:var(--blue)}
.qa-mini-card{border-radius:15px;padding:13px;text-align:center;height:100%}.qa-mini-card strong{display:block;margin-bottom:.25rem;font-size:.86rem}.qa-mini-card span{color:var(--muted);font-weight:800}.qa-badge-confidence{display:inline-block;padding:.25rem .75rem;background:var(--warning);border:1px solid var(--border);border-radius:9999px;font-size:.75rem;font-weight:950!important}
.qa-price-section{margin-top:20px;padding:18px;border-radius:22px;background:var(--card2);border:1px solid var(--border)}.qa-price-card{border-radius:16px;padding:15px;height:100%}.qa-provider{color:var(--muted);font-size:.82rem;font-weight:850}.qa-price{font-size:1.4rem;font-weight:950;margin:6px 0 4px}.qa-desc{color:var(--muted);font-size:.87rem;min-height:36px}.qa-btn{display:block;margin-top:12px;text-align:center;text-decoration:none!important;color:#fff!important;background:var(--primary);border-radius:999px;padding:9px 11px;font-weight:900}.qa-btn-blue{background:var(--blue)}
.qa-route-wrap,.qa-map-wrap,.qa-activity-wrap{margin-top:24px}.qa-route-title,.qa-map-title,.qa-activity-title{display:flex;align-items:center;gap:10px;margin-bottom:10px}.qa-route-title h3,.qa-map-title h3,.qa-activity-title h3{margin:0;color:var(--text)}.qa-route-card{border-radius:18px;padding:16px;height:100%;position:relative;overflow:hidden}.qa-route-day{display:inline-flex;align-items:center;gap:8px;padding:7px 10px;border-radius:999px;background:var(--chip);color:var(--chiptext);font-weight:950;margin-bottom:12px}.qa-route-item{display:flex;gap:10px;align-items:flex-start;margin:10px 0;color:var(--muted)}.qa-route-time{font-size:.78rem;font-weight:900;color:var(--blue);min-width:70px}.qa-route-text{font-size:.93rem;color:var(--text);font-weight:650}
.qa-activity-card{border-radius:18px;padding:16px;height:100%}.qa-activity-type{color:var(--muted);font-size:.8rem;font-weight:850}.qa-activity-name{font-weight:950;color:var(--text);margin:5px 0}.qa-panel{border-radius:18px;padding:16px;height:100%}.qa-ad{margin:22px 0;padding:22px;border-style:dashed;border-radius:20px;text-align:center;color:var(--muted);font-weight:850}.qa-side-ad{border:1px dashed var(--border);background:var(--card2);border-radius:18px;padding:18px;text-align:center;color:var(--muted);font-weight:800;margin-top:12px}.qa-footer{text-align:center;color:var(--muted);margin-top:30px;padding-top:18px;border-top:1px solid var(--border);font-size:.9rem}
@media(max-width:800px){.qa-hero{padding:30px 22px}.qa-result-img{height:230px}.qa-nav{align-items:flex-start;flex-direction:column}.qa-score-row{flex-wrap:wrap}}
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
    budget_map = {"£ (Shoestring)": "£", "££ (Moderate)": "££", "£££ (Comfort)": "£££", "Any": place["budget_band"]}
    target = budget_map.get(budget, "££")
    if target == place["budget_band"]:
        score += 25
    elif target == "£" and place["budget_band"] == "££":
        score += 10
    elif target == "££" and place["budget_band"] in ["£", "£££"]:
        score += 10
    if vibe == "Surprise me" or vibe == place["primary_vibe"] or vibe in place["secondary_vibes"]:
        score += 23
    if trip_length in place["trip_lengths"]:
        score += 12
    return min(score, 98)


def pick_destination(region, budget, vibe, trip_length):
    scored = sorted([(calc_score(p, region, budget, vibe, trip_length), p) for p in DESTINATIONS], key=lambda x: x[0], reverse=True)
    pool = [x for x in scored if x[0] >= 65] or scored[:4]
    return random.choice(pool[:3]), scored


def multiplier(trip_length):
    return {"Weekend": 1.0, "3–5 days": 1.35, "1 week": 1.95, "2 weeks": 3.2}.get(trip_length, 1.25)


def affiliate_url(provider, place, starting_from):
    dest = quote_plus(f"{place['name']} {place['country']}")
    origin = quote_plus(starting_from or "London")
    iata = quote_plus(place["iata"])
    if provider == "booking":
        return f"https://www.booking.com/searchresults.html?ss={dest}&aid=quidaway-demo"
    if provider == "skyscanner":
        return f"https://www.skyscanner.net/transport/flights/{origin}/{iata}/?associateid=quidaway-demo"
    if provider == "expedia":
        return f"https://www.expedia.co.uk/Hotel-Search?destination={dest}&affcid=quidaway-demo"
    if provider == "getyourguide":
        return f"https://www.getyourguide.co.uk/s/?q={dest}&partner_id=quidaway-demo"
    return "#"


# =========================================================
# RENDER HELPERS
# =========================================================
def mini_card(label, value, confidence=False):
    value_html = f"<span class='qa-badge-confidence'>{value}</span>" if confidence else f"<span>{value}</span>"
    st.markdown(f"<div class='qa-mini-card'><strong>{label}</strong>{value_html}</div>", unsafe_allow_html=True)


def price_card(provider, price, desc, link, button_text, blue=False):
    btn = "qa-btn qa-btn-blue" if blue else "qa-btn"
    st.markdown(
        f"""
<div class="qa-price-card">
  <div class="qa-provider">{provider}</div>
  <div class="qa-price">{price}</div>
  <div class="qa-desc">{desc}</div>
  <a class="{btn}" href="{link}" target="_blank" rel="sponsored noopener">{button_text}</a>
</div>
""",
        unsafe_allow_html=True,
    )


def render_prices(place, trip_length, starting_from):
    m = multiplier(trip_length)
    flight = "No flight needed" if place["fake_flight_from"] == 0 else f"from £{place['fake_flight_from']}"
    stay = f"from £{int(place['fake_stay_from'] * m)}"
    package = f"from £{int(place['fake_package_from'] * m)}"

    st.markdown(
        f"""
<div class="qa-price-section">
  <h3 style="margin:0;color:var(--text);">Check live options</h3>
  <p class="qa-muted" style="margin-top:6px;">Demo partner cards. In WordPress these would be Travelpayouts/Booking/Skyscanner style affiliate widgets or deep links.</p>
  <span style="display:inline-flex;padding:7px 11px;border-radius:999px;border:1px solid var(--border);background:var(--card);color:var(--muted);font-size:.8rem;font-weight:850;margin-bottom:12px;">Demo refreshed: {datetime.now().strftime("%d %b %Y")}</span>
</div>
""",
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        price_card("Skyscanner-style flights", flight, f"Compare flights from {starting_from or 'London'} to {place['iata']}.", affiliate_url("skyscanner", place, starting_from), "Compare flights", True)
    with c2:
        price_card("Booking.com-style stays", stay, f"Search stays in {place['name']}. Demo nightly guide.", affiliate_url("booking", place, starting_from), "Check stays")
    with c3:
        price_card("Expedia-style packages", package, f"Demo package estimate for {trip_length.lower()} planning.", affiliate_url("expedia", place, starting_from), "View packages")

    c4, c5, c6 = st.columns(3)
    with c4:
        price_card("GetYourGuide-style activities", "from £18", "Tours, viewpoints and local experiences.", affiliate_url("getyourguide", place, starting_from), "Find activities", True)
    with c5:
        price_card("Budget confidence", place["budget_confidence"], "How stable this destination feels for planning.", "#", "Why this score?")
    with c6:
        price_card("QuidAway note", place["budget_band"], "Budget guidance first, live prices before booking.", "#", "Save idea")

    st.caption("Prototype disclosure: demo price cards only. Real site should show affiliate disclosure and send users to live partner searches.")


def route_items(place, days):
    things = [a["name"] for a in place["attractions"]]
    templates = [
        [("Arrival", "Arrive and settle in"), ("Afternoon", things[0]), ("Evening", "Budget-friendly local dinner")],
        [("Morning", things[1]), ("Afternoon", things[2]), ("Evening", "Viewpoint or local walk")],
        [("Morning", things[3] if len(things) > 3 else things[0]), ("Lunch", "Local food stop"), ("Evening", "Relaxed final evening")],
        [("Morning", "Flexible day trip"), ("Afternoon", "Neighbourhood explore"), ("Evening", "Cheap/free activity")],
        [("Morning", "Slow morning"), ("Afternoon", "Final photos"), ("Evening", "Travel back")],
        [("Morning", "Extra local route"), ("Afternoon", "Budget picnic"), ("Evening", "Rest evening")],
        [("Morning", "Backup plan"), ("Afternoon", "Market/cafe stop"), ("Evening", "Return journey")],
    ]
    return templates[:days]


def render_route(place, trip_length):
    days = {"Weekend": 2, "3–5 days": 3, "1 week": 5, "2 weeks": 7}.get(trip_length, 3)
    st.markdown(
        """
<div class="qa-route-wrap">
  <div class="qa-route-title">
    <span style="font-size:1.8rem;">🗺️</span>
    <div>
      <h3>Suggested route idea</h3>
      <div class="qa-muted">A simple visual itinerary based on your destination, vibe and trip length.</div>
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    templates = route_items(place, days)
    for start in range(0, days, 3):
        cols = st.columns(min(3, days - start))
        for col, idx in zip(cols, range(start, min(start + 3, days))):
            with col:
                items = "".join(
                    [f"<div class='qa-route-item'><div class='qa-route-time'>{t}</div><div class='qa-route-text'>{txt}</div></div>" for t, txt in templates[idx]]
                )
                st.markdown(f"<div class='qa-route-card'><div class='qa-route-day'>Day {idx + 1}</div>{items}</div>", unsafe_allow_html=True)


def render_map(place):
    st.markdown(
        """
<div class="qa-map-wrap">
  <div class="qa-map-title">
    <span style="font-size:1.8rem;">📍</span>
    <div>
      <h3>Map preview</h3>
      <div class="qa-muted">Destination pin + a few example activity/attraction pins. This is the map foundation for the real website.</div>
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    m = folium.Map(location=[place["lat"], place["lon"]], zoom_start=11, tiles="OpenStreetMap")
    folium.Marker(
        [place["lat"], place["lon"]],
        popup=f"{place['name']}, {place['country']}",
        tooltip=f"{place['name']} main area",
        icon=folium.Icon(color="green", icon="globe"),
    ).add_to(m)

    for att in place["attractions"]:
        folium.Marker(
            [att["lat"], att["lon"]],
            popup=f"{att['name']} — {att['type']}",
            tooltip=att["name"],
            icon=folium.Icon(color="blue", icon="info-sign"),
        ).add_to(m)

    # Draw a simple line between pins for route-feel.
    route_points = [[a["lat"], a["lon"]] for a in place["attractions"][:4]]
    if len(route_points) >= 2:
        folium.PolyLine(route_points, color="#0f766e", weight=3, opacity=0.7).add_to(m)

    st_folium(m, width=None, height=430)


def render_activities(place):
    st.markdown(
        """
<div class="qa-activity-wrap">
  <div class="qa-activity-title">
    <span style="font-size:1.8rem;">🎟️</span>
    <div>
      <h3>Activities around this place</h3>
      <div class="qa-muted">These are example activity cards. Later, this can come from OpenTripMap, Geoapify, or GetYourGuide/Viator-style partners.</div>
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    cols = st.columns(4)
    for col, att in zip(cols, place["attractions"][:4]):
        with col:
            st.markdown(
                f"""
<div class="qa-activity-card">
  <div class="qa-activity-type">{att["type"]}</div>
  <div class="qa-activity-name">{att["name"]}</div>
  <div class="qa-muted" style="font-size:.86rem;">Good option for this route.</div>
</div>
""",
                unsafe_allow_html=True,
            )


def render_result(place, score, scored, trip_length, starting_from):
    st.markdown('<div class="qa-result">', unsafe_allow_html=True)
    col_img, col_text = st.columns([0.82, 1.18], gap="large")

    with col_img:
        st.markdown(f"<div class='qa-result-img' style=\"background-image:url('{place['image']}')\"></div>", unsafe_allow_html=True)
        st.markdown("<div class='qa-side-ad'>AdSense / partner banner space<br><span style='font-size:.82rem;'>Use this only after approval</span></div>", unsafe_allow_html=True)

    with col_text:
        tags = f"<span class='qa-primary-badge'>{place['primary_vibe']}</span>" + "".join([f"<span class='qa-tag'>{v}</span>" for v in place["secondary_vibes"][:3]])
        st.markdown(f"<h2 class='qa-destination'>{place['name']}</h2><div class='qa-country'>{place['country']} · IATA: {place['iata']}</div><div>{tags}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='qa-score-row'><span class='qa-score-label'>Match Score</span><div class='qa-score-track'><div class='qa-score-fill' style='width:{score}%'></div></div><span class='qa-score-value'>{score}%</span></div>", unsafe_allow_html=True)

        m1, m2, m3 = st.columns(3)
        with m1:
            mini_card("Budget Band", place["budget_band"])
        with m2:
            mini_card("Est. Daily", place["daily_spend"])
        with m3:
            mini_card("Pricing Confidence", place["budget_confidence"], True)

        st.markdown(f"**Quick decision:** {place['summary']}")
        st.markdown(f"**Why this works:** {place['why']}")
        st.markdown(f"**Good to know:** {place['good_to_know']}")
        st.markdown(f"**Budget tip:** {place['tip']}")
        st.warning(f"**Avoid if:** {place['avoid']}")

    st.markdown("</div>", unsafe_allow_html=True)

    render_prices(place, trip_length, starting_from)

    st.markdown("### Not quite right?")
    a, b, c = st.columns(3)
    a.info(f"**Cheaper alternative:** {place['cheaper']}")
    b.info(f"**Similar vibe:** {place['similar']}")
    c.info(f"**Another option:** {scored[1][1]['name'] if len(scored) > 1 else place['similar']}")

    render_route(place, trip_length)
    render_map(place)
    render_activities(place)


# =========================================================
# PAGE LAYOUT
# =========================================================
st.markdown(
    """
<div class='qa-nav'>
  <div class='qa-logo'>🌍 QuidAway</div>
  <div class='qa-nav-links'>
    <span class='qa-nav-chip'>Budget-first</span>
    <span class='qa-nav-chip'>Escape finder</span>
    <span class='qa-nav-chip'>Map preview</span>
    <span class='qa-nav-chip'>Activities</span>
    <span class='qa-nav-chip'>Affiliate-ready</span>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="qa-hero">
  <h1>Find your budget escape.</h1>
  <p>Tell us your budget band, travel vibe and trip length. QuidAway suggests where your money could go furthest, then shows a route idea, map preview, activities and partner price-check cards.</p>
  <div>
    <span class="qa-pill">💸 Budget guidance</span>
    <span class="qa-pill">🌍 Destination decision-maker</span>
    <span class="qa-pill">🗺️ Map preview</span>
    <span class="qa-pill">🎟️ Activities</span>
    <span class="qa-pill">🔗 Affiliate-ready layout</span>
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
        vibe = st.selectbox("Travel vibe", ["City", "Beach", "Hiking", "Food", "Nature", "Culture", "Adventure", "Surprise me"], index=0)
    with c3:
        trip_length = st.selectbox("Trip length", ["Weekend", "3–5 days", "1 week", "2 weeks"], index=1)
        st.markdown("<br>", unsafe_allow_html=True)

    submitted = st.form_submit_button("🌍 Find my escape", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

if submitted:
    ph = st.empty()
    with ph:
        st.markdown("<div class='qa-spinner-box'><div class='qa-spinner'>🌍</div><h3>Searching the globe...</h3><p class='qa-muted'>Matching budget · checking vibes · building route and map</p></div>", unsafe_allow_html=True)
    time.sleep(1.1)
    ph.empty()
    (score, place), scored = pick_destination(region, budget, vibe, trip_length)
    st.session_state["result"] = {"place": place, "score": score, "scored": scored, "trip_length": trip_length, "starting_from": starting_from}

if st.session_state.get("result"):
    st.markdown("## Your Match")
    r = st.session_state["result"]
    render_result(r["place"], r["score"], r["scored"], r["trip_length"], r["starting_from"])
else:
    st.markdown(
        """
<div class="qa-ad">
  Tip: choose a budget, vibe and trip length, then click <b>Find my escape</b>. This app is a production-MVP style prototype, not a booking engine.
</div>
""",
        unsafe_allow_html=True,
    )

st.markdown("<div class='qa-ad'>AdSense placeholder — best used on destination/blog sections, or as a small side banner near the image after approval.</div>", unsafe_allow_html=True)

st.markdown("## How this becomes WordPress")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("<div class='qa-panel'><b>1. Static destination data</b>Store airport code, coordinates, budget band, vibe and route logic in WordPress ACF fields.</div>", unsafe_allow_html=True)
with c2:
    st.markdown("<div class='qa-panel'><b>2. Map and activities</b>Use latitude/longitude to show destination pins. Later add OpenTripMap/Geoapify for more places.</div>", unsafe_allow_html=True)
with c3:
    st.markdown("<div class='qa-panel'><b>3. Affiliate handoff</b>Generate partner links/widgets from destination name and IATA code. No exact price promise.</div>", unsafe_allow_html=True)

st.markdown("<div class='qa-footer'>QuidAway prototype. Demo prices only. Real website should include affiliate disclosure, privacy policy and clear budget disclaimers.</div>", unsafe_allow_html=True)
