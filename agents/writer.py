from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_explanation(research, nutrition_analysis):

    prompt = f"""
You are a nutrition expert.

Ingredient Research:
{research}

Nutrition Analysis:
{nutrition_analysis}

Explain clearly:
- Each ingredient meaning
- Health impact
- Final verdict (Good / Moderate / Avoid)
"""

    models_to_try = [
        "mixtral-8x7b-32768",
        "gemma2-9b-it",
        "llama-3.1-8b-instant"
    ]

    for m in models_to_try:
        try:
            response = client.chat.completions.create(
                model=m,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"{m} failed:", e)

    return "Error: No working model available"