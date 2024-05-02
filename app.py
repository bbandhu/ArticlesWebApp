from flask import Flask, render_template
import os
from dotenv import load_dotenv
import requests
from newspaper import Article

load_dotenv()  # Load environment variables from .env file
app = Flask(__name__)

NEWS_API_KEY = os.getenv('NEWS_API_KEY')
NEWS_API_ENDPOINT = "https://newsapi.org/v2/top-headlines"

@app.route('/')
def index():
    articles = fetch_news()
    return render_template('index.html', articles=articles)

def fetch_news():
    params = {
        'country': 'us',
        'apiKey': NEWS_API_KEY
    }
    response = requests.get(NEWS_API_ENDPOINT, params=params)
    response_json = response.json()
    news_items = []

    for item in response_json.get('articles', []):
        try:
            article = Article(item['url'])
            article.download()
            article.parse()
            news_items.append({
                'title': article.title,
                'content': article.text,
                'source_link': item['url'],
                'image': article.top_image,
                'timestamp': item['publishedAt']  # Assuming the API returns this
            })
        except Exception as e:
            print(f"Skipping article {item['url']}: {e}")

    return news_items

if __name__ == '__main__':
    app.run(debug=True)
