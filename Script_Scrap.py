from flask import Flask, jsonify
from newspaper import Article
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = Flask(__name__)

@app.route("/")
def index():
    return "API de scraping da CNN Brasil está online."

@app.route("/news")
def noticias():
    url = "https://edition.cnn.com/"

    try:
        response = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        })
        response.raise_for_status()
    except requests.RequestException as e:
        return jsonify({"error": "Erro ao acessar a CNN Brasil", "details": str(e)}), 500

    soup = BeautifulSoup(response.text, "html.parser")
    anchors = soup.find_all("a", href=True)
    links = []

    for a in anchors:
        href = a["href"]
        if href.startswith("/") or href.startswith("http"):
            full_url = urljoin(url, href)
            if "cnnbrasil.com.br" in full_url and full_url not in links:
                links.append(full_url)

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
        except Exception:
            continue

    return jsonify(headlines)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
