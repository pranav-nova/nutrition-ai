import streamlit as st
import os
from groq import Groq

st.set_page_config(page_title="Nutrition AI", page_icon="🥗", layout="centered")

client = Groq(api_key=os.getenv("GROQ_API_KEY") or st.secrets["GROQ_API_KEY"])

# ---------- SIMPLE UI ----------
st.title("🥗 Nutrition AI")

st.markdown("Analyze food ingredients and get health insights.")

ingredients = st.text_input("Ingredients (comma separated)")
calories = st.number_input("Calories", min_value=0)
sugar = st.number_input("Sugar (g)", min_value=0.0)
fat = st.number_input("Fat (g)", min_value=0.0)

# ---------- BUTTON ----------
if st.button("Analyze"):

    if not ingredients:
        st.warning("Please enter ingredients")
    else:
        with st.spinner("Analyzing..."):

            prompt = f"""
Analyze this food:

Ingredients: {ingredients}
Calories: {calories}
Sugar: {sugar}
Fat: {fat}

Give:
1. Ingredient explanation
2. Health impact
3. Score out of 100
4. Final verdict (Good/Moderate/Avoid)
"""

            try:
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                )

                output = res.choices[0].message.content

                st.success("Analysis Complete ✅")

                st.write(output)

            except Exception as e:
                st.error(f"Error: {e}")