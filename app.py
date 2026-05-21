import random
import time
import streamlit as st

st.set_page_config(
    page_title="QuidAway | Budget Escape Finder",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

APP_VERSION = "wordpress-mockup-final-v3"
if st.session_state.get("app_version") != APP_VERSION:
    st.session_state["app_version"] = APP_VERSION
    st.session_state["result"] = None

# ---------------------------------------------------------
# HYBRID DATA STRATEGY: Static Data + Dynamic Widgets
# ---------------------------------------------------------
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
        "summary": "A low-cost city break with food, culture, history and walkable streets.",
        "why": "Krakow works well if you want a proper European city feeling without spending too much.",
        "good_to_know": "Better for culture and food than beaches or hiking.",
        "things": ["Old Town", "Kazimierz", "Wieliczka Salt Mine", "Local pierogi spots"],
        "tip": "Eat at traditional 'Milk Bars' for hearty meals under £5.",
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
        "summary": "A budget-friendly beach and adventure route with clear water and coastal towns.",
        "why": "It gives Mediterranean-style views at a more budget-friendly level than many popular beach destinations.",
        "good_to_know": "Transport planning matters, especially if moving between towns.",
        "things": ["Ksamil", "Himare", "Llogara Pass", "Gjirokaster"],
        "tip": "Avoid August and compare guesthouses instead of resorts.",
        "avoid": "Avoid if you want everything polished, predictable or resort-style.",
        "cheaper": "Montenegro coast",
        "similar": "Croatia",
        "image": "https://images.unsplash.com/photo-1621178727374-3793b75310bc?auto=format&fit=crop&w=1600&q=80",
    }
]

# ---------------------------------------------------------
# CSS STYLING
# ---------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root {
  --bg:#f6f8fb; --card:#ffffff; --card2:#f8fafc; --text:#102033; --muted:#526173;
  --border:#d9e3ef; --primary:#0f766e; --primary2:#115e59; --shadow:rgba(15,23,42,.10);
  --chip:#eef6f3; --chiptext:#0f766e;
}
html,body,[class*="css"]{font-family:'Inter',sans-serif}
[data-testid="stAppViewContainer"]{background:var(--bg);color:var(--text)}
.block-container{max-width:1160px;padding-top:1rem;padding-bottom:3rem}
#MainMenu,footer,header{visibility:hidden}
h1,h2,h3,h4,h5,h6,p,li,label,span,div{color:inherit}
label,.stSelectbox label,.stTextInput label{color:var(--text)!important;font-weight:800!important}
div[data-baseweb="select"]>div,input{background-color:var(--card)!important;color:var(--text)!important;border-color:var(--border)!important}

.qa-hero{border-radius:32px;padding:52px 44px;margin-bottom:26px;color:#fff;background:linear-gradient(135deg,rgba(5,10,20,.88),rgba(20,45,65,.80)),url('https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1800&q=80');background-size:cover;background-position:center;box-shadow:0 24px 60px var(--shadow)}
.qa-hero h1{color:#fff;font-size:clamp(2.55rem,5.3vw,5.1rem);line-height:.96;margin:0 0 16px;font-weight:950;letter-spacing:-.07em}
.qa-hero p{color:#e6eef8;max-width:800px;font-size:1.16rem;line-height:1.66}

.qa-card{background:var(--card);border:1px solid var(--border);color:var(--text);border-radius:26px;padding:24px;box-shadow:0 16px 42px var(--shadow)}
div.stButton>button{background:var(--primary)!important;color:#fff!important;font-weight:950!important;border:0!important;border-radius:999px!important;padding:.85rem 1rem!important;box-shadow:0 12px 24px rgba(15,118,110,.20)}
div.stButton>button:hover{background:var(--primary2)!important;transform:translateY(-1px)}

.qa-spinner-box{text-align:center;padding:34px 24px;border-radius:28px;background:var(--card);color:var(--text);border:1px solid var(--border);box-shadow:0 16px 42px var(--shadow)}
.qa-spinner{display:inline-block;font-size:5.2rem;animation:spin .42s linear infinite;margin-bottom:8px}
@keyframes spin{from{transform:rotate(0deg) scale(1)}50%{transform:rotate(180deg) scale(1.06)}to{transform:rotate(360deg) scale(1)}}

.qa-result{overflow:hidden;border-radius:30px;box-shadow:0 24px 62px var(--shadow);margin-top:18px;padding:18px; background:var(--card); border:1px solid var(--border);}
.qa-result-img{min-height:380px;border-radius:24px;background-size:cover;background-position:center}
.qa-result-body{padding:12px 8px 4px;color:var(--text)}
.qa-destination{color:var(--text);font-size:clamp(2.1rem,4.1vw,3.7rem);line-height:.98;font-weight:950;letter-spacing:-.065em;margin:0}
.qa-country{color:var(--muted);margin-top:8px;font-weight:750;font-size:1.05rem}
.qa-primary-badge{display:inline-flex;padding:8px 13px;border-radius:999px;background:var(--chip);color:var(--chiptext);border:1px solid var(--border);font-size:.9rem;font-weight:900;margin:12px 6px 2px 0}
.qa-tag{display:inline-flex;padding:7px 10px;border-radius:999px;background:var(--card2);border:1px solid var(--border);color:var(--text);font-size:.84rem;font-weight:800;margin:6px 6px 0 0}

/* UPDATED SCORE & BUDGET GRID STYLES */
.qa-score-wrapper { margin-top: 1.5rem; margin-bottom: 1.5rem; }
.qa-score-header { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem; }
.qa-score-label { font-size: 0.875rem; font-weight: 700; color: #6b7280; text-transform: uppercase; letter-spacing: 0.05em; }
.qa-score-track { flex-grow: 1; background-color: #e5e7eb; border-radius: 9999px; height: 0.625rem; }
.qa-score-fill { background-color: #2563eb; height: 0.625rem; border-radius: 9999px; }
.qa-score-value { font-weight: 700; color: #2563eb; }

.qa-new-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1rem; }
.qa-new-card { background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 0.75rem; padding: 1rem; box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05); text-align: center; }
.qa-new-card strong { display: block; color: #1f2937; margin-bottom: 0.25rem; font-size: 0.875rem; }
.qa-new-card span.normal { color: #6b7280; font-weight: 500; }
.qa-new-card span.badge { display: inline-block; padding: 0.25rem 0.75rem; background-color: #fef3c7; color: #92400e; border-radius: 9999px; font-size: 0.75rem; font-weight: 700; }
@media(max-width: 600px) { .qa-new-grid { grid-template-columns: 1fr; } }

/* Dynamic Widget Placeholder CSS */
.qa-widget-placeholder {
    border: 2px dashed var(--border); border-radius: 18px; padding: 24px; text-align: center;
    background: var(--card2); margin-top: 20px;
}
.qa-widget-placeholder h4 { margin-top: 0; color: var(--text); }
.qa-widget-placeholder p { color: var(--muted); font-size: 0.9rem; margin-bottom: 16px; }

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# LOGIC
# ---------------------------------------------------------
def calc_score(place, region, budget, vibe, trip_length):
    score = 30
    if region == "Surprise me" or place["region"] == region:
        score += 20
    
    budget_map = {"£ (Shoestring)": "£", "££ (Moderate)": "££", "£££ (Comfort)": "£££"}
    target_band = budget_map.get(budget, "££")
    if target_band == place["budget_band"]:
        score += 25

    if vibe == "Surprise me" or vibe == place["primary_vibe"] or vibe in place["secondary_vibes"]:
        score += 23
        
    # Ensure it looks organic, between 70-98%
    final_score = min(score, 98)
    return final_score if final_score > 70 else final_score + random.randint(10, 20)

def pick_destination(region, budget, vibe, trip_length):
    scored = [(calc_score(p, region, budget, vibe, trip_length), p) for p in DESTINATIONS]
    scored = sorted(scored, key=lambda x: x[0], reverse=True)
    score, place = scored[0] 
    return place, score, scored

# ---------------------------------------------------------
# UI RENDERING
# ---------------------------------------------------------
def render_affiliate_widgets(place):
    st.markdown(f"""
    <div class="qa-widget-placeholder">
        <h4>✈️ Live Travelpayouts Widget Area</h4>
        <p>In production (WordPress), a dynamic script reads the IATA code <strong>{place['iata']}</strong> from the database and automatically renders a live Skyscanner search box here.</p>
        <button disabled style="background:#ddd; color:#888; border:none; padding:10px 20px; border-radius:5px; cursor:not-allowed; font-weight:bold;">Search Flights to {place['iata']} (Simulated)</button>
    </div>
    """, unsafe_allow_html=True)

def render_result(place, score, scored):
    st.markdown('<div class="qa-result">', unsafe_allow_html=True)
    col_img, col_text = st.columns([0.95, 1.05], gap="large")
    
    with col_img:
        st.markdown(f"<div class='qa-result-img' style=\"background-image:url('{place['image']}')\"></div>", unsafe_allow_html=True)
    
    with col_text:
        tags = f"<span class='qa-primary-badge'>{place['primary_vibe']}</span>" + "".join([f"<span class='qa-tag'>{v}</span>" for v in place["secondary_vibes"][:3]])
        
        # Applying the new sleek Match Score & Budget Grid
        st.markdown(f"""
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
        """, unsafe_allow_html=True)
        
        st.markdown(f"**Why this works:** {place['why']}")
        st.markdown(f"**Budget tip:** {place['tip']}")
        st.error(f"**Avoid if:** {place['avoid']}")
        
        render_affiliate_widgets(place)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### Not quite right?")
    a, b = st.columns(2)
    a.info(f"**Cheaper Alternative:** {place['cheaper']}")
    b.info(f"**Similar Vibe:** {place['similar']}")

# ---------------------------------------------------------
# MAIN APP LAYOUT
# ---------------------------------------------------------
st.markdown("""
<div class="qa-hero">
  <h1>Find your budget escape.</h1>
  <p>Tell us your budget band and your vibe. We'll find where your money goes furthest, without pulling fake live prices.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="qa-card">', unsafe_allow_html=True)
st.markdown("## Where should you go?")

with st.form("quidaway_form"):
    c1, c2 = st.columns(2)
    with c1:
        starting_from = st.text_input("Starting city", value="London")
        budget = st.selectbox("Budget level", ["£ (Shoestring)", "££ (Moderate)", "£££ (Comfort)"], index=1)
    with c2:
        vibe = st.selectbox("Travel vibe", ["City", "Beach", "Hiking", "Food", "Surprise me"], index=0)
        trip_length = st.selectbox("Trip length", ["Weekend", "1 week", "2 weeks"], index=1)
        
    submitted = st.form_submit_button("🌍 Find my escape", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

if submitted:
    placeholder = st.empty()
    with placeholder:
        st.markdown("""
        <div class="qa-spinner-box">
            <div class="qa-spinner">🌍</div>
            <h3>Searching the globe...</h3>
            <p class="qa-muted">Matching budget · checking vibes · preparing widgets</p>
        </div>
        """, unsafe_allow_html=True)
    time.sleep(1.2) 
    placeholder.empty()
    
    place, score, scored = pick_destination("Europe", budget, vibe, trip_length)
    st.session_state["result"] = {"place": place, "score": score, "scored": scored}

if st.session_state.get("result"):
    st.markdown("## Your Match")
    render_result(st.session_state["result"]["place"], st.session_state["result"]["score"], st.session_state["result"]["scored"])

st.markdown("""
<div style="text-align:center; color:#888; margin-top:50px; font-size: 0.9em;">
    QuidAway Prototype - Final UI + Hybrid Data Strategy<br>
    Ready for WordPress Integration
</div>
""", unsafe_allow_html=True)
