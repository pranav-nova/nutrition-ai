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

# ---------- ANALYSIS ----------
def generate_analysis(input_text):
    prompt = f"""
You are a professional nutrition expert.

Analyze the following food label:

{input_text}

Return STRICTLY in this format:

INGREDIENT BREAKDOWN:
...

HEALTH IMPACT:
...

SCORE:
(number only)

FINAL VERDICT:
(Good / Moderate / Avoid)
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

# ---------- PARSER ----------
def parse_output(result):
    try:
        parts = result.split("SCORE:")
        top = parts[0]
        score = parts[1].split("\n")[0].strip()

        ingredient = top.split("INGREDIENT BREAKDOWN:")[1].split("HEALTH IMPACT:")[0].strip()
        health = top.split("HEALTH IMPACT:")[1].strip()

        verdict = result.split("FINAL VERDICT:")[1].strip()

        return ingredient, health, score, verdict
    except:
        return result, "", "N/A", "N/A"

# ---------- UI ----------
st.title("🥗 Nutrition AI Analyzer")
st.caption("Paste full ingredients + nutrition label below.")

# ONE INPUT BOX
user_input = st.text_area("Food Label Input")

if st.button("Analyze"):

    if not user_input:
        st.warning("⚠️ Please enter food label data")
    else:
        with st.spinner("Analyzing..."):
            result = generate_analysis(user_input)

        ingredient, health, score, verdict = parse_output(result)
        judge = judge_output(result)

        st.success("Analysis Complete ✅")

        # ---------- PROFESSIONAL OUTPUT ----------
        st.markdown("### 🧪 Ingredient Breakdown")
        st.write(ingredient)

        st.markdown("### ⚡ Health Impact")
        st.write(health)

        st.markdown("### 📊 Nutrition Score")
        st.metric(label="Score", value=f"{score}/100")

        st.markdown("### 🏁 Final Verdict")
        if "good" in verdict.lower():
            st.success(verdict)
        elif "moderate" in verdict.lower():
            st.warning(verdict)
        else:
            st.error(verdict)

        st.markdown("---")

        # ---------- JUDGE ----------
        st.markdown("### 🧠 Evaluation (Judge)")
        st.write(f"Score: {judge['score']}")
        for f in judge["feedback"]:
            st.write(f"- {f}")