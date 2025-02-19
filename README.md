<p align="center">
	<img src="https://media.githubusercontent.com/media/Qaiten/war-thunder-news-bot/main/images/HeaderImage.png" alt="WT News Bot Banner" />
	<br />
	<a href="https://github.com/Qaiten/war-thunder-news-bot/wiki">
		<img src="https://img.shields.io/badge/WT_News_Bot-Wiki-orange.svg?style=for-the-badge&logo=github" alt="Wiki" />
	</a>
	<a href="https://discord.gg/XS6w8D8">
		<img src="https://img.shields.io/discord/532683310409842728.svg?label=Discord&logo=Discord&colorB=7289da&style=for-the-badge" alt="Discord Server">
	</a>
</p>

# WarThunder News Bot
Allows posting of any WarThunder news article to a channel in Discord.

It does this by detecting the newest element on the news-page when ran and posting it with a short description and embed URL to the channel of the users choosing (see below). If you have a cloud or just want to keep the .bat running, it will do so  once per day.

## To Use:
1. Download the repository or clone it.
2. Change the "channel_id" field in "/data/last_news.json" to the respective channel id in your discord.
3. Click "run_WTNewsCheck_bot.bat" or run the command "WTNewsCheck.py" for it to run.
4. It will re-check at 12 noon per day (on the system time), once a day.