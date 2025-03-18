import requests
from bs4 import BeautifulSoup
import datetime
from data_handler import load_news_data, save_news_data

NEWS_URL = "https://warthunder.com/en/news/"

def get_latest_news():
    response = requests.get(NEWS_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.find_all("a", class_="widget__link")
    news_data = load_news_data()
    seen_titles = news_data.get("seen_titles", [])

    new_articles = []

    for article in articles:
        title_tag = article.find_next("div", class_="widget__title")
        title = title_tag.text.strip() if title_tag else None

        description_tag = article.find_next("div", class_="widget__comment")
        description = description_tag.text.strip() if description_tag else None

        image_tag = article.find_next("div", class_="widget__poster").find("img")
        image_url = image_tag["data-src"] if image_tag else None
        if image_url and image_url.startswith("//"):
            image_url = "https:" + image_url

        link = f"https://warthunder.com{article['href']}"

        if title and title not in [t for t, _ in seen_titles]:
            new_articles.append((title, link, description, image_url))
            seen_titles.append((title, datetime.datetime.now().isoformat()))

    if new_articles:
        news_data["seen_titles"] = seen_titles
        save_news_data(news_data)

    return new_articles