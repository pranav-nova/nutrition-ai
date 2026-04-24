from tools.tavily_tool import search_ingredient

def research_ingredients(ingredients):
    results = {}

    for item in ingredients:
        query = f"What is {item} and is it healthy?"
        results[item] = search_ingredient(query)

    return results