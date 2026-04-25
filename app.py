import streamlit as st
import os
import re
from groq import Groq
from dotenv import load_dotenv
from agents.judge import judge_output

load_dotenv()

st.set_page_config(page_title="Nutrition AI", page_icon="🥗", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

#MainMenu, footer, header { visibility: hidden; }

section.main > div {
    background: #0a1612;
    padding-top: 0 !important;
}

.hero {
    background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 50%, #40916c 100%);
    border-radius: 20px;
    padding: 2.5rem 2rem 2rem;
    text-align: center;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "";
    position: absolute; inset: 0;
    background: radial-gradient(ellipse at 20% 50%, rgba(255,255,255,0.06) 0%, transparent 60%),
                radial-gradient(ellipse at 80% 20%, rgba(255,255,255,0.04) 0%, transparent 50%);
}
.hero-emoji-row {
    font-size: 2rem;
    letter-spacing: 0.4rem;
    margin-bottom: 0.75rem;
    filter: drop-shadow(0 2px 6px rgba(0,0,0,0.3));
}
.hero h1 {
    font-family: 'Playfair Display', serif;
    color: #d8f3dc;
    font-size: 2.4rem;
    margin: 0 0 0.4rem;
    line-height: 1.2;
}
.hero p {
    color: #95d5b2;
    font-size: 1rem;
    margin: 0;
}

.badge-row {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    justify-content: center;
    margin-top: 1rem;
}
.badge {
    background: rgba(255,255,255,0.12);
    color: #b7e4c7;
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.78rem;
    font-weight: 500;
}

.input-card {
    background: #112218;
    border-radius: 16px;
    padding: 1.75rem;
    border: 1px solid #2d6a4f;
    box-shadow: 0 2px 16px rgba(0,0,0,0.3);
    margin-bottom: 1.5rem;
}
.input-label {
    font-weight: 600;
    color: #74c69d;
    font-size: 0.95rem;
    margin-bottom: 0.5rem;
}

.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 2rem 0 0.75rem;
}
.section-icon {
    width: 36px; height: 36px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    flex-shrink: 0;
}
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.25rem;
    color: #95d5b2;
    margin: 0;
}

.result-card {
    background: #112218;
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    border: 1px solid #2d6a4f;
    box-shadow: 0 1px 8px rgba(0,0,0,0.25);
    line-height: 1.75;
    color: #d8f3dc;
    font-size: 0.93rem;
}

.score-wrapper {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    background: #112218;
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    border: 1px solid #2d6a4f;
    box-shadow: 0 1px 8px rgba(0,0,0,0.25);
}
.score-label {
    font-size: 0.82rem;
    color: #52796f;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 2px;
}
.score-value {
    font-family: 'Playfair Display', serif;
    font-size: 2.6rem;
    color: #d8f3dc;
    line-height: 1;
}
.score-sub {
    font-size: 0.85rem;
    color: #74c69d;
    margin-top: 4px;
}

.fancy-divider {
    text-align: center;
    margin: 2rem 0;
    color: #2d6a4f;
    font-size: 1.4rem;
    letter-spacing: 0.5rem;
}

.verdict-card {
    background: linear-gradient(160deg, #061009 0%, #112218 100%);
    border-radius: 16px;
    padding: 2rem;
    border: 1px solid #2d6a4f;
    border-left: 5px solid #52b788;
    font-family: 'Courier New', monospace;
    color: #d8f3dc;
    white-space: pre-wrap;
    line-height: 1.85;
    font-size: 0.875rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    position: relative;
    overflow: hidden;
}
.verdict-card::before {
    content: "✦";
    position: absolute;
    top: 1rem; right: 1.25rem;
    font-size: 1.5rem;
    color: rgba(82,183,136,0.2);
}

.info-strip {
    display: flex;
    gap: 10px;
    margin-top: 1.5rem;
    flex-wrap: wrap;
}
.info-chip {
    background: #112218;
    border: 1px solid #2d6a4f;
    border-radius: 10px;
    padding: 8px 14px;
    font-size: 0.8rem;
    color: #74c69d;
    display: flex;
    align-items: center;
    gap: 6px;
}

div.stButton > button {
    background: linear-gradient(135deg, #2d6a4f, #40916c) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.65rem 2.5rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    font-family: 'DM Sans', sans-serif !important;
    letter-spacing: 0.02em !important;
    transition: opacity 0.2s !important;
    width: 100% !important;
}
div.stButton > button:hover {
    opacity: 0.88 !important;
}

textarea {
    border-radius: 10px !important;
    border: 1.5px solid #40916c !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.92rem !important;
    background: #1a2e22 !important;
    color: #d8f3dc !important;
    caret-color: #52b788 !important;
}
textarea:focus {
    border-color: #52b788 !important;
    box-shadow: 0 0 0 3px rgba(82,183,136,0.2) !important;
}
textarea::placeholder {
    color: #52796f !important;
    opacity: 1 !important;
}

/* Success / warning / error box dark theme */
div[data-testid="stAlert"] {
    background: #112218 !important;
    border: 1px solid #2d6a4f !important;
    color: #d8f3dc !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)


# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-emoji-row">🥦 🫐 🥑 🍋 🥕 🫒 🍎</div>
    <h1>Nutrition AI Analyzer</h1>
    <p>Clinical-grade food label analysis powered by AI</p>
    <div class="badge-row">
        <span class="badge">🔬 Ingredient Scan</span>
        <span class="badge">📊 Nutrient Scoring</span>
        <span class="badge">🩺 Health Impact</span>
        <span class="badge">⚖️ Expert Verdict</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ── How it works ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="info-strip">
    <div class="info-chip">🥗 Paste any food label</div>
    <div class="info-chip">🤖 AI analyzes ingredients</div>
    <div class="info-chip">🧠 Expert model evaluates</div>
    <div class="info-chip">✅ Get your verdict</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ── Input ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="input-label">📋 Paste your food label / ingredients list below</div>',
            unsafe_allow_html=True)

user_input = st.text_area(
    label="food_label",
    label_visibility="collapsed",
    placeholder="e.g.  Ingredients: Enriched flour, sugar, palm oil, cocoa, soy lecithin...\nCalories: 210  |  Fat: 11g  |  Sodium: 140mg  |  Sugar: 12g",
    height=180,
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze_btn = st.button("🔍  Analyze Now")


# ── API setup ──────────────────────────────────────────────────────────────────
def get_api_key():
    key = os.getenv("GROQ_API_KEY")
    if not key:
        try:
            key = st.secrets["GROQ_API_KEY"]
        except:
            return None
    return key

api_key = get_api_key()
if not api_key:
    st.error("❌ GROQ_API_KEY not found")
    st.stop()

client = Groq(api_key=api_key)


# ── Core functions ─────────────────────────────────────────────────────────────
def generate_analysis(input_text):
    prompt = f"""
You are a professional nutrition expert.
Analyze this food label:
{input_text}
Return STRICTLY in this format:
INGREDIENT BREAKDOWN:
...
HEALTH IMPACT:
...
SCORE:
Return ONLY a number between 0 and 100
"""
    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    return res.choices[0].message.content


def parse_output(result):
    try:
        ingredient = result.split("INGREDIENT BREAKDOWN:")[1].split("HEALTH IMPACT:")[0].strip()
        health = result.split("HEALTH IMPACT:")[1].split("SCORE:")[0].strip()
        score_match = re.search(r"\b\d{1,3}\b", result)
        score = score_match.group() if score_match else "N/A"
        return ingredient, health, score
    except:
        return result, "", "N/A"


def score_color(score_str):
    try:
        s = int(score_str)
        if s >= 70: return "#52b788", "Healthy", "🟢"
        if s >= 40: return "#f4a261", "Moderate", "🟡"
        return "#e63946", "Poor", "🔴"
    except:
        return "#74c69d", "N/A", "⚪"


# ── Results ────────────────────────────────────────────────────────────────────
if analyze_btn:
    if not user_input.strip():
        st.warning("⚠️ Please enter food label data before analyzing.")
    else:
        with st.spinner("🔬 Scanning ingredients and nutrients..."):
            result = generate_analysis(user_input)

        ingredient, health, score = parse_output(result)

        with st.spinner("🧠 Running expert clinical evaluation..."):
            judge = judge_output(result, client)

        st.success("✅ Analysis complete!")

        # Ingredient Breakdown
        st.markdown("""
        <div class="section-header">
            <div class="section-icon" style="background:#1b4332;">🧪</div>
            <h3 class="section-title">Ingredient Breakdown</h3>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<div class="result-card">{ingredient}</div>', unsafe_allow_html=True)

        # Health Impact
        st.markdown("""
        <div class="section-header">
            <div class="section-icon" style="background:#1b4332;">⚡</div>
            <h3 class="section-title">Health Impact</h3>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<div class="result-card">{health}</div>', unsafe_allow_html=True)

        # Score ring
        ring_color, rating_label, rating_icon = score_color(score)
        st.markdown("""
        <div class="section-header">
            <div class="section-icon" style="background:#1b4332;">📊</div>
            <h3 class="section-title">Nutrition Score</h3>
        </div>
        """, unsafe_allow_html=True)

        try:
            score_int = int(score)
        except:
            score_int = 0

        circumference = 2 * 3.14159 * 34
        offset = circumference * (1 - score_int / 100)

        st.markdown(f"""
        <div class="score-wrapper">
            <svg width="90" height="90" viewBox="0 0 80 80">
              <circle cx="40" cy="40" r="34" fill="none" stroke="#1b4332" stroke-width="8"/>
              <circle cx="40" cy="40" r="34" fill="none" stroke="{ring_color}" stroke-width="8"
                stroke-dasharray="{circumference:.2f}"
                stroke-dashoffset="{offset:.2f}"
                stroke-linecap="round"
                transform="rotate(-90 40 40)"/>
              <text x="40" y="45" text-anchor="middle" font-size="16" font-weight="700"
                fill="{ring_color}" font-family="DM Sans, sans-serif">{score}</text>
            </svg>
            <div>
                <div class="score-label">Overall Score</div>
                <div class="score-value">{score}<span style="font-size:1.2rem;color:#52796f;"> / 100</span></div>
                <div class="score-sub">{rating_icon} {rating_label} nutritional profile</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Divider
        st.markdown('<div class="fancy-divider">🌿 · · · 🌿</div>', unsafe_allow_html=True)

        # Final Verdict
        st.markdown("""
        <div class="section-header">
            <div class="section-icon" style="background:#1b4332;">🧠</div>
            <h3 class="section-title">Final Verdict</h3>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            f'<div class="verdict-card">{judge}</div>',
            unsafe_allow_html=True,
        )

        # Footer
        st.markdown("""
        <div style="text-align:center; margin-top:2.5rem; padding-top:1.5rem;
                    border-top:1px solid #1b4332; color:#2d6a4f; font-size:0.82rem;">
            🥗 Nutrition AI &nbsp;·&nbsp; Powered by LLaMA 3.3 &nbsp;·&nbsp; For informational purposes only
        </div>
        """, unsafe_allow_html=True)