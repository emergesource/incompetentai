from django.shortcuts import render
import requests
from django.core.cache import cache
from datetime import datetime
from newsapi import NewsApiClient
from pprint import pprint
from django.conf import settings

newsapi = NewsApiClient(api_key=settings.NEWS_API_KEY)

def fetch_news():
    data = newsapi.get_everything(
        qintitle="AI AND (fail OR incompetent OR sucks OR stinks OR blows OR bad OR failure OR brutal OR awful)",
        sort_by="publishedAt",
        language="en",
    )

    if data.get("status") == "ok":
        unique_articles = []
        seen_urls = set()

        for article in data["articles"]:
            # clean up time
            article["publishedAt"] = datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")

            # try to limit duplicates
            if article["title"] not in seen_urls:
                seen_urls.add(article["title"])
                unique_articles.append(article)
        
        return unique_articles[:50]
    return []

def news_page(request):
    articles = cache.get("daily_news")

    if not articles:
        articles = fetch_news()
        cache.set("daily_news", articles, timeout=86400)  # Cache for 24 hours
    
    return render(request, "news/news_page.html", {"articles": articles})