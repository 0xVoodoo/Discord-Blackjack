import blackjack as b
import random
import discord
from dotenv import load_dotenv
from os import getenv

if __name__ == "__main__":
    load_dotenv()
    api_key = getenv("DISCORD_KEY")
    activegames = []
    gameexists = False
    
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    @client.event
    async def on_ready():
        print(f'Dealer on duty: {client.user}')

    @client.event
    async def on_message(message):
        msg = message.content.lower()
        if message.author == client.user:
            return
        
        player = b.getstats(message.author.name.lower())

        if msg.startswith("$deal") or msg.startswith("$d"):
            bet = msg.split()
            gameinfo = b.getgame(activegames, player.name)
            if gameinfo[0] == True:
                await message.channel.send("> **Game in progress, please !hit | !stand**")
            elif len(bet) < 2:
                await message.channel.send(">>> :clown: **Please place a bet!** :clown:\n\t\t\t\t__$u for help__")
            elif bet[1].isnumeric() == False:
                await message.channel.send(">>> :clown: **Please place a bet!** :clown:\n\t\t\t\t__$u for help__")
            elif int(bet[1]) > int(player.money):
                await message.channel.send("> :clown: **BET INVALID NOT ENOUGH CASH** :clown:")
            else:
                player = b.Player(player.name, player.wins, player.losses, player.money, bet[1])
                b.writestats(player)
                newgame = b.Game(player.name, b.newhand(), b.newhand())
                await message.channel.send(f"> :clubs::diamonds: **Welcome __{newgame.player}!__** :hearts::spades:\n{b.showhand(newgame.phand, 'Player', 'hand')}\n> :joker::joker:Dealer hand: __{newgame.dhand[0]},?__ :joker::joker:\n>\t\t\t\t\tTotal: ?")
                activegames.append(newgame)

        elif msg.startswith("$hit") or msg.startswith("$h"):
            player = b.getstats(message.author.name.lower())
            gameinfo = b.getgame(activegames, player.name)
            if gameinfo[0] == False:
                await message.channel.send("No game found, please start one with $deal or get help with $usage!")
            else:
                currentgame = activegames[gameinfo[1]]
                gameover = await b.hit(message, currentgame, player)
                if gameover == True:
                    del activegames[gameinfo[1]]

        elif msg.startswith("$stand") or msg.startswith("$s"):
            player = b.getstats(message.author.name.lower())
            gameinfo = b.getgame(activegames, player.name)
            if gameinfo[0] == False:
                await message.channel.send("No game found, please start one with !deal")
            else:
                currentgame = activegames[gameinfo[1]]
                await b.stand(message, currentgame, player)
                del activegames[gameinfo[1]]

        elif msg.startswith("$useage") or msg.startswith("$u"):
            await message.channel.send(">>> Welcome to the :clubs::hearts:**__Blackjack Bot__**:diamonds::spades:\nTo sart a game, use: $deal/$d + bet | ex: $d 10\nTo hit, use: $hit/$h\nTo stand, use: $stand/$s\nWritten by **__0xVoodoo__**")

        elif msg.startswith("$info") or msg.startswith("$i"):
            await message.channel.send(f">>> :joker: Blackjack Player: **__{player.name}__**\n:diamonds: W|L: {player.wins} | {player.losses}\n:money_with_wings: Money: {player.money}")
        
    client.run(api_key)
