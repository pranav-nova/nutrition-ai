import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# ---------- LOAD ENV ----------
load_dotenv()

st.set_page_config(page_title="Nutrition AI", page_icon="🥗", layout="centered")

# ---------- API KEY ----------
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

# ---------- ANALYSIS FUNCTION ----------
def generate_analysis(ingredients, nutrition_text):

    prompt = f"""
You are a nutrition expert.

Analyze this product:

Ingredients:
{ingredients}

Nutrition Label:
{nutrition_text}

Give output clearly including:
- Ingredient explanation
- Health impact
- Final verdict (Good / Moderate / Avoid)
"""

    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return res.choices[0].message.content


# ---------- SIMPLE JUDGE ----------
def judge_output(output):
    score = 0
    feedback = []

    text = output.lower()

    if "ingredient" in text:
        score += 1
    else:
        feedback.append("Missing ingredient explanation")

    if "health" in text:
        score += 1
    else:
        feedback.append("Missing health impact")

    if "verdict" in text:
        score += 1
    else:
        feedback.append("Missing final verdict")

    return {
        "score": f"{score}/3",
        "feedback": feedback if feedback else ["Good explanation"]
    }


# ---------- UI ----------
st.title("🥗 Nutrition Label Analyzer")

st.markdown("Paste ingredients and nutrition facts to get analysis.")

ingredients = st.text_area("🧾 Ingredients")
nutrition_text = st.text_area("📊 Nutrition Facts")

# ---------- BUTTON ----------
if st.button("Analyze"):

    if not ingredients or not nutrition_text:
        st.warning("⚠️ Please fill both fields")
    else:
        with st.spinner("Analyzing..."):
            result = generate_analysis(ingredients, nutrition_text)

        # Judge
        judge = judge_output(result)

        # ---------- SINGLE OUTPUT BOX ----------
        st.markdown("### 📦 Final Output")

        st.text_area(
            "Result + Evaluation",
            f"""{result}

------------------------
Evaluation Score: {judge["score"]}

Feedback:
- {"\n- ".join(judge["feedback"])}
""",
            height=400
        )