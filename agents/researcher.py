from tools.tavily_tool import search_ingredient

def research_ingredients(ingredients):
    results = {}

    for item in ingredients[:10]:  # limit to 10 ingredients
        try:
            query = f"What is {item} and is it healthy?"
            results[item] = search_ingredient(query)
        except Exception as e:
            results[item] = f"Error fetching data: {str(e)}"

    return results