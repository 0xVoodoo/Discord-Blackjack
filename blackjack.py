import random

class Game:
    def __init__(game, player, phand, dhand):
        game.player = player
        game.phand = phand
        game.dhand = dhand
    def __str__(game):
        return f"{game.player} {game.phand}"

class Player:
    def __init__(player, name, wins, losses, money, bet):
        player.name = name
        player.wins = wins
        player.losses = losses
        player.money = money
        player.bet = bet
    def __str__(player):
        return f"{player.name} WL: {player.wins}/{player.losses} | ${player.money}"

def getgame(activegames, author):
    gameexists = False
    i = -1
    for x in activegames:
        i += 1
        if x.player == author:
            gameexists = True
    return [gameexists, i]

def newhand():
    hand = []
    hand.append(random.randint(2, 11))
    hand.append(random.randint(2, 11))
    return aces(hand)

def aces(hand):
    i = 0
    total = totalhand(hand)
    if total > 21:
        for card in hand:
            if card == 11:
                hand[i] = 1
                break
            i = i + 1
    return hand

def totalhand(hand):
    total = 0
    for card in hand:
        total = total + card
    return total

def showhand(hand, player, action):
    strlist = [str(card) for card in hand]
    handstr = ",".join(strlist)
    msg = f"> :joker::joker:{player} {action}: __{handstr}__ :joker::joker:\n>\t\t\t\t\tTotal: {totalhand(hand)}"
    return msg

def score(dtotal, ptotal):
    won = False
    draw = False
    winmsg = "> :tada: **__YOU WIN!__** :tada:"
    losemsg = "> :sob: **__You lose__** :sob:"
    if dtotal > 21 and ptotal <= 21:
        won = True
    elif dtotal < 21 and ptotal > 21:
        won = False
    elif dtotal < 21 and ptotal < 21:
        if dtotal > ptotal:
            won = False
        elif dtotal < ptotal:
            won = True
        elif dtotal == ptotal:
            draw = True
    elif dtotal == 21 and ptotal < 21:
        won = False
    elif dtotal < 21 and ptotal == 21:
        won = True
    elif dtotal == 21 and ptotal > 21:
        won = False
    elif dtotal > 21 and ptotal == 21:
        won = True
    elif dtotal > 21 and ptotal > 21:
        draw = True
    elif dtotal == ptotal:
        draw = True
    else: return ["SCORING ERROR", won, draw]

    if won == True:
        return [winmsg, won, draw]
    elif draw == True:
        return ["> :clown: It's a push :clown:", won, draw]
    else:
        return [losemsg, won, draw]

def getstats(player):
    fn = "stats/"+player+".txt"
    try:
        with open(fn, "r") as f:
            currentstats = f.read().split(",")
            if len(currentstats) < 5:
                print("[-] Error parsing player stats")
            else:
                stats = Player(currentstats[0], currentstats[1], currentstats[2], currentstats[3], currentstats[4])
    except FileNotFoundError:
        initplayer(player)
        stats = getstats(player)
    return stats

def initplayer(player):
    fn = "stats/"+player+".txt"
    try:
        with open(fn, "x") as f:
            f.write(player+",0,0,100,0")
    except FileExistsError:
        print("[-] Error parsing player data!")

def writestats(player):
    fn = "stats/"+player.name+".txt"
    with open(fn, "w") as f:
        statsline = player.name+","+player.wins+","+player.losses+","+str(player.money)+","+str(player.bet)
        f.writelines(statsline)

async def hit(message, currentgame, player):
    gameover = False
    if totalhand(currentgame.phand) >= 21:
        await stand(message, currentgame, player)
        gameover = True
    else:
        currentgame.phand.append(random.randint(2,11))
        currentgame.phand = aces(currentgame.phand)
        await message.channel.send(showhand(currentgame.phand, currentgame.player, "drew"))
        if totalhand(currentgame.phand) > 21:
            await message.channel.send(f"> :boom: **BUST** :boom:")
            await stand(message, currentgame, player)
            gameover = True
    return gameover

async def stand(message, currentgame, player):
    await message.channel.send(showhand(currentgame.dhand, "Dealer", "hand"))
    if totalhand(currentgame.dhand) >= 17:
        pass
    else:
        while totalhand(currentgame.dhand) < 17:
            currentgame.dhand.append(random.randint(2,11))
            currentgame.dhand = aces(currentgame.dhand)
            await message.channel.send(showhand(currentgame.dhand, "Dealer", "drew"))
    result = score(totalhand(currentgame.dhand), totalhand(currentgame.phand))
    player = player
    if result[1] == True:
        payout = int(player.money) + int(player.bet)
        updatedplayer = Player(player.name, str(int(player.wins) + 1), str(player.losses), payout, 0)
    elif result[1] == False and result[2] == True:
        updatedplayer = Player(player.name, player.wins, player.losses, player.money, 0)
    else:
        payout = int(player.money) - int(player.bet)
        updatedplayer = Player(player.name, player.wins, str(int(player.losses) + 1), payout, 0)
    writestats(updatedplayer)
    await message.channel.send(result[0])
