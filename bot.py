import discord
from discord.ext import commands, tasks
import requests
from bs4 import BeautifulSoup
import json
import os

NEWS_URL = "https://warthunder.com/en/news/"

# Update the get_latest_news function to scrape essential information and embed it
def get_latest_news():
    response = requests.get(NEWS_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the first widget__link element to get the latest news
    latest_article = soup.find("a", class_="widget__link")
    
    if latest_article:
        title = latest_article["href"].split("/")[-1].replace("-", " ").title()  # Extract the title from the URL (you can refine this if needed)
        link = f"https://warthunder.com{latest_article['href']}"
        
        # Scrape additional information from the specific news page
        article_page = requests.get(link)
        article_soup = BeautifulSoup(article_page.text, "html.parser")
        
        # Try to get the description or summary of the article (you can modify this selector as needed)
        description = article_soup.find("div", class_="news-text").text.strip() if article_soup.find("div", class_="news-text") else "No description available."
        
        # Try to get the image if it exists
        image_url = article_soup.find("meta", property="og:image")
        image_url = image_url["content"] if image_url else None

        return title, link, description, image_url
    else:
        print("No latest news found.")
        return None, None, None, None

# Load the config and news data
def load_config():
    with open("config.json", "r") as file:
        return json.load(file)

def load_news_data():
    if not os.path.exists("data/last_news.json"):
        return {"channel_id": None, "last_title": None}
    with open("data/last_news.json", "r") as file:
        return json.load(file)

def save_news_data(data):
    with open("data/last_news.json", "w") as file:
        json.dump(data, file, indent=4)

# Set up the bot and intents
intents = discord.Intents.default()
intents.message_content = True  # Ensure message content is enabled
bot = commands.Bot(command_prefix="!", intents=intents)

# Event when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

    # Automatically get the #warthunder-news channel
    news_data = load_news_data()
    channel_id = news_data["channel_id"]
    
    # If channel is set, start checking news
    if channel_id:
        channel = bot.get_channel(channel_id)
        print(f"News channel set: {channel.mention}")
        check_news.start(channel)  # Pass the channel to check_news
    else:
        print("No news channel set. Please set it first.")

# Asynchronous task to check for news
@tasks.loop(seconds=60)  # Default to check every 60 seconds
async def check_news(channel):
    await bot.wait_until_ready()

    # Fetch the latest news
    title, link, description, image_url = get_latest_news()

    if title and link:
        print(f"Latest news: {title}, {link}")  # This will print every time the bot checks for news

        # If it's new news, send it to the channel
        news_data = load_news_data()
        if title != news_data["last_title"]:
            news_data["last_title"] = title
            save_news_data(news_data)

            # Create an embed for the news
            embed = discord.Embed(
                title=title,
                description=description,
                url=link,
                color=discord.Color.blue()
            )

            # If an image exists, set it as the embed's thumbnail
            if image_url:
                embed.set_thumbnail(url=image_url)

            # Send the embed to the channel
            await channel.send(embed=embed)
    else:
        print("No news to report.")

config = load_config()
bot.run(config.get("token"))  # Run the bot with the token from the config

# TGC Channel id: 1059515770725486692