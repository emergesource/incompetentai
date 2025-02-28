import requests
from pprint import pprint

API_KEY = "b5072cdd55d94c83a660b2a22d96289e"

url = "https://newsapi.org/v2/everything"

params = {
    "qInTitle": "AI AND (fail)",  # AI must be present, plus at least one fruit
    "sortBy": "publishedAt",
    "language": "en",
    "apiKey": API_KEY
}

response = requests.get(url, params=params)
data = response.json()

if data["status"] == "ok":
    articles = data["articles"]
    if not articles:
        print("No articles found matching your query.")
    else:
        for i, article in enumerate(articles[:1], start=1):  # Show top 5 results
            pprint(article)
            print(f"{i}. {article['title']}")
            print(f"   {article['url']}\n")
else:
    print("Error:", data.get("message"))
