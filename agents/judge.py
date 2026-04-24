# agents/judge.py

def judge_output(output, client):
    prompt = f"""
You are an expert evaluator.

You will:
1. Evaluate the quality of the analysis
2. Compare ingredient breakdown and health impact
3. Give a FINAL CONCLUSION

Rubric (each out of 25):
- Accuracy
- Completeness
- Clarity
- Practical Usefulness

Total score out of 100.

Return STRICTLY in this format:

Accuracy: X/25  
Completeness: X/25  
Clarity: X/25  
Usefulness: X/25  
Total: X/100  

Final Conclusion:
(Give a clear final decision: Good / Moderate / Avoid with reasoning)

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