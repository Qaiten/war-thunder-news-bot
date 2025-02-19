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

# Update the get_latest_news function to scrape essential information and embed it
def get_latest_news():
    response = requests.get(NEWS_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the first widget__link element to get the latest news
    latest_article = soup.find("a", class_="widget__link")
    
    if latest_article:
        # Scrape title from the widget__title div
        title = latest_article.find_next("div", class_="widget__title").text.strip()
        
        # Scrape description from the widget__comment div
        description = latest_article.find_next("div", class_="widget__comment").text.strip()

        # Scrape image URL from the widget__poster-media img element
        image_tag = latest_article.find_next("div", class_="widget__poster").find("img")
        image_url = image_tag["data-src"] if image_tag else None
        
        # Ensure the image URL is a full URL (not just a relative path)
        if image_url and image_url.startswith("//"):
            image_url = "https:" + image_url

        # Extract the link to the full news article
        link = f"https://warthunder.com{latest_article['href']}"

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
@tasks.loop(hours=5)  # Check every 5 hours
async def check_news(channel):
    await bot.wait_until_ready()

    # Fetch the latest news
    title, link, description, image_url = get_latest_news()

    if title and link:
        print(f"Latest news: {title}, {link}")  # This will print every time the bot checks for news

        # If it's new news, send it to the channel
        news_data = load_news_data()
        if title != news_data["last_title"]:
            print(f"New news found. Saving and posting...")
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
            print("No new news to post.")
    else:
        print("No news to report.")

# Retrieve the token from the environment variable
token = os.getenv("TOKEN")
bot.run(token)  # Run the bot with the token from the environment variable

input("\nPress Enter to exit...")