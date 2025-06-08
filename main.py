from flask import Flask, render_template
from post import Post
import requests


news_data = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()
news_objects = []
for item in news_data:
    news_object = Post(item['id'],item['title'],item['title'], item['body'])
    news_objects.append(news_object)


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html",all_posts=news_objects)



@app.route('/news')
def show_all_news():
    return render_template("news.html", all_posts=news_objects)



@app.route("/news/<int:index>")
def show_news(index):
    requested_news = next((post for post in news_objects if post.id == index), None)
    return render_template("post.html", post= requested_news)



@app.route('/my_portfolio')
def my_portfolio():
    return render_template("my_portfolio.html")


@app.route('/my_article')
def my_article():
    return render_template("my_article.html")

@app.route('/about_me')
def about_me():
    return render_template("about_me.html")



if __name__ == "__main__":
    app.run(debug=True)
