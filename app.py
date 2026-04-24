import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# ---------- LOAD ENV ----------
load_dotenv()

st.set_page_config(page_title="Nutrition AI", page_icon="🥗", layout="centered")

# ---------- API KEY ----------
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except:
        st.error("Missing GROQ_API_KEY")
        st.stop()

client = Groq(api_key=api_key)

# ---------- FUNCTIONS ----------

def generate_analysis(ingredients, calories, sugar, fat):
    prompt = f"""
Analyze this food:

Ingredients: {ingredients}
Calories: {calories}
Sugar: {sugar}
Fat: {fat}

Give output in this format:

Ingredient Breakdown:
...

Health Impact:
...

Score: (just number)

Final Verdict: (Good / Moderate / Avoid)
"""

    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return res.choices[0].message.content


def judge_output(output):
    prompt = f"""
Evaluate this nutrition explanation.

Criteria:
- Accuracy (0-10)
- Clarity (0-10)
- Usefulness (0-10)

Return format:

Accuracy: X/10
Clarity: X/10
Usefulness: X/10
Total: X/30
Feedback: short explanation

Text:
{output}
"""

    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )

    return res.choices[0].message.content


# ---------- UI ----------

st.title("🥗 Nutrition AI")

ingredients = st.text_input("Ingredients (comma separated)")
calories = st.number_input("Calories", min_value=0)
sugar = st.number_input("Sugar (g)", min_value=0.0)
fat = st.number_input("Fat (g)", min_value=0.0)

if st.button("Analyze"):

    if not ingredients:
        st.warning("Please enter ingredients")
    else:
        with st.spinner("Analyzing..."):

            result = generate_analysis(ingredients, calories, sugar, fat)

        # ---------- PARSE OUTPUT ----------
        try:
            parts = result.split("Score:")
            main_text = parts[0]
            score_part = parts[1].split("\n")[0].strip()

            verdict = result.split("Final Verdict:")[1].strip()

        except:
            main_text = result
            score_part = "N/A"
            verdict = "N/A"

        # ---------- DISPLAY ----------

        st.success("Analysis Complete ✅")

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

        # ---------- LLM JUDGE ----------
        with st.spinner("Evaluating quality..."):
            judge = judge_output(result)

        st.markdown("### 🧠 Evaluation (LLM Judge)")
        st.info(judge)