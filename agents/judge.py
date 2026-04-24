def judge_output(output):
    prompt = f"""
You are an evaluator.

Evaluate the following nutrition analysis using this rubric:

Criteria (each out of 25):
1. Accuracy (0-25)
2. Completeness (0-25)
3. Clarity (0-25)
4. Practical Usefulness (0-25)

Total score out of 100.

Return STRICTLY in this format:

Accuracy: X/25  
Completeness: X/25  
Clarity: X/25  
Usefulness: X/25  
Total: X/100  

Feedback:
Short explanation

Text:
{output}
"""

    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return res.choices[0].message.content