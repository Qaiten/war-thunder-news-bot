<p align="center">
	<img src="https://github.com/Qaiten/war-thunder-news-bot/blob/main/images/HeaderImage.png" alt="WT News Bot Banner" />
	<br />
	<a href="https://github.com/Qaiten/war-thunder-news-bot/wiki">
		<img src="https://img.shields.io/badge/WT_News_Bot-Wiki-orange.svg?style=for-the-badge&logo=github" alt="Wiki" />
	</a>
	<a href="https://discord.gg/XS6w8D8">
		<img src="https://img.shields.io/discord/532683310409842728.svg?label=Discord&logo=Discord&colorB=7289da&style=for-the-badge" alt="Discord Server">
	</a>
</p>

# 🚀 WarThunder News Bot

Stay up-to-date with the latest **WarThunder** news in your Discord server! This bot automatically detects and posts the newest WarThunder news article to a Discord channel of your choice. 📢

## ✨ Features
- 📰 **Auto-detects** the latest news article from the WarThunder website.
- 🤖 **Posts** the article with a short description and an embedded link.
- ⏰ **Runs Daily**—checks for news at **12 noon (system time)** every day.
- ☁️ **Cloud & Local Support**—Run it manually or keep it running on a cloud service!

## 📌 How to Use
1. **Download or Clone** this repository.
   - Ensure you add the bot to your server.
2. **Set the Discord Channel**: 
   - Open `/data/last_news.json`
   - Change the **"channel_id"** field to your desired Discord channel ID.
3. **Run the Bot**:
   - Double-click `run_WTNewsCheck_bot.bat` _or_
   - Run `WTNewsCheck.py` from the command line.
4. **That's it! 🎉**
   - The bot will check for new articles daily at **12 noon** (system time) and post them automatically.
   - The bot will also check from previously posted articles kept in it's last_news.json storage and not post duplicate items.

---

💡 *Want to improve or contribute? Feel free to fork and submit a PR!* 😃