# WarThunder News Bot
Allows posting of any WarThunder news article to a channel in Discord.

It does this by detecting the newest element on the news-page when ran and posting it with a short description and embed URL to the channel of the users choosing (see below). If you have a cloud or just want to keep the .bat running, it will do so  once per day.

## To Use:
1. Download the repository or clone it.
2. Change the "channel_id" field in "/data/last_news.json" to the respective channel id in your discord.
3. Click "run_WTNewsCheck_bot.bat" or run the command "WTNewsCheck.py" for it to run.
4. It will re-check at 12 noon per day (on the system time), once a day.