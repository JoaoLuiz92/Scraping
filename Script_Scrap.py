from flask import Flask, jsonify
from newspaper import Article
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/noticias")
def noticias():
    url = "https://www.cnnbrasil.com.br/"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    links = [a['href'] for a in soup.find_all('a', href=True) if "/" in a['href']]
    headlines = []

    for link in links[:5]:
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
