import streamlit as st
from agents.researcher import research_ingredients
from agents.analyst import analyze_nutrition
from agents.writer import generate_explanation

st.set_page_config(page_title="Nutrition AI", layout="centered")

# 🎨 FULL POLISHED UI
st.markdown("""
<style>

/* Remove top spacing */
.block-container {
    padding-top: 0rem;
}

/* Hide header/footer */
header {visibility: hidden;}
footer {visibility: hidden;}

/* Background */
.stApp {
    background: radial-gradient(circle at center, #1e3a8a, #020617);
    color: white;
}

/* Glass card */
.card {
    background: rgba(255,255,255,0.08);
    padding: 30px;
    border-radius: 20px;
    backdrop-filter: blur(20px);
    width: 420px;
    margin: auto;
    margin-top: 40px;
    box-shadow: 0 0 40px rgba(0,0,0,0.6);
}

/* Title */
.title {
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    margin-bottom: 20px;
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 10px;
    width: 100%;
    padding: 10px;
    font-weight: bold;
}

/* Result card */
.result-card {
    background: rgba(0,0,0,0.4);
    padding: 15px;
    border-radius: 10px;
    margin-top: 15px;
}

/* Badge */
.badge {
    padding: 6px 12px;
    border-radius: 8px;
    font-weight: bold;
    display: inline-block;
    margin-top: 10px;
}

.good {background: #16a34a;}
.moderate {background: #eab308;}
.bad {background: #dc2626;}

</style>
""", unsafe_allow_html=True)

# 🧊 UI START
st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown('<div class="title">🥗 Nutrition AI</div>', unsafe_allow_html=True)

ingredients = st.text_input("Ingredients (comma separated)")
calories = st.number_input("Calories", min_value=0)
sugar = st.number_input("Sugar (g)", min_value=0)
fat = st.number_input("Fat (g)", min_value=0)

# 🔍 BUTTON
if st.button("Analyze"):

    if not ingredients:
        st.warning("Please enter ingredients")
    else:
        ingredient_list = [i.strip() for i in ingredients.split(",")]

        with st.spinner("Analyzing..."):
            research = research_ingredients(ingredient_list)

            nutrition_data = {
                "calories": calories,
                "sugar": sugar,
                "fat": fat
            }

            analysis = analyze_nutrition(nutrition_data)

            explanation = generate_explanation(research, analysis)

        # 🎯 Verdict detection
        verdict = "Moderate"
        if "avoid" in explanation.lower():
            verdict = "Avoid"
        elif "good" in explanation.lower():
            verdict = "Good"

        # 🎨 RESULT DISPLAY
        st.markdown('<div class="result-card">', unsafe_allow_html=True)

        st.markdown("### 📊 Analysis Result")
        st.write(explanation)

        # Badge
        if verdict == "Good":
            st.markdown('<div class="badge good">✔ Good</div>', unsafe_allow_html=True)
        elif verdict == "Avoid":
            st.markdown('<div class="badge bad">✖ Avoid</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="badge moderate">⚠ Moderate</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)