import os  # Add this line at the top of your file
import discord
from discord.ext import commands, tasks
import requests
from bs4 import BeautifulSoup
import json
from dotenv import load_dotenv

# Set the working directory to the script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Load environment variables from .env file
load_dotenv()

NEWS_URL = "https://warthunder.com/en/news/"

def get_latest_news():
    response = requests.get(NEWS_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    # Get all article elements
    articles = soup.find_all("a", class_="widget__link")

    # Load previously seen articles
    news_data = load_news_data()
    seen_titles = news_data.get("seen_titles", [])

    new_articles = []  # Store new articles to return

    for article in articles:
        # Scrape title
        title_tag = article.find_next("div", class_="widget__title")
        title = title_tag.text.strip() if title_tag else None

        # Scrape description
        description_tag = article.find_next("div", class_="widget__comment")
        description = description_tag.text.strip() if description_tag else None

        # Scrape image URL
        image_tag = article.find_next("div", class_="widget__poster").find("img")
        image_url = image_tag["data-src"] if image_tag else None
        if image_url and image_url.startswith("//"):
            image_url = "https:" + image_url

        # Extract the full link
        link = f"https://warthunder.com{article['href']}"

        # Check if the article is already seen
        if title and title not in seen_titles:
            new_articles.append((title, link, description, image_url))
            seen_titles.append(title)  # Add to seen list

    # Save updated seen titles
    if new_articles:
        news_data["seen_titles"] = seen_titles
        save_news_data(news_data)

    return new_articles  # Returns a list of new articles


# Load the config and news data
def load_config():
    with open("config.json", "r") as file:
        return json.load(file)

def load_news_data():
    if not os.path.exists("data/last_news.json"):
        print("No news data found, creating default data...")
        return {"channel_id": None, "last_title": None}
    with open("data/last_news.json", "r") as file:
        data = json.load(file)
        print(f"Loaded news data: {data}")
        return data

def save_news_data(data):
    print(f"Saving news data: {data}")
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
        if channel:
            print(f"News channel set: {channel.mention}")
            check_news.start(channel)  # Pass the channel to check_news
        else:
            print(f"Invalid channel ID: {channel_id}")
    else:
        print("No news channel set. Please set it first.")

# Asynchronous task to check for news
@tasks.loop(hours=6)  # Run 4x per day
async def check_news(channel):
    await bot.wait_until_ready()
    
    new_articles = get_latest_news()  # Get new articles

    if new_articles:
        for title, link, description, image_url in new_articles:
            embed = discord.Embed(
                title=title,
                description=description,
                url=link,
                color=discord.Color.blue()
            )

            if image_url:
                embed.set_thumbnail(url=image_url)

            await channel.send(embed=embed)  # Post each new article
    else:
        print("No new news to post.")


# Retrieve the token from the environment variable
token = os.getenv("TOKEN")
bot.run(token)  # Run the bot with the token from the environment variable

input("\nPress Enter to exit...")