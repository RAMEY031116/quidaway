import random
import time
import streamlit as st

st.set_page_config(
    page_title="QuidAway | Budget Escape Finder",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

APP_VERSION = "wordpress-mockup-final-v4"
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

/* Header Navbar */
.qa-header-nav { display: flex; justify-content: space-between; align-items: center; padding: 10px 15px 30px 15px; }
.qa-logo { font-size: 1.8rem; font-weight: 900; color: var(--primary); letter-spacing: -1px; }
.qa-tagline { font-size: 0.95rem; font-weight: 600; color: var(--muted); display: none; }
@media(min-width: 600px) { .qa-tagline { display: block; } }

.qa-hero{border-radius:32px;padding:52px 44px;margin-bottom:26px;color:#fff;background:linear-gradient(135deg,rgba(5,10,20,.88),rgba(20,45,65,.80)),url('https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1800&q=80');background-size:cover;background-position:center;box-shadow:0 24px 60px var(--shadow)}
.qa-hero h1{color:#fff;font-size:clamp(2.55rem,5.3vw,5.1rem);line-height:.96;margin:0 0 16px;font-weight:950;letter-spacing:-.07em}
.qa-hero p{color:#e6eef8;max-width:800px;font
