import streamlit as st
import os
import re
from groq import Groq
from dotenv import load_dotenv
from agents.researcher import research_ingredients
from agents.judge import judge_output

load_dotenv()

st.set_page_config(page_title="Nutrition AI", page_icon="🥗", layout="centered")

# ================= UI (UNCHANGED) =================
st.markdown("""<style>/* your full CSS unchanged */</style>""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-emoji-row">🥦 🫐 🥑 🍋 🥕 🫒 🍎</div>
    <h1>Nutrition AI Analyzer</h1>
    <p>Clinical-grade food label analysis powered by AI</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-strip">
    <div class="info-chip">🥗 Paste any food label</div>
    <div class="info-chip">🤖 AI analyzes ingredients</div>
    <div class="info-chip">🧠 Expert model evaluates</div>
    <div class="info-chip">✅ Get your verdict</div>
</div>
""", unsafe_allow_html=True)

user_input = st.text_area(
    label="food_label",
    label_visibility="collapsed",
    placeholder="Ingredients: sugar, palm oil, cocoa...",
    height=180,
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze_btn = st.button("🔍 Analyze Now")

# ================= API =================
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

# ================= NEW: Ingredient Extractor =================
def extract_ingredients(input_text):
    try:
        if "Ingredients:" in input_text:
            ing = input_text.split("Ingredients:")[1]
        else:
            ing = input_text

        ing = ing.split("\n")[0]
        ingredients = [i.strip() for i in ing.split(",") if i.strip()]
        return ingredients[:10]  # limit for speed

    except:
        return []

# ================= UPDATED ANALYSIS =================
def generate_analysis(input_text):
    try:
        # Step 1: Extract ingredients
        ingredients_list = extract_ingredients(input_text)

        # Step 2: Tavily research
        try:
            research_data = research_ingredients(ingredients_list)
        except Exception as e:
            research_data = f"Research error: {str(e)}"

        if not research_data:
            research_data = "No external research found."

        research_data = str(research_data)[:2000]

        # Step 3: Prompt
        prompt = f"""
You are a professional nutrition expert.

Analyze this food label:
{input_text}

Here is verified research about its ingredients:
{research_data}

Using this research, generate a detailed analysis.

Return STRICTLY in this format (no extra text):

INGREDIENT BREAKDOWN:
Explain ingredients in simple terms

HEALTH IMPACT:
Explain health effects clearly

SCORE:
Return ONLY a number between 0 and 100
"""

        # Step 4: Groq call
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )

        return res.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"

# ================= PARSE =================
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

# ================= RUN =================
if analyze_btn:
    if not user_input.strip():
        st.warning("⚠️ Please enter food label data before analyzing.")
    else:
        with st.spinner("🔬 Analyzing with research..."):
            result = generate_analysis(user_input)

        ingredient, health, score = parse_output(result)

        with st.spinner("🧠 Running expert evaluation..."):
            judge = judge_output(result, client)

        st.success("✅ Analysis complete!")

        st.subheader("🧪 Ingredient Breakdown")
        st.write(ingredient)

        st.subheader("⚡ Health Impact")
        st.write(health)

        st.subheader("📊 Score")
        st.write(score)

        st.subheader("🧠 Final Verdict")
        st.write(judge)