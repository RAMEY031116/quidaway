
import random
import time
from urllib.parse import quote_plus
import streamlit as st

st.set_page_config(
    page_title="QuidAway | Budget Escape Finder",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

APP_VERSION = "wordpress-mockup-final-v1"
if st.session_state.get("app_version") != APP_VERSION:
    st.session_state["app_version"] = APP_VERSION
    st.session_state["result"] = None


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
        "best_months": "March–June, September–November",
        "budget_range": "£450–£850",
        "daily_spend": "£45–£80/day",
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
        "region": "Europe",
        "budget": "Low",
        "primary_vibe": "City",
        "secondary_vibes": ["Food", "Culture", "Low-cost break"],
        "trip_lengths": ["Weekend", "3–5 days"],
        "difficulty": "Easy",
        "best_months": "April–June, September–December",
        "budget_range": "£250–£550",
        "daily_spend": "£30–£60/day",
        "summary": "A low-cost city break with food, culture, history and walkable streets.",
        "why": "Krakow works well if you want a proper European city feeling without spending too much.",
        "good_to_know": "Better for culture and food than beaches or hiking.",
        "things": ["Old Town", "Kazimierz", "Wieliczka Salt Mine", "Local pierogi spots"],
        "tip": "Stay near tram links rather than directly on the main square.",
        "avoid": "Avoid if you mainly want beaches or guaranteed warm weather.",
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
        "best_months": "May–September",
        "budget_range": "£120–£350",
        "daily_spend": "£25–£60/day",
        "summary": "A proper UK mountain escape for hiking, lakes and budget adventure.",
        "why": "Snowdonia is a strong option if you want a scenic trip without paying for flights.",
        "good_to_know": "Weather can change quickly, so pack sensibly.",
        "things": ["Yr Wyddfa / Snowdon", "Llanberis", "Waterfalls and lakes", "Betws-y-Coed"],
        "tip": "Use hostels, campsites or shared stays and avoid peak summer weekends.",
        "avoid": "Avoid if you want guaranteed sun or a city-style break.",
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
        "best_months": "April–June, September–October",
        "budget_range": "£300–£650",
        "daily_spend": "£40–£75/day",
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
        "region": "Europe",
        "budget": "Low",
        "primary_vibe": "Beach",
        "secondary_vibes": ["Adventure", "Value", "Coastal road trip"],
        "trip_lengths": ["1 week", "2 weeks"],
        "difficulty": "Moderate",
        "best_months": "May–June, September",
        "budget_range": "£400–£800",
        "daily_spend": "£30–£65/day",
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
        "name": "Lake Bled",
        "country": "Slovenia",
        "region": "Europe",
        "budget": "Medium",
        "primary_vibe": "Nature",
        "secondary_vibes": ["Hiking", "Romantic", "Scenic"],
        "trip_lengths": ["3–5 days", "1 week"],
        "difficulty": "Easy",
        "best_months": "May–September",
        "budget_range": "£450–£850",
        "daily_spend": "£50–£90/day",
        "summary": "A scenic lake and mountain escape that feels special without going full Switzerland.",
        "why": "Lake Bled works for people who want nature, calm views and easy outdoor activities.",
        "good_to_know": "It is not the cheapest place in Europe, so staying slightly outside Bled helps.",
        "things": ["Lake Bled walk", "Vintgar Gorge", "Triglav National Park", "Bled Castle viewpoint"],
        "tip": "Stay outside the main lake area and use buses where practical.",
        "avoid": "Avoid if you want nightlife or very cheap food every day.",
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
        "best_months": "April–June, September–October",
        "budget_range": "£350–£700",
        "daily_spend": "£45–£85/day",
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

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

:root {
  --bg:#f6f8fb; --card:#ffffff; --card2:#f8fafc; --text:#102033; --muted:#526173;
  --border:#d9e3ef; --primary:#0f766e; --primary2:#115e59; --shadow:rgba(15,23,42,.10);
  --chip:#eef6f3; --chiptext:#0f766e; --warning:#fff7df; --heroText:#ffffff;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg:#0b1120; --card:#111827; --card2:#172033; --text:#f8fafc; --muted:#cbd5e1;
    --border:#334155; --primary:#14b8a6; --primary2:#0d9488; --shadow:rgba(0,0,0,.35);
    --chip:#083f3a; --chiptext:#99f6e4; --warning:#2a210b; --heroText:#ffffff;
  }
}
html,body,[class*="css"]{font-family:'Inter',sans-serif}
[data-testid="stAppViewContainer"]{background:var(--bg);color:var(--text)}
.block-container{max-width:1160px;padding-top:1rem;padding-bottom:3rem}
#MainMenu,footer,header{visibility:hidden}
h1,h2,h3,h4,h5,h6,p,li,label,span,div{color:inherit}
label,.stSelectbox label,.stTextInput label{color:var(--text)!important;font-weight:800!important}
div[data-baseweb="select"]>div,input{background-color:var(--card)!important;color:var(--text)!important;border-color:var(--border)!important}
div[data-baseweb="select"] span{color:var(--text)!important}

.qa-nav{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:10px 4px 18px}
.qa-logo{color:var(--text);font-size:1.45rem;font-weight:950;letter-spacing:-.045em}
.qa-nav-links{display:flex;flex-wrap:wrap;gap:10px}
.qa-nav-chip{background:var(--card);border:1px solid var(--border);color:var(--text);padding:8px 12px;border-radius:999px;font-size:.88rem;font-weight:800}

.qa-hero{border-radius:32px;padding:52px 44px;margin-bottom:26px;color:#fff;background:linear-gradient(135deg,rgba(5,10,20,.88),rgba(20,45,65,.80)),url('https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1800&q=80');background-size:cover;background-position:center;box-shadow:0 24px 60px var(--shadow)}
.qa-hero h1{color:#fff;font-size:clamp(2.55rem,5.3vw,5.1rem);line-height:.96;margin:0 0 16px;font-weight:950;letter-spacing:-.07em}
.qa-hero p{color:#e6eef8;max-width:800px;font-size:1.16rem;line-height:1.66}
.qa-pills{display:flex;gap:10px;flex-wrap:wrap;margin-top:24px}
.qa-pill{color:#fff;display:inline-flex;padding:9px 14px;border-radius:999px;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.24);font-weight:850}

.qa-card,.qa-problem,.qa-soft-card,.qa-result,.qa-ad{background:var(--card);border:1px solid var(--border);color:var(--text)}
.qa-card{border-radius:26px;padding:24px;box-shadow:0 16px 42px var(--shadow)}
.qa-section-title{color:var(--text);font-size:1.75rem;font-weight:950;letter-spacing:-.045em;margin:2px 0 8px}
.qa-muted{color:var(--muted);line-height:1.62}
.qa-problem,.qa-soft-card{border-radius:22px;padding:20px;height:100%}
.qa-problem b,.qa-soft-card b{color:var(--text);display:block;font-size:1.05rem;margin-bottom:6px}
div.stButton>button{background:var(--primary)!important;color:#fff!important;font-weight:950!important;border:0!important;border-radius:999px!important;padding:.85rem 1rem!important;box-shadow:0 12px 24px rgba(15,118,110,.20)}
div.stButton>button:hover{background:var(--primary2)!important;transform:translateY(-1px)}

.qa-spinner-box{text-align:center;padding:34px 24px;border-radius:28px;background:var(--card);color:var(--text);border:1px solid var(--border);box-shadow:0 16px 42px var(--shadow)}
.qa-spinner{display:inline-block;font-size:5.2rem;animation:spin .42s linear infinite;margin-bottom:8px}
@keyframes spin{from{transform:rotate(0deg) scale(1)}50%{transform:rotate(180deg) scale(1.06)}to{transform:rotate(360deg) scale(1)}}

.qa-result{overflow:hidden;border-radius:30px;box-shadow:0 24px 62px var(--shadow);margin-top:18px;padding:18px}
.qa-result-img{min-height:380px;border-radius:24px;background-size:cover;background-position:center}
.qa-result-body{padding:12px 8px 4px;color:var(--text)}
.qa-destination{color:var(--text);font-size:clamp(2.1rem,4.1vw,3.7rem);line-height:.98;font-weight:950;letter-spacing:-.065em;margin:0}
.qa-country{color:var(--muted);margin-top:8px;font-weight:750;font-size:1.05rem}
.qa-primary-badge{display:inline-flex;padding:8px 13px;border-radius:999px;background:var(--chip);color:var(--chiptext);border:1px solid var(--border);font-size:.9rem;font-weight:900;margin:12px 6px 2px 0}
.qa-tag{display:inline-flex;padding:7px 10px;border-radius:999px;background:var(--card2);border:1px solid var(--border);color:var(--text);font-size:.84rem;font-weight:800;margin:6px 6px 0 0}
.qa-score-box{margin:16px 0;padding:14px;background:var(--card2);border:1px solid var(--border);border-radius:18px}
.qa-score-label{display:flex;justify-content:space-between;gap:12px;margin-bottom:8px;color:var(--text);font-weight:900}
.qa-score-bg{height:12px;border-radius:999px;overflow:hidden;background:var(--border)}
.qa-score-fill{height:12px;border-radius:999px;background:linear-gradient(90deg,#0ea5e9,#10b981)}
.qa-info-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:16px 0}
.qa-mini{background:var(--card2);border:1px solid var(--border);border-radius:18px;padding:14px}
.qa-mini strong{display:block;color:var(--text);margin-bottom:4px}
.qa-mini span{color:var(--muted);font-size:.92rem}

.qa-affiliate{margin-top:18px;padding:20px;border-radius:24px;background:var(--warning);border:1px solid var(--border);color:var(--text)}
.qa-aff-grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;margin-top:14px}
.qa-aff-link{display:block;text-decoration:none!important;color:var(--text)!important;background:var(--card);border:1px solid var(--border);border-radius:18px;padding:13px;font-weight:900}
.qa-aff-link span{display:block;color:var(--muted);font-size:.78rem;font-weight:700;margin-top:3px}
.qa-ad{margin:22px 0;padding:26px;border-style:dashed;border-radius:22px;text-align:center;color:var(--muted);font-weight:850}
.qa-footer{text-align:center;color:var(--muted);margin-top:38px;padding-top:20px;border-top:1px solid var(--border);font-size:.9rem;line-height:1.7}
div[data-testid="stMetric"]{background:var(--card);color:var(--text);border:1px solid var(--border);border-radius:18px;padding:14px}
@media(max-width:900px){.qa-hero{padding:34px 24px;border-radius:25px}.qa-info-grid,.qa-aff-grid{grid-template-columns:1fr}.qa-result-img{min-height:260px}.qa-nav{align-items:flex-start;flex-direction:column}}

.qa-route {
    margin-top:18px;
    padding:20px;
    border-radius:24px;
    background:var(--card2);
    border:1px solid var(--border);
    color:var(--text);
}
.qa-route h4 {
    margin-top:0;
    color:var(--text);
}
.qa-route-grid {
    display:grid;
    grid-template-columns:repeat(3,minmax(0,1fr));
    gap:12px;
    margin-top:14px;
}
.qa-day-card {
    background:var(--card);
    border:1px solid var(--border);
    border-radius:18px;
    padding:14px;
    height:100%;
}
.qa-day-card b {
    display:block;
    color:var(--text);
    margin-bottom:8px;
}
.qa-day-card ul {
    margin:0;
    padding-left:18px;
    color:var(--muted);
}
.qa-route-meta {
    display:grid;
    grid-template-columns:repeat(3,minmax(0,1fr));
    gap:10px;
    margin-top:12px;
}
.qa-route-meta div {
    background:var(--card);
    border:1px solid var(--border);
    border-radius:16px;
    padding:12px;
}
.qa-route-meta strong {
    display:block;
    color:var(--text);
    margin-bottom:4px;
}
.qa-route-meta span {
    color:var(--muted);
    font-size:.9rem;
}
@media(max-width:900px){.qa-route-grid,.qa-route-meta{grid-template-columns:1fr}}

</style>
""", unsafe_allow_html=True)


def affiliate_url(kind, place):
    q = quote_plus(f"{place['name']} {place['country']}")
    fake_partner = "quidaway-demo"
    if kind == "booking":
        return f"https://www.booking.com/searchresults.html?ss={q}&aid={fake_partner}"
    if kind == "skyscanner":
        return f"https://www.skyscanner.net/transport/flights/lond/{quote_plus(place['name'])}/?associateid={fake_partner}"
    if kind == "expedia":
        return f"https://www.expedia.co.uk/Hotel-Search?destination={q}&affcid={fake_partner}"
    if kind == "getyourguide":
        return f"https://www.getyourguide.co.uk/s/?q={q}&partner_id={fake_partner}"
    if kind == "insurance":
        return f"https://example-travel-cover.com/?destination={q}&partner={fake_partner}"
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
    if vibe == "Surprise me" or vibe == place["primary_vibe"] or vibe in place["secondary_vibes"]:
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


def render_affiliates(place):
    st.markdown(f"""
<div class="qa-affiliate">
  <h4>Check live options when you are ready</h4>
  <p class="qa-muted">This is a realistic demo of how affiliate links could look on your WordPress site. The links are fake/demo-style and show the type of partners you might use later.</p>
  <div class="qa-aff-grid">
    <a class="qa-aff-link" href="{affiliate_url('booking', place)}" target="_blank" rel="sponsored noopener">🏨 Booking.com<span>Find stays</span></a>
    <a class="qa-aff-link" href="{affiliate_url('skyscanner', place)}" target="_blank" rel="sponsored noopener">✈️ Skyscanner<span>Compare flights</span></a>
    <a class="qa-aff-link" href="{affiliate_url('expedia', place)}" target="_blank" rel="sponsored noopener">🌍 Expedia<span>Packages/hotels</span></a>
    <a class="qa-aff-link" href="{affiliate_url('getyourguide', place)}" target="_blank" rel="sponsored noopener">🎟️ GetYourGuide<span>Activities</span></a>
    <a class="qa-aff-link" href="{affiliate_url('insurance', place)}" target="_blank" rel="sponsored noopener">🛡️ Cover<span>Insurance demo</span></a>
  </div>
  <p class="qa-muted" style="font-size:.84rem;margin-top:12px;">Affiliate disclosure example: QuidAway may earn a small commission if someone books through these links, at no extra cost to them.</p>
</div>
""", unsafe_allow_html=True)




def trip_days_from_label(label):
    if label == "Weekend":
        return 2
    if label == "3–5 days":
        return 3
    if label == "1 week":
        return 5
    if label == "2 weeks":
        return 7
    return 3


def create_itinerary(place, trip_length, starting_from):
    days = trip_days_from_label(trip_length)

    base = place["name"]
    vibe = place["primary_vibe"]

    # Simple rule-based route plan. In WordPress this can be generated from destination fields
    # or later upgraded to AI.
    if vibe == "Hiking":
        day_templates = [
            ["Arrive and settle in", "Easy local walk", "Cheap local dinner"],
            [place["things"][0], place["things"][1], "Sunset viewpoint"],
            [place["things"][2], "Local market or old town", "Relaxed evening"],
            ["Optional guided hike", "Scenic lunch stop", "Free viewpoint"],
            ["Slow morning", "Final photos", "Travel back"],
            ["Extra nature route", "Budget picnic", "Evening rest"],
            ["Flexible spare day", "Backup rainy-day plan", "Return journey"],
        ]
        stay = "Guesthouse, hostel or apartment near transport links"
        transport = "Public transport where possible; consider tours/car hire for remote trails"
    elif vibe == "Beach":
        day_templates = [
            ["Arrive and check in", "Beach walk", "Simple local dinner"],
            [place["things"][0], "Swim or coastal viewpoint", "Sunset by the water"],
            [place["things"][1], "Local town exploring", "Budget seafood/local meal"],
            ["Boat trip or nearby beach", "Relaxed afternoon", "Evening stroll"],
            ["Slow morning", "Souvenir stop", "Travel back"],
            ["Optional coastal route", "Beach picnic", "Rest evening"],
            ["Flexible spare day", "Backup indoor plan", "Return journey"],
        ]
        stay = "Budget hotel, apartment or guesthouse near beach/transport"
        transport = "Use buses/transfers; car hire only if moving between towns"
    elif vibe == "City" or vibe == "Food" or vibe == "Culture":
        day_templates = [
            ["Arrive and check in", "Old town walk", "Budget food spot"],
            [place["things"][0], place["things"][1], "Evening viewpoint or local area"],
            [place["things"][2], "Cafe/market stop", "Relaxed final evening"],
            ["Day trip or museum", "Local lunch", "Neighbourhood walk"],
            ["Slow morning", "Final photos", "Travel back"],
            ["Extra food/culture route", "Free attraction", "Evening explore"],
            ["Flexible spare day", "Shopping/local market", "Return journey"],
        ]
        stay = "Budget hotel/apartment near metro, tram or walkable centre"
        transport = "Walk and use local public transport instead of taxis"
    else:
        day_templates = [
            ["Arrive and settle in", "Easy explore", "Cheap local dinner"],
            [place["things"][0], place["things"][1], "Evening walk"],
            [place["things"][2], "Local food stop", "Relaxed final evening"],
            ["Optional day trip", "Scenic stop", "Free viewpoint"],
            ["Slow morning", "Final photos", "Travel back"],
            ["Extra flexible day", "Budget activity", "Evening rest"],
            ["Backup day", "Local area", "Return journey"],
        ]
        stay = "Budget-friendly stay close to transport"
        transport = "Use public transport and avoid unnecessary taxis"

    itinerary = []
    for i in range(days):
        itinerary.append({
            "day": f"Day {i+1}",
            "items": day_templates[i]
        })

    return {
        "days": days,
        "stay": stay,
        "transport": transport,
        "starting_from": starting_from or "Your city",
        "itinerary": itinerary,
    }


def render_route_planner(place, trip_length, starting_from):
    plan = create_itinerary(place, trip_length, starting_from)

    day_cards = ""
    for day in plan["itinerary"]:
        items = "".join([f"<li>{item}</li>" for item in day["items"]])
        day_cards += f"""
        <div class="qa-day-card">
            <b>{day["day"]}</b>
            <ul>{items}</ul>
        </div>
        """

    st.markdown(f"""
<div class="qa-route">
  <h4>Suggested {plan["days"]}-day route plan</h4>
  <p class="qa-muted">
    This is a demo itinerary generated from the destination type, trip length and travel vibe.
    In WordPress, this can be rule-based first, then upgraded to AI later.
  </p>
  <div class="qa-route-meta">
    <div><strong>Start from</strong><span>{plan["starting_from"]}</span></div>
    <div><strong>Stay style</strong><span>{plan["stay"]}</span></div>
    <div><strong>Travel style</strong><span>{plan["transport"]}</span></div>
  </div>
  <div class="qa-route-grid">
    {day_cards}
  </div>
</div>
""", unsafe_allow_html=True)

def render_result(place, score, scored):
    st.markdown('<div class="qa-result">', unsafe_allow_html=True)
    col_img, col_text = st.columns([0.95, 1.05], gap="large")
    with col_img:
        st.markdown(f"<div class='qa-result-img' style=\"background-image:url('{place['image']}')\"></div>", unsafe_allow_html=True)
    with col_text:
        tags = f"<span class='qa-primary-badge'>{place['primary_vibe']}</span>" + "".join([f"<span class='qa-tag'>{v}</span>" for v in place["secondary_vibes"][:3]])
        st.markdown(f"""
<div class="qa-result-body">
  <h2 class="qa-destination">{place['name']}</h2>
  <div class="qa-country">{place['country']} · {place['region']}</div>
  <div>{tags}</div>
  <div class="qa-score-box">
    <div class="qa-score-label"><span>QuidAway decision match</span><span>{score}%</span></div>
    <div class="qa-score-bg"><div class="qa-score-fill" style="width:{score}%"></div></div>
  </div>
  <div class="qa-info-grid">
    <div class="qa-mini"><strong>Budget range</strong><span>{place['budget_range']}</span></div>
    <div class="qa-mini"><strong>Daily spend</strong><span>{place['daily_spend']}</span></div>
    <div class="qa-mini"><strong>Best time</strong><span>{place['best_months']}</span></div>
  </div>
</div>
""", unsafe_allow_html=True)
        st.markdown(f"**Quick decision:** {place['summary']}")
        st.markdown(f"**Why this place works:** {place['why']}")
        st.markdown(f"**Good to know:** {place['good_to_know']}")
        st.markdown(f"**Budget tip:** {place['tip']}")
        st.markdown(f"**Avoid if:** {place['avoid']}")
        st.markdown("**Simple trip ideas:**")
        for t in place["things"]:
            st.markdown(f"- {t}")
        render_affiliates(place)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### More decision help")
    a, b, c = st.columns(3)
    a.info(f"**Cheaper option:** {place['cheaper']}")
    b.info(f"**Similar vibe:** {place['similar']}")
    another = scored[1][1]["name"] if len(scored) > 1 else place["similar"]
    c.info(f"**Another good match:** {another}")


st.markdown("""
<div class="qa-nav">
  <div class="qa-logo">🌍 QuidAway</div>
  <div class="qa-nav-links">
    <span class="qa-nav-chip">Budget-first</span>
    <span class="qa-nav-chip">Escape finder</span>
    <span class="qa-nav-chip">Hiking & nature</span>
    <span class="qa-nav-chip">Worldwide ideas</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="qa-hero">
  <h1>Find a place that fits your budget and vibe.</h1>
  <p>QuidAway helps people who want to go somewhere but cannot decide where. Choose your budget, trip style and time available — then get a practical destination idea with honest tips, estimated costs and alternatives.</p>
  <div class="qa-pills">
    <span class="qa-pill">💸 Budget-friendly ideas</span>
    <span class="qa-pill">🥾 Hiking, city, beach & nature</span>
    <span class="qa-pill">🧭 Decision maker</span>
    <span class="qa-pill">🗺️ Route planner demo</span>
  </div>
</div>
""", unsafe_allow_html=True)

intro_left, intro_right = st.columns([1.25, 0.75], gap="large")
with intro_left:
    st.markdown('<div class="qa-section-title">The problem it solves</div>', unsafe_allow_html=True)
    st.markdown("""<p class="qa-muted">Most travel sites are built for people who already know where they want to go. QuidAway is for the earlier moment: “I have a budget and a vibe, but I have no idea where to go.” It helps them decide before they check prices or book anything.</p>""", unsafe_allow_html=True)
with intro_right:
    m1, m2 = st.columns(2)
    m1.metric("Demo places", len(DESTINATIONS))
    m2.metric("Main use", "Decide")

p1, p2, p3 = st.columns(3)
with p1:
    st.markdown("<div class='qa-problem'><b>1. Too many choices</b><span class='qa-muted'>Endless flight, hotel and TikTok ideas make it harder to choose.</span></div>", unsafe_allow_html=True)
with p2:
    st.markdown("<div class='qa-problem'><b>2. Budget confusion</b><span class='qa-muted'>A cheap flight does not always mean a cheap trip. QuidAway gives budget context.</span></div>", unsafe_allow_html=True)
with p3:
    st.markdown("<div class='qa-problem'><b>3. Wrong destination risk</b><span class='qa-muted'>Each result says who it suits, who should avoid it and cheaper alternatives.</span></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="qa-card">', unsafe_allow_html=True)
st.markdown("## Find my escape")
with st.form("quidaway_form"):
    c1, c2, c3 = st.columns(3)
    with c1:
        budget = st.selectbox("Budget level", ["Low", "Medium", "High", "Any"], index=1)
        region = st.selectbox("Where are you open to?", ["Europe", "UK", "Worldwide", "Surprise me"], index=0)
    with c2:
        vibe = st.selectbox("What kind of trip do you want?", ["Hiking", "Nature", "Beach", "City", "Food", "Culture", "Adventure", "Relaxing", "Budget", "Warm escape", "Surprise me"], index=0)
        trip_length = st.selectbox("How long?", ["Weekend", "3–5 days", "1 week", "2 weeks", "Flexible"], index=1)
    with c3:
        difficulty = st.selectbox("Activity level", ["Easy", "Moderate", "Challenging", "Any"], index=3)
        starting_from = st.text_input("Starting from", value="London")
    submitted = st.form_submit_button("🌍 Find my escape", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

if submitted:
    placeholder = st.empty()
    with placeholder:
        st.markdown("""
<div class="qa-spinner-box">
  <div class="qa-spinner">🌍</div>
  <h3>Finding a sensible escape...</h3>
  <p class="qa-muted">Checking budget fit · matching your vibe · looking for useful alternatives</p>
</div>
""", unsafe_allow_html=True)
    time.sleep(1.5)
    placeholder.empty()
    place, score, scored = pick_destination(region, budget, vibe, trip_length, difficulty)
    st.session_state["result"] = {"place": place, "score": score, "scored": scored, "trip_length": trip_length, "starting_from": starting_from}

if st.session_state.get("result"):
    st.markdown("## Your QuidAway suggestion")
    render_result(st.session_state["result"]["place"], st.session_state["result"]["score"], st.session_state["result"]["scored"])
    render_route_planner(
        st.session_state["result"]["place"],
        st.session_state["result"].get("trip_length", "3–5 days"),
        st.session_state["result"].get("starting_from", "London"),
    )

st.markdown("""<div class="qa-ad">AdSense demo placement — this could appear after the tool or between destination sections once the real site is approved.</div>""", unsafe_allow_html=True)

st.markdown("## What would make this website unique")
f1, f2, f3 = st.columns(3)
with f1:
    st.markdown("<div class='qa-soft-card'><b>Budget fit, not just random places</b><br><br>The tool explains whether the destination makes sense for the visitor's budget and trip length.</div>", unsafe_allow_html=True)
with f2:
    st.markdown("<div class='qa-soft-card'><b>Honest travel decision help</b><br><br>Each result includes avoid-if notes and good-to-know context, so it feels more trustworthy.</div>", unsafe_allow_html=True)
with f3:
    st.markdown("<div class='qa-soft-card'><b>Cheaper and similar alternatives</b><br><br>If a destination is not right, the visitor gets cheaper or similar ideas immediately.</div>", unsafe_allow_html=True)

st.markdown("## How this could work in WordPress")
wp1, wp2 = st.columns(2)
with wp1:
    st.markdown("""
**Simple WordPress setup**
- WordPress with Kadence or Astra theme
- One-page homepage with this tool embedded
- Custom HTML/JavaScript for the decision maker
- RankMath for SEO
- Google Site Kit or Ad Inserter for AdSense
- Affiliate links/widgets from travel partners
""")
with wp2:
    st.markdown("""
**Expansion features later**
- Save places in the browser first
- Login and profiles later
- “Want to go” and “Already visited” lists
- User recommended routes
- Route planner and itinerary generator
- Destination pages for SEO
- Google Sheets or Airtable as simple destination database
""")

st.markdown("""
<div class="qa-footer">
Prototype only. Budget ranges are example estimates, not live prices. Affiliate links are demo links.
A real website should include Privacy Policy, Affiliate Disclosure, Terms/Disclaimer and manually reviewed destination data.
</div>
""", unsafe_allow_html=True)
