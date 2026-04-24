def judge_output(output):
    score = 0
    feedback = []

    if "ingredient" in output.lower():
        score += 1
    else:
        feedback.append("Missing ingredient explanation")

    if "health" in output.lower():
        score += 1
    else:
        feedback.append("Missing health impact")

    if "verdict" in output.lower():
        score += 1
    else:
        feedback.append("Missing final verdict")

    return {
        "score": f"{score}/3",
        "feedback": feedback if feedback else ["Good explanation"]
    }