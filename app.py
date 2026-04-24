import streamlit as st
import os
from groq import Groq
from tavily import TavilyClient
from dotenv import load_dotenv

# ---------- LOAD ENV ----------
load_dotenv()

st.set_page_config(page_title="Nutrition Label Explainer", page_icon="🥗", layout="centered")

# ---------- SAFE API KEYS ----------
def get_key(name):
    val = os.getenv(name)
    if not val:
        try:
            val = st.secrets[name]
        except:
            return None
    return val

GROQ_API_KEY = get_key("GROQ_API_KEY")
TAVILY_API_KEY = get_key("TAVILY_API_KEY")

if not GROQ_API_KEY:
    st.error("Missing GROQ_API_KEY")
    st.stop()

if not TAVILY_API_KEY:
    st.warning("TAVILY_API_KEY not found (ingredient research will be basic)")

# ---------- CLIENTS ----------
groq_client = Groq(api_key=GROQ_API_KEY)

tavily_client = None
if TAVILY_API_KEY:
    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

# ---------- FUNCTIONS ----------
def research_ingredient(name):
    if not tavily_client:
        return f"{name}: general food ingredient."

    try:
        res = tavily_client.search(query=name, search_depth="basic")
        return res["results"][0]["content"]
    except:
        return f"{name}: info not found."

def generate_analysis(ingredients, calories, sugar, fat):

    research_text = "\n".join([research_ingredient(i) for i in ingredients])

    prompt = f"""
Analyze this food:

Ingredients: {", ".join(ingredients)}
Calories: {calories}
Sugar: {sugar}
Fat: {fat}

Ingredient info:
{research_text}

Give:
1. Ingredient Breakdown
2. Health Impact
3. Score (0-100)
4. Final Verdict (Good / Moderate / Avoid)
"""

    try:
        res = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# ---------- UI ----------
st.title("🥗 Nutrition Label Explainer")

st.markdown("Analyze ingredients and understand health impact.")

ingredients_input = st.text_input("Ingredients (comma separated)")
calories = st.number_input("Calories", min_value=0)
sugar = st.number_input("Sugar (g)", min_value=0.0)
fat = st.number_input("Fat (g)", min_value=0.0)

if st.button("Analyze"):

    if not ingredients_input:
        st.warning("Please enter ingredients")
    else:
        ingredients = [i.strip() for i in ingredients_input.split(",")]

        with st.spinner("Analyzing..."):
            result = generate_analysis(ingredients, calories, sugar, fat)

        st.success("Analysis Complete ✅")
        st.write(result)