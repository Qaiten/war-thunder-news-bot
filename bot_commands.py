import discord
from discord.ext import commands
import asyncio
from data_handler import load_news_data, save_news_data

@commands.command(name='wtnews', help='Set the channel for posting news')
@commands.has_permissions(administrator=True)
async def set_news_channel(ctx):
    await ctx.send("Please mention the channel you want to set for posting news (e.g., #news-channel or channel ID).")

    def check(m):
        return m.author == ctx.author and m.guild == ctx.guild

    try:
        msg = await ctx.bot.wait_for('message', check=check, timeout=60.0)
        if msg.channel_mentions:
            channel = msg.channel_mentions[0]
        else:
            try:
                channel_id = int(msg.content.strip())
                channel = ctx.bot.get_channel(channel_id)
                if channel is None:
                    raise ValueError("Invalid channel ID")
            except ValueError:
                await ctx.send("Invalid channel mentioned or ID provided. Please try again.")
                return

        news_data = load_news_data()
        news_data["channel_id"] = channel.id
        save_news_data(news_data)
        await ctx.send(f"News channel set to {channel.mention}")
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond. Please try again.")