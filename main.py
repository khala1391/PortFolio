from flask import Flask, render_template
from post import Post
import requests, os, json

def load_news_from_file():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # news_path = os.path.join(base_dir, "news.json")
    news_path = os.path.join(base_dir, "static/data/company_top3_news.json")

    with open(news_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return Post.from_json(data)


app = Flask(__name__)
news_objects = load_news_from_file()

@app.route('/')
def index():
    # Load from the static/data/sampled_news_across_companies.json
    data_path = os.path.join(app.root_path, 'static/data/sampled_news_across_companies.json')
    with open(data_path, encoding='utf-8') as f:
        sampled_news = json.load(f)
    return render_template('index.html', all_posts=news_objects, news=sampled_news)



@app.route('/news')
def show_all_news():
    global news_objects
    news_objects = load_news_from_file()
    return render_template('news.html', all_posts=news_objects)


@app.route('/my_portfolio')
def my_portfolio():
    return render_template("my_portfolio.html")


@app.route('/my_article')
def my_article():
    return render_template("my_article.html")

@app.route('/about_me')
def about_me():
    return render_template("about_me.html")

@app.route("/run-fetch-news")
def run_fetch_news():
    import fetch_news
    fetch_news.main()  # or whatever function triggers your logic
    return "News fetched successfully", 200


if __name__ == "__main__":
    app.run(debug=True)
