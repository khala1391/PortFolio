import requests
import json
import os

NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
COMPANIES = ["Google", "Microsoft", "Amazon"]
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

def fetch_news(company):
    params = {
        'apiKey': NEWS_API_KEY,
        'qInTitle': company,
        'pageSize': 3,
        'sortBy': 'publishedAt',
        'language': 'en',
    }
    response = requests.get(NEWS_ENDPOINT, params=params)
    if response.status_code == 200:
        return response.json().get("articles", [])[:3]
    return []

all_news = {}
for company in COMPANIES:
    all_news[company] = fetch_news(company)

with open("news.json", "w") as f:
    json.dump(all_news, f, indent=2)
