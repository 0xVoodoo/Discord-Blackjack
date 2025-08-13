# Discord Blackjack

This all started when some of my buddies and I saw the games feature in Discord voice chat. We wanted to play the built in Blackjack game but didn't like the account permissions it asked for. The next day, this bot was up and running, letting us play all the Blackjack we want on Discord!


# Usage

Create a .env file containing your Discord bot token and optionally the channel Id that you'd like scoreboard messages sent to.
```
.env:
DISCORD_KEY=<Bot Token>
DISCORD_CHAN=<Channel Id>
```
Create a virtual environment and install the required packages.
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Finally, from your venv, run the bot.
```
python3 bot.py
```

# Requirements
```
discord.py
python-dotenv
```
# Playing the game
- Each player begins with $100.
- To begin, place a bet with: $deal \<bet amount> | $d \<bet amount>
- To draw an additional card: $hit | $h
- To stand: $stand | $s
- To get your current stats: $info | $i
- For help: $help | $h

# Scoreboard and Allowance
The scoreboard is optional and will send a message containing the stats of all players. This can be configured with Cron jobs or scheduled tasks to repeat automatically. The scoreboard also gives every player an additional $10 by default, preventing lockout by way of repeated losses.

# License
GPLV3, as all good software should be :)
