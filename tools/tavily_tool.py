import os

def get_tavily_client():
    try:
        from tavily import TavilyClient
    except:
        return None

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        return None

    return TavilyClient(api_key=api_key)


def search_ingredient(query):
    client = get_tavily_client()

    if not client:
        return f"{query}: basic ingredient (no external data)"

    try:
        result = client.search(query=query, search_depth="basic")
        return result["results"][0]["content"]
    except:
        return f"{query}: info not found"