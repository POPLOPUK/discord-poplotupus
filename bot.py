import random
import subprocess
from datetime import datetime

from discord.ext import commands

token = open("token.txt", "r").readline()
bot = commands.Bot(command_prefix=".")

random_quotes = ["{0} was educated by stray dogs",
                 "{0} wants to move reckless, fine",
                 "{0} is capping",
                 "cap",
                 "no cap",
                 "personally, i wouldn't have that",
                 "not trying to start a fight or anything but...",
                 "Personally I wouldn't have that {0}",
                 "{0} wants to fuck a child",
                 "{0} tried to swim in lava",
                 "{0} probably feels sad today, cheer them up!",
                 "{0} fell off a cliff and used his next turn to write a will",
                 "{0}'s entrails were ripped out",
                 "{0}, chirag hates you :)",
                 "your ass",
                 "{0}, you're so cringe",
                 "{0} is such a rat",
                 "{0} is a goblin child"
                 "{0}. Suck your mum",
                 "{0} Do you want to start a fight or something?",
                 "{0}, get lost",
                 "{0} this is my area. piss off",
                 "I'll bite you uwu {0}",
                 "{0}, I'll kick you nan :)",
                 "{0}, I'll cut your dick off",
                 "{0} looks like a horse",
                 "Oh look, we have a child here. waa waa {0}",
                 "I see you {0} :) :) :))))",
                 "Bow before me {0}, you peasant!",
                 "There's no sense in being precise when you don't even know what you're talking about. Get lost {0}",
                 "{0} got their dick stuck in the blender",
                 "Hiiiiii {0}",
                 "{0} looks like a chocolate :D",
                 "{0} is looking like a snack today yum",
                 "{0} have a nice day o/",
                 "Me: Knock knock\n{0}: Who's there\nMe: Where when\n{0}: Where when who\nMe: My place, tomorrow, "
                 "you and me ;)",
                 "{0}. you looking like a garlic bread today",
                 "You are my best friend {0} UwU",
                 "Wana go out on a date {0}?"]


def getProbability():
    return chance


def reduceProbability():
    global chance
    chance = chance - 1


def resetProbability():
    global chance
    chance = 1600


@bot.event
async def on_ready():
    bot.load_extension("cogs.music")
    resetProbability()
    print("Bot ready!")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')


async def custom_cmds(message):
    # legacy code / custom code
    if message.author.bot:
        # await message.channel.send('Khavan probably: \"Jay is gay\"')
        # check if new message is from bot
        return
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    message_lower = message.content.lower()
    if not message.channel.id == 577213129080045568:
        print(current_time, str("#") + str(bot.get_channel(message.channel.id)),
              str(message.author)[:-5] + ": " + str(message.content), )
    if message_lower == ".bestgamer":
        await message.channel.send("May")
    elif message_lower == ".bestmlg":
        await message.channel.send("Berk")
        await message.channel.send("https://tenor.com/view/pepe-the-frog-dance-happy-meme-pixel-gif-17428498")
    elif message_lower == ".julia":
        await message.channel.send("<:AYAYA:770095211593465886> AYAYA <:AYAYA:770095211593465886>")
    elif message_lower == ".khavan":
        await message.channel.send('Khavan probably: \"Jay is gay\"')
    elif message_lower == "uwu" or message_lower == "owo":
        emoji = bot.get_emoji(609085517857816577)
        await message.add_reaction(emoji)
    elif "jay gay" in message_lower:
        emoji = bot.get_emoji(609086025968648213)
        await message.add_reaction(emoji)
        await message.channel.send(str(message.author)[:-5] + " is gay")
    elif message_lower == "never one":
        await message.channel.send("Without the other")
    # below is shoddy code. look away
    probability = getProbability()
    if random.randint(1, probability) == 1:
        await message.channel.send(
            random_quotes[random.randint(0, len(random_quotes) - 1)].format(str(message.author)[:-5]))
        resetProbability()
    else:
        reduceProbability()
        if random.randint(1, 400) == 1:
            if random.randint(1, 2) == 1:
                await message.add_reaction("🧢")
            else:
                await message.add_reaction("🚫")
                await message.add_reaction("🧢")


@bot.command(name="reboot")  # Now only the bot owner can call reboot.
async def reboot(ctx):
    await ctx.channel.send("Rebooting")
    bot.unload_extension("cogs.music")
    await ctx.bot.logout()
    subprocess.call(["python3", "bot.py"])

chance = 0
resetProbability()
bot.load_extension("cogs.drawing")
bot.load_extension("cogs.quotes")
bot.load_extension("cogs.media")
bot.load_extension("cogs.sound")
# bot.load_extension("cogs.utility")
bot.add_listener(custom_cmds, 'on_message')
bot.run(token)
