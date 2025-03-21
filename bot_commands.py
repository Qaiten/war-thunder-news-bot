import discord
from discord.ext import commands
from discord.ui import Select, View
import asyncio
from data_handler import load_news_data, save_news_data

class ChannelSelectView(View):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.value = None

    @discord.ui.select(
        placeholder="Choose to add or remove a channel from use...",
        options=[
            discord.SelectOption(label="Add Channel", value="add"),
            discord.SelectOption(label="Remove Channel", value="remove")
        ]
    )
    async def select_callback(self, interaction, select):
        self.value = select.values[0]
        await interaction.response.defer()
        self.stop()

@commands.command(name='wtnews', help='Add or remove a channel for posting news')
@commands.has_permissions(administrator=True)
async def set_news_channel(ctx):
    view = ChannelSelectView(ctx)
    await ctx.send("Please choose an action:", view=view)
    await view.wait()

    if view.value is None:
        await ctx.send("You took too long to respond. Please try again.")
        return

    action = view.value
    if action == 'add':
        await ctx.send("Please mention the channel you want to add for posting news (e.g., #news-channel or channel ID).")
    elif action == 'remove':
        await ctx.send("Please mention the channel you want to remove from posting news (e.g., #news-channel or channel ID).")

    def check_message(m):
        return m.author == ctx.author and m.guild == ctx.guild

    try:
        msg = await ctx.bot.wait_for('message', check=check_message, timeout=60.0)
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
        if "channel_ids" not in news_data:
            news_data["channel_ids"] = []

        if action == 'add':
            if channel.id not in news_data["channel_ids"]:
                news_data["channel_ids"].append(channel.id)
                save_news_data(news_data)
                await ctx.send(f"News channel {channel.mention} added.")
            else:
                await ctx.send(f"Channel {channel.mention} is already in the list.")
        elif action == 'remove':
            if channel.id in news_data["channel_ids"]:
                news_data["channel_ids"].remove(channel.id)
                save_news_data(news_data)
                await ctx.send(f"News channel {channel.mention} removed.")
            else:
                await ctx.send(f"Channel {channel.mention} is not in the list.")
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond. Please try again.")