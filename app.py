import streamlit as st
import os
import re
from groq import Groq
from dotenv import load_dotenv
from agents.judge import judge_output   # 👈 import judge agent

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

# ---------- ANALYSIS ----------
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

FINAL VERDICT:
(Good / Moderate / Avoid)
"""

    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return res.choices[0].message.content


# ---------- PARSER ----------
def parse_output(result):
    try:
        ingredient = result.split("INGREDIENT BREAKDOWN:")[1].split("HEALTH IMPACT:")[0].strip()
        health = result.split("HEALTH IMPACT:")[1].split("SCORE:")[0].strip()

        # robust score extraction
        score_match = re.search(r"\b\d{1,3}\b", result)
        score = score_match.group() if score_match else "N/A"

        verdict = result.split("FINAL VERDICT:")[1].strip()

        return ingredient, health, score, verdict

    except:
        return result, "", "N/A", "N/A"


# ---------- UI ----------
st.title("🥗 Nutrition AI Analyzer")
st.caption("Paste full ingredients + nutrition label below.")

# ✅ SINGLE INPUT BOX
user_input = st.text_area("Food Label Input")

# ---------- BUTTON ----------
if st.button("Analyze"):

    if not user_input:
        st.warning("⚠️ Please enter food label data")
    else:
        with st.spinner("Analyzing..."):
            result = generate_analysis(user_input)

        ingredient, health, score, verdict = parse_output(result)

        # 👇 LLM Judge (from separate agent)
        with st.spinner("Evaluating quality..."):
            judge = judge_output(result, client)

        st.success("Analysis Complete ✅")

        # ---------- OUTPUT ----------
        st.markdown("### 🧪 Ingredient Breakdown")
        st.write(ingredient)

        st.markdown("### ⚡ Health Impact")
        st.write(health)

        st.markdown("### 📊 Nutrition Score")
        st.metric("Score", f"{score} / 100")

        st.markdown("### 🏁 Final Verdict")
        if "good" in verdict.lower():
            st.success(verdict)
        elif "moderate" in verdict.lower():
            st.warning(verdict)
        else:
            st.error(verdict)

        st.markdown("---")

        # ---------- JUDGE OUTPUT ----------
        st.markdown("### 🧠 Evaluation (LLM Judge)")
        st.info(judge)