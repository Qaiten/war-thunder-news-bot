import os  # Add this line at the top of your file
import discord
from discord.ext import commands, tasks
import requests
from bs4 import BeautifulSoup
import json
from dotenv import load_dotenv
import datetime  # Add this import at the top

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
        if title and title not in [t for t, _ in seen_titles]:
            new_articles.append((title, link, description, image_url))
            seen_titles.append((title, datetime.datetime.now().isoformat()))  # Add to seen list with timestamp

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
        return {"channel_id": None, "seen_titles": []}
    with open("data/last_news.json", "r") as file:
        data = json.load(file)
        print(f"Loaded news data: {data}")
        
        # Convert old format to new format if necessary
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

    # Filter out old news
    news_data["seen_titles"] = [
        (title, timestamp) for title, timestamp in seen_titles
        if datetime.datetime.fromisoformat(timestamp) > three_months_ago
    ]

    save_news_data(news_data)

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
    
    clean_news_data.start()  # Start the cleanup task

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

@tasks.loop(hours=1440)  # Run every 60 days (60 days * 24 hours)
async def clean_news_data():
    clean_old_news_data()

@bot.command(name='setnews', help='Set the channel for posting news')
@commands.has_permissions(administrator=True)
async def set_news_channel(ctx):
    await ctx.author.send("Please mention the channel you want to set for posting news (e.g., #news-channel or channel ID).")

    def check(m):
        return m.author == ctx.author and m.guild is None

    try:
        msg = await bot.wait_for('message', check=check, timeout=60.0)
        if msg.channel_mentions:
            channel = msg.channel_mentions[0]
        else:
            try:
                channel_id = int(msg.content.strip())
                channel = bot.get_channel(channel_id)
                if channel is None:
                    raise ValueError("Invalid channel ID")
            except ValueError:
                await ctx.author.send("Invalid channel mentioned or ID provided. Please try again.")
                return

        news_data = load_news_data()
        news_data["channel_id"] = channel.id
        save_news_data(news_data)
        await ctx.author.send(f"News channel set to {channel.mention}")
    except asyncio.TimeoutError:
        await ctx.author.send("You took too long to respond. Please try again.")

# Retrieve the token from the environment variable
token = os.getenv("TOKEN")
bot.run(token)  # Run the bot with the token from the environment variable

input("\nPress Enter to exit...")