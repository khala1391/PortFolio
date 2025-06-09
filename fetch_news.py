import random
import os
import requests
import json
from datetime import datetime
from collections import defaultdict

NEWS_API_KEY = os.environ.get("NEWS_Hmail_API_KEY")
COMPANIES = ["Google",
             "Microsoft",
             "Facebook",
             "TSMC",
             "NVIDIA",
             "AMD",
             ]
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


from datetime import datetime, timedelta

now = datetime.now()
start = (now - timedelta(days=4)).replace(hour=0, minute=0, second=0, microsecond=0)
end = now

start_iso = start.isoformat()  # e.g. '2025-06-04T00:00:00'
end_iso = end.isoformat()      # e.g. '2025-06-08T15:23:45.123456'

print("From (start):", start_iso)
print("To (end):", end_iso)




# Single API request for all companies
def fetch_all_news():
    params = {
        'apiKey': os.environ.get('NEWS_Hmail_API_KEY'),
        'q': ' OR '.join(COMPANIES) + ' AND (datascience OR "machine learning" OR "deep learning" OR AI)',
        'language': 'en',
        'from': start_iso,
        'to': end_iso,
        'sortBy': 'publishedAt',
        'pageSize': 100  # Max is 100 for NewsAPI
    }
    response = requests.get(NEWS_ENDPOINT, params=params)
    if response.status_code == 200:
        return response.json().get("articles", [])
    return []

# Group articles by company
def group_articles_by_company(articles, companies):
    grouped = defaultdict(list)
    for article in articles:
        title = article.get('title', '').lower()
        for company in companies:
            if company.lower() in title:
                grouped[company].append(article)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(base_dir, 'static/data')
    output_file = os.path.join(static_dir, "news.json")
    # Select top 3 per company
    return {company: grouped[company][:3] for company in companies}

# Run
all_articles = fetch_all_news()
all_news = group_articles_by_company(all_articles, COMPANIES)

# Optional: print or use `all_news`
for company, news in all_news.items():
    print(f"\nTop 3 for {company}:")
    for article in news:
        print(f" - {article['title']}")



# Save as JSON

base_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(base_dir, 'static/data')
output_file = os.path.join(static_dir, "company_top3_news.json")

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_news, f, indent=2, ensure_ascii=False)

print(f"Saved top 3 news articles per company to {output_file}")



############################ select news ##################################


# Get current directory (compatible with Jupyter or script)
base_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(base_dir, 'static/data')

# Paths for input and output files
input_path = os.path.join(static_dir, "company_top3_news.json")
output_path = os.path.join(static_dir, "sampled_news_across_companies.json")

# Load the full dictionary of company news
with open(input_path, "r") as f:
    company_news = json.load(f)

# Flatten all news articles into one list
all_articles = []

for company, articles in company_news.items():
    if isinstance(articles, list):
        for article in articles:
            # Optionally tag each article with its company
            article["company"] = company
            all_articles.append(article)

# Safety check
if len(all_articles) == 0:
    raise ValueError("No articles found across all companies.")

# Randomly select up to 3 articles total
num_to_select = min(3, len(all_articles))
selected_news = random.sample(all_articles, num_to_select)

# Print the selected articles
for i, article in enumerate(selected_news, 1):
    print(f"\nNews {i}:")
    print("Company:", article.get("company"))
    print("Title:", article.get("title"))
    print("Description:", article.get("description"))

# Save to output JSON
with open(output_path, "w") as f:
    json.dump(selected_news, f, indent=2)

print(f"\nSaved {num_to_select} sampled articles to:\n{output_path}")


def main():
    all_articles = fetch_all_news()
    all_news = group_articles_by_company(all_articles, COMPANIES)

    for company, news in all_news.items():
        print(f"\nTop 3 for {company}:")
        for article in news:
            print(f" - {article['title']}")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(base_dir, 'static/data')
    output_file = os.path.join(static_dir, "company_top3_news.json")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_news, f, indent=2, ensure_ascii=False)

    print(f"Saved top 3 news articles per company to {output_file}")

    # Select a few across all companies
    input_path = os.path.join(static_dir, "company_top3_news.json")
    output_path = os.path.join(static_dir, "sampled_news_across_companies.json")

    with open(input_path, "r") as f:
        company_news = json.load(f)

    all_articles = []
    for company, articles in company_news.items():
        for article in articles:
            article["company"] = company
            all_articles.append(article)

    if len(all_articles) == 0:
        raise ValueError("No articles found across all companies.")

    num_to_select = min(3, len(all_articles))
    selected_news = random.sample(all_articles, num_to_select)

    for i, article in enumerate(selected_news, 1):
        print(f"\nNews {i}:")
        print("Company:", article.get("company"))
        print("Title:", article.get("title"))
        print("Description:", article.get("description"))

    with open(output_path, "w") as f:
        json.dump(selected_news, f, indent=2)

    print(f"\nSaved {num_to_select} sampled articles to:\n{output_path}")


# Optional: allow direct script run
if __name__ == "__main__":
    main()
