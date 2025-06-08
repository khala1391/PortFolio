from datetime import datetime

class Post:
    def __init__(self, company, title, description, url, urlToImage, publishedAt):
        self.company = company
        self.title = title
        self.description = description
        self.url = url
        self.urlToImage = urlToImage
        self.publishedAt = publishedAt
        
        # parse and format publishedAt from ISO string to "07 Jun 2025"
        if publishedAt:
            dt = datetime.strptime(publishedAt, "%Y-%m-%dT%H:%M:%SZ")
            self.publishedAt = dt.strftime("%d %b %Y")
        else:
            self.publishedAt = "Unknown"

    @classmethod
    def from_json(cls, data):
        posts = []
        for company, articles in data.items():
            for article in articles:
                posts.append(
                    cls(
                        company=company,
                        title=article.get("title"),
                        description=article.get("description"),
                        url=article.get("url"),
                        urlToImage=article.get("urlToImage"),
                        publishedAt=article.get("publishedAt")
                    )
                )
        return posts
