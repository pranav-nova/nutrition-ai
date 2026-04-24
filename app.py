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

# ---------- FUNCTIONS ----------

def generate_analysis(ingredients, nutrition_text):

    prompt = f"""
You are a professional nutrition expert.

Analyze this product:

INGREDIENTS:
{ingredients}

NUTRITION LABEL:
{nutrition_text}

Give output EXACTLY in this format:

🧪 Ingredient Breakdown:
...

⚡ Health Impact:
...

📊 Nutritional Analysis:
...

📈 Score:
(number only)

🏁 Final Verdict:
(Good / Moderate / Avoid)
"""

    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return res.choices[0].message.content


def judge_output(output):
    prompt = f"""
Evaluate this nutrition analysis.

Criteria:
Accuracy (0-10)
Clarity (0-10)
Usefulness (0-10)

Return format:

Accuracy: X/10
Clarity: X/10
Usefulness: X/10
Total: X/30
Feedback: short

Text:
{output}
"""

    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )

    return res.choices[0].message.content


# ---------- UI ----------

st.title("🥗 Nutrition AI Analyzer")

st.markdown("Paste full ingredient list and nutrition label for detailed analysis.")

ingredients = st.text_area("🧾 Ingredients")

nutrition_text = st.text_area("📊 Nutrition Facts")

if st.button("Analyze"):

    if not ingredients or not nutrition_text:
        st.warning("⚠️ Please fill both fields")
    else:

        with st.spinner("Analyzing..."):
            result = generate_analysis(ingredients, nutrition_text)

        # ---------- PARSE ----------
        try:
            sections = result.split("📈 Score:")
            main_text = sections[0]

            score_part = sections[1].split("\n")[0].strip()

            verdict = result.split("🏁 Final Verdict:")[1].strip()

        except:
            main_text = result
            score_part = "N/A"
            verdict = "N/A"

        # ---------- DISPLAY ----------

        st.success("✅ Analysis Complete")

        st.markdown("### 🧪 Ingredient & Health Analysis")
        st.write(main_text)

        st.markdown("### 📊 Score")
        st.success(f"{score_part} / 100")

        st.markdown("### 🏁 Final Verdict")

        if "Good" in verdict:
            st.success(verdict)
        elif "Moderate" in verdict:
            st.warning(verdict)
        else:
            st.error(verdict)

        # ---------- JUDGE ----------
        with st.spinner("Evaluating quality..."):
            judge = judge_output(result)

        st.markdown("### 🧠 LLM Evaluation")
        st.info(judge)