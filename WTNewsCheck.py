import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from news import get_latest_news
from data_handler import load_news_data, clean_old_news_data
from bot_commands import set_news_channel

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

    news_data = load_news_data()
    channel_ids = news_data.get("channel_ids", [])
    
    if channel_ids:
        channels = [bot.get_channel(channel_id) for channel_id in channel_ids if bot.get_channel(channel_id)]
        if channels:
            print(f"News channels set: {', '.join([channel.mention for channel in channels])}")
            check_news.start(channels)
        else:
            print("No valid channels found.")
    else:
        print("No news channels set. Please set them first.")
    
    clean_news_data.start()

@tasks.loop(hours=6)
async def check_news(channels):
    await bot.wait_until_ready()
    
    new_articles = get_latest_news()

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

            for channel in channels:
                await channel.send(embed=embed)
    else:
        print("No new news to post.")

@tasks.loop(hours=1440)
async def clean_news_data():
    clean_old_news_data()

bot.add_command(set_news_channel)

token = os.getenv("TOKEN")
bot.run(token)

input("\nPress Enter to exit...")