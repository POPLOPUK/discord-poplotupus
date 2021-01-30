from discord.ext import commands
import pickle
import random
from datetime import datetime
import aiohttp
import io

token = open("token.txt", "r").readline()
bot = commands.Bot(command_prefix="..")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')



bot.load_extension("cogs.drawing")
bot.load_extension("cogs.quotes")
bot.run(token)
