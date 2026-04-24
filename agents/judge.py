def judge_output(output, client):
    prompt = f"""
You are a Senior Nutrition Scientist and Food Safety Expert with 20+ years of clinical experience.
You have received a nutrition analysis report. Your task is to evaluate it rigorously and professionally across three core dimensions, then deliver a final clinical-grade conclusion.
---
EVALUATION RUBRIC:
1. INGREDIENT BREAKDOWN ASSESSMENT (0-30 pts)
   - Are ingredients correctly identified and categorized?
   - Are harmful additives, preservatives, or allergens flagged?
   - Is processing level (whole food vs ultra-processed) noted?
   - Quality score: X/30
2. NUTRITIONAL SCORE ASSESSMENT (0-30 pts)
   - Is the score (0-100) justified based on macro/micronutrients?
   - Are calorie density, sugar, sodium, and fat levels addressed?
   - Is the score consistent with the ingredient and health data?
   - Quality score: X/30
3. HEALTH IMPACT ASSESSMENT (0-40 pts)
   - Are short-term and long-term effects discussed?
   - Are risks for specific populations (diabetics, heart patients, children) mentioned?
   - Is the advice actionable and evidence-based?
   - Quality score: X/40
---
RETURN STRICTLY IN THIS FORMAT:
FINAL VERDICT
INGREDIENT BREAKDOWN REVIEW:
[2-3 sentences evaluating ingredient quality, red flags, additives]
Score: X / 30
NUTRITIONAL SCORE REVIEW:
[2-3 sentences on whether the score is justified, key nutrient concerns]
Score: X / 30
HEALTH IMPACT REVIEW:
[2-3 sentences on health implications, population risks, evidence quality]
Score: X / 40
---------------------------------------------------
OVERALL EVALUATION SCORE: X / 100
---------------------------------------------------
FINAL CLINICAL CONCLUSION:
[One of: RECOMMENDED | CONSUME WITH CAUTION | NOT RECOMMENDED]
Verdict: (One clear sentence)
Clinical Reasoning:
(2-4 sentences explaining the verdict with specific nutritional evidence)
Recommended For: (e.g., Healthy adults, Athletes)
Avoid If: (e.g., High blood pressure, Kidney disease, Pregnant women)
EXPERT RECOMMENDATION:
(One actionable tip - e.g., healthier substitute or consumption limit)
Analysis to evaluate:
{output}
"""
    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return res.choices[0].message.content