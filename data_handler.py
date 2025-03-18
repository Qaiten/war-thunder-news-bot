import os
import json
import datetime

def load_news_data():
    if not os.path.exists("data/last_news.json"):
        print("No news data found, creating default data...")
        return {"channel_id": None, "seen_titles": []}
    with open("data/last_news.json", "r") as file:
        data = json.load(file)
        print(f"Loaded news data: {data}")
        
        if data.get("seen_titles") and isinstance(data["seen_titles"][0], str):
            data["seen_titles"] = [(title, datetime.datetime.now().isoformat()) for title in data["seen_titles"]]
        
        return data

def save_news_data(data):
    print(f"Saving news data: {data}")
    with open("data/last_news.json", "w") as file:
        json.dump(data, file, indent=4)

def clean_old_news_data():
    news_data = load_news_data()
    seen_titles = news_data.get("seen_titles", [])
    current_time = datetime.datetime.now()
    three_months_ago = current_time - datetime.timedelta(days=90)

    news_data["seen_titles"] = [
        (title, timestamp) for title, timestamp in seen_titles
        if datetime.datetime.fromisoformat(timestamp) > three_months_ago
    ]

    save_news_data(news_data)