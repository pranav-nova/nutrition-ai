def analyze_nutrition(nutrition):
    analysis = {}

    if nutrition.get("sugar", 0) > 25:
        analysis["sugar"] = "High sugar intake (risk of diabetes if frequent)"

    if nutrition.get("fat", 0) > 10:
        analysis["fat"] = "High fat content (may affect heart health)"

    if nutrition.get("calories", 0) > 200:
        analysis["calories"] = "High calorie food (can lead to weight gain)"

    if not analysis:
        analysis["overall"] = "Nutritional values are within moderate range"

    return analysis