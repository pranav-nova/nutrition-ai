from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

print("DEBUG KEY:", os.getenv("TAVILY_API_KEY"))  # 👈 ADD THIS

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_ingredient(query):
    result = client.search(query=query, search_depth="basic")
    return result["results"][0]["content"]