from discord.ext import commands
from datetime import datetime

token = open("token.txt", "r").readline()
bot = commands.Bot(command_prefix=".")


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

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    messageL = message.content.lower()
    print(current_time, str("#") + str(bot.get_channel(message.channel.id)),
          str(message.author)[:-5] + ": " + str(message.content), )
    if messageL == ".bestgamer":
        await message.channel.send("May")
    elif messageL == ".bestmlg":
        await message.channel.send("Berk")
        await message.channel.send("https://tenor.com/view/pepe-the-frog-dance-happy-meme-pixel-gif-17428498")
    elif messageL == ".julia":
        await message.channel.send("<:AYAYA:770095211593465886> AYAYA <:AYAYA:770095211593465886>")
    elif messageL == ".khavan":
        await message.channel.send('Khavan probably: \"Jay is gay\"')
    elif messageL == "uwu" or messageL == "owo":
        emoji = bot.get_emoji(609085517857816577)
        await message.add_reaction(emoji)
    elif "jay gay" in messageL:
        emoji = bot.get_emoji(609086025968648213)
        await message.add_reaction(emoji)
        await message.channel.send(str(message.author)[:-5] + " is gay")
    elif messageL == "never one":
        await message.channel.send("Without the other")

bot.load_extension("cogs.drawing")
bot.load_extension("cogs.quotes")
bot.load_extension("cogs.media")
bot.load_extension("cogs.sound")
# bot.load_extension("cogs.utility")
bot.add_listener(custom_cmds, 'on_message')
bot.run(token)
