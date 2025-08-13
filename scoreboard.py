import discord
import os
import blackjack as b
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("DISCORD_KEY")
    channel_id = os.getenv("DISCORD_CHAN")
    print(channel_id)

    print("[*] Initializing scoreboard")
    scoreboard = []
    msg = f">>> **__---LEADERBOARD---__**\n"
    players = os.listdir(path="stats/")
    for player in players:
        currentplayer = os.path.basename(player).split('.')[0]
        playerstats = b.getstats(currentplayer)
        scoreboard.append(playerstats)
        updatedplayer = b.Player(playerstats.name, playerstats.wins, playerstats.losses, str(int(playerstats.money) + 10), playerstats.bet)
        b.writestats(updatedplayer)
    scoreboard.sort(reverse=True, key=lambda player: player.money)
    print("[*] Scoreboard ready")
    place = 0;
    while place < len(scoreboard):
        if place == 0:
            msg = msg + f':crown: - **__{scoreboard[place].name}__** - {scoreboard[place].money}\n'
        elif place == 1:
            msg = msg + f':second_place: - **__{scoreboard[place].name}__** - {scoreboard[place].money}\n'
        elif place == 2:
            msg = msg + f':third_place: - **__{scoreboard[place].name}__** - {scoreboard[place].money}\n'
        else:
            msg = msg + f'**{place + 1}** - **{scoreboard[place].name}** - {scoreboard[place].money}\n'
        place += 1
    print("[*] Message created")
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    print("[*] Bot configured")
    @client.event
    async def on_ready():
        print("[*] Bot authenticated")
        channel = client.get_channel(channel_id)
        if channel:
            await channel.send(msg)
            print("[+] Scoreboard sent!")
        else:
            print("[-] CHANNEL NOT FOUND!")
        await client.close()
    
    client.run(api_key)
