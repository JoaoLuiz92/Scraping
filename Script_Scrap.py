from flask import Flask, jsonify
from newspaper import Article
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/noticias")
def noticias():
    url = "https://edition.cnn.com/"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    links = [a['href'] for a in soup.select("a") if "/" in a['href']]
    headlines = []

    for link in links[:10]:  # só os 5 primeiros
        try:
            article = Article(link)
            article.download()
            article.parse()
            headlines.append({
                "title": article.title,
                "link": link,
                "summary": article.text[:300]
            })
        except:
            continue

    return jsonify(headlines)
