def judge_output(output):
    prompt = f"""
You are an evaluator.

Evaluate this nutrition explanation:

Criteria:
1. Accuracy (0-10)
2. Clarity (0-10)
3. Practical usefulness (0-10)

Return in format:

Accuracy: X/10  
Clarity: X/10  
Usefulness: X/10  
Total: X/30  
Feedback: short explanation

Text:
{output}
"""
    res = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )

    return res.choices[0].message.content